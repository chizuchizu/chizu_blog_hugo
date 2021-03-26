---
title: "PyCharmでColabをSSH経由で使いたい"
author: "chizuchizu"
date: 2021-03-26
tags: ["colab"]
images: ["/img/main/colab_pycharm.png"]
---


# PyCharmでColabをSSH経由で使いたい


## はじめに

### 対象読者

- Google Colabを使っている（それはそう）
- PyCharmを使っている
  - VSCodeの人は ( https://qiita.com/Koshka/items/f75ffb910d9ee9202baf )をみてください

### 背景

colab（これから小文字表記します）はたった1072円/月でGPU(V100, P100)やTPU(v2)を使うことができる超優良サービスです。

自分は `.ipynb`でコーディングするのに慣れてないのと愛用してるエディタを大切にしたいという思いがあってSSH接続を試みています。

## やり方

### colab上でやること

1ブロック目にこれをコピペして実行してください。

ngrokのトークンを求められるのでそれもコピペしてください。

```python
import random, string, urllib.request, json, getpass

#Generate root password
password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

#Download ngrok
! wget -q -c -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
! unzip -qq -n ngrok-stable-linux-amd64.zip

#Setup sshd
! apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null

#Set root password
! echo root:$password | chpasswd
! mkdir -p /var/run/sshd
! echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
! echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
! echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc
! echo "export LD_LIBRARY_PATH" >> /root/.bashrc

#Run sshd
get_ipython().system_raw('/usr/sbin/sshd -D &')

#Ask token
print("Copy authtoken from https://dashboard.ngrok.com/auth")
authtoken = getpass.getpass()

#Create tunnel
get_ipython().system_raw('./ngrok authtoken $authtoken && ./ngrok tcp 22 &')

#Get public address and print connect command
with urllib.request.urlopen('http://localhost:4040/api/tunnels') as response:
  data = json.loads(response.read().decode())
  (host, port) = data['tunnels'][0]['public_url'][6:].split(':')
  print(f'SSH command: ssh -p{port} root@{host}')

#Print root password
print(f'Root password: {password}')
```

すると、下のように出力されます。`hoge`の部分は実行ごとに変わります。

- `hoge_1` : ポート番号
- `root` :  ユーザー名
- `hoge_2.tcp.ngrok.io` : ホスト名
- `hogehogehoge_3`: パスワード

```bash
SSH command: ssh -phoge_1 root@hoge_2.tcp.ngrok.io
Root password: hogehogehoge_3
```

### PyCharm上でやること

#### SSH接続

[Settings]→[Add Python Interpreter]で先程colab上で出力されたポート番号からホスト名まで入力してNEXTを押してください。

<img src="https://media.discordapp.net/attachments/795149266258493494/824790196079689768/unknown.png?width=705&height=478" style="zoom:80%;" />

すると、パスワードを求められるのでこちらも同様にcolabの出力をコピペしてください。

<img src="https://media.discordapp.net/attachments/795149266258493494/824790840341823518/unknown.png?width=705&height=478" style="zoom:80%;" />

変更点です。

1. インタプリタ
   1. Interpreterを `/usr/bin/python`　→　`/usr/bin/python3`

<img src="https://media.discordapp.net/attachments/795149266258493494/824791151570845756/unknown.png?width=705&height=478" style="zoom:80%;" />

次に[Python Interpreter]→⚙→show all→（さっき追加したSSHのものを）Edit

<img src="https://cdn.discordapp.com/attachments/795149266258493494/824792728411701258/unknown.png" style="zoom:33%;" />  <img src="https://cdn.discordapp.com/attachments/795149266258493494/824795845744394291/unknown.png" style="zoom: 50%;" />

そしたら`Root path`を `/content`に変更してください。また、Mappingsのほうでは`Deployment path`と`Web path`を`/`に設定してください。

<img src="https://cdn.discordapp.com/attachments/795149266258493494/824796423211450408/unknown.png" style="zoom:50%;" /><img src="/home/yuma/.config/Typora/typora-user-images/image-20210326090723986.png" style="zoom:50%;" />

そしたらOK押して、`Deployment configuration`がさっき変更した名前と同じか確認してください。違っていたら、`Deployent configuration`の右を押すと一覧が出てくるので変更したものを選択してください。

#### 確認

右のタブから`Remote Host`を押してください。そこに下のような画面が出てきたらOKです。（contentと1.pyは無いと思うが）

逆に`bin`や`root`というフォルダが見えているようであれば、さきほどの設定で`Root path`を設定し忘れているはずです。今回はcolabにあわせて`/content`を`Root path`にしています。

<img src="https://cdn.discordapp.com/attachments/795149266258493494/824795318142107648/unknown.png" style="zoom:50%;" />

あとは、適当なファイルを作って実行をすると勝手にSSH接続先にファイルを転送して実行してくれます。上の画像は実行後の画像なので、下にCPUのコア数と作業ディレクトリの場所が表示されています。

うまく転送できていた場合、colabからも確認することができます。

![](https://cdn.discordapp.com/attachments/795149266258493494/824795378712182804/unknown.png)

#### 実行ができない場合

ファイルの転送先が間違ってる可能性が高いです。この画像の`Deployment configuration`の設定を確認してください。

<img src="https://cdn.discordapp.com/attachments/795149266258493494/824795845744394291/unknown.png" style="zoom: 50%;" />

あとデバッグする方法として、`FileTransfer `をみるものがあります。接続先と転送先をちゃんとみてください。

<img src="https://cdn.discordapp.com/attachments/795149266258493494/824798640312025148/unknown.png" style="zoom:50%;" />

## 参考にしたもの、メモなど

[How can I to google colaboratory VM? | Stack Overflow](https://stackoverflow.com/questions/48459804/how-can-i-ssh-to-google-colaboratory-vm)

### colabでエラー

こんなやつ。

```python
URLError: <urlopen error [Errno 99] Cannot assign requested address>
```

ngrokは1つしか転送できないことに起因してそうなので、既にngrokを使っているnotebookをshutdownするかアカウントを変えるかなどして対処してください。

### colabでどうにもならないとき

`http://localhost:4040/api/tunnels`に何も存在しないっていうエラーがあると思います。（この前それになった）

[Colab SSH](https://github.com/lamhoangtung/colab_ssh)　というライブラリを使ってとりあえずSSH接続してください。ファイル転送（SFTP）はPyCharmでできるので設定してください。（OpenSSHというところで）

自分は `~/.ssh/config`を設定したのですが、これをせずにできるかは未検証です。

実行はTerminalでSSH接続してシェル叩けばどうにかなると思います。
