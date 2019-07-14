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
                            if color_number in block.color_table:
                                cc = block.color_table[color_number]
                            else:
                                cc = reader.color_table[color_number]
                            c.set_pixel(i, j, cc)
                    c.write_to_file('test' + str(k) + '.bmp')
                    k += 1


def bmp_to_gif(list_of_files):
    if len(list_of_files) == 0:
        print('Список пустой')
        return 0

    s = bmp.Bmp(2, 2)
    s.read_from_file(list_of_files[0])
    width = s.width
    height = s.height
    colors = [0] * (s.width * s.height)
    colors_dict = {}
    background_color = 0
    version = gif.Version.GIF89a
    filename = 'test.gif'

    writer = gif.Writer(open(filename, 'wb'))
    writer.write_header(version)

    # создание палитры
    k = 0
    for file_name in list_of_files:
        f = bmp.Bmp(2, 2)
        f.read_from_file(file_name)
        for pixel in f.graphics:
            pixel_from_color = (pixel[2], pixel[1], pixel[0])
            if pixel_from_color not in colors:
                colors[k] = pixel_from_color
                k += 1
    colors = colors[:k]

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
        number_in_colors_for_pixel = [colors_dict[(pixel[2], pixel[1], pixel[0])] for pixel in graphics_for_gif]


        writer.write_image(width, height, depth, number_in_colors_for_pixel)
    writer.write_trailer()


def main():
    print('Тесты находятся в example.py')


if __name__ == '__main__':
    main()
