# Domain Adaptation

Domain shift: Training and testing data have different distributions.

在Source domain 上面训练好了之后去target model 上面跑一两个 epoch 就可以了


Feature Extractor(network) 无论来自 Source domain 还是 Target domain ,经过 feature extractor 之后都是相似的，直接训练一个 feature -> answer 的网络就可以了
```
输入 x
  ↓
Feature Extractor F
  ├── Label Predictor C：预测类别
  └── Domain Classifier D：预测来自 source 还是 target
```
公式是
$$ min_{F,C} max_{D} L_{class}(C(F(x_s)), y_s) - λ L_{domain}(D(F(x)), d) $$


而 Feature extractor是通过 Domain Adversarial Training 来实现的，使得Source domain 和 Target domain 的 feature extractor 提取出来的 feature 是相似的。

用GAN 来实现 ， 对 Feature extractor 类似训练一个 Domian Classifier ，去欺骗 Domain Classifier， 同时 也还得让 Label Predictor 能做出来分类区分。

# Limitation

Decision boundary should be far away from class clusters, otherwise the model will be sensitive to domain shift.

# Domain Generalization 

**情况1** 训练资料就有多个Domain了，测试资料多了一个domain，这样模型本就会对新domain有一定的适应性。

**情况2** 训练资料只有一个Domain，测试资料多了一个domain，这样模型本就不会对新domain有一定的适应性。

