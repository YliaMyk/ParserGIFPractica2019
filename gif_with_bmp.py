import gif
import bmp
import math


def gif_to_bmp(file_name):
    file = open(file_name, 'rb')
    reader = gif.Reader()
    reader.feed(file.read())
    if reader.has_screen_descriptor():
        k = 0
        width = reader.width
        height = reader.height
        for block in reader.blocks:
            if isinstance(block, gif.Image):
                pixels = block.get_pixels()
                if len(pixels) >= width * height:
                    c = bmp.Bmp(height, width)
                    for i in range(height):
                        for j in range(width):  # Заполняем ее цветами
                            color_number = pixels[i * width + j]
                            c.set_pixel(i, j, reader.color_table[color_number])
                    c.write_to_file('test' + str(k) + '.bmp')
                    k += 1
                    print(k)


def bmp_to_gif(list_of_files):
    if len(list_of_files) == 0:
        print('Список пустой')
        return 0

    s = bmp.Bmp(2, 2)
    s.read_from_file(list_of_files[0])
    width = s.width
    height = s.height
    colors = []
    colors_dict = {}
    background_color = 0
    version = gif.Version.GIF89a
    filename = 'test.gif'

    writer = gif.Writer(open(filename, 'wb'))
    writer.write_header(version)

    # создание палитры
    for file_name in list_of_files:
        f = bmp.Bmp(2, 2)
        f.read_from_file(file_name)
        for pixel in f.graphics:
            if pixel not in colors:
                colors.append(pixel)
    # перенос палитры в словарь для быстрого доступа
    for i, color in enumerate(colors):
        colors_dict[color] = i

    if len(colors) > 0:
        depth = math.ceil(math.log2(len(colors)))
        writer.write_screen_descriptor(width, height, has_color_table=True, depth=depth,
                                       background_color=background_color)
        writer.write_color_table(colors, depth)
    else:
        writer.write_screen_descriptor(width, height, background_color=background_color)
    writer.write_netscape_extension(loop_count=0)

    for file_name in list_of_files:
        writer.write_graphic_control_extension(delay_time=50)
        f = bmp.Bmp(2, 2)
        f.read_from_file(file_name)

        graphics_for_gif = f.graphics.copy()

        for i in range(height):
            for j in range(width):
                graphics_for_gif[(height - i - 1) * width + j] = f.graphics[width * i + j]

        writer.write_image(width, height, depth, [colors_dict[elem] for elem in graphics_for_gif])
    writer.write_trailer()


def main():  # Тестирую работоспособность
    gif_to_bmp('Yoda.gif')
    list_of_files = ['test0.bmp', 'test1.bmp', 'test2.bmp']
    bmp_to_gif(list_of_files)
    gif_to_bmp('test.gif')  # На маленьких гифках сложно увидеть цвет. Поэтому я ее режу. На этой это не обязательно.


if __name__ == '__main__':
    main()
