---
title: "Student cup 2020の振り返り"
author: "chizuchizu"
date: 2020-09-13T08:29:24+09:00
draft: true
description: "夏に開催されたSIGNATE主催のstudent cupについてです"
categories: ["コンペ"]
tags: ["コンペ"]
---





## コンペ概要

お疲れ様でした！　

https://signate.jp/competitions/281

- NLP
- 4クラス分類
- データ数が少ない

英語圏の求人情報に含まれるテキストデータから

- DS
- ML Engineer
- SE
- Consultant

を分類しろというタスクです！最近DSとコンサルタントが近くなってる気も……



## 自分のチームのsolution(49 th)

自分は藤戸四恩さんとチームを組んでました！（https://twitter.com/continueonlyone）

またソースコードはこちら→ https://github.com/Chizuchizu/student_cup_chizuchizu

49thなので上位解法ではありませんｗ

反省会で共有したスライドです！

<script async class="speakerdeck-embed" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

### モデル紹介

<script async class="speakerdeck-embed" data-slide="6" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

#### BERT

安定してもう強かった　強すぎて何も言えなかった

#### RoBERTa

BERTよりかは少し劣ってるけどまぁまぁ良い

#### XLNet

たまにロスが全く落ちないことがあったり学習時間が遅かったりするけどまぁまぁ働いてくれた

#### LSTM

めっちゃ頑張ったけど結局あんまり効かなかった

Jigsawコンペの3位解法で使われたLSTMを真似ました。

https://www.kaggle.com/sakami/single-lstm-3rd-place

- GRU
- Pooling
- embedding
- dropout

optimizer: scale_cos

三角関数のoptimizerを使ってるので出力というか推論に使う重みはepochごとの指数重み付け平均にしました。また、重みのEMA（指数移動平均）も使って平均をとることもしました。

やっぱりデータ数が少ないのでLSTMみたいな多少largeに対応するようなモデルには厳しかったようです。

余談ですが、自分はLSTMを書く前はPyTorchでモデルを組んだことも、Adamを理解することもしてなかったのでチームメイトの藤戸さんに聞きまくってましたｗ

<script async class="speakerdeck-embed" data-slide="16" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

### Augmentation

Jigsawでよく使われた方法を用いました。

英→日→英、英→独→英、英→仏→英　というように３種類＋オリジナルの系４種類のデータセットができました。

train, testの両方にaugment処理を行ったので16倍です！

<script async class="speakerdeck-embed" data-slide="10" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

### Regression

このデータセットのラベル間の差が小さいこともあって

stackingに突っ込んだらちょっとだけ良くなったので効いてくれたみたいです。

<script async class="speakerdeck-embed" data-slide="11" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

### LB vs CV

結論からいうとTrust LBが勝ちました。自分のチームはCVを信じたので49位と……

理由はリークが見つかってデータセットを差し替えたときに不均衡になってしまったからのようです。上位陣はこれを知った上であえてLBを信じるということをしていて頭が良いな〜と思いました。



結果としては間違った憶測でしたが、LBとCVに全く相関がなかったのでCVを信じてしまいました。

<script async class="speakerdeck-embed" data-slide="19" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

終わる1週間近く前に提出したTrust LBサブが4位でした……

<script async class="speakerdeck-embed" data-slide="20" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

## 反省会

終了してから5日後に開いた反省会です！

### mosamosaさん

保守的戦略というのが面白いです。undersamplingの平均を使ったようです。

<script async class="speakerdeck-embed" data-id="9ff418dfeca540d2b9b17a8514e727ce" data-ratio="1.41436464088398" src="//speakerdeck.com/assets/embed.js"></script>

### rinch_mathさん

overfit対策をしっかりやってる印象でした。

<script async class="speakerdeck-embed" data-id="2e66da1eb8fa4f70af7354194881572f" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>



### yCarbonさん

2位入賞おめでとうございます！　見極める力が強そう……

<iframe src="//www.slideshare.net/slideshow/embed_code/key/GslIvvFm6aLWCf" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/HogeBona/student-cup-2020-2nd-solution-lt" title="Student Cup 2020 2nd(?) solution LT" target="_blank">Student Cup 2020 2nd(?) solution LT</a> </strong> from <strong><a href="https://www.slideshare.net/HogeBona" target="_blank">HogeBona</a></strong> </div>

他にも数人参加されてた方がいましたが、スライドはありません 🙏

upuraさんがstudent cupのsolutionに関するツイートをまとめてくれたのでそれも参考になるかと！

https://togetter.com/li/1582669





## 振り返り

- データ数が少ないのは嬉しい
- 不均衡はかなり辛い
- student cupのコミュニティが楽しかった
- チームで参加できたためにモチベがめっちゃ安定してた（作戦会議も楽しかった）

