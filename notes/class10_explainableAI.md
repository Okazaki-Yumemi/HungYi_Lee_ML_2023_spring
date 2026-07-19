# Explainable ML
- Correct answers != intelligent answers

# why we need explainable ML
- loan issuers are required by law to explain their models
- medical diagnosis model is responsible for human life.
- if a model is used at the court, we must make sure the model behaves in a nondiscriminatory way.
- if a self-driving car crashes, we need to know why it crashed.

**we can improve ML model based on explaination**

# Interpretable v.s. Powerful
- Some models are intrinsically interpretable (e.g., linear regression, decision trees)
- - for example , linear model

- Deep network is difficult to interpret. Deep network is a black box.

# GOAL OF EXPLAINABLE ML
- Completely know how an ML model works?
- - We do not completely know how brains work
- - But we trust the decision of humans!
- - - 
- 可以通过设置一个灰色方块在图片中，移动位置，每次遮盖一定的内容，画出一张热力图，来解释模型的决策依据。

- 方法2则是算梯度
{x1 ... xn ... xN} -> {x1 ... xn + dx ... xN} -> {y1 ... yn + dy ... yN}

得到的不同就可以画出不同像素的重要性了

# What does a digit look like for CNN?

- Find the image that maximizes class probability

$$ X^* = argmax y_i $$

-> 但是对人来说，可能是一个很奇怪的图像，甚至是噪声。

$$ X^* = argmax y_i + R(X) $$
$$ R(X) = -\sum_{i,j} (|X_{i,j}|)$$

# OUTLOOK

using an interpretable model to mimic the behavior of an uninterpretable model.

eg.

x1 x2 xn ->  [black box] ->          y
                                     |---> as close as possible
x1 x2 xn -> [interpretable model] -> y

Local interpretable model agnostic explanations (LIME)

# 5 CNN explain ways.

## 1. LIME  

```
把图片切成若干区域
→ 随机保留或遮挡区域
→ 观察分类结果变化
→ 用简单线性模型拟合当前图片附近的行为
```

## 2.Saliency map

$$ S_c(I) = \frac{\partial f_c(x)}{\partial I} $$

```py
image.requires_grad_(True)

logits = model(image)
score = logits[0, target_class]
score.backward()

saliency = image.grad.abs()
```

对该像素做微小改变，明显改变当前类别分数

## 3.SmoothGrad

$$ SmoothGrad(x) = \frac{1}{N} \sum_{i=1}^{N} f_c(x + \mathcal{N}(0, \sigma^2)) $$

- 稳定特征反复出现
- 随机噪声会消失

## 4. Filter Visualization

从随机噪声开始固定参数，用梯度上升法找到最大激活的输入图像

## 5. Integrated Gradients

从一个baseline图片累计贡献

| 方法                   | 做了什么               | 是否需要梯度 | 主要局限        |
| -------------------- | ------------------ | -----: | ----------- |
| LIME                 | 遮挡区域并拟合局部线性模型      |      否 | 随机且依赖分区     |
| Saliency             | 计算输出对像素的梯度         |      是 | 噪声、饱和       |
| SmoothGrad           | 多次加噪后平均梯度          |      是 | 只是降噪        |
| Filter Visualization | 优化输入以最大化 filter 激活 |      是 | 结果可能不自然     |
| Integrated Gradients | 从 baseline 到输入累计梯度 |      是 | 依赖 baseline |

# BERT

## 1. attention visualization

观察某层某个head的 attention matrix Aij 表示token i 对 token j 的注意力权重。

## 2. Embedding visualization

观察不同token不同类别或者不同层的表示是否聚类

## 3. Embedding Analysis

计算欧氏距离 or Cosine similarity