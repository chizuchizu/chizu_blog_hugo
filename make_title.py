import os
from gen_image import main
from bs4 import BeautifulSoup
import markdown2


# with open('content/blog/test.md') as f:
#     print(f.read())


def get_links_from_md(file_path, markdowner=markdown2.Markdown()):
    with open(file_path) as f:
        md = f.read()
    html = markdowner.convert(md)
    soup = BeautifulSoup(html, 'html.parser')
    # print(html)
    l = [[a.text, a.attrs.get('href')] for a in soup.find_all('p')][0]
    print(l)
    m = str(l[0])
    title = m.split("\n")[0].split('"')[1]

    flag = True
    if m.split("\n")[1][:6] == "images":
        flag = False
    return title, flag


for path in os.listdir("content/blog"):
    if path == "_index.md":
        continue
    file_path = "content/blog/" + path
    title, flag = get_links_from_md(file_path)
    if flag:
        # static/
        img_path = main(title, path[:-3])[7:]

        with open(file_path) as f:
            l = f.readlines()
        add = 'images: ["{}"]\n'.format(img_path) + 'img: ["{}"]'\n.format(img_path)
        l.insert(2, add)
        with open(file_path, mode="w") as f:
            f.writelines(l)
