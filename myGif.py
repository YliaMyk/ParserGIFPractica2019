import struct


def end_of_subblock (data, offset):
    n_required = 0
    n_available = len (data) - offset
    subblocks = []
    while True:
        if n_available < n_required + 1:
            return (None, 0)
        subblock_size = data[offset + n_required]
        n_required += 1
        if subblock_size == 0:
            return (subblocks, n_required)
        subblocks.append ((offset + n_required, subblock_size))
        n_required += subblock_size
        if n_available < n_required:
            return (None, 0)


class Gif:
    def __init__(self):
        self.buffer = b''
        self.version = b''
        self.width = 0
        self.height = 0
        self.original_depth = 0
        self.color_table_sorted = False
        self.background_color = 0
        self.pixel_aspect_ratio = 0
        self.color_table = []
        self.blocks = []

    def read_from_file(self, file_name):
        with open(file_name, 'rb') as gif_byte:
            self.gif_arr = gif_byte.read()

        self.version = self.gif_arr[:6]
        self.width = struct.unpack('H', self.gif_arr[6:8])[0]
        self.height = struct.unpack('H', self.gif_arr[8:10])[0]
        for_flags = self.gif_arr[10]
        self.ct = (for_flags >> 7) & 1  #наличие палитры глоабльных цветов
        self.color = (for_flags >> 4) & 7
        self.sf = (for_flags >> 3) & 1
        self.size_color = for_flags & 7
        self.sreen_coolor = self.gif_arr[11]
        self.r = self.gif_arr[12]
        print(self.ct, self.color, self.sf, self.size_color, self.sreen_coolor, self.r)

        array_shift = 13
        if self.ct:
            n = 2 ** (self.size_color + 1)
            self.global_color_table = [0 * i for i in range(n)]
            #print(len(self.global_color_table))
            for i in range(n):
                offset = 13 + i * 3
                (red, green, blue) = struct.unpack('BBB', self.gif_arr[offset: offset + 3])
                self.global_color_table[i] = (red, green, blue)
            #print(self.global_color_table)
            array_shift = 13 + n * 3
        #print(array_shift)

        while True:
            block_type = self.gif_arr[array_shift]

            if block_type == 0x21: #EXTENSION
                start_of_subblock = array_shift + 2
                print(start_of_subblock, self.gif_arr[start_of_subblock])
                while self.gif_arr[start_of_subblock] != 0:
                    start_of_subblock += self.gif_arr[start_of_subblock] + 1
                    #print(start_of_subblock, self.gif_arr[start_of_subblock])
                array_shift = start_of_subblock + 1
            elif block_type == 0x2c: #IMAGE
                width = struct.unpack('H', self.gif_arr[array_shift + 5:array_shift + 7])[0]
                height = struct.unpack('H', self.gif_arr[array_shift + 7:array_shift + 9])[0]
                print('imag', width, height) # проверка что размер картинки совпадет с размером гифки
                for_flags = self.gif_arr[array_shift + 9]
                ct = (for_flags >> 7) & 1  # наличие палитры глоабльных цветов
                if ct != 0:
                    print('GIF c локальной палитрой не поддерживается')
                    break
                mc = self.gif_arr[array_shift + 10]
                size_of_block = self.gif_arr[array_shift + 11]

                start_of_subblock = array_shift + 2

                print(start_of_subblock, self.gif_arr[start_of_subblock])
                while self.gif_arr[start_of_subblock] != 0:
                    start_of_subblock += self.gif_arr[start_of_subblock] + 1
                print(start_of_subblock)

                break


            elif block_type == 0x3b: #TRAILER
                print(self.t)
        print("\x2c")


def main():
    s = Gif()
    s.read_from_file('Yoda.gif')


if __name__ == "__main__":
    main()