![CI](https://github.com/Chizuchizu/chizu_blog_hugo/workflows/CI/badge.svg)
## 記事テンプレート生成コマンド
  
```
hugo new blog/post.md
```
## ライブビュー編集モード
```
hugo sever
# http://localhost:1313 にアクセス
```
## 公開用圧縮変換モード
```
hugo --minify
```

## TIPS
```
title: "Aa"
author: "chizuchizu"
date: 2020-05-26T02:42:38+09:00
draft: false
description: "概要"
categories: ["aaa"]
tags: ["未指定"]
---
```
内の'draft'を'true'に変更すると公開設定になります。
