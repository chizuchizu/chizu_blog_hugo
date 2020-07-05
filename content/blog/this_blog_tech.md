---
title: "オレオレ最強ブログ環境を作った"
author: "chizuchizu"
date: 2020-06-06T17:07:39+09:00
draft: true
description: "いろんなものを自動化させました"
categories: ["ブログ"]
tags: ["ブログ"]
---



皆さん、ブログ書いてますか？　正直ブログを書いてるか書いてないかというのは興味ないです（？？？）

ブログ環境は何を使ってますか？

- wordpress
- はてなブログ（これ多そう）
- 自前（マイナー）

僕は以前WordPressを使ってたのですが、色々あってWordPressが使えなくなりデータが吹っ飛んで今のブログになりました。

この記事を通して、新しい（やってる人はいるけど少ない？？）ブログの形態を紹介できたらなと思っています。

# 変化

## Before

使ってた環境

- Xserver
- WordPress

本当に普通のやつ。1万５千のテーマを買って本気になっていたが、全然記事がかけずに素振りしてしまった悲しい思い出。

- プラグインのおかげでSEOとかよくなってた　らしい
- 重い（プラグインもテーマも）
- UIが崩れてた
- 記事書きづらい（画像の貼り付けや数式の挿入含めて）
- WordPress遅いし眩しい（dark themeが無いから無理矢理黒くしたけど今度は見えなくなった）
- 困ることは無かった

何か酷いことばかり言ってますが、当時のぼくはこれが当たり前なのだと錯覚してたようです。

## After

- Hugo（静的サイトジェネレーター　後で説明します）

Hugoを使ってます。変わったことは他にもたくさんありますが、後で説明します。（概要のみ）

- ブログの反映が超簡単
- データのバックアップの必要がなくなった
- 細かいところがいじれる
- とにかく速い

# 何をしたのか

## 概要

1. WordPressのデータを消す
2. Hugoを導入してみる
3. GitHubにオープンソースとして公開
4. GitHub Actionsでpush時にサーバーにデータが移されるように
5. アイキャッチ画像自動生成
6. コントリビューターにテーマのカスタマイズなど色々してもらった

## 1. WordPressのデータを消す

不手際でWordPressの一部データを削除してしまい、どうにもならなくなったので全部消しちゃいました。

理由はシンプルで、FTPソフトのFileZillaで遊んでたからです。

## 2. Hugoを導入してみる

Hugoとは ([ここより引用](http://www.study-hugo.com/basic/whats-hugo/))

> HUGOは、静的なhtmlを生成する事ができる**静的ページジェネレータ**です。HUGOの場合、ローカル環境ではHUGOの動的機能を使って動的にサイトを開発し、成果物の出力時に動的要素を全て静的要素（html,css,js,img等）として出力します。 生成された成果物にはサーバサイドの処理を含まないため、**サイトの表示速度は高速**になり、サーバサイドの処理が無い分**セキュリティリスク**が減ります。

つまるところ速いんですね。Hugoは記事が完成したらビルドをして、公開用のファイルを作成します。そこでかなり最適化されているっぽいので静的＆最適化で爆速らしいです。（このブログも速いかな？？）

## 3. GitHubにオープンソースとして公開

ここです。ただ、作業ディレクトリをpushするだけ。2020/07/05時点で261 commits/3 contributorsがいます。 

https://github.com/Chizuchizu/chizu_blog_hugo

## 4. GitHub Actionsでpush時にサーバーにデータが移されるように

恐らくどのサーバーを使っていたとしても仕組みは同じでサーバーの指定のディレクトリ内に表示させるファイルなどを更新していきます。方法は色々とあって

1. WordPressで完全自動
2. FTPソフトで手動でいれる
3. コマンドで自動化

最初2の実験をしようと思ったら手がすべって消しちゃいけないWordPressのデータを消しちゃったので、1と2は論外とします。特に2は面倒だし。

3が有力なのですが、これも中々面倒でした。

できたのがこれです。所々隠してますが。

1. Hugoをインストール
2. Hugoでサイトをビルドする
3. SSH接続をするなど（秘密鍵や公開鍵をしまっておく）
4. サーバー内を空にする
5. アップロード

途中から 弥生水葉　という部活の先輩に手伝ってもらってようやくここまで来ました。pushごとに実行されるようになっているので更新がある度にアップロードしてくれます。大体30秒くらいで終わります。

元々はFTPでもよくね？というノリだったのですが、セキュリティがどうたらでSSH通信にしました。ただSCPは全部送る関係上遅いので差分を送るrsyncに変えました。

```bash
	name: CI_test

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ master ]
#   pull_request:
#     branches: [ master ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@master   # リポジトリのデータを仮想環境にチェックアウトしてくるアクションを実行する

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2.2.0
        with:
          hugo-version: "latest"
          extended: true
       
      - name: Build Project
        run: hugo  --gc --minify                    # hugo ビルド
     
      - name: Get SSH Key
        run: |
          PWD=`pwd`
          cd ~
          pwd
          mkdir .ssh
          touch .ssh/id_rsa
          touch .ssh/id_rsa.pub
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > .ssh/id_rsa
          echo "[sv7521.xserver.jp,183.90.241.42]:10022 ssh-rsa SHA256:V0GmZVuUlP6tQw5MYbGelfcq+IQwq/6+HnH1OPAcaLo" > .ssh/known_hosts
          echo "${{ secrets.SSH_PUBLIC_KEY }}" > .ssh/id_rsa.pub
          chmod 700 -R .ssh
          chmod 600 .ssh/*
          ssh -v -T -p 10022 *.xserver.jp  -o StrictHostKeyChecking=no
          
      - name: Delete Remote Files
        run: ssh -v -T -p 10022 *.xserver.jp "rm -r chizuchizu.com/public_html/*"
        
      - name: Send Files
        run: |
          cd $PWD
          #scp -v -P 10022 -r public/* 
          rsync -avzP -e "ssh -p 10022" public/* *.xserver.jp:chizuchizu.com/public_html/
```

## 5. アイキャッチ画像自動生成

これは昔WordPressでも同じことをしていたので気兼ねなくできています。

Qiitaやはてブロを意識しました。個人的に気に入っています。

これもいちいち手元でやるのは面倒なのでGitHub Actionsの中に組み込んでおきました。最強すぎる。ただ、全記事に対して生成を行っているので差分だけできるようにしたいとか思っています。（いずれ修正します）

あと、英語だとスペースで改行されちゃうから全角空白で改行に変えようかなとも思ってます。

面倒なことはPythonにやらせました。

```python
from PIL import Image, ImageDraw, ImageFont

"""
空白は改行(半角全角どちらでも)
-----------------------------
"""


def main(title, name):
    title = title.replace(" ", "\n").replace("　", "\n")
    # txt = "TF-gpuをメモリ落ちさせずに\n使う方法"
    # 保存されるディレクトリパス
    file_path = "static/img/eye-catch"
    # 元画像
    image_path = "static/img/main/face.png"
    # フォントのパス
    font_path = "static/font/Kokoro.otf"
    # about me
    about_me = "@chizu_potato(チズチズ)"

    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(font_path, size=50)

    h, w = im.size

    # テキストのサイズを取得（そのまま）
    txtsz = draw.textsize(title, fnt)

    # box
    osd = Image.new("RGB", (txtsz[0] + 10, txtsz[1] + 10), "skyblue")

    # center
    h_draw = (h - txtsz[0]) // 2
    w_draw = (w - txtsz[1]) // 2

    dctx = ImageDraw.Draw(osd)  # create drawing context
    dctx.text((5, 5), title, font=fnt, fill="black", align="center")  # draw text to osd

    im.paste(
        osd,
        box=(h_draw, w_draw, osd.size[0] + h_draw, osd.size[1] + w_draw),
        mask=Image.new("L", osd.size, 210))  # 透明度

    fnt = ImageFont.truetype(font_path, size=30)
    # ここの座標は自分で変更してください。人や画像によって最適なものが違うと思います。
    draw.text((580, 450), about_me, font=fnt, fill="black")  # draw text to osd

    im.save("{}/{}.png".format(file_path, name))
    return "{}/{}.png".format(file_path, name)
```

## 6. コントリビューターにテーマのカスタマイズなど色々してもらった

### ダークテーマ

これはマジで凄いです。右上の方に月のマークがあるでしょ？押してみてください。目に優しいです。しかも、ダークテーマにしたかどうかが端末に保存されているので二度目からは設定なしでダークテーマになるという仕様らしい。

### 非同期ページ遷移

FireFoxだと挙動が怪しいのですが、Chromeだとページ遷移のときが滑らかになっています。しかも読み込み中マークが出てきてすごいな〜とか思ってる。

### MathJax対応

もともとKaTeXだったけどやっぱりMathJaxなのかなとか。
$$
e^{i\pi}=-1
$$

### SNSアイコンの色指定

色を修正してくれました。LINEも追加してくれたっぽい。あといつの間にプロフィールのところにAtCoderやKaggleのURLも載っけてくれてたｗ

### ありがとう

本当にありがとう。

# 振り返って

SCP通信のところはマジで詰んで数日苦しんでましたｗ　ただ、今となってはTyporaでブログの記事が書ける幸せを実感しています。

僕のブログはオープンソースなので気兼ねなくプルリクやissue送ってください！　気になることがあればここのコメントでもリプでも質問してください！

みなさんもこの機会にHugoを使ってオープンソースなブログを作ってみてはいかがでしょうか！