---
title: "Gentoo Linuxを入れた話"
author: "chizuchizu"
date: 2022-01-25T14:36:59+09:00
draft: false
description: "自分がGentoo Linuxという、世間的に難易度が高いLinuxOSを入れたきっかけや他のディストリビューションとの違いを話します。"
categories: ["linux", "gentoo", "ポエム"]
tags: [""]
---



# なぜGentooを入れようと思ったのか

## 私のスペック

- Ubuntuをメインで2年ほど使っていた
- Linuxは初心者
    - `man`コマンドを使ったことがない
    - コピペで環境したせいで段々bashが壊れていた

メインでLinuxを使っているとはいえ、本当に初心者でした。

## ある日の惨劇

Pythonのインタプリタが死んだ。poetryが使えない…… pyenvのバージョンも効かない

本業でPythonを使っているので、Python環境が死ぬと人生が終わったのと同然です。No Python No Life.

こうなってようやく、自分がLinuxのこと何もわかっていないなと気づきました。だったらArchでも入れちゃおうと。

## Arch Linuxを入れる

具体的にはdriverだけ良い感じのを入れてくれるEndeavourOSというArchベースのディストロです。とはいえ、最初は日本語入力の設定から始まりました。
これだけだと、GentooじゃなくてArch Linuxを入れた話になってしまいます。

## Linux面白くね？？

段々と気づき始めました。
通学時間や授業の暇な時間にはスマホでArch Wiki, Distro Watchをひたすら読んでいました。

## Gentoo Linuxと出会う

WikipediaのGentoo Linuxに関する記事では、**最上級**の難易度と語られています。

> 公式のインストーラーが存在しないので、インストールの難易度は最上級ともいわれる。ただ、一度インストールしてしまうと、システムを完全にアップデートすることのできる機構があるため、管理はインストール作業ほど難しくはない。管理に関しては、多くの場合、ほとんどの追加パッケージを手動ビルドしなければならない Slackware と比べて、簡単にできる。

https://ja.wikipedia.org/wiki/Gentoo_Linux


# Gentoo Linuxの特徴

## 他のLinuxOSとの比較

|                                | Ubuntu               | Arch                    | Gentoo                               | 
| ------------------------------ | -------------------- | ----------------------- | ------------------------------------ | 
| 難易度                         | かんたん             | 少しむずかしい          | 難しい                               | 
| OSのインストール               | GUI                  | CLI                     | CLI                                  | 
| vimのインストール              | apt install vim      | pacman -S vim           | emerge -a vim                        | 
| stableの新しさ                 | 古い（年単位）       | 最新                    | Archよりも数ヶ月遅い                 | 
| 情報量（日本語記事）           | 多いor多すぎる       | やや少ない              | 少なめ                               | 
| 参考にするサイト（個人の感想） | Qiita, stackoverflow | Arch Wiki, zenn, GitHub | Gentoo Wiki, Arch Wiki, Gentoo Forum |


難易度というのは、インストールから普段使いを含めた主観的な評価なのであまり参考にならないと思います。
細分化したら、伝わりやすいかなと思うので、sectionに区切って話していこうと思います。

### OSのインストール

OSのインストールっていうのは以下の工程を指します。

- USBメモリ(DVDでも)にinstall imageを焼く
- install imageで起動する
- HDDを分割する（お前はブート用、お前はスワップ、お前は普通のファイルだ。的な）
- Linux Kernelを入れる
- 必要なパッケージをインストール
- 起動に関する設定を行う


これが何を意味しているかというのはあまり重要ではなく、とにかくこういう工程を全部良い感じにやってくれてるのがUbuntuです。
マウスポチポチしてれば勝手にパソコンが動きます。

マウスポチポチでどうにもならないのがArchとGentooです。インストールの工程は**ほぼ**同じです。マウスが使えないCLI環境でコマンドを打って
必要なパッケージをインストールしたり、設定をしたりします。


<!--

では、Ubuntu, Arch, Gentooで何が違うかみていきましょう。

- USBメモリ(DVDでも)にinstall imageを焼く
    - Ubuntu: やる
    - Arch: やる
    - Gentoo: やる
- install imageで起動する
    - Ubuntu: GUIが起動する　Windowsみたい
    - Arch: CLIが起動する
    - Gentoo: CLIが起動する
- HDDを分割する（お前はブート用、お前はスワップ、お前は普通のファイルだ。的な）
    - Ubuntu: 推奨にボタンをクリックするだけ
    - Arch: コマンドで分割
    - Gentoo: コマンドで分割
- Linux Kernelを入れる
    - Ubuntu: パッケージのインストールでやってくれる
    - Arch: コマンドでインストール
    - Gentoo: 手動でダウンロードして設定してビルドする
- 必要なパッケージをインストール
    - Ubuntu: ボタン押したら勝手にやってくれる
    - Arch: コマンドでインストール（一括）
    - Gentoo: コマンドでインストール（1個1個）
- 起動に関する設定を行う
    - Ubuntu: 知らぬ間にやってくれる
    - Arch: コマンドで設定
    - Gentoo: コマンドで設定


UbuntuはWindowsと同じ　いや、よりも簡単に終わる気がする。ここではUbuntuが普通として扱います。

ArchもGentooもほぼ同じです。自分でTerminalにコマンドを打ち込んで色々やるだけです。

唯一違うのがLinux Kernelです。Archはパッケージをインストールするだけですが、Gentooはソースビルドをする必要があります。
それはそういうもんだなと思ってください。
-->


### パッケージのインストール

ここが一番Gentooらしいところです。

全部コマンド一発でインストールできるという意味では、全部同じです。


しかし、特殊なのがGentooです。Gentooはソースコードを引っ張ってローカルマシンでビルドしてバイナリファイルを作成しています。

例を出しましょう。イオンに行って服を買うのがUbuntuやArchです。Gentooは自分で服を作ります。
既に作られている製品=バイナリファイルです。服の原料=ソースコードです。自分の体に合った服を原料から自分で作るのがGentooといえます。

Gentooの例をパッケージに当てはめれば、使っているCPUに合うようにソースコードから良い感じにビルドする作業といえます。

Gentooのメリット
- とにかく最適化される
- 細かい設定が可能
- どんなCPUでも動く
Gentooのデメリット
- 時間がかかる(CPUの強さに依存)

多くの人はだから何くらいにしか思いません。正直自分はバイナリファイルから入れてもいいじゃんと思っている部分はあります。


### バージョンに関する考え方

1. ローリングリリースと固定リリース

Ubuntuは固定リリース。ArchとGentooはローリングリリースです。

Ubuntuは基本的に2年ごとにメジャーなアップデートが入ります。一方でArchやGentooは毎日更新が入ります。

**古いが、固定して安定したサポートを受けられる固定リリースか、どんどん新しくなっていくローリングリリース、それぞれに良さがあります。**

固定リリースはもちろん安定していますが、かといってローリングリリースが不安定というわけでもありません。
ローリングリリースも、stableなバージョンを採用しているので今まで変なバグに遭遇したことは一度もありません。

2. stableの慎重さ

これはArchとGentooの比較になります。

結論から言うと、Gentooはバージョンに対してかなり慎重です。Archのほうが新しいパッケージをstableとして採用しています。

Archは新しいパッケージをバンバン使わせてくれますが、Gentooはあまりそうではありません。

ここから先は人から聞いた話なので、参考程度に。

Archはx86しかサポートしていないが、Gentooは幅広い(ほぼなんでも)アーキテクチャをサポートしているので、テストに時間がかかるので、stableに慎重なのかも。約3ヶ月違う気がする。　とのこと。

納得の理由ではあります。


### 困ったときにどうするか

検索ワードにOSを入れてググるのですが、出てくる情報の量、質に違いがあると思っています。

Ubuntu: 比較的新しい日本語記事がいっぱいヒットするが、質はピンキリ
Arch: 古めの日本語記事、stackoverflowやredditがヒットする　質は良いものが多い
Gentoo: 日本語はほぼない、海外サイトもあんまない　質はピンキリ

これは、使っているユーザーの層を示していると私は考えています。
Ubuntuはライトユーザーが多いので、日本語の記事もいっぱいある。
Archはコアなユーザーが集まるOSなので、日本語英語限らず質が高い印象。

問題に遭遇したときにGentooに関する情報が少ないのはユーザー数が少ないからでしょうか？確かにUbuntuやArchと比べたら少ないです。
しかし、原因はそこではないと思っています。

それは、なにかの問題に遭遇した際、問題がOS依存なのか、パッケージ依存なのかが切り分けられるので、最初から一次ソースに近い情報を得られる
人が集まっているからだと思っています。

これは、周りのGentooユーザーを見た感想やForumsの議論のされ方から推測したことです。（真実かは知らんが、限りなくそうだと思っている）


## GentooならではのKernel Config

最初は自分でも意味がわからなかったのですが、GentooではLinux Kernelをソースコードから引っ張って、使いたい機能を取捨選択するコンフィグの設定をしてビルドする必要があるらしいです。

今となっては親の顔より見たKernel Configなので、なんとも思ってませんが、Linux Kernelのconfigは多すぎます。精神が削れます。

必要最低限しか使わなければ、ディスクの節約、パフォーマンスの向上につながります。
他のOSではやったことがありませんが、この機能必要だったわ！！ってなったときにすぐLinux Kernelを差し替えることができるようになりました。







# GentooInstallBattle

Linuxの界隈ではOSのインストール時に#〇〇InstallBattleというハッシュタグを使う文化があります。

自分もやりました。

最初は、メインパソコンのVirtualBox上に入れました。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr"><a href="https://twitter.com/hashtag/GentooInstallBattle?src=hash&amp;ref_src=twsrc%5Etfw">#GentooInstallBattle</a> 4回目、10時間以上費やしてようやくinstall成功！！！　嬉しすぎて涙出そう<br><br>本当に勉強になった(´；ω；｀)(´；ω；｀)　僕一人じゃ絶対成し遂げられなかった　アドバイスしてくれた人やwikiまとめてくれた人、全人類に感謝 <a href="https://t.co/lG6nYtr3DA">pic.twitter.com/lG6nYtr3DA</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1481271538477580291?ref_src=twsrc%5Etfw">January 12, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


自信がついたので、実機の余ってるHDDに入れてみました。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">気合でGUI対応させた <a href="https://t.co/QzDrK0psjI">pic.twitter.com/QzDrK0psjI</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1484160091922505730?ref_src=twsrc%5Etfw">January 20, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

授業中暇だったのでMacbookのVirtual環境にも入れてみました。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">MacbookにGentoo Linux入ってしまったｗｗ <a href="https://t.co/Rlg926xjtG">pic.twitter.com/Rlg926xjtG</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1483994118921793536?ref_src=twsrc%5Etfw">January 20, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


# 通して得たこと

## 問題解決能力

一次ソースに当たれるようになりました。
コマンドの使い方がわからなくても`man`コマンドを使って調べられるようになったし。
何かができなくても、パッケージの開発元にたどって調べられるようになった。

## いろいろなことのきっかけ

自分はこれを機に自作OS、自作CPU、Linux Kernelに興味が湧きました。

興味が湧いた人は[TURING COMPLETE FM](https://turingcomplete.fm/)というPodcastを聴いてみるのをオススメします。作業しながらでも普通にいけます。

低レイヤの第一人者をゲストとして読んで、CPUやLinux、コンパイラなどディープで面白い話が聴けます。
低レイヤに詳しくない人でもわかるように噛み砕いてくれてるので、自分でも楽しめました。

特に私のオススメが、[21. 東大CPU実験でRISC-Vプロセッサを自作した話](https://turingcomplete.fm/21)です。
自作CPUで自作OSを動かすという話なのですが、感銘を受けすぎて聴きながら春休みに自作CPUを作る決心をしました。


## 開発に対する姿勢が変わる

今までブラックボックスとして扱われてた部分がクリアになって、世界が違う色に見えました。嘘ではありません。



Gentoo Linuxを入れて後悔はしていません。

最初はハードルが高いかもしれませんが、一度でも入れてみる価値があるOSだと思っています。


こんな長いダラダラとした文章を読んでくださってありがとうございます。

何か感想や質問があれば、コメントやTwitter(@chizu_potato)まで教えていただけたら私が喜びます。



