import struct


class Bmp:
    def __init__(s, height, width):  # Прописываем  BITMAPFILEHEADER и BITMAPINFO для создания bmp файла
        s._bfType = 19778  # Сигнатура
        s._bfReserved1 = 0
        s._bfReserved2 = 0
        s._bcPlanes = 1
        s._bcSize = 12
        s._bcBitCount = 24
        s._bfOffBits = 26
        s._bcWidth = width
        s._bcHeight = height
        s._bfSize = 26 + s._bcWidth * 3 * s._bcHeight
        s._graphics = [(0, 0, 0)] * s._bcWidth * s._bcHeight

    def read_from_bmp(s, file_name):  # Считываем BITMAPFILEHEADER и BITMAPINFO с готового bmp Файла
        bmp = open(file_name, 'rb')

        s._bfType = bmp.read(2).decode()
        s._bfType = 19778  # Из за того что cтандарты отличачаются, некоторые значения приходится прописывать вручную
        s._bfSize = struct.unpack('I', bmp.read(4))[0]  # Для тестового примера
        s._bfSize = 101
        s._bfReserved1 = struct.unpack('H', bmp.read(2))[0]
        s._bfReserved2 = struct.unpack('H', bmp.read(2))[0]
        s._bfOffBits = struct.unpack('I', bmp.read(4))[0]
        s._bfOffBits = 26

        s._bcSize = struct.unpack('I', bmp.read(4))[0]  # Размер структуры в байтах, указывающий на версию структуры
        s._bcSize = 12
        s._bcWidth = struct.unpack('I', bmp.read(4))[0]  # Ширина растра в пикселях
        s._bcHeight = struct.unpack('I', bmp.read(4))[0]  # Высота растра в пикселях
        s._bcPlanes = struct.unpack('H', bmp.read(2))[0]
        s._bcBitCount = struct.unpack('H', bmp.read(2))[0]  # Количество бит на пиксель
        s._graphics = [(0, 0, 0)] * s._bcWidth * s._bcHeight

        bmp.seek(s._bfOffBits)

        for i in range(s._bcHeight):
            for j in range(s._bcWidth):
                r = struct.unpack('B', bmp.read(1))[0]
                g = struct.unpack('B', bmp.read(1))[0]
                b = struct.unpack('B', bmp.read(1))[0]
                s._graphics[i * s._bcWidth + j] = (r, g, b)
            for j in range((4 - s._bcWidth * 3 % 4) % 4):
                e = struct.unpack('B', bmp.read(1))[0]

    def setPixel(s, x, y,
                 color):  # строчки хранятся в перевернутом состояние, для изменения значение в массиве
        s._graphics[s._bcWidth * (s._bcHeight - x - 1) + y] = (color[2], color[1], color[0])  # Использую эту формулу

    def write(s, file):  # Считываем с файла цветные пиксели и переносим их в наш массив
        with open(file, 'wb') as f:
            f.write(struct.pack('<HLHHL',
                                s._bfType,  # BITMAPFILEHEADER
                                s._bfSize,
                                s._bfReserved1,
                                s._bfReserved2,
                                s._bfOffBits))
            f.write(struct.pack('<LHHHH',  # BITMAPINFO
                                s._bcSize,
                                s._bcWidth,
                                s._bcHeight,
                                s._bcPlanes,
                                s._bcBitCount))
            f.seek(s._bfOffBits)

            k = 0
            for i in range(s._bcHeight):
                for j in range(s._bcWidth):
                    px = s._graphics[k]
                    k += 1
                    f.write(struct.pack('<BBB', *px))
                for j in range((4 - s._bcWidth * 3 % 4) % 4):  # Добавляем нули для 4х байтового выравнивания
                    f.write(struct.pack('B', 0))



    #b = Bmp(1, 1)  # Считываем bmp файла и вносим его значения в структуру
    #b.read_from_bmp('test2.bmp')
    #b.write('cool.bmp')# Выводим структуру в отдельный файл

    # width = 8 # Создаем bmp файл
    # height = 5 # Задаем размер картики
    # c = Bmp(height, width)
    #   for j in range(width): # заполняем ее цветами
    #        if i == j:
    #            c.setPixel(i, j, (0, 0, 150))
    # c.setPixel(4, 3, (0, 150, 0))
    # c.write('test.bmp')
    # b = Gif()
    # b.read_from_gif('Gif.gif')