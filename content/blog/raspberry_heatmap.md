---
title: "Raspbery Piでリアルタイム温度検知をしてみる"
author: "chizuchizu"
date: 2020-09-17T15:54:38+09:00
images: ["/img/main/12.jpg"]
draft: false
description: "赤外線センサとseabornを使ってリアルタイム温度検知機構を作りました"
categories: ["Raspberrry Pi", "python"]
tags: ["Raspberry Pi", "python"]
---





## できるもの

Raspberry Piから実行してます。この赤いセンサから温度を測定し、ヒートマップがリアルタイムで表示されます。だいたい1 FPSで動きます。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">リアルタイムで温度検知できた〜〜 <a href="https://t.co/eMuCRSRnsf">pic.twitter.com/eMuCRSRnsf</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1305869050006958081?ref_src=twsrc%5Etfw">September 15, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## Raspberry Piで使えるようにする

自分はAMG8833という赤外線温度センサを買いました。これを買った8月は新型某ロナの影響でネットに全く商品がなくて秋葉原に買い出しに行くことになったのですが、秋葉原でも全然売ってませんでした。唯一売っていた店があって安堵です。

![](/img/main/11.jpg)

これは、そのままだとピンが接続できないので頑張って半田付けする必要があります。

裏で留めておきました。

![](/img/main/12.jpg)

安定のI2C通信です。

## Raspberry Piに接続

Raspberry Pi側にピンを接続します。

- SDA：SDA1
- SCL：SCL1
- 3.3V：3V3
- GND：GND
- INT：なし

![](/img/main/13.jpg)

`sudo i2cdetect -y 1`を実行して、接続されてるか確認します。

人によっては68に出てくることもあると思います。出てこない人は接触を確認するか、Raspberry PiでのI2C通信について調べると対処法がわかると思います。

```bash
pi@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- 69 -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --    
```

## サンプルコーディング

amg8833を扱うためにAdafruit社のライブラリを使用します。

```bash
sudo pip3 install adafruit-circuitpython-amg88xx
```

サンプルプログラムを実行してみます。

```python
import time

import busio
import board

import adafruit_amg88xx

# I2Cバスの初期化
i2c_bus = busio.I2C(board.SCL, board.SDA)

# アドレスを68に指定
sensor = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x68)

time.sleep(.1)

# 8x8の表示
print(sensor.pixels)
```

`sensor.pixels`でそのときそのときのセンサを読み取ってくれます。

## 実行

上のコードを基にopencvのwindowで表示させてみました。matplotlibのグラフのデータは直接opencvに渡すことができないのでpngに吐き出してから再度読み込んでます。

`cap`はWebカメラに関するコードですが、今回は使わないのでコメントアウトしています。応用として透過させることもできるので色々試しがいがあります。

```python
import time
import busio
import board
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import adafruit_amg88xx

i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

time.sleep(.1)

def draw_heatmap(data):
    ax = sns.heatmap(data, annot=True)
    ax.set_ylim(len(data), 0)

    # plt.show()
    plt.savefig("img.png")
    plt.clf()
    return None

# cap = cv2.VideoCapture(-1)
cv2.namedWindow("img")
k = 0

while k != 13:
    print("capture")

    # cap.read()
    # r, img = cap.read()
    draw_heatmap(np.array(sensor.pixels))
    img = cv2.imread("img.png")

    cv2.imshow("img", img)

    k = cv2.waitKey(1)
```

### 応用例1：透過させてみる

まず、`addWeighted`という関数で画像の合成ができます。（重み付き平均で良い感じに合成）

ヒートマップを作成するところは前と変わっていませんが、Webカメラで取得した画像と合成してみました。

`また、cv2.waitKey`が遅かったので`matplotlib`でリアルタイム描画させました。

```python
while True:
    # plotデータの更新

    r, frame = cap.read()
    draw_heatmap(np.array(sensor.pixels))
    img = cv2.imread("/home/pi/Desktop/festival/img.png")
    img = cv2.addWeighted(frame, 1, img, 0.2, 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.pause(1)
```

使ってみるとこんなふうになります。温度を伝えたければ合成はやめたほうがいいと思います。ただノリで人を感知するくらいなら使いみちはありそうです。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">グラフを透過させてみた〜〜 <a href="https://t.co/IjBp2lQBYJ">pic.twitter.com/IjBp2lQBYJ</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1306179362212007938?ref_src=twsrc%5Etfw">September 16, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

### 応用例2：体温測定

手元にある小さなディスプレイに検知した最大の温度を表示させる機構を作ってみました。

描画させない分、軽快に動くようになりました。これなら割と実用性ありそう？

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">リアルタイム体温測定器 <a href="https://t.co/aWBtCRTee4">pic.twitter.com/aWBtCRTee4</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1306171806517137408?ref_src=twsrc%5Etfw">September 16, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>



```python
import time
import busio
import board
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import adafruit_amg88xx

i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

time.sleep(.1)

print(sensor.pixels)


def draw_heatmap(data):
    ax = sns.heatmap(data, annot=True)
    ax.set_ylim(len(data), 0)

    # plt.show()
    plt.savefig("/home/pi/Desktop/festival/img.png")
    plt.clf()
    return None

cap = cv2.VideoCapture(-1)
cv2.namedWindow("img")
k = 0

while k != 13:
    print("capture")

    # cap.read()
    r, img = cap.read()
    draw_heatmap(np.array(sensor.pixels))
    img = cv2.imread("/home/pi/Desktop/festival/img.png")

    cv2.imshow("img", img)

    k = cv2.waitKey(1)
```

## 思ったこと

### `cv2.waitKey`が遅い

C++で実装されてるOpenCVでも言われてます。特にRaspberry Piという小さなハードウェアで動かすときは代替手段が必要っぽいです。（matplotlibのpause、Tkinterなど）

- [debunking the waitKeyは遅いよね](https://qiita.com/tomoaki_teshima/items/8f20e8c65e3568f6060f)
- [cv::waitKey()の処理時間を計測してみた](http://13mzawa2.hateblo.jp/entry/2015/12/28/180021)

### SSH経由でリアルタイムの描画ができない

何でそんなに無理にやろうとするかというと、モニタにHDMIを繋げるのが億劫だからという理由だけなのですがGUI描画ができたらいいな〜とか思ってます。

追記：VNCでできました

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">VNCで接続できたわ　これで人生easy mode <a href="https://t.co/GDETBnqLmq">pic.twitter.com/GDETBnqLmq</a></p>&mdash; チズチズ (@chizu_potato) <a href="https://twitter.com/chizu_potato/status/1306508657295724544?ref_src=twsrc%5Etfw">September 17, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>