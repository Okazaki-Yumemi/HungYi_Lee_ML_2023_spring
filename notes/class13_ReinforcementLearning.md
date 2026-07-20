# Introduction of Deep Reinforcement Learning

机器会在和环境互动之后得到Reward. 来知道自己做的到底好不好。

Machine learning ≈ Looking for a function

Actor-> score = f(observation)

Machine Learning->

Step1 : Function with Unknown
-> Actor in RL (Policy Network)
- Input: Observation of machine represented as a vector or a matrix
- Output: each action corresponds to a neuron in output layer

Step2 : define loss from training data

Action (x?) -> reward -> action -> no reward? -> action punishment-> ... 

This set of actions is called episode.

Total reward 是我们要最大化的东西

负total reward 就可以算是 loss函数


Step3 : optimization

Env-> observation s1 -> actor -> a1 -> env -> s2 -> actor .... 

Trajectory 就是 {s1,a1,s2,a2,...}

s1      a1
  \    /
   \  /
    vv
    reward r1  就是最大化的目标! Oh yeah!


# How to control your actor

- Make it take a specific action ahat give specific observation s:

给适当的 label 和 适当的 s 

- Take action a given s
- Dont take action a' ahat given s'

例如训练资料->

{s1 , a1} +1  Yes
{s2 , a2} -1  No
{s3 , a3} +1  Yes
   ...
{sN , aN} +1  Yes    -> 定义一个 Loss function 之类的 咯 
~~我是傻逼~~

上面的这个actor 是 **short sighted 的 vector**

- An action affects the subsequent observations and thus subsequent rewards.
- Reward delay: Actor has to sacrifice immediate reward to gain more long-term reward
- In space invader , only fire yields positive reward ,so vision 0 will learn an actor that always fire.


# Version 1

s1 s2  s3   ///    sn
a1 a2  a3   ///    an
r1 r2  r3   ///    rn

G1 = r1 + r2 + r3 + ... + rn
G2 = r2 + r3 + ... + rn
G3 = r3 + ... + rn

cumulated reward  一个动作的价值应该是其后所有操作的reward

# Version 2

G1' = r1 + γr2 + γ^2 r3 + .... 

加一个 Discount factor γ <  1

# version3

给所有的 g 减去一个baseline，让其有正有负

# Policy Gradient

- Initialize actor network parameters 
- For training iteration i = 1 to T
- - Using actor theta to interact
- - Obtain data {} {} {}
- - Compute A1 A2 ...
- - Compute Loss L
- - θ <- θi-1 - ηgradient L

要让收集资料的actor和训练的actor是同一个
-> On policy learning

(off policy learning 是分开的，就是快一些 但是肯定效果没有那么好咯~~~~~)
# Exploration
The actor needs to have randomness during data collection.

A major reason why we sample actions! 
(for example: 就是有些地方你得先开火才知道开火有用)

# Critic

Critic
- Given actor θ, how good it is when observing s (and take action α)

- Value function : When using actor θ, the discounted cumulated reward expects to be obtained after seeing s

# How to estimate V??

- **Temporal-difference (TD) approach**
... st,at,rt,st+1 ...

# Version 3.5
# Version 4
执行完at之后的得到 st+1 ， 然后把很多平均值平均化，然后加上rt

$$ A_t = r_t + V^θ(s_{t+1}) - V^θ(s_t) $$

# Sparse Reward

If rt = 0 in most cases -> We dont know actions are good or bad

