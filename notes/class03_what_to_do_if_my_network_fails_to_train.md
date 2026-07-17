# Part1

## why optimization fails

local minima: The optimization algorithm may converge to a local minimum instead of the global minimum, leading to suboptimal performance. (gradient = 0)

saddle points: The optimization algorithm may get stuck at a saddle point, where the gradient is zero but the point is not a minimum, leading to slow convergence or divergence. (gradient = 0)

总称为 critical point

## Tayler Series Approximation

L(θ) around θ0 can be approximated using a Taylor series expansion:

L(θ) = L(θ0) + (θ - θ0)^T * ∇L(θ0) + 1/2 * (θ - θ0)^T * H(θ0) * (θ - θ0) + O(||θ - θ0||^3)

Hessian H is a matrix of second-order partial derivatives of the loss function with respect to the model parameters. It provides information about the curvature of the loss landscape.

拿出来 θ-θ0 , 令其为 v

所以 q(v) = vT * H(θ0) * v

if

For all v, vT * H(θ0) * v > 0, then θ0 is a local minimum.
(H is positive definite (中文: 正定矩阵) = 所有特征值都大于0)
else if 

For all v, vT * H(θ0) * v < 0, then θ0 is a local maximum.
(H is negative definite (中文: 负定矩阵) = 所有特征值都小于0)
else if

Sometimes vT * H(θ0) * v > 0, sometimes vT * H(θ0) * v < 0, then θ0 is a saddle point.
(H is indefinite (中文: 不定矩阵) = 既有特征值大于0，也有特征值小于0)

### Dont afraid of saddle points

H 告诉了我们更新的方向

u is an eigenvector of H
λ is the eigen value of u

-> uTHu = λuTu = λ||u||^2

因为 θ-θ0 = v = ||v|| * u  所以可以根据这几个大小去更新

L(θ) = L(θ0) + (θ - θ0)^T * ∇L(θ0) + 1/2 * (θ - θ0)^T * H(θ0) * (θ - θ0) + O(||θ - θ0||^3)

例如 λ = -2 ， u = [1,1]T , 直接沿着 u 的方向更新 θ0 ，就会下降 loss

主要看第二项

# Part2

Review: Optimization with Batch

Large batch: Long time for cooldown,but powerful (dont consider parallelization)

Small batch: Short time for cooldown, but noisy

## Small batch v.s. Large batch

Flat minima is better than sharp minima (cause sometimes the shape of batch will be different from the shape of the whole dataset)

batch size is a hyperparameter we have to decide.

## momentum

Movement: movement of last step minus gradient at present

# Part3 自动调节learning rate

tarining stuck != small gradient

在两边震荡

learning rate 最好要对每一个方向客制化

learning rate: η -> η/σ^t_i

σ = Root Mean Square of gradient
(根号下平方和)

**RMSProp(没有论文)**

σ1 = sqrt(α * σ0^2 + (1-α) * g^2)  

可以自己根据觉得哪个gradient比较重要，给它一个更大的α

σ2 = sqrt(α * σ1^2 + (1-α) * g^2)

**Adam:RMSProp + Momentum**


**learning rate scheduling**:

1. Learning rate decay: As the training gose , we are closer to destination,so we reduce the learning rate.

2. Warm up: learning rate increase first, then decay.

# Part4 Classification

classification(one hot?)

y = b + W' σ(b+Wx)
y` = softmax(y)

softmax  yi = exp(yi) / sum(exp(yj))  j=1,2,...,k

Cross Entropy(交叉熵): 交叉熵是衡量预测概率分布与真实概率分布之间差异的指标。

e = - sum(p(x) * log(q(x)))  x∈X

MSE 均方误差

e = sum((y - y`)^2)  i=1,2,...,n

pytorch会自动加一层 softmax,所以如果你自己加了 softmax,就会 double softmax,导致 loss 很大

对于
```py
criterion = nn.CrossEntropyLoss()
```
模型应该直接输出logits
```py
logits = model(x)
loss = criterion(logits, labels)
```
不需要在模型最后手动加
```py
nn.Softmax(dim=1)
```

推理的时候需要概率才写
```py
probabilities = torch.softmax(logits, dim=1)
```
鉴别类别只需要
```py
predictions = logits.argmax(dim=1)
```

MSE在loss很大的时候常常梯度很小，没有办法更新参数，导致训练失败。所以一般用 Cross Entropy Loss 作为分类任务的 loss function。

# Part5 Batch Normalization

Feature normalization: normalization是一种数据预处理技术，用于将数据的特征值缩放到一个标准范围内，以便更好地进行模型训练。常见的归一化方法包括最小-最大归一化、Z-score标准化等.

Testing 一般又叫 Inference

tilda(z) = (z - μ) /σ

μ 和 σ 是来自batch，但是testing阶段不一定能凑到一个完整的batch，所以 μ 和 σ 是来自 training阶段的 moving average

moving average: moving average 是一种统计方法，用于平滑时间序列数据。它通过计算一段时间内数据的平均值来减少噪声和波动，从而更好地捕捉数据的趋势。

average μ = p(average μ) + (1-p)(μ)^t 