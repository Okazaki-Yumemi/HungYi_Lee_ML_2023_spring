# HW2 Phoneme Classification

## Task

Predict one of 41 phoneme classes for each speech frame.

## Input

A frame has 39-dimensional MFCC features.

After concatenating n frames:

input_dim = 39 * n

## Model Output

logits shape:

[B, 41]

## Label

label shape:

[B]

label dtype:

torch.long

## Loss

CrossEntropyLoss accepts raw logits.

Do not apply Softmax before CrossEntropyLoss.

## Prediction

pred = logits.argmax(dim=1)