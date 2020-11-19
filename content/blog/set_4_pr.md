---
title: "集合・位相入門 4章についてのノート"
author: "chizuchizu"
date: 2020-11-19T20:21:55+09:00
draft: false
description: "主に演習問題"
categories: ["set"]
tags: ["set", "math"]
---







普通にノートとして書いてますが、何かあれば優しくコメントしてくれたら助かります。

## 定義

$$
f: A \rightarrow B
$$


$$
P, P_1, P_2 \subset A \\  
Q, Q_1, Q_2 \subset B
$$


## 1. 写像について

### 定理

$$
f(P_1 \cup P_2) = f(P_1) \cup f(P_2)
$$

### 証明

$$
P_1 \cup P_2 \subset P_1, 
f(P_1 \cup P_2) \subset f(P_1)
$$

同様にして、
$$
P_1 \cup P_2 \subset P_2, 
f(P_1 \cup P_2) \subset f(P_2)
$$
より、
$$
f(P_1 \cup P_2) = f(P_1) \cup f(P_2)
$$

## 2. 逆像について

### 定理

$$
f^{-1}(f(P)) \supset P
$$

### 証明

$$
a \in f^{-1}(f(P))
$$

とすると、
$$
\exists b \in f(P)\  s.t. \ 
f(a) = b
$$
つまり、
$$
f^{-1}(b) \in P \Leftrightarrow f^{-1}(f(a)) \in P \Leftrightarrow f^{-1}(f(P)) \supset P
$$

### メモ：等号が成り立たない例

あとでやる

## 3. 単射や全射

### 定理1

fは単射とすると、以下が成り立つ。
$$
f^{-1}(f(P)) = P
$$

### 証明1





### 定理2

fは全射とすると、以下が成り立つ。
$$
f(f^{-1}(Q)) = Q
$$

### 証明2

