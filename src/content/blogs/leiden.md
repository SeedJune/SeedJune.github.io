---

title: 'Leiden 社区发现算法学习笔记'
date: 2026-08-12
summary: '从 Louvain 的局限出发，梳理 Leiden 算法的局部移动、划分细化与图聚合三个阶段，并记录目标函数、参数选择和实验方法。'

series: 'algorithm'

tags: ['Leiden', 'Community Detection', 'Graph Algorithm', 'Network Science']

# Optional cover image. Put the file in src/assets/blogs/ first.
# cover: ../../assets/blogs/your-image.png
# coverAlt: 'What the image shows, for screen readers.'

# true = keeps the file but publishes nothing, not even the URL.
draft: false
---

社区发现（community detection）的目标，是把网络中的节点划分成若干组，使得同一组内部的连接相对紧密，不同组之间的连接相对稀疏。它常被用于分析社交网络、引文网络、生物网络和知识图谱中的潜在结构。

Leiden 算法由 Traag、Waltman 和 van Eck 于 2019 年提出。它可以看作对 Louvain 算法的改进：两者都通过局部优化和图聚合来最大化某个划分质量函数，但 Leiden 在二者之间增加了一个关键的**细化（refinement）阶段**，从而避免 Louvain 产生内部不连通或连接很差的社区。

这篇文章先记录算法的整体框架，再逐步补充公式、实现和实验。

## 目录

- [1. 问题定义与基本记号](#1-问题定义与基本记号)
- [2. 划分质量如何衡量](#2-划分质量如何衡量)
- [3. 从 Louvain 的缺陷说起](#3-从-louvain-的缺陷说起)
- [4. Leiden 算法的三个阶段](#4-leiden-算法的三个阶段)
- [5. 伪代码与一个直观例子](#5-伪代码与一个直观例子)
- [6. Leiden、Louvain 与标签传播的对比](#6-leidenlouvain-与标签传播的对比)
- [7. Python 实现](#7-python-实现)
- [8. 参数、评估与常见误区](#8-参数评估与常见误区)
- [9. 当前理解与待补充内容](#9-当前理解与待补充内容)

## 1. 问题定义与基本记号

给定一个无向加权图 $G=(V,E)$，社区发现要寻找一个划分

$$
\mathcal{P}=\{C_1,C_2,\ldots,C_k\},
$$

使每个节点恰好属于一个社区。这里先约定：

- $A_{ij}$：节点 $i$ 与 $j$ 之间的边权；
- $k_i=\sum_j A_{ij}$：节点 $i$ 的加权度；
- $m=\frac{1}{2}\sum_{ij}A_{ij}$：图中所有边的总权重；
- $c_i$：节点 $i$ 所属的社区；
- $\delta(c_i,c_j)$：当 $c_i=c_j$ 时为 1，否则为 0。

社区发现通常是**无监督**问题。“社区”并没有唯一的标准答案，而是由图的构造方式、选用的质量函数和分辨率参数共同定义。因此，Leiden 更准确的描述不是“找到真实社区”，而是“高效地寻找一个使指定质量函数较大的划分”。

## 2. 划分质量如何衡量

Leiden 是一个优化框架，本身并不局限于某一个目标函数。最常见的选择是 Modularity 和 Constant Potts Model（CPM）。

### 2.1 Modularity

Modularity 比较“社区内实际存在的边”与“保持节点度数不变的随机网络中期望出现的边”。带分辨率参数 $\gamma$ 的一种写法是

$$
Q=\frac{1}{2m}\sum_{ij}
\left(A_{ij}-\gamma\frac{k_i k_j}{2m}\right)
\delta(c_i,c_j).
$$

当 $\gamma=1$ 时就是经典 Modularity。直观上：

- $A_{ij}$ 奖励把连接较强的节点放进同一社区；
- $\frac{k_i k_j}{2m}$ 是配置模型给出的随机基线；
- 较大的 $\gamma$ 通常产生更多、更小的社区，较小的 $\gamma$ 通常产生更少、更大的社区。

Modularity 的一个经典问题是**分辨率极限（resolution limit）**：在足够大的网络中，目标函数可能倾向于合并一些本来很自然的小社区。调节 $\gamma$ 可以改变观察尺度，但不会让“正确尺度”自动出现。

### 2.2 Constant Potts Model

CPM 不使用依赖整张图规模的随机网络作为基线。一种常见形式是

$$
Q_{\mathrm{CPM}}
=\sum_{C\in\mathcal{P}}
\left[m_C-\gamma\binom{n_C}{2}\right],
$$

其中 $m_C$ 是社区 $C$ 内部边的总权重，$n_C$ 是社区中的节点数。第一项奖励社区内部的连接，第二项惩罚过大的社区。

$\gamma$ 在这里可以理解为对社区内部连接密度的要求。CPM 具有明确的多尺度含义，并在特定定义下避免了 Modularity 的全局分辨率极限；但参数仍然需要结合数据含义和稳定性实验来选择。

> 目标函数决定“什么样的划分是好划分”，Leiden 决定“如何更可靠地搜索这样的划分”。二者不能混为一谈。

## 3. 从 Louvain 的缺陷说起

Louvain 算法反复执行两个阶段：

1. **局部移动**：逐个尝试把节点移动到邻居所在社区，只接受能提高目标函数的移动；
2. **图聚合**：把每个社区压缩成一个超节点，在更小的图上继续优化。

这个过程速度很快，但存在结构性问题。一个节点在较早阶段充当两个子群之间的“桥”，随后又被移动到其他社区时，原社区可能被撕裂。Louvain 只检查单个节点移动能否提高质量，不会主动把已经形成但内部连接很差的社区拆开。

因此，高质量函数值并不必然表示划分在拓扑上合理。Louvain 的结果中可能出现：

- 同一社区包含多个互不连通的部分；
- 社区虽然连通，但只靠很弱的桥连接；
- 重复迭代 Louvain 仍无法修复已经被聚合到同一超节点中的错误结构。

一旦若干节点被压成同一个超节点，后续层级就无法再分别移动它们。Leiden 的核心改动正是：**不要立刻按照局部移动后的社区聚合，先在社区内部做一次细化。**

## 4. Leiden 算法的三个阶段

一轮 Leiden 主要包括局部移动、划分细化和图聚合三个阶段。

### 4.1 阶段一：快速局部移动

算法通常从单节点社区或给定的初始划分出发。对节点 $v$，暂时把它从当前社区取出，计算将它放入各个相邻社区带来的质量增益 $\Delta Q$，再执行一次正增益移动。

Leiden 使用一种快速队列更新策略：

1. 初始时把所有节点加入待处理队列；
2. 节点移动后，只把受影响且不在队列中的邻居重新加入队列；
3. 队列为空时，本轮局部移动结束。

与每轮都重新扫描所有节点相比，这样可以减少大量没有必要的检查。阶段结束后得到一个局部改进的**粗划分** $\mathcal{P}$，但它的社区内部仍然可能需要修复。

### 4.2 阶段二：划分细化

这是 Leiden 与 Louvain 最关键的区别。对粗划分 $\mathcal{P}$ 中的每个社区，算法进行受约束的内部细化：

- 先把该社区内部的节点视为若干单节点社区；
- 只允许这些节点或子社区在原粗社区内部合并；
- 只有满足连接性条件且能带来正增益的合并才会被考虑；
- 原始算法会在正增益候选中引入随机选择，目标增益越大，被选择的概率通常越高。

最终得到细化划分 $\mathcal{P}_{\mathrm{refined}}$。它可能把一个粗社区拆成多个内部连接更合理的子社区。需要注意，细化的目标不是立即替代粗划分的语义，而是为下一步建立更安全的聚合单元。

### 4.3 阶段三：基于细化结果聚合

算法把 $\mathcal{P}_{\mathrm{refined}}$ 中的每个子社区压缩为一个超节点：

- 子社区内部的边变成超节点的自环；
- 两个子社区之间的边权相加，成为对应超节点之间的边权；
- 粗划分 $\mathcal{P}$ 被映射到新的聚合图上，作为下一轮优化的初始划分。

这个细节很重要：**超节点由细化划分决定，超节点初始属于哪个社区则由粗划分决定。** 因此，下一轮既保留了上一轮找到的社区结构，又仍能单独移动那些不应该被永久绑在一起的细化子社区。

随后，算法在更小的聚合图上重复三个阶段，直到继续移动不再提高目标函数。

### 4.4 Leiden 保证了什么

在论文讨论的质量函数与无向图设定下，Leiden 能避免 Louvain 产生的不连通社区，并通过重复迭代逐步得到满足更强局部最优性质的划分。论文使用 $\gamma$-连通、节点最优和子集最优等概念精确描述这些性质。

这里最需要记住两点：

1. **连通性保证不等于全局最优。** Leiden 仍然是启发式算法，可能停在不同的局部最优解；
2. **拓扑合理不等于语义正确。** 输出社区是否有意义，仍取决于建图方式、边权、目标函数与分辨率。

## 5. 伪代码与一个直观例子

忽略节点到聚合图之间的映射细节，Leiden 的框架可以写成：

```text
输入：图 G、质量函数 H、初始划分 P

repeat
    P_coarse  <- FastLocalMove(G, P, H)
    P_refined <- RefinePartition(G, P_coarse, H)
    G         <- AggregateGraph(G, P_refined)
    P         <- ProjectCoarsePartition(P_coarse, P_refined)
until 不再存在正的质量增益

返回：映射回原始节点的划分 P
```

考虑两个三角形通过一条很弱的边相连：

```text
A ----- B             D ----- E
 \     /               \     /
   C --------(弱边)------ F
```

在合适的分辨率下，一个自然结果是 $\{A,B,C\}$ 与 $\{D,E,F\}$ 两个社区。局部移动负责发现这种高内部密度结构；如果一次早期移动暂时把两侧错误地并在一起，细化阶段仍能把内部的两个连通子结构作为不同聚合单元保留下来，而不是立即将六个节点压成一个不可拆分的超节点。

这个例子只用于理解流程。实际划分仍由质量增益决定；“桥很弱”并不会脱离目标函数单独构成判据。

## 6. Leiden、Louvain 与标签传播的对比

| 方法 | 核心思想 | 优点 | 主要局限 |
| --- | --- | --- | --- |
| Louvain | 节点局部移动 + 社区聚合 | 快、实现简单、可扩展 | 可能得到不连通或内部连接很差的社区 |
| Leiden | 局部移动 + 细化 + 聚合 | 通常更快收敛到高质量划分，并保证社区连通 | 仍依赖目标函数、参数和随机初始化 |
| Label Propagation | 节点采用邻居中的主流标签 | 计算便宜，不需要显式优化 Modularity | 结果可能不稳定，社区尺度较难控制 |

Leiden 不是一种全新的质量函数，而是一种改进的优化过程。因此，比较实验时应该保持图、边权和目标函数一致，再比较优化质量、运行时间和划分稳定性。

## 7. Python 实现

Python 中常用 [`igraph`](https://python.igraph.org/) 和 [`leidenalg`](https://leidenalg.readthedocs.io/) 运行 Leiden。下面使用带配置模型空模型的 RB 质量函数；它与带分辨率参数的广义 Modularity 密切相关。

```python
import igraph as ig
import leidenalg as la

edges = [
    ("A", "B", 1.0), ("B", "C", 1.0), ("C", "A", 1.0),
    ("D", "E", 1.0), ("E", "F", 1.0), ("F", "D", 1.0),
    ("C", "F", 0.1),
]

graph = ig.Graph.TupleList(edges, directed=False, weights=True)

partition = la.find_partition(
    graph,
    la.RBConfigurationVertexPartition,
    weights="weight",
    resolution_parameter=1.0,
    n_iterations=-1,
    seed=42,
)

for community in partition:
    print([graph.vs[index]["name"] for index in community])

print("quality:", partition.quality())
```

如果使用 CPM，可以把划分类型换成 `la.CPMVertexPartition`。代码中的 `seed` 用于复现实验，但在正式分析中不应只观察一个随机种子的结果。

## 8. 参数、评估与常见误区

### 8.1 需要重点记录的参数

- **目标函数**：Modularity、RB Configuration 或 CPM 回答的是不同的优化问题；
- **分辨率 $\gamma$**：控制观察社区的尺度，但不能直接理解为“社区数量”；
- **边权**：权重的定义和量纲会直接改变质量增益；
- **随机种子**：Leiden 包含随机过程，不同运行可能得到不同局部最优解；
- **迭代次数和停止条件**：更多迭代通常能继续改善结果，但也增加计算开销；
- **初始划分**：使用已有划分进行热启动，可能加速优化，也可能带来路径依赖。

### 8.2 一个更可靠的实验流程

1. 明确节点、边和边权各自代表什么，先处理重复边、自环和孤立节点；
2. 根据任务选择质量函数，不要默认把 Modularity 当作唯一标准；
3. 扫描一组有解释意义的分辨率，而不是只运行 $\gamma=1$；
4. 每组参数使用多个随机种子，记录质量值、社区数量和运行时间；
5. 用 Adjusted Rand Index（ARI）、Normalized Mutual Information（NMI）或 Variation of Information（VI）比较多次划分的稳定性；
6. 检查每个社区的规模、内部密度、割边以及领域语义；
7. 若存在标签，只把标签作为外部评估信号，不要把“与标签一致”自动等同于结构最优。

### 8.3 常见误区

- **只看最高 Modularity**：目标函数相近的划分，结构可能差异很大；
- **把分辨率当作社区数旋钮**：$\gamma$ 与社区数量通常相关，但关系不一定连续或单调；
- **比较不同目标函数的原始分数**：它们的尺度与含义不同，数值不能直接横向比较；
- **忽略图的类型**：有向边、负权边和多重边需要确认实现的处理方式；
- **只运行一次**：单次结果无法反映局部最优和随机性带来的不确定性；
- **把算法输出当作真值**：社区是模型和数据共同定义的分析结果，而不是无需解释的事实。

## 9. 当前理解与待补充内容

我目前对 Leiden 的核心理解是：Louvain 的问题不只是“搜索得不够久”，而是它过早地把粗社区压成了不可拆分的超节点。Leiden 通过细化阶段改变聚合的最小单位，在保留多层次优化效率的同时，避免把内部不连通的结构永久锁死。

后续准备继续补充：

- [ ] 推导节点移动在 Modularity 和 CPM 下的 $\Delta Q$；
- [ ] 结合一张小图，逐步记录队列、划分和聚合图的变化；
- [ ] 整理 $\gamma$-连通、节点最优与子集最优的严格定义；
- [ ] 比较不同分辨率和随机种子下的社区稳定性；
- [ ] 在一个真实数据集上对比 Leiden 与 Louvain 的质量和运行时间；
- [ ] 补充有向图、负权图和超大规模图上的实现注意事项。

## 参考资料

1. V. A. Traag, L. Waltman, N. J. van Eck, [From Louvain to Leiden: guaranteeing well-connected communities](https://doi.org/10.1038/s41598-019-41695-z), *Scientific Reports*, 2019.
2. V. D. Blondel, J.-L. Guillaume, R. Lambiotte, E. Lefebvre, [Fast unfolding of communities in large networks](https://doi.org/10.1088/1742-5468/2008/10/P10008), *Journal of Statistical Mechanics*, 2008.
3. S. Fortunato, M. Barthélemy, [Resolution limit in community detection](https://doi.org/10.1073/pnas.0605965104), *PNAS*, 2007.
4. V. A. Traag, P. Van Dooren, Y. Nesterov, [Narrow scope for resolution-limit-free community detection](https://doi.org/10.1103/PhysRevE.84.016114), *Physical Review E*, 2011.
