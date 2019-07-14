import gif_with_bmp
import bmp
import gif
import math

# Пример 1: Считываем тестовый файл, созданый в Paint, и записываем получившиеся данные в другой файл

s = bmp.Bmp(2, 2)
s.read_from_file('abc.bmp')
print(vars(s))
s.write_to_file('cba.bmp')

# Пример 2: Создаем bmp

width = 8
height = 5
c = bmp.Bmp(height, width)
for i in range(height):
   for j in range(width):
        if i == j:
            c.set_pixel(i, j, (0, 0, 150))
c.set_pixel(4, 3, (0, 150, 0))
c.write_to_file('artificial.bmp')

# Пример 3: Создаем анимированную гифку

BLACK        = 0
WHITE        = 1
RED          = 2
GREEN        = 3
BLUE         = 4
CYAN         = 5
MAGENTA      = 6
YELLOW       = 7
DARK_GREY    = 8
LIGHT_GREY   = 9
DARK_RED     = 10
DARK_GREEN   = 11
DARK_BLUE    = 12
DARK_CYAN    = 13
DARK_MAGENTA = 14
DARK_YELLOW  = 15
palette16 =  [ (  0,   0,   0), (255, 255, 255), (255,   0,   0), (  0, 255,   0),
               (  0,   0, 255), (  0, 255, 255), (255,   0, 255), (255, 255,   0),
               ( 85,  85,  85), (170, 170, 170), (128,   0,   0), (  0, 128,   0),
               (  0,   0, 128), (  0, 128, 128), (128,   0, 128), (128, 128,   0)]
palette2 = palette16[:19]

file = open ('animation.gif', 'rb')
reader = gif.Reader ()
reader.feed(file.read ())
if reader.has_screen_descriptor ():
    print ('Size: %dx%d' % (reader.width, reader.height))
    print ('Colors: %s' % repr (reader.color_table))
    for block in reader.blocks:
        if isinstance (block, gif.Image):
            ppp = block.get_pixels ()
            print ('Pixels: %s' % repr (ppp))
    if reader.has_unknown_block ():
        print ('Encountered unknown block')
    elif not reader.is_complete ():
        print ('Missing trailer')
else:
    print ('Not a valid GIF file')


def make_gif (name, width, height,
              colors = [], background_color = 0,
              version = gif.Version.GIF89a,
              loop_count = 0, force_animation = False,
              buffer_size = None, comment = None,
              xmp_files = [], icc_files = []):

    filename = '%s.gif' % name
    writer = gif.Writer (open (filename, 'wb'))
    writer.write_header (version)
    if len (colors) > 0:
        depth = math.ceil (math.log2 (len (colors)))
        writer.write_screen_descriptor (width, height, has_color_table = True, depth = depth, background_color = background_color)
        writer.write_color_table (colors, depth)
    else:
        writer.write_screen_descriptor (width, height, background_color = background_color)
    return writer


writer = make_gif ('animation', 4, 4, palette2, loop_count = -1)
writer.write_netscape_extension (loop_count = 0)
writer.write_graphic_control_extension (delay_time = 50)
writer.write_image (4, 4, 1, [ RED, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK ,BLACK, BLACK, BLACK ,BLACK, BLACK, BLACK ,BLACK, BLACK, BLACK])
writer.write_graphic_control_extension (delay_time = 50)
writer.write_image (4, 4, 1, [ BLACK, BLACK, BLACK, RED, BLACK, BLACK, BLACK ,BLACK, BLACK, BLACK ,BLACK, BLACK, BLACK ,BLACK, BLACK, BLACK])
writer.write_graphic_control_extension (delay_time = 50)
writer.write_image (4, 4, 1, [ BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK , BLACK, BLACK, BLACK , BLACK, BLACK, BLACK ,BLACK, BLACK, RED ])
writer.write_graphic_control_extension (delay_time = 50)
writer.write_image (4, 4, 1, [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK ,BLACK, BLACK, BLACK ,BLACK, BLACK, RED ,BLACK, BLACK, BLACK ])
writer.write_trailer ()



