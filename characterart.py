from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os
import re


def createCharacterArt(img_file, danmaku_file, replies_file):
    fil = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fa5]+', re.UNICODE)
    try:
        img = Image.open(img_file)
        img_size = (int(img.width / 3), int(img.height / 3))
        img = img.resize(img_size)
        text = str()
        try:
            with open(danmaku_file, encoding='utf-8') as file:
                danmaku_list = list()
                danmaku_list = file.readlines()
            for each_danmaku in danmaku_list:
                text += each_danmaku.replace('\n', '')
        except:
            pass
        while (len(text) < (img.size[0] * img.size[1])):
            with open(replies_file, encoding='utf-8') as file:
                replies_list = list()
                replies_list = file.readlines()
            for each_reply in replies_list:
                text = fil.sub(' ', text).replace(' ', '')
                text += each_reply.replace('\n', '')
    except Exception as error:
        print('{}'.format(error))
        return

    img = ImageEnhance.Contrast(img).enhance(2)
    img = ImageEnhance.Color(img).enhance(2)

    text = fil.sub(' ', text).replace(' ', '')
    font_file = r'C:\Windows\Fonts\STXIHEI.TTF'
    font = ImageFont.truetype(font_file)
    font_size = 10

    img_txt = Image.new('RGB', (img.width * font_size, img.height * font_size),
                        (255, 255, 255))

    colors = list()
    count = 0
    txt = str()

    for i in range(img.width):
        for j in range(img.height):
            pixel = img.getpixel((i, j))
            colors.append((pixel[0], pixel[1], pixel[2]))
            txt += text[count]
            count += 1
        txt += '\n'
        colors.append((0, 0, 0))

    dr = ImageDraw.Draw(img_txt)

    x = 0
    y = 0
    for i in range(len(txt)):
        if (txt[i] == '\n'):
            x += font_size
            y = -font_size
        dr.text([x, y], txt[i], colors[i], font=font)
        y += font_size

    img_txt.save('characterArt.png', ecoding='utf-8')


if __name__ == "__main__":
    img_file = 'cover.jpg'
    danmaku_file = 'danmaku.txt'
    replies_file = 'replies.txt'
    os.chdir(r'C:\Users\William\Desktop\bili\videos_data\【香港真相大起底】暴力乱港实录')

    createCharacterArt(img_file, danmaku_file, replies_file)