# Network Compression

- Resource-constrained environments! 

# Network can be pruned

- Networks are typically over-parameterized (there is significant redundant weights or neurons!)
- Prune them!

# Network Pruning
1. Pretrained Network
2. 评估一个参数是否做事情
- 看绝对值 , 如果一个参数绝对值大那大概率有用
3. Remove -> smaller

- After pruning , the accuracy will drop
- Fine-tuning on training data for recover 
- Dont prune too much at once, or the network wont recover.

- Weight pruning
- Neuron pruning 

# Why Pruning?
- How about simply train a smaller network?
- It is widely known that smaller network is more difficult to learn successfully.
- - Larger network is easier to optimize?

- Lottery Ticket Hypothesis.
- - 可以抽奖留下来那个Train的动的subnetwork!

# Knowledge Distillation
蒸馏
Teacher Net <---> Student Net

让small net 模仿 Teacher Net 的 输出

- Temperature for softmax

在softmax 上面加一个temperature

普通的temperature

->  yi = e^y / sigma(e^yi)   ->   给y 除以一个t

# Parameter Quantization

1. Using less bits to represent a value
2. Weight clustering
3. Represent frequent clusters by less bits, represent rare clusters by more bits.

# Binary Weights

# Architecture Design
- Review: Standard CNN 


- DepthWise Separable Convolution 
- - Filter number = input channel number
- - Each filter only considers one channel (几个channel 几个 filter, 节约很多)
- - the filters are k x k matrices
- - There is no interactions between tokens.
- - -
- Pointwise convolution
- Filter 都是 1x1 , 可以去考虑不同channel 之间的关系

# Low Rank approximation
从

N -W-> M  到  N -V-> K -U-> M

两层的network的参数更小 (瘦高矩阵x矮胖矩阵-> 方阵)


# Dynamic Computation
- The network adjusts the computation it need


- Dynamic Depth
- - Extra layer (比如能量低的时候直接从前面的layer退出)

训练方法，从每一个layer出来，所有出来的结果和ground truth 做 cross entropy ，整体化最小化这个熵

- Dynamic Width
