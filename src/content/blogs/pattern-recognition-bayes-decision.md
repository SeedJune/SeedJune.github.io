---
title: '模式识别笔记（一）：Bayes 决策理论'
date: 2026-09-18
summary: '基于后验概率与条件风险推导 Bayes 决策准则，分析高斯判别函数、协方差结构及决策边界的几何性质。'
series: 'pattern-recognition'
tags: ['Pattern Recognition', 'Bayes Decision', 'Gaussian Classifier']
cover: ../../assets/blogs/pattern-recognition-bayes-decision-cover.png
coverAlt: '重叠的青绿与珊瑚橙概率分布经过弯曲决策边界，形成两类样本的判别区域'
draft: false
---

统计模式识别研究如何根据观测特征推断样本所属的类别。Bayes 决策理论以类别先验概率、类条件概率分布和损失函数为基础，将分类问题表述为期望损失的最小化问题。最小错误率决策与最小风险决策分别对应不同的损失设定；在高斯分布假设下，决策规则可以进一步化为具有明确几何意义的判别函数。

## 1. 统计决策的概率模型

设类别随机变量为 $\omega\in\{\omega_1,\ldots,\omega_K\}$，观测随机向量为 $\mathbf X\in\mathbb R^d$，其实现值记为 $\mathbf x$。类别先验概率 $\pi_i=P(\omega_i)$ 描述获得观测之前的类别分布；类条件密度 $p(\mathbf x\mid\omega_i)$ 描述给定类别时的特征分布。由全概率公式，观测的边缘密度为

$$
p(\mathbf x)=\sum_{j=1}^{K}\pi_jp(\mathbf x\mid\omega_j).
$$

在 $p(\mathbf x)>0$ 处，Bayes 公式给出类别后验概率：

$$
P(\omega_i\mid\mathbf x)
=\frac{\pi_i p(\mathbf x\mid\omega_i)}
{\sum_{j=1}^{K}\pi_jp(\mathbf x\mid\omega_j)}.
$$

后验概率综合了类别出现的先验频率与观测在各类条件分布下的相对密度。类条件密度较大，并不必然意味着类别后验概率较大，因为先验概率同样参与后验的计算。分母起归一化作用，使所有类别的后验概率之和为 1。

类别概率与观测密度具有不同含义。对于具有概率密度的连续随机向量，单点事件的概率为零，区域事件的概率由密度积分给出；密度值本身可以大于 1。因而，$p(\mathbf x\mid\omega_i)$ 不能直接解释为样本属于 $\omega_i$ 的概率。

决策规则 $D$ 将特征空间映射到类别集合。记

$$
S_i=\{\mathbf x:D(\mathbf x)=\omega_i\},
$$

则各决策区域构成特征空间的一个划分，相邻区域的边界称为决策边界。Bayes 最优性是相对于给定概率分布、损失函数和可用观测信息而言的。真实分布已知时，Bayes 决策达到相应期望风险的下界；使用估计分布构造的决策规则，则未必达到真实分布下的这一界限。

## 2. 最小错误率决策

### 2.1 最大后验分类规则

在所有误分类具有相同代价的情形下，分类目标可以表述为最小化错误率。给定观测 $\mathbf x$，若选择类别 $\omega_i$，其条件错误率为

$$
P(e\mid\mathbf x,D(\mathbf x)=\omega_i)
=1-P(\omega_i\mid\mathbf x).
$$

因此，最小条件错误率由最大后验概率对应的类别实现：

$$
i^*(\mathbf x)\in\arg\max_iP(\omega_i\mid\mathbf x),
\qquad D^*(\mathbf x)=\omega_{i^*(\mathbf x)}.
$$

若存在多个后验概率相等的最大值，选择其中任一类别均具有相同的条件错误率。

对于固定观测，边缘密度 $p(\mathbf x)$ 与类别下标无关，因此

$$
\arg\max_iP(\omega_i\mid\mathbf x)
=\arg\max_i\pi_i p(\mathbf x\mid\omega_i).
$$

在先验和密度均为正时，可以取对数定义判别函数

$$
g_i(\mathbf x)=\log p(\mathbf x\mid\omega_i)+\log\pi_i.
$$

对数变换保持大小关系，并将乘积转化为加法。分类结果由 $g_i(\mathbf x)$ 的最大值决定。零概率项可通过扩展约定 $\log0=-\infty$ 处理。

当各类别先验相等时，先验项不影响类别比较，规则简化为最大似然分类。一般情况下，忽略先验会改变决策目标。此处最大似然分类的优化对象是类别，而参数估计中最大似然方法的优化对象是分布参数。

### 2.2 总体错误率与最优性

决策规则 $D$ 的总体错误率为

$$
P_e(D)=1-\sum_{i=1}^{K}\int_{S_i}
P(\omega_i\mid\mathbf x)p(\mathbf x)\,d\mathbf x.
$$

最大后验规则在每个观测处均达到最小条件错误率。由于边缘密度非负，对条件错误率积分仍保持这一大小关系，故该规则也使总体错误率最小。其最小值称为 Bayes 错误率：

$$
\begin{aligned}
P_e^*
&=\int\left[1-\max_iP(\omega_i\mid\mathbf x)\right]
p(\mathbf x)\,d\mathbf x\\
&=1-\int\max_i\{\pi_i p(\mathbf x\mid\omega_i)\}\,d\mathbf x.
\end{aligned}
$$

该结论适用于所有允许的可测决策规则。若进一步要求分类器具有特定函数形式，例如仅允许线性边界，则相应受限模型未必能够实现 Bayes 规则。

Bayes 错误率反映了在给定特征信息下的类别可分性。若不同类别的条件分布在具有正概率的区域内重叠，即使分布完全已知，也可能存在不可消除的分类错误。

### 2.3 二分类中的似然比与决策边界

对于两类问题，在分母密度为正处定义似然比

$$
\Lambda(\mathbf x)=
\frac{p(\mathbf x\mid\omega_1)}{p(\mathbf x\mid\omega_2)}.
$$

当两类先验均为正时，最小错误率规则满足

$$
\Lambda(\mathbf x)>\frac{\pi_2}{\pi_1}
\quad\Longrightarrow\quad D^*(\mathbf x)=\omega_1.
$$

反向不等式对应 $\omega_2$，相等处允许任一选择。若某个类条件密度为零，则直接比较两个加权密度 $\pi_i p(\mathbf x\mid\omega_i)$，无需使用比值。

相应的对数判别函数为

$$
f(\mathbf x)=\log\Lambda(\mathbf x)+\log\frac{\pi_1}{\pi_2}.
$$

$f(\mathbf x)>0$ 和 $f(\mathbf x)<0$ 分别对应两个决策区域，等值集合 $f(\mathbf x)=0$ 给出候选边界。边界的几何结构由类条件密度决定，可能包含多个连通部分。

总体错误率可以分解为两种误分类的概率之和：

$$
P_e(D)=\pi_1\int_{S_2}p(\mathbf x\mid\omega_1)\,d\mathbf x
+\pi_2\int_{S_1}p(\mathbf x\mid\omega_2)\,d\mathbf x.
$$

最大后验规则在每一点选择加权密度较大的类别，其错误贡献对应较小的加权密度，因此

$$
P_e^*=\int\min\{\pi_1p(\mathbf x\mid\omega_1),
\pi_2p(\mathbf x\mid\omega_2)\}\,d\mathbf x.
$$

在一维情况下，该积分等于两条加权密度曲线下的重叠面积。先验概率的变化既影响决策阈值，也影响错误率积分中的类别权重。

## 3. 最小风险决策

### 3.1 损失函数与条件风险

最小错误率准则对所有误分类赋予相同代价。当不同误判具有不同后果时，需要通过损失函数描述这种差异。定义

$$
\lambda_{ij}=\lambda(\omega_i\mid\omega_j),
$$

表示真实类别为 $\omega_j$ 时，决策为 $\omega_i$ 所产生的损失。损失矩阵的行对应决策类别，列对应真实类别。正确分类的损失通常设为零，但一般决策理论并不要求这一限制。

给定观测后，选择 $\omega_i$ 的条件风险为对真实类别后验分布求得的期望损失：

$$
R(\omega_i\mid\mathbf x)
=\sum_{j=1}^{K}\lambda_{ij}P(\omega_j\mid\mathbf x).
$$

总体风险则为

$$
R(D)=\sum_{i=1}^{K}\int_{S_i}
R(\omega_i\mid\mathbf x)p(\mathbf x)\,d\mathbf x.
$$

对每个观测选择条件风险最小的决策，可使总体风险最小：

$$
i^*(\mathbf x)\in\arg\min_iR(\omega_i\mid\mathbf x),
\qquad D^*(\mathbf x)=\omega_{i^*(\mathbf x)}.
$$

由 Bayes 公式，该比较等价于

$$
\arg\min_i\sum_{j=1}^{K}\lambda_{ij}
\pi_jp(\mathbf x\mid\omega_j).
$$

省略边缘密度不改变风险的排序，但计算条件风险本身的数值仍需使用归一化的后验概率。

### 3.2 二分类风险阈值

记 $P_j=P(\omega_j\mid\mathbf x)$。选择 $\omega_1$ 的条件为

$$
\lambda_{11}P_1+\lambda_{12}P_2
<\lambda_{21}P_1+\lambda_{22}P_2,
$$

即

$$
(\lambda_{21}-\lambda_{11})P_1
>(\lambda_{12}-\lambda_{22})P_2.
$$

若 $\lambda_{21}>\lambda_{11}$ 且 $\lambda_{12}>\lambda_{22}$，并且先验概率与相关密度为正，则上述不等式可化为

$$
\Lambda(\mathbf x)>
\frac{\lambda_{12}-\lambda_{22}}{\lambda_{21}-\lambda_{11}}
\frac{\pi_2}{\pi_1}.
$$

若损失差为零或负数，应直接依据原始风险不等式确定决策区域，因为除法可能无定义或改变不等式方向。

当正确分类损失为零、两种误分类损失为正时，似然比阈值简化为

$$
\Lambda(\mathbf x)>\frac{\lambda_{12}\pi_2}{\lambda_{21}\pi_1}.
$$

利用 $P_1+P_2=1$，也可以将其写成后验概率阈值：

$$
P(\omega_1\mid\mathbf x)>
\frac{\lambda_{12}}{\lambda_{12}+\lambda_{21}}.
$$

增大将 $\omega_1$ 误判为 $\omega_2$ 的损失 $\lambda_{21}$，会降低选择 $\omega_1$ 所需的后验阈值，从而扩大其决策区域。因此，最小风险决策不必选择后验概率最大的类别，而是选择后验加权损失最小的行动。

### 3.3 最小错误率与最小风险的关系

令损失函数为 0–1 损失，即

$$
\lambda_{ij}=1-\delta_{ij},
$$

其中 $\delta_{ij}$ 为 Kronecker 符号。此时

$$
R(\omega_i\mid\mathbf x)
=\sum_{j\ne i}P(\omega_j\mid\mathbf x)
=1-P(\omega_i\mid\mathbf x).
$$

条件风险等于条件错误率，最小风险规则因此退化为最大后验分类规则。最小错误率决策是 Bayes 风险最小化框架在特定损失函数下的结果。

## 4. 高斯分布下的 Bayes 决策

### 4.1 高斯模型与判别函数

高斯模型具有较为简单的解析形式，可以通过均值与协方差描述特征的中心位置、尺度及相关性。在适当独立性和矩条件下，中心极限定理为部分观测量的近似正态性提供依据；在均值和正定协方差给定的连续分布中，高斯分布具有最大微分熵。这些性质说明了其建模价值，但具体数据是否适合高斯假设仍取决于其分布结构。

设第 $i$ 类的条件分布为

$$
\mathbf X\mid\omega_i\sim\mathcal N(\boldsymbol\mu_i,\Sigma_i),
\qquad \Sigma_i\succ0.
$$

其概率密度为

$$
p(\mathbf x\mid\omega_i)
=\frac{1}{(2\pi)^{d/2}|\Sigma_i|^{1/2}}
\exp\left[-\frac12(\mathbf x-\boldsymbol\mu_i)^T
\Sigma_i^{-1}(\mathbf x-\boldsymbol\mu_i)\right].
$$

这里 $|\Sigma_i|$ 表示行列式，正定条件保证逆矩阵存在且行列式为正。奇异协方差所对应的退化高斯分布不能直接使用这一相对于 $d$ 维体积测度的密度表达式。

在最小错误率准则下，取对数并省略所有类别共有的项，得到

$$
g_i(\mathbf x)=
-\frac12(\mathbf x-\boldsymbol\mu_i)^T\Sigma_i^{-1}(\mathbf x-\boldsymbol\mu_i)
-\frac12\log|\Sigma_i|+\log\pi_i.
$$

二次型刻画观测相对于类中心的标准化偏离程度，行列式项反映密度的尺度归一化，先验项则体现类别的总体比例。

### 4.2 一般协方差与二次判别

展开高斯判别函数可得

$$
g_i(\mathbf x)=\mathbf x^TW_i\mathbf x+\mathbf w_i^T\mathbf x+w_{i0},
$$

其中

$$
W_i=-\frac12\Sigma_i^{-1},\qquad
\mathbf w_i=\Sigma_i^{-1}\boldsymbol\mu_i,
$$

$$
w_{i0}=-\frac12\boldsymbol\mu_i^T\Sigma_i^{-1}\boldsymbol\mu_i
-\frac12\log|\Sigma_i|+\log\pi_i.
$$

当不同类别的协方差不同时，$g_i-g_j$ 一般保留二次项，类别之间的等判别值集合由二次方程描述。这对应二次判别分析（Quadratic Discriminant Analysis，QDA）。二维中的边界可能为椭圆、抛物线、双曲线或相应退化形式，决策区域也可能不连通。

此时即使先验相等，仍通常需要保留行列式项。仅比较各类对应的马氏距离，会忽略不同协方差所导致的密度归一化差异。

### 4.3 共享协方差与线性判别

若各类别共享协方差 $\Sigma$，则二次项 $-\frac12\mathbf x^T\Sigma^{-1}\mathbf x$ 以及行列式项对所有类别相同。消去这些公共项后，得到关于 $\mathbf x$ 的仿射判别函数，对应线性判别分析（Linear Discriminant Analysis，LDA）。

对于二分类，令 $f=g_1-g_2$，有

$$
f(\mathbf x)=\mathbf w^T\mathbf x+b,
\qquad
\mathbf w=\Sigma^{-1}(\boldsymbol\mu_1-\boldsymbol\mu_2),
$$

$$
b=-\frac12\left(
\boldsymbol\mu_1^T\Sigma^{-1}\boldsymbol\mu_1-
\boldsymbol\mu_2^T\Sigma^{-1}\boldsymbol\mu_2\right)
+\log\frac{\pi_1}{\pi_2}.
$$

当两个均值不同时，$f=0$ 为超平面。多分类的各对等判别值集合也为超平面，但只有在相应判别值不低于其他类别时，该集合才构成实际决策边界的一部分。

设 $\Delta=\boldsymbol\mu_1-\boldsymbol\mu_2\ne\mathbf0$，定义

$$
\mathbf x_0=\frac{\boldsymbol\mu_1+\boldsymbol\mu_2}{2}
-\frac{\log(\pi_1/\pi_2)}{\Delta^T\Sigma^{-1}\Delta}\Delta.
$$

则边界可写为 $\mathbf w^T(\mathbf x-\mathbf x_0)=0$，其中 $\mathbf x_0$ 为边界与两均值连线的交点。等先验时，交点位于均值中点；增大 $\pi_1/\pi_2$，交点沿连线向 $\boldsymbol\mu_2$ 方向移动，$\omega_1$ 的决策区域扩大。

若均值和协方差均相同，则两个类条件分布完全一致，观测不再提供区分类别的信息，最小错误率规则仅由先验决定。

### 4.4 马氏距离及其几何意义

在共享协方差且先验相等时，分类等价于选择马氏距离最小的类中心：

$$
i^*(\mathbf x)\in\arg\min_i
(\mathbf x-\boldsymbol\mu_i)^T\Sigma^{-1}(\mathbf x-\boldsymbol\mu_i).
$$

马氏距离定义为

$$
d_M^2(\mathbf x,\mathbf y)
=(\mathbf x-\mathbf y)^T\Sigma^{-1}(\mathbf x-\mathbf y).
$$

设 $\Sigma=U\operatorname{diag}(s_1,\ldots,s_d)U^T$，其中 $s_k>0$，$\mathbf u_k$ 为 $U$ 的第 $k$ 个列向量，则

$$
d_M^2(\mathbf x,\mathbf y)
=\sum_{k=1}^{d}\frac{[\mathbf u_k^T(\mathbf x-\mathbf y)]^2}{s_k}.
$$

该表达式表明，马氏距离按各主方向的方差对位移进行标准化。方差较大的方向具有较小权重，方差较小的方向具有较大权重，特征相关性则通过主方向的旋转体现。

令 $\mathbf z=\Sigma^{-1/2}\mathbf x$，则原空间的马氏距离等于白化空间中的欧氏距离。因此，共享协方差、等先验时的判别可解释为白化后的最近均值分类。在原坐标中，边界经过两均值的中点，但其法向量 $\Sigma^{-1}\Delta$ 一般不与 $\Delta$ 平行。

### 4.5 各向同性协方差与欧氏距离

若共享协方差进一步满足 $\Sigma=\sigma^2I$，则

$$
d_M^2(\mathbf x,\boldsymbol\mu_i)
=\frac1{\sigma^2}\|\mathbf x-\boldsymbol\mu_i\|_2^2.
$$

在等先验条件下，决策因此等价于最近欧氏距离分类，二分类边界为两均值连线的垂直平分超平面。若先验不等，则仍需保留先验项，边界相对于垂直平分面发生平移。

一般对角协方差允许不同坐标方向具有不同方差，相应距离为按各维方差加权的欧氏距离。只有各维方差相同，即协方差为 $\sigma^2I$ 时，上式才能化为普通欧氏距离的统一倍数。

### 4.6 非对称损失对边界的影响

对于二分类，若正确分类损失为零且误分类损失为正，则最小风险规则选择 $\omega_1$ 的条件为

$$
g_1(\mathbf x)-g_2(\mathbf x)>
\log\frac{\lambda_{12}}{\lambda_{21}}.
$$

定义

$$
f_{\mathrm{risk}}(\mathbf x)
=g_1(\mathbf x)-g_2(\mathbf x)
+\log\frac{\lambda_{21}}{\lambda_{12}},
$$

即可依据其正负确定类别。共享协方差时，非对称损失仅改变截距，不改变超平面的法向量；协方差不同时，它改变二次判别式的常数项，可能进一步影响边界的形态与存在性。

对于任意多类损失矩阵，最小风险决策仍需比较 $\sum_j\lambda_{ij}P(\omega_j\mid\mathbf x)$，一般不能表示为对每个高斯判别函数添加一个类别常数。
