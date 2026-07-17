# Image Classification

希望模型输出的 y' 与 one-hot 编码的 y 的Cross Entropy Loss最小。

Tensor: 维度大于2的矩阵

如果参数越来越大，例如如果 R G B 都是100x100的大小，那么总的参数量就会变成

100x100x3 x 1000 = 3x10^7 导致参数量爆炸

## Observation:1

每个Neron只用看局部的pattern，组合起来就能判断图片了

## Simplification1

每个neron只用看Receptive Field(局部的pattern)，组合起来就能判断图片了,不用在意整个图片的pattern

把一个3x3x3的向量拉直，变成一个27维的向量，作为一个Neron的输入

Receptive field 彼此之间是有重叠的

**Typical Setting**: all channels, 3x3 kernel size , stride(移动的步长) 1 or 2 ，padding(补 0)

## Observation:2

- The same patterns appear in different regions

因为我们不可能在每个位置都放一个侦测某个pattern的Neron，所以我们需要共享权重

## Simplification2

Parameter sharing.

Neron 1  σ(w1x1 + w2x2 + w3x3 + ...) 侦测某个pattern

Neron 2  σ(w1x1' + w2x2' + w3x3'+...) 侦测同样的pattern

每个一Receptive的Field 只有一组参数。

# 讲解2

## Convolutional Layer

一个convolution layer 里面有很多Filter

现在假设channel 是 1(black and white)

假设Filter里面的参数已经算出来了

Filter如何侦测？  把filter放进去，每个值进去 inner product,然后移动，从左上角到右下角

每个Filter都重复做这件事，得到一群数字，叫做Feature Map，可以看做一个多个channel的图片

如果Network比较深的话，其实其还是可以看到比较大的pattern的

把Filter扫过一张图片这件事情就是 convolution operation

## Observation:3

- Subsampling the pixels will not change the picture.

pooling没有参数，不需要learn

# t-SNE

Neighborhood Embedding

Manifold Learning:是一种非线性降维方法，假设数据分布在一个低维流形上，通过学习流形的结构来实现降维。

把塞在高维空间的点，投影到低维空间上，尽量保持原本的距离关系。

## Locally Linear Embedding (LLE)

LLE 保持 wij不变，寻找 a set of Zi minimize ||zi - Σ wij Zi||^2

"think globally, fit locally"

## Laplacian Eigenmaps

- Graph-based method, 通过构建图来表示数据点之间的关系，利用图的拉普拉斯矩阵进行降维。

## t-SNE

前面的点只是假设接近的点在低维空间也接近，没有考虑到远的点在低维空间也要远

