---
title: "何もしてないのに急にUpdateが出来なくなった件【Arch Linux|解決済み】"
author: "chizuchizu"
date: 2022-01-30T08:27:20+09:00
draft: false
images: ["/img/arch/image1.webp"]
description: "EndeavourOSを使っていたら、急にアップデートができなくなりました。"
categories: ["arch", "linux", "endeavouros"]
---

# 何が起きたか
2022/01/29 15時ごろ

いつもどおり、EndeavourOSを起動して作業していました。その日は`dotfiles`の設定に勤しんでいて精神的に
かなり充足していました。

作業のキリがよく、`doas pacman -Syu`を実行しました。`doas`というのは`sudo`と同じ意味のコマンドです。

そうすると、謎のエラーが吐かれるではありませんか。

```
error: GPGME error: No data
error: failed to synchronize all databases (invalid or corrupted database (PGP signature))
```

`pacman`だけでなく`yay`でも同じです。


![](/img/arch/image1.webp)


`signature`で何となく察しました。

# 考えられる原因

- 変なファイルを消してしまった
    - `dotfiles`をいじったときに`/etc`内のファイルも触ったので
- 依存関係に失敗した
    - 昨晩`osu!`というゲームをダウンロードしてしまった
    - 32bitの`wine`を入れたのでやらかしたかも
- 俺は悪くない
    - 何もしていないのに壊れた


# やること
- ググる　試す
    - Arch Wiki
    - Arch Forums
    - stackoverflow
- archlinuxjpコミュニティで質問

まず、自分ができるググって試すっていうことをしました。

## `/var/lib/pacman/sync`を消す

[Arch Linux system update: error: GPGME error: No data | stackoverflow](https://stackoverflow.com/questions/48117783/arch-linux-system-update-error-gpgme-error-no-data)

`/var/lib/pacman/sync`にはミラーサーバーのレポジトリ情報などが入っているらしいです。シンクロナイズドレポジトリングが失敗しているので、
一度消して、もう一度同期し直せばええやろということですね。

結果：だめでした

## 鍵を作り直す

どっかに書いてあったやつを試しました。

```
doas pacman -Scc
doas pacman-key --init
doas pacman-key --populate 
doas pacman-key --refresh-keys
```
<!---
![](/img/arch/image2.webp)
--->

結果：だめでした

よくみると、タイムアウトとかしてますね。ググった記事は全部これでエラー吐かれることはなかったので
ますます謎が深まりました。
```
gpg: error retrieving *** via WKD: No data
...
gpg: error retrieving *** via WKD: Connection timed out
```

諦めモードに入ったので、ダメ元で`archlinuxjp`コミュニティで相談しました。slackチャンネルがあるので、
質問も投げやすくて良い雰囲気です。

## `/var/lib/pacman/sync/*.db`をみる

コミュニティで相談したときに`/var/lib\pacman/sync/*`が良くないのかもねという話になり、この画像を見せました。

![](/img/arch/image4.webp)

```
/var/lib\pacman/sync/core.db:           gzip compressed data, from Unix, original size modulo 2^32 573440
...
/var/lib/pacman/sync/endeavouros.db:    HTML document, ASCII text, with very long lines (1090), with CRLF, LF line terminators
```


1個だけ変なのがありますね。謎のHTMLファイルがあります。配布元が死んでるかもという話になりました。
私はこの`ls`の結果を観てもHTMLだなぁとしか思いませんでしたが、強い人はこれみてすぐに異変を感じ取っていました。

後付ですが、Arch Wikiに書いてあることを引用しても、HTMLファイルは明らかにおかしいことがわかります。

> 通常 pacman のデータベースは /var/lib/pacman/sync に配置され、/etc/pacman.conf で指定したリポジトリのデータベースファイルがそこに作成されます。データベースファイルは gzip で圧縮された tar アーカイブになっており、パッケージごとにディレクトリが含まれています
[pacman - ArchWiki](https://wiki.archlinux.jp/index.php/Pacman)

### その謎のHTMLファイルをみてみる

![](/img/arch/image8.webp)

`This domain name expired on 2022-01-28 23:59:59`とあります。ドメイン失効やん(´；ω；｀)(´；ω；｀)

とりあえず、この`Funami tech`というサーバーが落ちている可能性が高いということがわかりました。


## ミラーサーバーを変える

普通、ミラーサーバーは`/etc/pacman.conf`に記載されています。
今死んでるのは`endeavouros`のdbなので、`pacman.conf`の`endeavouros`部分を探します。

```
[endeavouros]
SigLevel = PackageRequired
Include = /etc/pacman.d/endeavouros-mirrorlist
```

別ファイルを参照しているみたいなので、`/etc/pacman.d/endeavouros-mirrorlist`をみます。

```
# EndeavourOS mirrorlist:
Server = https://mirror.funami.tech/endeavouros/repo/$repo/$arch
Server = http://mirror.jingk.ai/endeavouros/$repo/$arch
...
```

やっぱ一番上にありました。`funami tech`は韓国のサーバー、`jingk ai`は中国のサーバーなので、納得ではあります。(日本にも置いてほしい)

死んでる一番上のサーバーをコメントアウトすればOKです。

![](/img/arch/image6.webp)

## 解決

`pacman -Syu`をしてみます。updateができただけで泣きそうになったのは初めてです。

![](/img/arch/image7.webp)

# まとめと、発見が遅れた理由

- ミラーサーバーのドメイン失効が原因だったよ
- ミラーサーバーを変えたら治ったよ

という話です。でもね、これに辿り着くまでに数時間はかかりました。

それは、サーバーが死んでいても動いていたことが原因だと思っています。
普通サーバーの死というのは`ping`しても帰ってこないような話なのですが、今回はドメイン失効なので
よくわからんHTMLサイトに遷移されたので、`pacman`側もサーバーが動いてると勘違いしていました。

`eos-rankmirrors`をしてみます。これは、ローカルマシンからのアクセスが一番速いミラーサーバーを探すコマンドです。

サーバーが死んでいても1位に食い込んでいます。よくみると、一番上だけ`HTML`とか書かれてて明らかにおかしいですよね。
これは例外処理が足らなかったことによるものだと思います。元気が出たらバグ報告したい。

![](/img/arch/image9.webp)


何もしていないのに壊れたという結果で終わりました。
Archのコミュニティでは、そういうこともよくあるらしいので、ミラーサーバーを変えるのが手っ取り早い解決策だということがわかりました。
自分に起因しているか起因していないかがわかりますもんね。


長くなりましたが、これが誰かの助けになればと思って記事を書きました。


