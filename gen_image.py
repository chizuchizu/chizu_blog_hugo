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

    """
    -----------------------------
    """

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
