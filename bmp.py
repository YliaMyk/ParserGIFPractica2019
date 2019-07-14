import struct
# При написание кода использовались эти источники:
# https://en.wikipedia.org/wiki/BMP_file_format
# https://stackoverflow.com/questions/8729459/how-do-i-create-a-bmp-file-with-pure-python
# https://stackoverflow.com/questions/10439104/reading-bmp-files-in-python
# https://github.com/antista/parsing_bmp/blob/master/bmp_picture.py

class Bmp:
    def __init__(self, height, width):  # Прописываем  BITMAPFILEHEADER и BITMAPINFO для создания bmp файла
        self.type = 19778  # BM
        # self.size = 154
        self.size = 54 + height * (width * 3 + (3 * 3 * width) % 4)
        self.reserved = 0
        self.offset = 54
        self.title_size = 40
        self.width = width
        self.height = height
        self.planes = 1
        self.bit_to_pixel = 24
        self.compression = 0
        self.picture_size = 100
        self.r_h = 0
        self.r_v = 0
        self.number_of_colors = 0
        self.important_color = 0
        self.graphics = [(0, 0, 0)] * self.width * self.height

    def read_from_file(self, filename):
        with open(filename, 'rb') as bmp_byte:
            self.bmp_arr = bmp_byte.read()
        if chr(self.bmp_arr[0]) + chr(self.bmp_arr[1]) != 'BM':
            print('Это не BMP файл')
            return 0
        if struct.unpack('I', self.bmp_arr[6:10])[0] != 0:
            print('Зарезервированные байты не равны 0')
            return 0
        if len(self.bmp_arr) != \
                struct.unpack('I', self.bmp_arr[2:6])[0]:
            print('Указанная в заголовке длина файла не равна фактической')
            return 0
        if self.bit_to_pixel != 24:
            print('BMP файлы не с 24 битной кодировкой не поддерживаются')
            return 0
        # self.type -- задан в init, 2 байта (BM)
        self.size = struct.unpack('I', self.bmp_arr[2:6])[0]
        self.reserved = struct.unpack('I', self.bmp_arr[6:10])[0]
        self.offset = struct.unpack('I', self.bmp_arr[10:14])[0]
        self.title_size = struct.unpack('I', self.bmp_arr[14:18])[0]
        self.width = struct.unpack('I', self.bmp_arr[18:22])[0]
        self.height = struct.unpack('I', self.bmp_arr[22:26])[0]
        self.planes = struct.unpack('H', self.bmp_arr[26:28])[0]
        self.bit_to_pixel = struct.unpack('H', self.bmp_arr[28:30])[0]
        self.compression = struct.unpack('I', self.bmp_arr[30:34])[0]
        self.picture_size = struct.unpack('I', self.bmp_arr[34:38])[0]
        self.r_h = struct.unpack('I', self.bmp_arr[38:42])[0]
        self.r_v = struct.unpack('I', self.bmp_arr[42:46])[0]
        self.number_of_colors = struct.unpack('I', self.bmp_arr[46:50])[0]
        self.important_color = struct.unpack('I', self.bmp_arr[50:54])[0]
        self.graphics = [(0, 0, 0)] * self.width * self.height

        index = self.offset

        for x in range(self.height):
            for y in range(self.width):
                c = (self.bmp_arr[index],
                     self.bmp_arr[index + 1],
                     self.bmp_arr[index + 2])
                index += 3
                self.graphics[x * self.width + y] = c
            index += (3 * 3 * self.width) % 4

    def set_pixel(self, x, y, color):
        self.graphics[self.width * (self.height - x - 1) + y] = (color[2], color[1], color[0])  # Использую эту формулу

    def write_to_file(self, file):
        with open(file, 'wb') as f:
            f.write(struct.pack('H', self.type))  # 0-2 байта
            f.write(struct.pack('I', self.size))  # 2-6 байта
            f.write(struct.pack('I', self.reserved))  # 6-10 байта
            f.write(struct.pack('I', self.offset))  # 10-14 байта
            f.write(struct.pack('I', self.title_size))  # 14-18 байта
            f.write(struct.pack('I', self.width))  # 18-22 байта
            f.write(struct.pack('I', self.height))  # 22-26 байта
            f.write(struct.pack('H', self.planes))  # 26-28 байта
            f.write(struct.pack('H', self.bit_to_pixel))  # 28-30 байта
            f.write(struct.pack('I', self.compression))  # 30-34 байта
            f.write(struct.pack('I', self.picture_size))  # 34-38 байта
            f.write(struct.pack('I', self.r_h))  # 38-42 байта
            f.write(struct.pack('I', self.r_v))  # 42-46 байта
            f.write(struct.pack('I', self.number_of_colors))  # 46-50 байта
            f.write(struct.pack('I', self.important_color))  # 50-54 байта

            k = 0
            for i in range(self.height):
                for j in range(self.width):
                    px = self.graphics[k]
                    k += 1
                    f.write(struct.pack('<BBB', *px))
                for j in range((4 - self.width * 3 % 4) % 4):  # Добавляем нули для 4х байтового выравнивания
                    f.write(struct.pack('B', 0))


def main():
    print('Тесты находятся в example.py')


if __name__ == "__main__":
    main()
