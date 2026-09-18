---
title: '模式识别笔记（二）：参数估计——最大似然与最大后验'
date: 2026-09-18
summary: '推导一元与多元高斯模型的最大似然和最大后验估计，讨论无偏性、相合性、先验约束及模型设定的局限。'
series: 'pattern-recognition'
tags: ['Pattern Recognition', 'Parameter Estimation', 'MLE', 'MAP']
cover: ../../assets/blogs/pattern-recognition-parameter-estimation-cover.png
coverAlt: '散布的样本点经过多条候选钟形曲线，逐渐形成清晰的拟合分布与椭圆不确定性轮廓'
draft: false
---

[Bayes 决策理论](/blog/pattern-recognition-bayes-decision/)以类别先验和类条件概率分布为基础。在实际模式识别任务中，这些分布通常未知，需要根据训练样本进行估计。参数估计预先指定概率分布族，再利用观测数据确定其中的有限维参数，从而将概率密度估计转化为参数推断问题。

最大似然估计与最大后验估计是两种基本方法。前者依据数据的似然函数确定参数，后者在似然之外引入参数先验。二者的差异体现在有限样本下先验信息的作用，以及由此产生的偏差与方差变化。

## 1. 概率模型与估计对象

### 1.1 类别先验的估计

设训练集包含 $N$ 个样本，其中第 $k$ 类有 $N_k$ 个。若样本独立同分布地来自目标总体，可以用类别频率估计先验概率：

$$
\widehat\pi_k=\frac{N_k}{N}.
$$

由二项分布的计数性质，

$$
\mathbb E[\widehat\pi_k]=\pi_k,\qquad
\operatorname{Var}(\widehat\pi_k)=\frac{\pi_k(1-\pi_k)}{N}.
$$

该估计无偏，且随样本数增加依概率收敛到真实先验。其有效性依赖训练样本的采样分布与目标总体一致。若训练集通过分层抽样或类别重采样构造，经验类别频率一般不能直接作为目标总体的先验概率。

### 1.2 类条件密度的参数化

对于第 $k$ 类，设类条件密度属于参数族 $p(\mathbf x\mid\omega_k,\boldsymbol\theta_k)$。高斯模型中的参数为均值向量和协方差矩阵，即 $\boldsymbol\theta_k=(\boldsymbol\mu_k,\Sigma_k)$。参数估计通过训练样本确定这些量，而非直接估计任意形式的密度函数。

非参数估计则不将密度限制在某个固定有限维参数族中，但仍需引入平滑性等结构假设。参数方法的性质既取决于估计准则，也取决于所选分布族能否合理描述数据。

若各类别的参数互不共享，可以分别进行估计。为简化记号，以下先考虑单个类别，记训练数据为

$$
\mathcal D=(\mathbf x_1,\ldots,\mathbf x_n),
\qquad \mathbf x_r\in\mathbb R^d,
$$

并假设给定参数 $\boldsymbol\theta$ 后，各样本独立同分布于 $p(\mathbf x\mid\boldsymbol\theta)$。样本之间的独立性不要求同一观测向量的各个分量相互独立；多元分布仍可包含特征间的相关性。

## 2. 最大似然估计

### 2.1 似然函数与优化目标

给定参数时，$p(\mathcal D\mid\boldsymbol\theta)$ 表示数据的联合概率质量或密度。将观测数据固定，并将其视为参数的函数，得到似然函数

$$
L(\boldsymbol\theta;\mathcal D)
=p(\mathcal D\mid\boldsymbol\theta)
=\prod_{r=1}^{n}p(\mathbf x_r\mid\boldsymbol\theta).
$$

最大似然估计（Maximum Likelihood Estimation，MLE）定义为

$$
\widehat{\boldsymbol\theta}_{\mathrm{ML}}
\in\arg\max_{\boldsymbol\theta\in\Theta}
L(\boldsymbol\theta;\mathcal D),
$$

其中 $\Theta$ 为参数空间。对于连续观测，该方法最大化的是数据的联合密度。似然函数并非参数的概率分布，因此不要求其对参数积分为 1。

在似然为正的区域内，对数函数的单调性给出等价目标：

$$
\ell(\boldsymbol\theta)
=\log L(\boldsymbol\theta;\mathcal D)
=\sum_{r=1}^{n}\log p(\mathbf x_r\mid\boldsymbol\theta).
$$

对数变换将样本密度的乘积转化为求和，便于解析推导，也能够缓解数值计算中的下溢问题。仅与观测有关、而与待估参数无关的项不影响最优解。

### 2.2 解的存在性与极值条件

若对数似然可微，且最优解位于参数空间内部，则满足必要条件

$$
\nabla_{\boldsymbol\theta}\ell(\boldsymbol\theta)=\mathbf0.
$$

这一方程仅刻画内部驻点。确定最大似然解还需考虑参数约束、边界行为以及极值的性质。严格凹目标在存在内部驻点时具有唯一全局最大值；非凹目标则可能存在多个局部极值。若似然无界，或上确界只能在不可取的边界上逼近，则最大似然估计可能不存在。

## 3. 一元高斯分布的最大似然估计

### 3.1 均值与方差的估计

设 $X_1,\ldots,X_n$ 独立同分布于 $\mathcal N(\mu,\sigma^2)$，其中 $\mu\in\mathbb R$、$\sigma^2>0$。给定观测后，对数似然为

$$
\ell(\mu,\sigma^2)
=-\frac n2\log(2\pi)-\frac n2\log\sigma^2
-\frac{1}{2\sigma^2}\sum_{r=1}^{n}(x_r-\mu)^2.
$$

对均值求偏导可得

$$
\frac{\partial\ell}{\partial\mu}
=\frac1{\sigma^2}\sum_{r=1}^{n}(x_r-\mu).
$$

令其为零，得到

$$
\widehat\mu_{\mathrm{ML}}=\bar x
=\frac1n\sum_{r=1}^{n}x_r.
$$

对于任意固定的正方差，二阶导数为 $-n/\sigma^2<0$，因此样本均值是唯一的条件最大点，且不依赖方差取值。

令 $v=\sigma^2$，将 $\widehat\mu=\bar x$ 代入对数似然后，对 $v$ 求导：

$$
\frac{\partial\ell(\bar x,v)}{\partial v}
=-\frac{n}{2v}+\frac{1}{2v^2}
\sum_{r=1}^{n}(x_r-\bar x)^2.
$$

若离差平方和为正，最大点为

$$
\widehat\sigma^2_{\mathrm{ML}}
=\frac1n\sum_{r=1}^{n}(x_r-\bar x)^2.
$$

若所有观测完全相同，则在 $\mu=\bar x$、$\sigma^2\to0^+$ 时似然无界，正方差参数空间内不存在有限最大值。因而，上式作为正方差高斯模型的最大似然解，需要样本具有非零离差。

### 3.2 无偏性与自由度修正

估计量是样本的函数，具有由抽样分布诱导的随机性。对标量参数 $\theta$，若

$$
\mathbb E_\theta[\widehat\theta]=\theta,
$$

则称 $\widehat\theta$ 为无偏估计量。无偏性描述重复抽样意义下的期望性质，不意味着每次估计均等于参数真值。

样本均值满足

$$
\mathbb E[\bar X]=\mu,\qquad
\operatorname{Var}(\bar X)=\frac{\sigma^2}{n},
$$

因此均值的最大似然估计无偏。对于方差，利用离差分解

$$
\sum_{r=1}^{n}(X_r-\bar X)^2
=\sum_{r=1}^{n}(X_r-\mu)^2-n(\bar X-\mu)^2,
$$

并对两边取期望，得到

$$
\mathbb E\left[\sum_{r=1}^{n}(X_r-\bar X)^2\right]
=n\sigma^2-n\operatorname{Var}(\bar X)
=(n-1)\sigma^2.
$$

因此

$$
\mathbb E[\widehat\sigma^2_{\mathrm{ML}}]
=\frac{n-1}{n}\sigma^2.
$$

方差的最大似然估计具有负偏差。对于 $n>1$，无偏估计为

$$
s^2=\frac1{n-1}\sum_{r=1}^{n}(X_r-\bar X)^2.
$$

分母的差异来自估计目标的差异：$n$ 由似然最大化导出，$n-1$ 则用于修正有限样本偏差。均值由同一组数据估计时，中心化残差满足 $\sum_r(X_r-\bar X)=0$，对应一个线性约束。若真实均值已知，则围绕真实均值的离差平方和除以 $n$ 同时具有最大似然与无偏性质。

### 3.3 相合性与均方误差

相合性描述估计量随样本量增加趋近参数真值的性质。弱相合性定义为

$$
\widehat\theta_n\xrightarrow{P}\theta.
$$

在独立同分布且二阶矩有限时，由大数定律，

$$
\widehat\sigma^2_{\mathrm{ML}}
=\frac1n\sum_{r=1}^{n}X_r^2-\bar X^2
\xrightarrow{P}\mathbb E[X^2]-\mu^2
=\sigma^2.
$$

因此，方差的最大似然估计虽然在有限样本下有偏，仍具有相合性。无偏性与相合性分别涉及固定样本量下的期望和样本量增长时的收敛行为，二者不能相互替代。

标量估计量的均方误差满足

$$
\operatorname{MSE}(\widehat\theta)
=\mathbb E[(\widehat\theta-\theta)^2]
=\operatorname{Var}(\widehat\theta)
+\operatorname{Bias}(\widehat\theta)^2.
$$

因而，评价估计质量需要同时考虑偏差与方差。有偏估计可能通过降低方差获得较小的均方误差，先验约束所产生的收缩估计即具有这一特征。

## 4. 多元高斯分布的最大似然估计

### 4.1 均值向量

设 $\mathbf X_r\sim\mathcal N(\boldsymbol\mu,\Sigma)$，各样本独立同分布，且 $\Sigma\succ0$。对数似然为

$$
\begin{aligned}
\ell(\boldsymbol\mu,\Sigma)
={}&-\frac{nd}{2}\log(2\pi)-\frac n2\log|\Sigma|\\
&-\frac12\sum_{r=1}^{n}(\mathbf x_r-\boldsymbol\mu)^T
\Sigma^{-1}(\mathbf x_r-\boldsymbol\mu).
\end{aligned}
$$

关于均值向量的梯度为

$$
\nabla_{\boldsymbol\mu}\ell
=\Sigma^{-1}\sum_{r=1}^{n}(\mathbf x_r-\boldsymbol\mu).
$$

由 $\Sigma$ 可逆，零梯度条件给出

$$
\widehat{\boldsymbol\mu}_{\mathrm{ML}}
=\bar{\mathbf x}=\frac1n\sum_{r=1}^{n}\mathbf x_r.
$$

其 Hessian 为 $-n\Sigma^{-1}\prec0$，因此对任意固定正定协方差，样本均值均为唯一最大点。

### 4.2 协方差矩阵

定义离差矩阵

$$
C=\sum_{r=1}^{n}
(\mathbf x_r-\bar{\mathbf x})(\mathbf x_r-\bar{\mathbf x})^T,
$$

并令精度矩阵 $A=\Sigma^{-1}$。由 $\mathbf v^TA\mathbf v=\operatorname{tr}(A\mathbf v\mathbf v^T)$，代入均值估计后，对数似然中与 $A$ 有关的部分为

$$
\ell(A)=\frac n2\log|A|-\frac12\operatorname{tr}(AC)+c,
$$

其中 $c$ 与 $A$ 无关。利用

$$
\nabla_A\log|A|=A^{-T},\qquad
\nabla_A\operatorname{tr}(AC)=C^T,
$$

以及 $A$、$C$ 的对称性，零梯度条件为

$$
\frac n2A^{-1}-\frac12C=0.
$$

若 $C$ 正定，则

$$
\widehat\Sigma_{\mathrm{ML}}
=\frac Cn
=\frac1n\sum_{r=1}^{n}
(\mathbf x_r-\bar{\mathbf x})(\mathbf x_r-\bar{\mathbf x})^T.
$$

对数行列式在正定矩阵集合上严格凹，迹项为线性项，因此该精度矩阵解为唯一最大点。每个离差项均为列向量与其转置的外积，形成 $d\times d$ 矩阵，从而同时刻画各维方差和维间协方差。

与一元情形类似，

$$
\mathbb E[\widehat{\boldsymbol\mu}_{\mathrm{ML}}]=\boldsymbol\mu,
\qquad
\mathbb E[\widehat\Sigma_{\mathrm{ML}}]=\frac{n-1}{n}\Sigma.
$$

因此，$n>1$ 时的无偏协方差估计为 $C/(n-1)$。

### 4.3 样本维数与协方差退化

中心化后的 $n$ 个样本向量之和为零，因此

$$
\operatorname{rank}(\widehat\Sigma_{\mathrm{ML}})
\leq\min(d,n-1).
$$

当 $n\leq d$ 时，经验协方差必然奇异；即使 $n>d$，仍需中心化样本张成整个特征空间，才能保证其正定。对于奇异离差矩阵，无约束正定高斯模型的似然可以通过令样本无变化方向上的方差趋于零而不断增大，此时不存在上述正定内部解。

这一现象表明，参数数量与样本数量之间的关系直接影响估计的可行性。限制协方差为对角形式、采用共享协方差或引入正则化，均可减少估计的不稳定性。常见的正则化形式为

$$
\widehat\Sigma_{\mathrm{reg}}
=\widehat\Sigma_{\mathrm{ML}}+\varepsilon I,
\qquad \varepsilon>0.
$$

它保证协方差正定，但同时改变了原始无约束最大似然估计。

## 5. 最大后验估计

### 5.1 参数先验与后验密度

最大后验估计（Maximum A Posteriori，MAP）在参数空间上指定先验分布 $p(\boldsymbol\theta)$，并根据观测更新为后验分布：

$$
p(\boldsymbol\theta\mid\mathcal D)
=\frac{p(\mathcal D\mid\boldsymbol\theta)p(\boldsymbol\theta)}
{p(\mathcal D)}.
$$

由于边缘概率或密度 $p(\mathcal D)$ 与待优化参数无关，最大后验估计可写为

$$
\widehat{\boldsymbol\theta}_{\mathrm{MAP}}
\in\arg\max_{\boldsymbol\theta}
\left[\sum_{r=1}^{n}\log p(\mathbf x_r\mid\boldsymbol\theta)
+\log p(\boldsymbol\theta)\right].
$$

对于连续参数，MAP 选择后验密度的众数。参数先验描述对分布参数的事前不确定性，与分类中的类别先验 $P(\omega_k)$ 具有不同的对象和作用。最大后验分类推断类别，最大后验参数估计推断模型参数，二者共享 Bayes 更新形式。

### 5.2 与最大似然及正则化的关系

若先验密度在相同参数域内为正常数，则 MAP 与 ML 具有相同最优解。对于无界参数空间，常数密度不能归一化为均匀概率分布，因此这一关系可能涉及非正规先验或适当先验的极限。

将 MAP 改写为最小化问题，可得

$$
\widehat{\boldsymbol\theta}_{\mathrm{MAP}}
\in\arg\min_{\boldsymbol\theta}
\left[-\ell(\boldsymbol\theta)-\log p(\boldsymbol\theta)\right].
$$

负对数先验在此具有正则项的形式。若参数服从零均值、各向同性高斯先验，满足

$$
p(\boldsymbol\theta)\propto
\exp\left(-\frac{\|\boldsymbol\theta\|_2^2}{2\tau^2}\right),
$$

则 MAP 等价于在负对数似然上增加 $\|\boldsymbol\theta\|_2^2/(2\tau^2)$ 的二次惩罚。先验方差越小，约束强度越大。若将数据项由总和改写为样本平均，需要对整个目标同时除以 $n$，才能保持同一估计问题。

在固定先验、模型可识别且满足适当正则条件时，数据量增加通常使似然项逐渐主导估计，MAP 与 ML 的差异相应减小。这一结论还要求先验在真实参数附近具有支持；排除真值的先验或不正确的模型假设不能由增加样本量自动消除。

## 6. 高斯均值的最大后验估计

### 6.1 一元高斯模型

设给定均值后，观测独立同分布于

$$
X_r\mid\mu\sim\mathcal N(\mu,\sigma^2),
\qquad
\mu\sim\mathcal N(\mu_0,\sigma_0^2),
$$

其中观测方差 $\sigma^2$ 已知，且 $\sigma_0^2>0$。先验均值 $\mu_0$ 描述参数的先验中心，先验方差 $\sigma_0^2$ 描述该参数的不确定性；它与观测本身的方差 $\sigma^2$ 不同。

省略与 $\mu$ 无关的项，后验对数密度为

$$
\log p(\mu\mid\mathcal D)
=-\frac1{2\sigma^2}\sum_{r=1}^{n}(x_r-\mu)^2
-\frac1{2\sigma_0^2}(\mu-\mu_0)^2+c.
$$

零导数条件给出

$$
\frac n{\sigma^2}(\bar x-\mu)
-\frac1{\sigma_0^2}(\mu-\mu_0)=0,
$$

因此

$$
\widehat\mu_{\mathrm{MAP}}
=\frac{n\bar x/\sigma^2+\mu_0/\sigma_0^2}
{n/\sigma^2+1/\sigma_0^2}.
$$

方差的倒数称为精度。样本均值的精度为 $n/\sigma^2$，参数先验的精度为 $1/\sigma_0^2$，故 MAP 估计是样本均值与先验均值的精度加权平均。令

$$
\alpha=\frac{n\sigma_0^2}{\sigma^2+n\sigma_0^2},
$$

则

$$
\widehat\mu_{\mathrm{MAP}}
=\alpha\bar x+(1-\alpha)\mu_0.
$$

在其他参数固定时，样本量增大使 $\alpha$ 趋近于 1，估计趋近样本均值。观测方差增大则降低样本均值的精度，使先验在估计中占据更大权重。当 $\sigma_0^2\to0$ 时，估计趋近 $\mu_0$；当 $\sigma_0^2\to\infty$ 时，估计趋近 $\bar x$。

也可以令 $\kappa_0=\sigma^2/\sigma_0^2$，得到

$$
\widehat\mu_{\mathrm{MAP}}
=\frac{n\bar x+\kappa_0\mu_0}{n+\kappa_0}.
$$

在该模型下，$\kappa_0$ 可以解释为先验的等效样本量，它由先验精度与单个观测的精度之比确定，不要求取整数。

### 6.2 收缩估计的偏差与方差

将真实均值固定为 $\mu_*$，并对样本的重复抽样分布求期望，可以得到

$$
\operatorname{Bias}(\widehat\mu_{\mathrm{MAP}})
=(1-\alpha)(\mu_0-\mu_*),
$$

$$
\operatorname{Var}(\widehat\mu_{\mathrm{MAP}})
=\alpha^2\frac{\sigma^2}{n}.
$$

先验约束使估计向 $\mu_0$ 收缩，并降低抽样方差。若先验中心偏离真实均值，收缩也会引入偏差，其均方误差为

$$
\operatorname{MSE}(\widehat\mu_{\mathrm{MAP}})
=\alpha^2\frac{\sigma^2}{n}
+(1-\alpha)^2(\mu_0-\mu_*)^2.
$$

因而，MAP 是否优于 ML 取决于样本量、观测方差、先验精度及先验中心的准确性。先验信息充分且合理时，收缩可能改善有限样本估计；过强且偏离真值的先验则可能增加误差。

### 6.3 后验分布与参数不确定性

对后验对数密度配方可得

$$
\mu\mid\mathcal D\sim\mathcal N(m_n,v_n),
$$

其中

$$
v_n=\left(\frac n{\sigma^2}+\frac1{\sigma_0^2}\right)^{-1},
\qquad m_n=\widehat\mu_{\mathrm{MAP}}.
$$

高斯后验的众数与均值相同，因此该模型的 MAP 估计也等于后验均值。但一般后验分布不具有这一性质。在平方误差损失下，Bayes 最优点估计为后验均值，未必为后验众数。

对参数不确定性积分可得到新观测的后验预测密度：

$$
\begin{aligned}
p(x_{\mathrm{new}}\mid\mathcal D)
&=\int p(x_{\mathrm{new}}\mid\mu)
 p(\mu\mid\mathcal D)\,d\mu\\
&=\mathcal N(x_{\mathrm{new}};m_n,\sigma^2+v_n).
\end{aligned}
$$

预测方差由观测方差与均值的后验方差组成。将 MAP 点估计直接代入观测模型时，所得方差仅为 $\sigma^2$，因此未包含参数不确定性。

### 6.4 多元高斯模型

设观测协方差已知，均值具有高斯先验：

$$
\mathbf X_r\mid\boldsymbol\mu\sim\mathcal N(\boldsymbol\mu,\Sigma),
\qquad
\boldsymbol\mu\sim\mathcal N(\boldsymbol\mu_0,\Sigma_0),
$$

其中 $\Sigma\succ0$、$\Sigma_0\succ0$。对后验对数密度求梯度，得到

$$
\Sigma^{-1}\sum_{r=1}^{n}(\mathbf x_r-\boldsymbol\mu)
-\Sigma_0^{-1}(\boldsymbol\mu-\boldsymbol\mu_0)=\mathbf0.
$$

于是

$$
(n\Sigma^{-1}+\Sigma_0^{-1})
\widehat{\boldsymbol\mu}_{\mathrm{MAP}}
=n\Sigma^{-1}\bar{\mathbf x}+\Sigma_0^{-1}\boldsymbol\mu_0,
$$

即

$$
\widehat{\boldsymbol\mu}_{\mathrm{MAP}}
=(n\Sigma^{-1}+\Sigma_0^{-1})^{-1}
(n\Sigma^{-1}\bar{\mathbf x}+\Sigma_0^{-1}\boldsymbol\mu_0).
$$

后验协方差为

$$
V_n=(n\Sigma^{-1}+\Sigma_0^{-1})^{-1}.
$$

该表达式是标量精度加权平均的矩阵推广。矩阵权重允许不同方向具有不同收缩强度，并通过非对角项反映方向间的相关结构。由于矩阵乘法一般不可交换，标量加权公式的代数变形不能直接用于任意矩阵。

对于正定矩阵 $A$、$B$，恒等式

$$
(A^{-1}+B^{-1})^{-1}
=A(A+B)^{-1}B
=B(A+B)^{-1}A
$$

成立。令 $M=(\Sigma/n+\Sigma_0)^{-1}$，可将均值估计等价地写成

$$
\widehat{\boldsymbol\mu}_{\mathrm{MAP}}
=\Sigma_0M\bar{\mathbf x}
+\frac\Sigma nM\boldsymbol\mu_0.
$$

两个矩阵权重之和为 $I$，但不必为标量权重。固定正定协方差时，$n$ 增大使数据精度项主导估计。若以 $\Sigma_0=tC$ 表示先验协方差，其中 $C\succ0$ 固定，则 $t\to0$ 时估计趋近先验均值，$t\to\infty$ 时估计趋近样本均值。

## 7. 模型设定与估计的局限

### 7.1 模型失配

参数估计以选定的分布族为前提，似然最大化仅保证在这一分布族内达到相应目标。若真实分布不属于该分布族，增加样本量可以降低抽样不确定性，但不保证消除模型失配。

分布的支持集、对称性、尾部行为和多峰结构均属于模型设定的重要依据。高斯模型定义在整个实空间且具有对称结构，对明显偏斜或受到取值范围约束的数据，可能产生系统性的拟合偏差。先验能够约束参数，却不能自动修正错误的分布族。

### 7.2 混合高斯的似然无界性

混合分布说明，即使概率密度对每个合法参数均归一化，似然关于参数仍可能无界。考虑具有一个可变高斯分量和一个固定高斯分量的模型：

$$
p(x\mid\mu,\sigma^2)
=\frac12\mathcal N(x;\mu,\sigma^2)
+\frac12\mathcal N(x;0,1).
$$

固定 $\mu=x_1$ 并令 $\sigma\to0^+$，有

$$
p(x_1\mid\mu=x_1,\sigma^2)
\geq\frac1{2\sqrt{2\pi}\sigma}\to\infty.
$$

其他观测处的密度由固定分量保证正下界：

$$
p(x_r\mid\mu,\sigma^2)
\geq\frac12\mathcal N(x_r;0,1)>0.
$$

因此

$$
L(\mu=x_1,\sigma^2)
\geq\frac1{2\sqrt{2\pi}\sigma}
\prod_{r=2}^{n}\frac12\mathcal N(x_r;0,1)
\to\infty.
$$

可变分量在单个样本处的方差退化导致似然无界，该问题不存在有限的全局最大似然解。这一现象属于模型与目标函数的性质，而非局部优化算法本身的缺陷。

对协方差特征值施加正下界，或采用能够抑制退化的先验与惩罚，可以限制这种行为。约束是否有效取决于其在方差趋于零附近的性质，不能仅由是否引入先验来判断。

## 8. 参数估计与高斯分类器

对每一类别分别估计先验、均值与协方差后，可将结果代入高斯判别函数：

$$
\begin{aligned}
\widehat g_k(\mathbf x)
={}&-\frac12(\mathbf x-\widehat{\boldsymbol\mu}_k)^T
\widehat\Sigma_k^{-1}
(\mathbf x-\widehat{\boldsymbol\mu}_k)\\
&-\frac12\log|\widehat\Sigma_k|+\log\widehat\pi_k.
\end{aligned}
$$

在协方差正定的条件下，选择最大判别值即可得到基于估计分布的最小错误率规则。一般损失下，则由估计的类别后验计算各决策的条件风险。这类规则称为代入式分类器，其性质同时受到概率模型、参数估计误差和损失设定的影响。

若各类别共享协方差，而均值分别估计，则协方差的最大似然估计为

$$
\widehat\Sigma_{\mathrm{shared,ML}}
=\frac1N\sum_{k=1}^{K}\sum_{\mathbf x\in\mathcal D_k}
(\mathbf x-\widehat{\boldsymbol\mu}_k)
(\mathbf x-\widehat{\boldsymbol\mu}_k)^T.
$$

该式合并各类别相对于各自均值的类内离差，不包含类别均值差异产生的类间变动。在各类非空且共同协方差假设成立时，对应的无偏合并估计使用分母 $N-K$，其中还要求 $N>K$。

完整协方差具有 $d(d+1)/2$ 个自由参数，各类别分别估计时参数量随维数平方增长。共享协方差或对角协方差假设降低了模型灵活性，也减少了有限样本下的估计负担。共享协方差导出线性高斯判别，各类独立协方差则一般导出二次判别，因而决策边界的复杂度与参数估计的结构约束直接相关。
