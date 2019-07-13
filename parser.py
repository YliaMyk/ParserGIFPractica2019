import gif
import bmp
import struct


#def f(obj):  # нужна для отладки кода
#    for k, v in obj.__dict__.items():
#        print(k, v)
#        if hasattr(v, '__dict__'):
#            f(v)
def gif_to_bmp(file_name):
    file = open(file_name, 'rb')
    reader = gif.Reader()
    reader.feed(file.read())
    if reader.has_screen_descriptor():
        #print('Size: %dx%d' % (reader.width, reader.height))
        #print('Colors: %s' % repr(reader.color_table))
        k = 0
        width = reader.width
        height = reader.height
        for block in reader.blocks:
            if isinstance(block, gif.Image):
                pixels = block.get_pixels()
                if len(pixels) >= width*height:

                    c = bmp.Bmp(height, width)
                    for i in range(height):
                        for j in range(width):  #  заполняем ее цветами
                            color_number = pixels[i*width + j]
                            c.setPixel(i, j, reader.color_table[color_number])
                    c.write('test'+ str(k) + '.bmp')
                    k += 1
                    print(k)


def main():  # Тестирую работоспособность
    gif_to_bmp('Yoda.gif')



if __name__ == '__main__':
    main()

