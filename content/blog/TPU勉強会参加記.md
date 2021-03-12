---
title: "TPU勉強会 #1"
author: "chizuchizu"
date: 2021-03-12
tags: ["TPU", "kaggle"]
draft: false
images: ["/img/main/tpu-1.png"]
---

# TPU勉強会参加記

かえるるるさんが主催する「フリーライダーは絶対に許さないTPU勉強会」の第1回に参加してきました。

https://twitter.com/kaeru_nantoka/status/1361270810732679168

とにかく充実してました！！！！！



自分が発見したことや、他の参加者が共有してくれた情報をここに載せるつもりです。

（とは言うものの、情報や知識の確信度的なところから、自分が調べたリソースばっかになってしまってしまいました。）

## そもそもTPUについて

- [What's inside a TPU?](https://medium.com/@antonpaquin/whats-inside-a-tpu-c013eb51973e)
  - 理論面　ふんわりとしか理解できなかった
  - TPUの中の行列演算について
  - TPUのアーキテクチャ
  - 半精度の話
- [Cloud TPU 入門ガイド](https://cloud.google.com/tpu/docs/beginners-guide?hl=ja)
  - TFのドキュメント
  - CPUとGPUとTPUの演算方法の違いについて
- [TPU-speed data pipelines](https://cloud.google.com/tpu/docs/beginners-guide?hl=ja)
  - colabの解説？
  - TPUの仕組みをGIFで説明
  - TFRecordの作り方

自分の中の認識だと複数の演算をくっつけることができるために高速な処理が可能になってるイメージです。MXUとか……ね（よくわかってない）

Kaggleをやる分にはただ実行するハードウェアが変わっただけで高速になるならいいなーーというお気持ちです。



## TensorFlow

結果として今回の勉強会でPyTorchを書いて成功した人はいませんでした。なぜなのかは後ろの章で書きますが、とにかくTFはすんなり書くことができました。

自分は普段PyTorchを使っているのでTFは何もわからない状態でしたが、一度書いちゃえば何となく分かった気がしました。（ﾁｮｯﾄﾃﾞｷﾙ）

### TFRecordsとは

バイナリレコードに変換し、シリアライズ化（全部つなげる）することで読み込みを効率的にしようというものです。

これはTPUを使わずとも利用できますし、ターゲットも含めて柔軟に保存することが可能なので割とアリなんじゃないかなって思ってます。

メリットは読み込み速度が速くなることです。（まだ実験してないので確証はないけど理論上はそう）

デメリットは生データの数倍データが大きくなってしまうことです。（ものによって違うけど大きくなるのは真）



[TFRecordsとtf.Exampleの使用法](https://www.tensorflow.org/tutorials/load_data/tfrecord?hl=ja)というTFのドキュメントを読めば大体はわかりました。

[Better performance with the tf.data API](https://www.tensorflow.org/guide/data_performance)というTFのドキュメントでは、tfrecordsに限りませんが、datasetのAPIのパフォーマンスを上げる手段について色々書かれていました。これもコーディングの参考になります。

#### TFRecords形式への変換＆保存

下のコードは自分が書いたコード（https://www.kaggle.com/chizuchizu/make-tfrecord）から引っ張ってきたものです。辞書型でデータを渡しているからか、保存されたtfrecordsを確認するとjsonっぽい形式になってます。自分の書いたコードは一番シンプルな方法だと思います。

```python
def _bytes_feature(value):
    """string / byte 型から byte_list を返す"""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """float / double 型から float_list を返す"""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature(value):
    """bool / enum / int / uint 型から Int64_list を返す"""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def serialize_train(image, target, image_name):
    feature = {
        'image': _bytes_feature(image),
        target_cols[0]: _int64_feature(target[0]),
        target_cols[1]: _int64_feature(target[1]),
        target_cols[2]: _int64_feature(target[2]),
        target_cols[3]: _int64_feature(target[3]),
        'image_name': _bytes_feature(image_name)
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()


with tf.io.TFRecordWriter(filename_train) as writer:
    for i, row in tqdm(train.iterrows()):
        label = row[target_cols]
        path = row["path"]

        img = cv2.imread(path)
        img = cv2.imencode('.jpg', img, (cv2.IMWRITE_JPEG_QUALITY, 100))[1].tobytes()

        example = serialize_train(img, label, str.encode(row["image_id"]))
        writer.write(example)
```



かえるるるさんが書いたコード(https://www.kaggle.com/kaerunantoka/plant-createtfrecord)はbatchごとに処理し、tfrecordsファイルを吐き出していて、自分の書いたコードは2:53掛かっているのに対し、かえるるるさんのコードは1:33で終わっています。自分のコードは画像を１枚ずつ処理していたから遅いのだと思います。

更に面白いところが、PyTorchのDataLoader、Datasetを用いているところです。たしかに（たしかに）という感じですが、TFでPyTorchを使うっていうのにはさすがに驚きました。（合理的ではある）

#### TFRecords形式の読み込み

私が作ったtfrecordsを読み込むデコーダーの部分のコードは下に貼ります。TFでモデルを訓練させたときのコード（https://www.kaggle.com/chizuchizu/tpu-train-inf）から引っ張ってきました。

```python
def build_decoder(with_labels=True):
    def read_tfrecord(example):
        # 各々のデータに対してパース
        if with_labels:
            TFREC_FORMAT = {
                'image': tf.io.FixedLenFeature([], tf.string),
                config.base.target_cols[0]: tf.io.FixedLenFeature([], tf.int64),
                config.base.target_cols[1]: tf.io.FixedLenFeature([], tf.int64),
                config.base.target_cols[2]: tf.io.FixedLenFeature([], tf.int64),
                config.base.target_cols[3]: tf.io.FixedLenFeature([], tf.int64),
                'image_name': tf.io.FixedLenFeature([], tf.string),
            }
        else:
            TFREC_FORMAT = {
                'image': tf.io.FixedLenFeature([], tf.string),
                'image_name': tf.io.FixedLenFeature([], tf.string),
            }
        example = tf.io.parse_single_example(example, TFREC_FORMAT)
        image = decode_image(example['image'])
        if with_labels:
            targets = [example[x] for x in config.base.target_cols]
            return image, targets
        else:
            return image
```

この関数を`tf.TFRecordDataset`のmapに渡してあげれば読み込むことができます。上手く表現するのが難しいのですが、tfrecordsはデータセットを全部くっつけているけどindexの情報しか持ってないので読み込まない限りはメモリの消費はしません。`Dataset`周りの処理はtfrecordsを使わないものと大差ないので割愛します。

#### 可変長配列の保存（便利）

今回、私がサブミットしたコンペは[Plant Pathology 2020 - FGVC7](https://www.kaggle.com/c/plant-pathology-2020-fgvc7/overview)と呼ばれるりんごの葉っぱから病気を検出するマルチラベルの分類問題でした。保存するときにわざわざtargetの数だけ引数を渡して…っていうのも面倒なのでリストで保存できないかなーって模索をしてました。

そしたらあることに気付きました。上のコードと比較してほしいのですが、`value=[value]`→`value=value`にすることで配列を保存することできました。

```python
def _int64_list_feature(value):
    """List[bool / enum / int / uint] 型から Int64_list を返す"""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))
```

すると、バイナリレコードに変換するところの関数はどうなるかと言うと、

```python
def serialize_train(image, target, image_name):
    feature = {
        'image': _bytes_feature(image),
        "target": _int64_list_feature(target.tolist()),
        'image_name': _bytes_feature(image_name)
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()
```

このように、1行で済んで汎用的かつわかりやすいコードになったと思います。

あともう一つ気をつけなければいけないのが、読み込むときの関数です。

https://www.tensorflow.org/api_docs/python/tf/io/FixedLenSequenceFeatureにある関数を使わなければなりません。`allow_missing=True`がないとエラーになります。

```python
def read_tfrecord(example):
    # 各々のデータに対してパース
    TFREC_FORMAT = {
        'image': tf.io.FixedLenFeature([], tf.string),
        "target": tf.io.FixedLenSequenceFeature([], tf.int64, allow_missing=True),
        'image_name': tf.io.FixedLenFeature([], tf.string),
    }
    example = tf.io.parse_single_example(example, TFREC_FORMAT)
    image = decode_image(example['image'])
    print(example)
    targets = example["target"]
    name = example['image_name']
    return image, targets, name
```

https://www.kaggle.com/chizuchizu/fork-of-tpu-train-infここのコードで読み込んで画像とターゲットを表示することは成功したのですが、訓練させることはまだできてません。（頑張ればうまくいくと思ってるのでいつか）

### モデルの訓練など

おまじないが必要らしいです。最下行はTPUを使った分散学習を明示的に宣言する感じらしいです。[にのぴらさんのissueより](https://github.com/ninopira/study_tpu/issues/2)

おまじないというとあんまり良くないですが、自分で調べても初期化とか宣言っぽいところしかわかりませんでした。

> You must initialize the tpu system explicitly at the *start* of the program. This is required before TPUs can be used for computation. Initializing the tpu system also wipes out the TPU memory, so it's important to complete this step first in order to avoid losing state.
>
> https://www.tensorflow.org/guide/distributed_training

```python
tpu = tf.distribute.cluster_resolver.TPUClusterResolver.connect()
strategy = tf.distribute.TPUStrategy(tpu)
```

Kaggleだと下のような関数を使っていることがあります。

```python
def auto_select_accelerator():
    """
    Reference:
        * https://www.kaggle.com/mgornergoogle/getting-started-with-100-flowers-on-tpu
        * https://www.kaggle.com/xhlulu/ranzcr-efficientnet-tpu-training
    """
    try:
        tpu = tf.distribute.cluster_resolver.TPUClusterResolver.connect()
        strategy = tf.distribute.TPUStrategy(tpu)
        print("Running on TPU:", tpu.master())
    except ValueError:
        strategy = tf.distribute.get_strategy()
    print(f"Running on {strategy.num_replicas_in_sync} replicas")

    return strategy
```

あと、モデルを定義するところだと下のようにscopeの内側に入ってからやらなきゃいけないようです。

```python
with strategy.scope():
    model = tf.keras.Sequential([
        efn.__getattribute__(cfg.model.model_name)(
            input_shape=(cfg.model.size, cfg.model.size, 3),
            weights='imagenet',
            include_top=False,
            drop_connect_rate=0.1),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(cfg.base.target_size, activation='sigmoid')
    ])
    model.compile(
        optimizer=get_optimizer(cfg),
        loss=cfg.loss.name,
        metrics=[tf.keras.metrics.AUC(multi_label=True)])
    model.summary()
```

#### strateyについて

[Distributed training with TensorFlow](https://www.tensorflow.org/guide/distributed_training)というTFドキュメントが共有されていました。分散学習の話らしいです。

複数GPUもいけるよ〜〜って書いてありました。でも深いところはまだわかってません。

#### 高速化(steps_per_execution)

これも勉強会で共有されたものです。

[Use TPUs](https://www.tensorflow.org/guide/tpu#train_a_model_using_keras_high_level_apis)というTFのドキュメントに`experimental_steps_per_execution`というものが書かれていました。

---

追記：バージョン

kerasのドキュメントにちゃんと書いてあっった

[Model training APIs](https://keras.io/api/models/model_training_apis/)

defaultが1なので増やせば速くなります。

また、TF2.4以降は`steps_per_execution`のみで実行可能になったようです。同様にしてTPUを用いた分散処理の宣言部分もexperimentalが外れて簡単に書くことができるようになっています。

----

結局なんなのかはわからなかったのですが、オーバーヘッドを減らしてパフォーマンスを上げるための引数で、1.5倍近く速くなっててすごい。

[TPUでの学習化を高速化出来る'experimental_steps_per_execution'について](https://qiita.com/T-STAR/items/e2998d4c22c882039ffb)という日本語のQiita記事がありましたが、読んでも何をしているのかがよくわかりませんでした。

[TF 2.3 using experimental_steps_per_execution in model.compile cause drop in model performance](https://stackoverflow.com/questions/64648513/tf-2-3-using-experimental-steps-per-execution-in-model-compile-cause-drop-in-mod)というstackoverflowの質問の回答をみる限り、callbackの更新のスピードを調節できることがわかりました。

要するに、学習率やverboseも含めてnバッチごとにcallbacksが呼ばれて処理を行うものなのでなるほど（？）というところでした。

公式だと50が使われてましたが、バッチサイズの指定なので8の倍数のほうが良いのではと思いました。（実験しないとわからないけど）

## PyTorch

### 動いている例

ネットで調べれば色々なものが引っかかります。

- [Vision Transformer (ViT): Tutorial + Baseline](https://www.kaggle.com/abhinand05/vision-transformer-vit-tutorial-baseline)
  - cassavaコンペのnotebook
  - ViTの解説と言いながら、ちゃんとTPUを使っていた　3ヶ月前
- [PyTorch on TPU with PyTorch Lightning](https://www.kaggle.com/pytorchlightning/pytorch-on-tpu-with-pytorch-lightning)
  - TPUを使ったPyTorch LightningでMNISTを訓練させるやつ
  - PyTorch Lightningの開発者が書いた
  - これはなぜか上手く行く

### 動かない例

- [tpu-lightning-1](https://t.co/MGQZmIb7Ak?amp=1)
  - だめでした。
  - commitしても一生終わらないのでOOMっぽいってことを教えてもらった

### そもそも動かない理由

versionっぽいです。Kaggleのコードでも半年前のを動かそうとしたらエラーになってしまうからtorch_xlaのインストールあたりでしっかりversion合わせないと動かない感じがしました。

ここはまだまだ課題になりそうです。

### 動かすために必要なこと

paoさんが共有してくれました。概要は掴んだ気がするので自分なりにまとめました。

#### dataset

[DistributedSampler](https://pytorch.org/cppdocs/api/classtorch_1_1data_1_1samplers_1_1_distributed_random_sampler.html)が必要になります。TPUのコアごとにデータを分散させるイメージです。

```python
import torch_xla.core.xla_model as xm

def train_dataloader(self):
    dataset = MNIST(
        os.getcwd(),
        train=True,
        download=True,
        transform=transforms.ToTensor()
    )

    # required for TPU support
    sampler = None
    if use_tpu:
        sampler = torch.utils.data.distributed.DistributedSampler(
            dataset,
            num_replicas=xm.xrt_world_size(),
            rank=xm.get_ordinal(),
            shuffle=True
        )

    loader = DataLoader(
        dataset,
        sampler=sampler,
        batch_size=32
    )

    return loader
```

#### 訓練

雰囲気はMultiProcessingです。上で紹介したViTのコードから引っ張ってきました。

```python
# Start training processes
def _mp_fn(rank, flags):
    torch.set_default_tensor_type("torch.FloatTensor")
    a = _run()


# _run()
FLAGS = {}
xmp.spawn(_mp_fn, args=(FLAGS,), nprocs=8, start_method="fork")
```

なぜかはよくわからないそうですが、学習率にコア数を掛ける必要があるらしいです。

```python
lr = LR * xm.xrt_world_size()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)
```

また、deviceは訓練させる関数内で定義しないといけないそうです。（コアごとに宣言するそう）

上の例だと`_run`関数内で定義してあげる必要があります。

```python
def _run():
	device = xm.xla_device()
```



### その他

:D社のshimacosさんの資料が参考になりまし。（勉強会で教えてくれた）

PyTorchのversionはDocker使うと良いと書かれてました。ほかのところも丁寧に書かれてるので日本語リソースとしては最高です。（でも2年前なので注意が必要）

<script async class="speakerdeck-embed" data-id="202de55c75e44cdb8beca6f7012aa650" data-ratio="1.77777777777778" src="//speakerdeck.com/assets/embed.js"></script>

- [にのぴらさんの勉強会メモ](https://github.com/ninopira/study_tpu/issues/3)

  - GitHub issueは見やすいですね
  - 動かしたときのメモが書いてあるのでざっと目を通しておくと良さそう
  - PyTorchチャレンジに向けた情報やソースも参考になりそう

  



第2回は来月頃で、それぞれ目標を立てたのですが

- 生PyTorchで実装
- RANZCRの振り返り

などが出ていました。

自分は上2つもやりたいのですが、JAXが気になってるので余力があればやってみようと思います。


かえるるるさんとほかの参加者の方々に感謝！:pray:

