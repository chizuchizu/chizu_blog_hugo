---
title: "家からでもTPUを使いたい"
author: "chizuchizu"
date: 2021-01-11
images: ["/img/main/tpu_gcp.jpg"]
tags: ["gcp", "kaggle"]
---


# 作業
## TPUインスタンスを作る



```bash
export PROJECT_ID=hogehoge
export TPU_NAME=hogehoge
```

`TPU_NAME`という環境変数が無いとTPUを動かすことができないので最低でもこれだけは定義しておかないといけません。

gcloudを使ってローカルから作る。TF-versionを選択しなかったら最新版の2.4が選択されるが、GCPが対応してるのは2.3.1までらしく、エラーが出てしまうので**明示的に
2.3.1としておきましょう**。（この仕様 is 何）
また、プリエンプティブルインスタンスにしたいときはTPUとマシンそれぞれ引数が必要とのこと。

```bash
ctpu up --project=$PROJECT_ID \
 --zone=us-central1-b \
 --tf-version=2.3.1 \
 --name=TPU_NAME
 --preemptible \
 --preemptible-vm
```

これで、インスタンスが立ち上がります。

## ssh接続→Jupyter Lab

Jupyter Labを使うので少し複雑になります。

```bash
gcloud compute ssh $TPU_NAME -- -L 8080:localhost:8080
```
これでポート転送ができます。

TPUのインスタンスには基本的なPython環境（3.7.5）しか入ってないので、Jupyter Labも自分で入れる必要があります。

しかも、Python2も入っているのでpipを使うとかなり環境の復旧が面倒になるのでpip3、python3と打つことを心がけましょう。（Deep Learning VMではその必要が無い）

```bash
pip3 install jupyterlab
```
これで、入りました。
```bash
jupyter lab --no-browser --port 8080
```
とすることで、いつもどおりトークン付きリンクが表示されるのであとはローカルのブラウザから開いて実行しましょう。


## 動作確認

以下のコードを実行して、エラーにならなければTPUが認識されています。初回だとずらりとTPUがどうたらこうたらっていう表示がありますが、エラーにならなければそれは認識している意味なので問題はありません。


```python
import tensorflow as tf

print(tf.__version__)

resolver = tf.distribute.cluster_resolver.TPUClusterResolver()
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)
strategy = tf.distribute.experimental.TPUStrategy(resolver)
```


↓正常な場合下のような出力になる

![](https://pbs.twimg.com/media/ErbpNE5UYAMjnJy?format=png&name=medium)


### エラーが出る時

恐らく環境変数にミスがあると思われます。一旦Jupyter Labをshut downしてターミナルから以下のように `TPU_NAME` を登録してあげましょう。
```bash
export TPU_NAME=hogehoge
```

# 余談

前回の記事は語尾を「〜である。」といった堅い口調にしていたのですが、何となく性に合わなかったのでこれからは「〜です。」といった口調にしてみます。

そういえばKaggle KernelのTPUはV3-8だったから128GBも使えるのか…　30h使うとなるとプリエンプティブルでも数千円は余裕でかかるからめっちゃお得だなって思います。

コスパが良いのはもちろんなんですけど、実行時間が圧倒的に速いので高速で実験回せるのでGPUより絶対良いなーとも思いました。TPUのワークステーションとか買えるのかな。（買えないけど）

![](https://cdn.discordapp.com/attachments/795149266258493494/798124173989249054/unknown.png)


これは謝罪に近くなるのですが、前回の記事のJupyter Labあたりの説明を強引にやりすぎていて、動くか怪しいです。近いうちに修正をしておきます。

# 参考
- [クイックスタート | Cloud TPU](https://cloud.google.com/tpu/docs/quickstart?hl=ja)
- [VM インスタンスへの安全な接続](https://cloud.google.com/solutions/connecting-securely?hl=ja#port-forwarding-over-ssh)
