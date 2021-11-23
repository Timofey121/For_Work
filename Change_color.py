import tkinter
from PIL import Image

master = tkinter.Tk()
canvas1 = tkinter.Canvas(master, width=500, height=500)
canvas1.pack()

entry1 = tkinter.Entry(master)
canvas1.create_window(350, 50, window=entry1)
f = tkinter.Label(master, text="Введите 1 изображение")
canvas1.create_window(150, 50, window=f)

entry2 = tkinter.Entry(master)
canvas1.create_window(350, 100, window=entry2)
c = tkinter.Label(master, text="Введите 2 изображение")
canvas1.create_window(150, 100, window=c)

entry3 = tkinter.Entry(master)
canvas1.create_window(350, 150, window=entry3)
d = tkinter.Label(master, text="От какого цвета начать заменять")
canvas1.create_window(150, 150, window=d)

entry4 = tkinter.Entry(master)
canvas1.create_window(350, 200, window=entry4)
t = tkinter.Label(master, text="Конец диапозона")
canvas1.create_window(150, 200, window=t)


def e():
    im1 = Image.open(str(entry1.get()))
    pixels = im1.load()
    x, y = im1.size
    im2 = Image.open(str(entry2.get()))
    pixels1 = im2.load()
    d = str(entry3.get()).split(', ')
    t = str(entry4.get()).split(', ')
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            r1, g1, b1 = pixels1[i, j]
            if (r >= int(''.join(d[0])) and g >= int(''.join(d[1])) and b >= int(''.join(d[2]))) \
                    and (r <= int(''.join(t[0])) and g <= int(''.join(t[1])) and b <= int(''.join(t[2]))):
                pixels[i, j] = r1, g1, b1
            else:
                pixels[i, j] = r, g, b
    im1.save("res3.jpg")


restart = tkinter.Button(master, text="Преобразовать", command=e)
restart.pack()
master.mainloop()
