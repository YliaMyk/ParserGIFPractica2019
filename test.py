import gif
import math

BLACK        = 0  # Файл для проверки работы gif Создаем анимированную гифку
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
print(reader.color_table)
print(reader.blocks)

def make_gif (name, width, height,
              colors = [], background_color = 0,
              version = gif.Version.GIF89a,
              loop_count = 0, force_animation = False,
              buffer_size = None, comment = None,
              xmp_files = [], icc_files = []):

    # Write test GIF
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