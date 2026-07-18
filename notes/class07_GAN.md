# Network as Generator

输入会加入一个 simple distribution ，是不固定的 (但是这个distribution够简单，能够让我们去sample)

# Why distribution ?

- Especially for the tasks needs "creativity"
- - Drawing
- - Chatbot

# Generative Adversarial Networks (GANs)

- Unconditional generation

- Discriminator: 判别器，判别输入的样本是来自真实数据还是生成器生成的假数据

- Generator: 生成器，生成假数据，试图欺骗判别器

# Algorithm

- Step 1: Fix generator G , and update discriminator D
- Step 2: Fix discriminator D , and update generator G

# Theory Behind GANs

## Our Objective

Normal Distribution -> Generator -> PG  <- - -> Pdata (More similar. better)

G* = argminDiv(Pg,Pdata)

-> 如何计算Divergence

-> 
$$ D* = argmaxV(D,G) = Ex~pdata[logD(x)] + Ez~pz[log(1-D(G(z)))] $$

# Tips for GAN to train

- In most cases, Pg and Pdata are not overlapped.

- 1. The nature of data

- 2. Sampling

没有重叠的分布放到 JS divergence里面算出来的分布永远是 log2
(但是明明相近一些的，算出来也是log2，无法评判好坏)

## Wasserstein Distance

假设一个推土机把P推到Q上面，算出距离

WGAN如何计算:

$$ maxD E_{x~Pdata}[D(x)] - E_{z~Pz}[D(G(z))] $$

## GAN for sequence Generation

 GAN没啥意思，和LLM方向不一样，不管了。

 也没有代码

 