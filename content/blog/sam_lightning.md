---
title: "PyTorch LightningでSAMを動かす"
author: "chizuchizu"
date: 2021-02-26
# images: ["https://raw.githubusercontent.com/Chizuchizu/chizu_blog_hugo/master/static/img/main/booking.jpg"]
draft: true
---

# SAMのヤバさ

- [SoTAを総なめ！衝撃のオプティマイザー「SAM」爆誕&解説！](https://qiita.com/omiita/items/f24e4f06ae89115d248e)

> ICLR2021に衝撃的な手法が登場しました。その名も**Sharpness-Aware Minimization、通称SAM**です。どれくらい衝撃かというと、画像分類タスクにおいて、**SAMがImageNet(88.61%)/CIFAR-10(99.70%)/CIFAR-100(96.08%)などを含む9つものデータセットでSoTAを更新**したくらいです(カッコ内はSAMによる精度)。話題の[Vision Transformer(ViT)](https://qiita.com/omiita/items/0049ade809c4817670d7)のImageNetの結果(88.55%)を早速超しました(SoTA更新早すぎます)。

簡単に要約すると、損失が最小かつ平坦なパラメータを探しに行くようなoptimizerです。そうすることで汎用性が高まります。

とにかく強いです。

公式実装は下にあります。

https://github.com/davda54/sam

見ればわかりますが、optimizerを2回呼び出す必要があるので計算量は少し増えてしまいます。（自分環境だと元と比較して約1.2倍、時間がかかる）

# PyTorch Lightningで動かすときの問題

そもそもPyTorch Lightningはいちいち `backward()`や`step()`とかを書くのが嫌で、kerasっぽい学習をしたいけどPyTorchの拡張性も使いたいっていう良い所どりしたい人が使うもの（偏見強め）なので、新しい手法だと問題が生じることが多々有ります。

今回のSAMはまさにそうで、`first_step()`と`second_step()`を呼び出す必要がありますが、PyTorch Lightningではもちろん1回しか呼ぶことができません。



結局良い書き方が分からず、Twitterで呼びかけた所、有識者が現れました。

https://twitter.com/kuto_bopro/status/1363406456469422083

# solution

改良したSAMのコードとrunnerのコードを貼っておきます。ほとんどは先程のツイートのリプライに貼ってあるコードをコピペしたところです。（少し修正はしてあります）

```python
import torch

"""
https://github.com/kuto5046/kaggle-rainforest/blob/main/src/sam.py#L16
"""


class SAM(torch.optim.Optimizer):
    def __init__(self, params, base_optimizer, rho=0.05, **kwargs):
        assert rho >= 0.0, f"Invalid rho, should be non-negative: {rho}"

        defaults = dict(rho=rho, **kwargs)
        super(SAM, self).__init__(params, defaults)

        self.base_optimizer = base_optimizer(self.param_groups, **kwargs)
        self.param_groups = self.base_optimizer.param_groups

    @torch.no_grad()
    def first_step(self, closure=None, zero_grad=False):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                try:
                    loss = closure()
                except:
                    pass
        grad_norm = self._grad_norm()
        for group in self.param_groups:
            scale = group["rho"] / (grad_norm + 1e-12)

            for p in group["params"]:
                if p.grad is None: continue
                e_w = p.grad * scale.to(p)
                p.add_(e_w)  # climb to the local maximum "w + e(w)"
                self.state[p]["e_w"] = e_w

        if zero_grad: self.zero_grad()
        return loss

    @torch.no_grad()
    def second_step(self, closure=None, zero_grad=False):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                try:
                    loss = closure()
                except:
                    pass
        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None: continue
                p.sub_(self.state[p]["e_w"])  # get back to "w" from "w + e(w)"

        self.base_optimizer.step()  # do the actual "sharpness-aware" update

        if zero_grad: self.zero_grad()
        return loss

    def step(self, closure=None):
        raise NotImplementedError(
            "SAM doesn't work like the other optimizers, you should first call `first_step` and the `second_step`; see the documentation for more info.")

    def _grad_norm(self):
        shared_device = self.param_groups[0]["params"][
            0].device  # put everything on the same device, in case of model parallelism
        norm = torch.norm(
            torch.stack([
                p.grad.norm(p=2).to(shared_device)
                for group in self.param_groups for p in group["params"]
                if p.grad is not None
            ]),
            p=2
        )

        return norm

```



```python
class SAMRunner(BASERunner):
    def __init__(self, cfg):
        super().__init__(cfg)
        
    def optimizer_step(self, epoch, batch_idx, optimizer, optimizer_idx, optimizer_closure, on_tpu, using_native_amp,
                       using_lbfgs):
        optimizer.first_step(closure=optimizer_closure, zero_grad=True)
        optimizer.second_step(closure=optimizer_closure, zero_grad=True)

```



Runnerは元々定義していた、SAM以外で動くRunnerのクラスを継承してください。PyTorch Lightningの `optimizer_step`のところでoptimizerの調整が可能らしいです。



また、SAMのオリジナルのコードのほうでは、そのまま動かしただけだとバグが発生してしまったので`closure`あたりのコードを修正しました。closureを2回呼び出すと怒られるのでtry構文でゴリ押しました。

```python
loss = None
if closure is not None:
    with torch.enable_grad():
        try:
            loss = closure()
        except:
            pass
```



## うまくいかなかったこと

- step関数に`first_step`と`second_step`の両方を埋め込む

  Adam optimizerのコードを読んでデバッグして奮闘したがうまくいかなかった

  
