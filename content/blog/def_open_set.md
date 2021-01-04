---
title: "開集合の定義の誤解が解けた"
author: "chizuchizu"
date: 2021-01-04
tags: ["math"]
images: ["/img/main/Black Technology Blog Banner.jpg"]
draft: false
---

# きっかけ
発端となったツイートが、「数研講座シリーズ　大学教養　微分積分」と「チャート式シリーズ　大学教養　微分積分」という本
において開集合の定義が違うのじゃないかというお話です。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">開集合🤔 <a href="https://t.co/OJeb9UumIf">pic.twitter.com/OJeb9UumIf</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1345932815523725312?ref_src=twsrc%5Etfw">January 4, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


開集合の定義において、包含関係の記号は$$\subset$$と$$\subseteq$$のどちらが正しいのか気になりました。



## 答え

とりあえず

$$\subset$$と$$\subseteq$$は部分集合という意味で同値であるとします。

### 一般の距離空間上では偽
離散空間上で1点集合を作った時、真部分集合は存在しません。
よって、一般の距離空間では＝となるような場合も考慮する必要があります。

### 今回の仮定においてはどちらも真
ユークリッド空間上では距離関数がユークリッド距離として定められています。

上で例として挙げたものは今回の仮定にそぐわないので今回の仮定では絶対に真部分集合がとれます。

要するに今回の仮定だったら等式が成り立っていなくても良いという認識です。

# 混乱した原因

- 一緒の著者の本なのに記号が違う
- 2つの記号を別の意味として捉える集合の本を最近読んでいた

ソースは無いのですが、一般的には半順序を意識しているので反射律が成り立つような部分集合を考えるのが普通らしいです。

勉強になった。

