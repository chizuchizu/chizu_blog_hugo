---
title: "Hugoで埋め込みができない時の対処法"
author: "chizuchizu"
date: 2020-09-13T15:40:03+09:00
draft: false
description: "Hugo v0.60以上からMarkdown内のタグが反映されないらしいです"
categories: ["hugo"]
tags: ["hugo"]
---





## 問題点

Markdownの中で埋め込みをしようとしてscriptタグを使っても反映されない。speaker deck、YouTube、Twitterも同様です。

```markdown
<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">Expertになりました！！<br><br>m5銀🥈&amp;銅🥉でした<br>辛かったけど楽しかった！！！ <a href="https://t.co/5mlQuPY8F2">pic.twitter.com/5mlQuPY8F2</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1278213647521611782?ref_src=twsrc%5Etfw">July 1, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
```

## 原因

Hugo v0.60からdefaultではインラインのHTMLをレンダリングしないからだそうです。

> **unsafe**
> By default, Goldmark does not render raw HTMLs and potentially dangerous links. If you have lots of inline HTML and/or JavaScript, you may need to turn this on.

https://gohugo.io/getting-started/configuration-markup/#goldmark



## 対処法

`config.tml` に以下のものを追加します。

```bash
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
```



## example

### speaker deck

```html
<script async class="speakerdeck-embed" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>
```

<script async class="speakerdeck-embed" data-id="707dd07342954683a6299fb30fe6521b" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

### Twitter

```html
<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">コナン観る</p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1304387363368386569?ref_src=twsrc%5Etfw">September 11, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
```

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">コナン観る</p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1304387363368386569?ref_src=twsrc%5Etfw">September 11, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

### YouTube

```html
<iframe width="560" height="315" src="https://www.youtube.com/embed/TGyBNOTP99Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

<iframe width="560" height="315" src="https://www.youtube.com/embed/TGyBNOTP99Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



## 参考

https://budougumi0617.github.io/2020/03/10/hugo-render-raw-html/