---

title: '从 DFS 到 MCTS：经典搜索算法梳理'
date: 2026-07-15
summary: '从状态空间搜索出发，梳理 DFS、BFS、A*、Minimax 与 α–β 剪枝，以及蒙特卡洛树搜索之间的联系与区别。'

# Which series this belongs to. Must be one of the ids in `blogSeries`
# in src/data/site.ts. A typo here fails the build and names this file.
series: 'algorithm'

tags: ['Search']

# Optional cover image. Put the file in src/assets/blogs/ first.
# cover: ../../assets/blogs/your-image.png
# coverAlt: 'What the image shows, for screen readers.'

# true = keeps the file but publishes nothing, not even the URL.
draft: false
---

搜索算法解决的核心问题可以概括为：**如何在一个由状态和转移构成的空间中，找到满足目标的状态或一条通往目标的路径？**

迷宫寻路、地图导航、八数码、棋类博弈看起来差异很大，但都可以抽象成对一棵树或一张图的搜索。不同算法的主要区别，在于它们如何回答下面几个问题：

1. 接下来扩展哪个节点？
2. 如何利用已经掌握的信息减少无效搜索？
3. 何时可以停止，并相信当前答案足够好？

本文依次整理五类经典算法：DFS、BFS、A*、Minimax + α–β 剪枝和蒙特卡洛树搜索（MCTS）。前两者是无信息搜索，A* 引入启发式知识，后两类则把搜索扩展到存在对手的决策问题中。

> 本文是一份学习框架。后续可以为每个算法补充手绘搜索过程、具体题目、完整实现和自己的理解。

## 目录

- [1. 统一视角：状态空间搜索](#1-统一视角状态空间搜索)
- [2. 深度优先搜索 DFS](#2-深度优先搜索-dfs)
- [3. 广度优先搜索 BFS](#3-广度优先搜索-bfs)
- [4. A*：用启发式函数引导搜索](#4-a用启发式函数引导搜索)
- [5. Minimax 与 α–β 剪枝](#5-minimax-与-αβ-剪枝)
- [6. 蒙特卡洛树搜索 MCTS](#6-蒙特卡洛树搜索-mcts)
- [7. 算法之间的联系](#7-算法之间的联系)
- [8. 如何选择搜索算法](#8-如何选择搜索算法)
- [9. 总结与待补充内容](#9-总结与待补充内容)

## 1. 统一视角：状态空间搜索

在讨论具体算法之前，先定义搜索问题中的几个基本元素：

- **状态（state）**：对当前局面的完整描述，例如迷宫中的坐标或棋盘布局。
- **初始状态（initial state）**：搜索开始的位置。
- **动作（action）**：在一个状态下允许执行的操作。
- **状态转移（transition）**：执行动作后如何得到下一个状态。
- **目标测试（goal test）**：判断当前状态是否满足目标。
- **路径代价（path cost）**：从起点到当前状态所付出的总代价，通常记为 $g(n)$。

搜索过程还会维护一个**边界集合（frontier）**，其中存放已经发现但尚未扩展的节点。DFS、BFS 和 A* 的通用形式非常相似，真正决定算法行为的是“从 frontier 中取出哪个节点”。

| 算法 | frontier 的主要结构 | 下一个扩展的节点 |
| --- | --- | --- |
| DFS | 栈 | 最晚加入的节点 |
| BFS | 队列 | 最早加入的节点 |
| A* | 优先队列 | $f(n)=g(n)+h(n)$ 最小的节点 |

### 树搜索与图搜索

同一个状态可能由不同路径到达。如果完全不记录访问历史，算法实际上在一棵“搜索树”上工作，可能反复搜索同一状态，甚至陷入环中。图搜索通常额外维护 `visited`、`closed` 或当前已知的最小代价，从而避免不必要的重复。

需要区分两个概念：

- **搜索状态**是问题本身的状态，例如坐标 `(x, y)`。
- **搜索节点**除了状态，还可能保存父节点、深度、累计代价等搜索过程中的信息。

这个区别在 A* 中尤其重要，因为同一个状态可能被一条代价更低的新路径再次到达。

## 2. 深度优先搜索 DFS

深度优先搜索（Depth-First Search）会优先沿一条路径不断向下探索，直到无法继续，再回退到最近的分叉点。它可以用递归自然地实现，也可以显式维护一个栈。

### 2.1 基本思路

假设当前位于一个迷宫岔路口，DFS 会先选择其中一个方向一直走到底；如果遇到死路，就退回上一个岔路口尝试其他方向。这种策略只需要保存当前路径和少量尚未访问的分支，因此空间开销通常较小。

### 2.2 伪代码

```python
def dfs(start):
    stack = [start]
    visited = {start}

    while stack:
        node = stack.pop()

        if is_goal(node):
            return reconstruct_path(node)

        for child in successors(node):
            if child not in visited:
                visited.add(child)       # 入栈时标记，避免重复入栈
                child.parent = node
                stack.append(child)

    return None
```

如果需要保证生成的路径与预期的邻居顺序一致，要注意栈的后进先出性质：邻居的入栈顺序与实际访问顺序相反。

### 2.3 性质与复杂度

用 $b$ 表示平均分支因子，$m$ 表示搜索树的最大深度：

- 时间复杂度最坏为 $O(b^m)$。
- 树搜索的空间复杂度约为 $O(bm)$，通常显著小于 BFS。
- DFS 找到的第一个解不一定是最短或代价最低的解。
- 在无限深的状态空间中，DFS 可能永远沿错误分支向下搜索。
- 在有限图上加入正确的去重机制后，DFS 能够遍历所有可达节点，此时时间复杂度为 $O(|V|+|E|)$。

### 2.4 适用场景

DFS 常用于：

- 图的连通性判断；
- 拓扑排序和环检测；
- 回溯问题，如排列、组合、数独和 N 皇后；
- 只关心是否存在解，而且内存比较有限的问题。

### 2.5 容易忽略的问题

1. **忘记处理环**：在图上搜索时可能无限循环。
2. **过早标记或取消访问**：普通图遍历与回溯枚举对 `visited` 的语义不同。前者一般永久标记，后者可能需要在返回时撤销选择。
3. **把第一个解当作最优解**：普通 DFS 没有这一保证。

> 可补充：用一个小迷宫画出 DFS 的入栈、出栈和回溯顺序。

## 3. 广度优先搜索 BFS

广度优先搜索（Breadth-First Search）从起点开始逐层扩展：先访问所有距离为 1 的状态，再访问距离为 2 的状态，以此类推。它使用队列维护 frontier。

### 3.1 基本思路

可以把 BFS 想象成水波从起点向四周扩散。只要每一步的代价相同，目标第一次被发现时，对应的路径就是步数最少的路径。

### 3.2 伪代码

```python
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()

        if is_goal(node):
            return reconstruct_path(node)

        for child in successors(node):
            if child not in visited:
                visited.add(child)       # 入队时标记，避免重复入队
                child.parent = node
                queue.append(child)

    return None
```

这里选择在节点**入队时**标记访问。如果等到出队才标记，同一个节点可能在被处理前多次进入队列，造成额外的时间与空间开销。

### 3.3 性质与复杂度

用 $d$ 表示最浅目标节点的深度：

- 在有限分支因子的前提下，BFS 是完备的，即存在解时最终能够找到解。
- 当每条边的代价相同时，BFS 找到的第一个解是最短路径。
- 按搜索树分析，时间和空间复杂度都为 $O(b^{d+1})$。
- 按显式图分析，时间复杂度为 $O(|V|+|E|)$，空间复杂度为 $O(|V|)$。

BFS 的主要瓶颈通常不是时间，而是保存整层节点带来的内存消耗。

### 3.4 BFS 与 DFS 的对比

| 对比项 | DFS | BFS |
| --- | --- | --- |
| 数据结构 | 栈 / 递归 | 队列 |
| 搜索顺序 | 优先向深处 | 逐层扩展 |
| 内存占用 | 通常较小 | 通常较大 |
| 无权最短路 | 不保证 | 保证 |
| 无限深空间 | 可能陷入深分支 | 有限分支时可找到浅层解 |

> 可补充：比较 DFS 和 BFS 在同一个迷宫中找到的两条路径，以及它们各自扩展的节点数。

## 4. A*：用启发式函数引导搜索

DFS 和 BFS 不理解“目标大概在哪个方向”。A* 在累计路径代价之外，引入启发式函数来估计当前位置到目标的剩余代价。

对节点 $n$，A* 的评价函数为：

$$
f(n)=g(n)+h(n)
$$

其中：

- $g(n)$ 是从起点到节点 $n$ 的实际代价；
- $h(n)$ 是从节点 $n$ 到目标的估计代价；
- $f(n)$ 是经过节点 $n$ 到达目标的估计总代价。

每一步，A* 都从优先队列中选择 $f(n)$ 最小的节点进行扩展。

### 4.1 从 Dijkstra 到 A*

如果令 $h(n)=0$，A* 就退化为一致代价搜索；在非负权图上，这与 Dijkstra 算法的核心选择规则相同。如果只考虑 $h(n)$ 而忽略 $g(n)$，则接近贪心最佳优先搜索。

因此，可以把 A* 理解为两种倾向之间的平衡：

- $g(n)$ 让算法尊重已经付出的真实代价；
- $h(n)$ 让算法倾向于靠近目标。

### 4.2 启发式函数

启发式函数决定了 A* 的效率和最优性。常见的两个条件是：

**可采纳性（admissibility）**：启发式函数从不高估真实的最小剩余代价。

$$
0 \le h(n) \le h^*(n)
$$

其中 $h^*(n)$ 表示从 $n$ 到目标的真实最小代价。

**一致性（consistency）**：对于任意从 $n$ 到 $n'$、代价为 $c(n,n')$ 的转移，都满足：

$$
h(n) \le c(n,n') + h(n')
$$

一致性相当于启发式函数满足一种三角不等式。它能够保证沿路径的 $f$ 值不会下降。对采用 closed set 且不重新打开节点的常见图搜索实现，一致性是保证最优性的一个重要条件。

以四方向移动的网格为例，如果每次移动代价为 1，可以使用曼哈顿距离：

$$
h(n)=|x_n-x_{goal}|+|y_n-y_{goal}|
$$

### 4.3 伪代码

```python
from heapq import heappop, heappush

def astar(start, goal):
    # 元素形式：(f, tie_breaker, node)
    open_heap = []
    heappush(open_heap, (heuristic(start, goal), 0, start))

    best_g = {start: 0}
    parent = {start: None}
    counter = 1

    while open_heap:
        f, _, node = heappop(open_heap)

        # 优先队列里可能保留同一状态的旧条目
        if f > best_g[node] + heuristic(node, goal):
            continue

        if node == goal:
            return reconstruct_path_from(parent, goal)

        for child, step_cost in successors(node):
            new_g = best_g[node] + step_cost

            if child not in best_g or new_g < best_g[child]:
                best_g[child] = new_g
                parent[child] = node
                new_f = new_g + heuristic(child, goal)
                heappush(open_heap, (new_f, counter, child))
                counter += 1

    return None
```

`tie_breaker` 用来避免两个 $f$ 值相同且节点对象不可比较时，堆继续比较节点本身。实际实现还需要明确是否维护 closed set，以及找到更短路径后是否允许重新打开节点。

### 4.4 性质与局限

- 在常见条件下，使用可采纳启发式的 A* 能找到最优解；图搜索的具体保证还取决于一致性和节点重开策略。
- 启发式越接近真实剩余代价，通常扩展的无关节点越少。
- 当 $h(n)=0$ 时，A* 不再获得方向信息。
- A* 最坏情况下仍可能扩展指数数量的节点。
- 与 BFS 类似，A* 通常需要保存大量候选节点，内存可能成为主要限制。

### 4.5 设计启发式函数的原则

1. 从问题的“放松版本”中推导一个容易计算的下界。
2. 在保证所需最优性的前提下，让估计尽量接近真实代价。
3. 同时考虑启发式函数本身的计算成本；更精确但极其昂贵的估计未必更快。
4. 明确业务需要的是严格最优解，还是更快得到一个足够好的解。

> 可补充：展示同一张网格上 BFS、Dijkstra 和 A* 的扩展区域，并比较不同启发式函数的效果。

## 5. Minimax 与 α–β 剪枝

前面的算法面对的是一个相对静态的环境，而棋类博弈中存在一个会主动阻止我们获胜的对手。搜索目标因此从“找到一条通往目标的路径”变成“在假设双方都采取最佳行动时，选择自己的最佳行动”。

这一节先考虑以下类型的博弈：

- 双人、轮流行动；
- 确定性环境；
- 完全信息；
- 零和博弈。

### 5.1 Minimax

在博弈树中，己方节点称为 MAX 节点，希望最大化局面价值；对方节点称为 MIN 节点，希望最小化局面价值。

设 $V(s)$ 为状态 $s$ 的价值，则 Minimax 的递归定义为：

$$
V(s)=
\begin{cases}
U(s), & s \text{ 是终局} \\
\max\limits_{a \in A(s)} V(\operatorname{Result}(s,a)), & s \text{ 是 MAX 节点} \\
\min\limits_{a \in A(s)} V(\operatorname{Result}(s,a)), & s \text{ 是 MIN 节点}
\end{cases}
$$

其中 $U(s)$ 是终局的效用，例如胜、负、和分别取 $1$、$-1$、$0$。

如果无法搜索到终局，就在固定深度停止，并用评价函数 $E(s)$ 估计局面价值。这也带来了两个问题：评价函数是否可靠，以及截断深度是否足够。

### 5.2 α–β 剪枝

Minimax 会枚举深度范围内的整棵博弈树，但其中一些分支不可能影响最终选择。α–β 剪枝通过维护两个边界提前停止这些分支的搜索：

- $\alpha$：MAX 在当前路径上已经能够保证的最好值；
- $\beta$：MIN 在当前路径上已经能够保证的最好值。

当出现 $\alpha \ge \beta$ 时，当前节点后续未搜索的分支不可能改变祖先节点的决策，因此可以被剪掉。

```python
def alphabeta(state, depth, alpha, beta, maximizing):
    if depth == 0 or is_terminal(state):
        return evaluate(state)

    if maximizing:
        value = float("-inf")
        for child in ordered_successors(state):
            value = max(
                value,
                alphabeta(child, depth - 1, alpha, beta, False),
            )
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    value = float("inf")
    for child in ordered_successors(state):
        value = min(
            value,
            alphabeta(child, depth - 1, alpha, beta, True),
        )
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value
```

根节点第一次调用时，通常令 $\alpha=-\infty$、$\beta=+\infty$。

### 5.3 为什么剪枝不会改变结果

假设 MAX 已经在其他分支中找到一个值为 5 的选择，即 $\alpha=5$。现在搜索另一个 MIN 子树时，只要发现 MIN 能把该分支的值压到 4 或更低，MAX 就不会选择它。这个 MIN 子树剩余的分支即使继续搜索，也无法让 MIN 主动放弃已经存在的更小值，因此没有必要再计算。

α–β 剪枝改变的是需要访问的节点数量，而不是 Minimax 的最终结果。

### 5.4 搜索顺序的重要性

α–β 剪枝的效果高度依赖行动顺序：

- 最坏情况下仍需搜索 $O(b^d)$ 个节点，与普通 Minimax 相同。
- 理想排序下，节点数量可接近 $O(b^{d/2})$，相当于在相同计算预算下把搜索深度近似翻倍。

实践中常结合迭代加深、历史启发、杀手启发或上一次搜索结果来优先搜索更可能优秀的行动。

### 5.5 局限

- 博弈树规模随搜索深度指数增长。
- 评价函数质量直接影响决策质量。
- 固定深度截断可能产生**水平线效应（horizon effect）**：算法看不到搜索边界之后即将发生的重要事件。
- 基础 Minimax 更适合分支因子较小、规则确定且可以设计有效评价函数的游戏。

> 可补充：画一棵三层博弈树，从叶节点向上回传数值，并用不同颜色标出被 α–β 剪掉的分支。

## 6. 蒙特卡洛树搜索 MCTS

当博弈树太大、难以设计精确评价函数时，可以不完整地遍历整棵树，而是把计算资源集中到更有希望的分支上。蒙特卡洛树搜索（Monte Carlo Tree Search，MCTS）通过反复模拟来估计行动价值。

MCTS 的每次迭代包含四个阶段。

### 6.1 选择（Selection）

从根节点开始，根据“利用当前最好选择”和“探索访问较少的选择”之间的平衡，沿树向下选择节点。常见策略是 UCT（Upper Confidence Bounds applied to Trees）：

$$
\operatorname{UCT}(i)=\frac{Q_i}{N_i}+c\sqrt{\frac{\ln N_p}{N_i}}
$$

其中：

- $Q_i$ 是子节点 $i$ 的累计回报；
- $N_i$ 是子节点 $i$ 的访问次数；
- $N_p$ 是父节点的访问次数；
- $c$ 是控制探索强度的常数。

第一项偏向平均回报高的节点，称为**利用**；第二项偏向访问次数少的节点，称为**探索**。尚未访问的节点通常被优先选择，而不是直接代入 $N_i=0$ 的公式。

### 6.2 扩展（Expansion）

如果当前节点不是终局，并且仍有尚未尝试的动作，就选择其中一个动作并为产生的新状态创建子节点。

### 6.3 模拟（Simulation / Rollout）

从新节点出发，根据随机策略或轻量策略继续行动，直到到达终局或预设的截断条件，得到一次模拟结果。

纯随机模拟实现简单，但可能产生大量不符合常识的对局。加入领域知识的 rollout policy 往往能提高估计质量，同时也会增加单次模拟成本。

### 6.4 回传（Backpropagation）

沿本次访问的路径向上更新每个节点的访问次数和累计回报。

在双人零和游戏中，必须统一价值的观察视角。例如：

- 始终记录根节点玩家的收益，并在对手节点选择较小值；或
- 每个节点记录“轮到该节点行动的玩家”的收益，在逐层回传时改变符号。

两种方法都可以，但实现时不能混用。

### 6.5 伪代码

```python
def mcts(root, iterations):
    for _ in range(iterations):
        node = root

        # 1. Selection
        while node.is_fully_expanded() and not node.is_terminal():
            node = select_child_by_uct(node)

        # 2. Expansion
        if not node.is_terminal():
            node = expand_one_untried_action(node)

        # 3. Simulation
        reward = rollout(node.state)

        # 4. Backpropagation
        while node is not None:
            node.visits += 1
            node.total_reward += reward_from_node_perspective(reward, node)
            node = node.parent

    # 实战中常选择访问次数最多的根节点子节点
    return max(root.children, key=lambda child: child.visits).action
```

### 6.6 MCTS 的特点

- **随时可用（anytime）**：预算用完时即可返回当前结果，更多迭代通常带来更稳定的估计。
- **不要求遍历完整博弈树**：搜索会逐渐集中到更有希望的区域。
- **对评价函数依赖较小**：可以主要通过模拟结果估计价值。
- **容易并行化部分计算**，但共享搜索树时仍需处理同步和访问偏差。
- 对模拟策略、探索常数、奖励设计和计算预算较敏感。
- 如果有意义的结果只出现在很深的位置，随机模拟的信号可能非常稀疏。

> 可补充：以井字棋为例，记录根节点各动作的访问次数和平均胜率如何随迭代次数变化。

## 7. 算法之间的联系

这些算法并不是互不相关的知识点，而是对“选择下一个要扩展的节点”这一问题给出的不同答案。

| 算法 | 问题环境 | 主要依据 | 是否保证最优 | 主要代价 |
| --- | --- | --- | --- | --- |
| DFS | 单智能体、无信息 | 当前深度 | 通常不保证 | 可能走入很深的错误分支 |
| BFS | 单智能体、无信息 | 节点深度 | 等代价边上保证 | frontier 占用大量内存 |
| A* | 单智能体、有启发信息 | $g(n)+h(n)$ | 满足相应条件时保证 | 启发式设计与内存开销 |
| Minimax + α–β | 双人对抗、确定性 | 对手也采取最优行动 | 搜索范围内给出 Minimax 最优决策 | 节点数随深度指数增长 |
| MCTS | 大规模决策或博弈 | 采样得到的价值与不确定性 | 有渐近收敛性质，但有限预算下不保证 | 需要大量模拟，结果具有随机性 |

可以用三条线索理解它们的演进：

1. **从盲目到有方向**：DFS、BFS 只依赖结构；A* 通过启发式函数利用问题知识。
2. **从单方规划到对抗决策**：Minimax 把“环境变化”替换为“理性对手的选择”。
3. **从完整枚举到采样估计**：α–β 安全地删除不影响结果的分支；MCTS 则在有限预算下有选择地构建搜索树。

值得注意的是，Minimax 与 MCTS 经常解决相似的博弈问题，但思路不同。Minimax 倾向于在固定深度内系统搜索，并依赖叶节点评价函数；MCTS 倾向于反复采样，让访问次数逐渐集中到高价值行动上。

## 8. 如何选择搜索算法

面对一个具体问题，可以依次问以下问题：

1. **状态空间是图还是树？** 如果状态可能重复，需要考虑去重或更优路径更新。
2. **是否要求最短或最低代价？** 不要求时 DFS 可能足够；无权最短路可用 BFS；有权图可考虑 Dijkstra 或 A*。
3. **是否有可靠的方向信息？** 如果能构造低成本的启发式函数，可以考虑 A*。
4. **是否存在对手？** 对确定性双人零和博弈，可以从 Minimax + α–β 剪枝开始。
5. **搜索树是否大到无法系统展开？** 如果可以快速模拟结果，MCTS 可能更合适。
6. **时间和内存预算是多少？** BFS 与 A* 往往受内存限制；DFS 省内存但可能浪费大量时间；MCTS 可以直接按时间或迭代次数分配预算。
7. **需要严格最优，还是近似但及时的决策？** 这个要求通常比算法名字本身更能决定最终方案。

## 9. 总结与待补充内容

从统一的状态空间视角看，搜索算法的差别主要体现在节点选择策略和信息利用方式上：

- DFS 用深度换取较低的空间开销；
- BFS 逐层搜索，并在等代价边上保证最短路径；
- A* 用 $g(n)+h(n)$ 同时考虑已付代价和未来估计；
- Minimax 假设对手同样理性，α–β 剪枝在不改变结果的前提下减少搜索；
- MCTS 用反复模拟近似行动价值，在探索与利用之间动态平衡。

后续完善本文时，可以重点补充：

- [ ] 为 DFS、BFS 和 A* 设计同一个网格寻路例子；
- [ ] 为每种算法添加可运行的 Python 实现和测试；
- [ ] 画出 Minimax 的数值回传与 α–β 剪枝过程；
- [ ] 实现一个井字棋 MCTS，并记录不同迭代次数下的表现；
- [ ] 补充双向 BFS、迭代加深 DFS、IDA* 等相关变体；
- [ ] 根据自己的理解重写“适用场景”和“算法联系”两节；
- [ ] 加入参考资料与延伸阅读。
