---
title: "KagglerのためのGCPのメモ"
author: "chizuchizu"
date: 2021-01-10
draft: false
images: ["/img/main/Yellow and Blue Initiative Blog Banner.png"]
tags: ["kaggle", "gcp"]
---


# 導入
GCPというGoogleのクラウドのプラットフォームがある（そのまま）。

さすがにローカルの環境だけではやっていけないことが多いのでGCPでインスタンスを借りて動かそうかなと思った次第。

3万クレジットがあるので割と自由が利くけど、アップグレードし忘れてると制限ばかりでGPUすらまともに建てられないしCPUは低スペだけだしと色々と悲しいことだらけなのでアップグレードはしておこう。


# やりたいこと
- GPU付き
- プリエンプティブル
- TF環境が用意されている

インスタンスを立ち上げたい。情報によると、GPUのプリエンプティブルインスタンスはCLI経由でしか立ち上げることができないので、いわゆるGUI(サイト)からでは立ち上げられない。
少し厄介になるが、外出先でもお気軽に接続できるという意味では良いのかもしれない。

# 書くこと
- GCPインストール
- 設定等
- インスタンスを建てるコマンド
- Jupyter Labを起動

コマンド系は忘れがちなのでここに書いておいて振り返ることのできるようにと思っている。


# 本論
## インストール（Debian）
僕が使っているchromebook及び、メインのPCはDebianベースなのでコピペで動く。

```bash
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

[Debian と Ubuntu 用のクイックスタート](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu?hl=ja)


## ログイン

```bash
gcloud init
```
1. (初回のみ)ログイン
2. プロジェクトの選択
3. ベースとなるzoneの選択

## インスタンスの立ち上げ

```bash
export IMAGE_FAMILY="tf2-ent-latest-gpu"  # ベースとなるイメージ
export ZONE="us-west1-b"  # インスタンスのリージョン
export INSTANCE_TYPE="n1-standard-8"  # マシンのタイプ（CPUとメモリの選択が可能）
export INSTANCE_NAME="tf-instance-1"  # インスタンスの名前
gcloud compute instances create $INSTANCE_NAME \
  --zone=$ZONE \
  --image-family=$IMAGE_FAMILY \
  --image-project=deeplearning-platform-release \
  --maintenance-policy=TERMINATE \
  --accelerator="type=nvidia-tesla-t4,count=1" \
  --metadata="install-nvidia-driver=True" \
  --machine-type=$INSTANCE_TYPE \
  --preemptible  # プリエンプティブルON
```

- ベースとなるイメージ [イメージの選択](https://cloud.google.com/ai-platform/deep-learning-vm/docs/images)
- [リージョンとゾーン](https://cloud.google.com/compute/docs/regions-zones?hl=ja)
- [マシンタイプ](https://cloud.google.com/compute/docs/machine-types?hl=ja)
- [Compute EngineのGPU](https://cloud.google.com/compute/docs/gpus?hl=ja)
- 

### イメージについて
GCPのドキュメントのイメージのページでKaggleの環境が無かったのが不思議だった。というのも、VMをGUIで立ち上げる時はKaggleの環境（BETA）を選択できたから。
おやと思ってコマンドを打って全部調べてみたら無事あったので、もしKaggleに合わせる時は使ってみたい。

[イメージの選択](https://cloud.google.com/ai-platform/deep-learning-vm/docs/images)

利用可能なすべてのイメージは以下のコマンドで表示が可能。
```bash
gcloud compute images list \
        --project deeplearning-platform-release \
        --no-standard-images
```

```bash
kaggle-container-v20201105-ubuntu-1804                         deeplearning-platform-release  kaggle-container-ubuntu-1804                               READY
kaggle-container-v20201229                                     deeplearning-platform-release  kaggle-container                                           READY
kaggle-container-v20201229-debian-10                           deeplearning-platform-release  kaggle-container-debian-10                                 READY
kaggle-container-v20201231-debian-9                            deeplearning-platform-release  kaggle-container-debian-9                                  READY
```


[TensorFlow Deep Learning VM インスタンスを作成する](https://cloud.google.com/ai-platform/deep-learning-vm/docs/tensorflow_start_instance)

## Jupyter Labの立ち上げ

先程のイメージでtf等を選択していれば、予めPythonの環境が入っているのでDocker等を使って環境構築をする必要はなくなる。
あとは必要なライブラリをインストールして使うだけ。ただ、エディタが無い👀

GCPのAI PlatformはJupyter Labをサポートしているので、簡単に立ち上げられる！

SSH通信を一回でもしていないとなぜかJupyter Labに繋げられない(´；ω；｀)
```bash
export PROJECT_NAME="hogehoge"
gcloud beta compute ssh \
  --zone $ZONE \
  $INSTANCE_NAME \
  --project $PROJECT_NAME \
  
```
そしたらexitしてローカルに戻ってJupyter Labを起動しよう。

```bash
export PROJECT_ID="hogehoge"
export ZONE="us-west1-b"
export INSTANCE_NAME="hoge-instance"
gcloud compute ssh --project $PROJECT_ID --zone $ZONE \
  $INSTANCE_NAME -- -L 8080:localhost:8080
```

ローカルから接続できる。

[http://localhost:8080](http://localhost:8080)

やったぜ！！！
![](https://cdn.discordapp.com/attachments/795149266258493494/797756928071565342/unknown.png)


# 使いそうなコマンド

### インスタンスの起動、停止

```bash
gcloud compute instances start $INSTANCE_NAME

```

```bash
gcloud compute instances stop $INSTANCE_NAME
```

### プロジェクト一覧
```bash
gcloud projects list
```

### プロジェクトの切り替え
```bash
gcloud config set project $INSTANCE_NAME
```

### インスタンス一覧
```bash
gcloud compute instances list
```

### インスタンスにssh接続
```bash
gcloud compute ssh $INSTANCE_NAME
```

# TPUの場合

大体はGPUと同じだけどコマンドの使い勝手が違うところがややこしい。こっちは予めtf（デフォルトでlatest）がインストールされてるそう。

リファレンス読んでるとプリエンプティブルにするときはTPUとVM自体の両方選択しないといけない感じがする。

```bash
ctpu up --project=$PROJECT_ID \
  --zone=$ZONE \
  --name=$INSTANCE_NAME \
  --machine-type=$INSTNACE_TYPE \
  --tpu-size=v2-8 \
  --preemptible  \
  --preemptible-vm
```


[CTPU リファレンス](https://cloud.google.com/tpu/docs/ctpu-reference)
