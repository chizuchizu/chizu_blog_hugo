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

### 別のアプローチ

### 

$$
P \supset f^{-1}(Q)
$$

だから、
$$
f(P) \supset f(f^{-1}(Q))
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

像が一意に定まることを利用する。n個のAの写像（B）の元が存在する。
$$
\exists b \in f(A) = B
$$
また、Bの逆像（A）の元もn個存在する。
$$
\exists a \in f^{-1}(B) = A
$$
これらの元は１対１対応するので
$$
f^{-1}(f(P)) = P
$$


### 定理2

fは全射とすると、以下が成り立つ。
$$
f(f^{-1}(Q)) = Q
$$

### 証明2

$$
P \supset f^{-1}(Q)
$$

fは全射なので、
$$
f(A) = B
$$
つまり、どんなBの元bに対しても
$$
\exists a \in A \ s.t. \ f^{-1}(b)=a
$$
このようなaが存在するので
$$
f(f^{-1}(Q)) = Q
$$

## 4. 単射について

### 定理

fが単射ならば、以下が成り立つ。
$$
f(P_1 \cap P_2) = f(P_1) \cap f(P_2)
$$

### 証明

#### 1 

はじめに、下を示す。
$$
f(P_1 \cap P_2) \supset f(P_1) \cap f(P_2)
$$

$$
\forall a \in f(P_1) \cap f(P_2)
$$
をとると、fは単射なので、
$$
a = f(x) \ (x \in P_1)
$$

$$
a = f(y)\ (y\in P_2)
$$

がいえる。以上より上の式は示せた。

#### 2

次に、下を示す。
$$
f(P_1 \cap P_2) \subset f(P_1) \cap f(P_2)
$$

$$
\forall a \in f(P_1 \cap P_2)
$$

をとると、ある
$$
\exists y \in P_1 \cap P_2
$$
を用いて
$$
a = f(y)
$$
と表せる。以上より、
$$
a = f(b) \ (\forall b\in P_1)
$$

$$
a = f(b) \ (\forall b \in P_2)
$$

上の２つが成り立つ。

したがって、
$$
f(P_1 \cap P_2) = f(P_1) \cap f(P_2)
$$


## 5. 差集合がちょっと関わる

### 定理

$$
f(A-P) \supset f(A) - f(P)
$$

### 証明

言い換える。共通部分。
$$
A-P =A \cap P^c
$$

$$
f(A \cap P^c) \supset f(A) \cap f(P)^c
$$


$$
\forall x \in f(A) \cap f(P)^c
$$

$$
x = f(y)\ (\exists y \in A)
$$

$$
x \neq f(y)\ (\exists y \in P)
$$

$$
x = f(y)\ (\exists y \in P^c)
$$

より、
$$
y \in A \cap P^c
$$
したがって、
$$
f(A \cap P^c)  \supset f(A) \cap f(P^c)
$$

### 等号の成り立たない例

定置写像（具体例は省く）

### fが単射のとき

逆向きを示す。

#### 定理

$$
f(A-P) = f(A) - f(P)
$$

#### 証明

$$
f(A-P) \subset f(A) - f(P)
$$

以下と同値
$$
f(A \cap P^c) \subset f(A) \cap f(P)^c
$$
を示せば上の定理より等号が示せる。


$$
\forall x \in f(A \cap P^c)
$$

$$
x = f(y)\ (\exists y \in A \cap P^c)
$$


$$
x = f(y)\ (\exists y \in A)
$$

$$
x \neq f(y)\ (\exists y \in P)
$$

$$
x = f(y) (\exists y \in P^c)
$$

つまり、
$$
x \in f(A)
$$


$$
x \in f(P)^c
$$

といえるので、
$$
f(A-P) \subset f(A) - f(P)
$$
したがって、等号がいえる。

## 6. 逆像など

### 定理

$$
f^{-1}(B - Q) = A - f^{-1}(Q)
$$

つまり、
$$
f^{-1}(B \cap Q^c) = A \cap f^{-1}(Q)^c
$$

### 証明



