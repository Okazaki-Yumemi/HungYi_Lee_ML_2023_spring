# Outline

## Pytorch 是什么

Pytorch is an machine learning framework in Python

- N-dimensional Tensor computation
- Automatic differentiation

## Traning and Testing Neural Networks

Training validation 循环，然后test

## Dataset and DataLoader

Dataset Stores data samples and expected values

Dataloader groups data in batches , enables multiprocessing and shuffling

- example
```py
dataset = MyDataset(file)

dataloader = DataLoader(dataset,batch_size,shuffle = True) # Training -> Shuffle = True, Testing -> Shuffle = False
```

```py
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, file):
        # Load data from file
        self.data = load_data(file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # Return a single data sample and its label
        sample = self.data[idx]
        return sample['input'], sample['label']
```

##  Tensors

Tensors 是 High-demensional matrices (arrays)

1-D Tensor: audio
2-D Tensor: image (black and white)
3-D Tensor: RGB image

`.shape` returns the shape of the tensor



### Tensor - Device

CPU
```py
x = x.to('cpu')
```
GPU
```py
x = x.to('cuda')
```

- check if GPU is available
```py
import torch
if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
```

- multiple GPUs
```py
if torch.cuda.device_count() > 1:
    print("Let's use", torch.cuda.device_count(), "GPUs!")
    model = nn.DataParallel(model)
```

- why GPU
- - parallel computing with more cores for arithmetic operations


### Tensor - Gradient Calculation
```py
import torch

x = torch.tensor([1.,0.],[-1.,1.], requires_grad=True)

z = x.pow(2).sum()

z.backward() # compute gradients

x.grad # get gradients
```

## torch.nn

### torch.nn - Build your own neural network

```py

import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        x = self.net(x)
        return x
```

or
```py

import torch.nn as nn
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(10, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
```

### torch.nn - Loss Function

- Mean Squared Error Loss (for regression tasks)

```py
criterion = nn.MSELoss()
```
- Cross Entropy Loss (for classification tasks)

```py
criterion = nn.CrossEntropyLoss()
```

- loss = criterion(model_output, target)

### torch.optim

optim 是优化器，用于更新模型参数

- Gradient-based optimization algorithms that adjust network parameters to reduce error

- eg. Stochastic Gradent Descent(SGD)

```py

torch.optim.SGD(model.parameters(),lr,momentum) # lr = learning rate, momentum = momentum factor
```

- For every batch of data

1. Call optimizer.zero_grad() to reset gradients
2. Call loss.backward() to compute gradients
3. Call optimizer.step() to update model parameters

## Steps of Traning a Neural Network

```py

dataset = MyDataset(file)

tr_set = DataLoader(dataset,batch_size,shuffle = True) # Training -> Shuffle = True, Testing -> Shuffle = False

model = MyModel().to(device)

criterion = nn.MSELoss() # or nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr, momentum)

for epoch in range(n_epochs):
    model.train() # set model to training mode
    for x , y in tr_set:
        optimizer.zero_grad() # reset gradients  ## 这个地方是因为pytorch是累积梯度的，所以每次训练前都要清零梯度，不是覆盖
        x, y = x.to(device), y.to(device) # move data to device
        pred = model(x) # forward pass
        loss = criterion(pred, y) # compute loss
        loss.backward() # compute gradients
        optimizer.step() # update model parameters
```

## Neural Network Validation LOOP
```py
model.eval() # set model to evaluation mode
total_loss = 0
for x , y in dv_set:
    x, y = x.to(device), y.to(device)
    with torch.no_grad(): # disable gradient calculation
        pred = model(x)
        loss = criterion(pred, y)
    total_loss += loss.cpu().item()*len(x) # accumulate loss
avg_loss = total_loss / len(dv_set.dataset) # average loss
```

## Neural Network Testing LOOP
```py
model.eval() # set model to evaluation mode
preds = []

for x in tt_set:
    x = x.to(device)
    with torch.no_grad(): # disable gradient calculation
        pred = model(x)
    preds.append(pred.cpu()) # move predictions to CPU and store them
```

## Notice - model.eval() and torch.no_grad()

- model.eval()
- - changes behavior of some model layers , such as dropout and batch normalization
不希望在测试阶段使用dropout和batch normalization的随机性，所以需要调用model.eval()来设置模型为评估模式。

- with torch.no_grad()
- - disables gradient calculation, which reduces memory consumption and speeds up computations during inference.
不希望在测试阶段计算梯度，因为我们不需要更新模型参数，所以使用with torch.no_grad()来禁用梯度计算，从而减少内存消耗并加快推理速度。

## Save / Load Trained Models
- save 
```py
torch.save(model.state_dict(), 'model.pth') # save model parameters
```
- load
```py
ckpt = torch.load('model.pth') # load model parameters
model.load_state_dict(ckpt) # load parameters into model
```