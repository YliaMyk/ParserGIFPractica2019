import struct
import bmp

class LZWDecoder:
    def __init__ (self, min_code_size = 3, max_code_size = 12):
        self.min_code_size = min_code_size
        self.max_code_size = max_code_size

        # Codes and values to output
        self.codes = []
        self.values = []
        self.n_used = 0

        # Code table
        self.clear_code = 2 ** (min_code_size - 1)
        self.eoi_code = self.clear_code + 1
        self.code_table = []
        for i in range (2 ** (min_code_size - 1)):
            self.code_table.append ((i,))
        self.code_table.append (self.clear_code)
        self.code_table.append (self.eoi_code)

        # Code currently being decoded
        self.code = 0                       # Current bits of code
        self.code_bits = 0                  # Current number of bits
        self.code_size = self.min_code_size # Required number of bits
        self.last_code = self.clear_code    # Previous code processed

    def feed (self, data, offset = 0, length = -1):
        if length < 0:
            length = len (data) - offset
        for i in range (offset, offset + length):
            d = data[i]
            self.n_used += 1
            n_available = 8
            while n_available > 0:
                # Number of bits to get
                n_bits = min (self.code_size - self.code_bits, n_available)

                # Extract bits from octet
                new_bits = d & ((1 << n_bits) - 1)
                d >>= n_bits
                n_available -= n_bits

                # Add new bits to the top of the code
                self.code = new_bits << self.code_bits | self.code
                self.code_bits += n_bits

                # Keep going until we get a full code word
                if self.code_bits < self.code_size:
                    continue
                code = self.code
                self.code = 0
                self.code_bits = 0
                self.codes.append (code)

                # Stop on end of information code
                if code == self.eoi_code:
                    return

                # Reset code table on clear
                if code == self.clear_code:
                    self.code_size = self.min_code_size
                    self.code_table = self.code_table[:self.eoi_code + 1]
                    self.last_code = code
                    continue

                if code < len (self.code_table):
                    for v in self.code_table[code]:
                        self.values.append (v)
                    if self.last_code != self.clear_code and len (self.code_table) < 2 ** self.max_code_size - 1:
                        self.code_table.append (self.code_table[self.last_code] + (self.code_table[code][0],))
                        assert (len (self.code_table) < 2 ** self.max_code_size)
                        if len (self.code_table) == 2 ** self.code_size and self.code_size < self.max_code_size:
                            self.code_size += 1
                    self.last_code = code
                elif code == len (self.code_table):
                    if len (self.code_table) < 2 ** self.max_code_size - 1:
                        self.code_table.append (self.code_table[self.last_code] + (self.code_table[self.last_code][0],))
                        assert (len (self.code_table) < 2 ** self.max_code_size)
                        if len (self.code_table) == 2 ** self.code_size and self.code_size < self.max_code_size:
                            self.code_size += 1
                    for v in self.code_table[-1]:
                        self.values.append (v)
                    self.last_code = code
                else:
                    print ('Ignoring unexpected code %d %d' % (code, i))

    def is_complete (self):
        return len (self.codes) > 0 and self.codes[-1] == self.eoi_code


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

        self.version = self.gif_arr[:6] # Версия
        self.width = struct.unpack('H', self.gif_arr[6:8])[0]
        self.height = struct.unpack('H', self.gif_arr[8:10])[0]
        for_flags = self.gif_arr[10]
        self.ct = (for_flags >> 7) & 1
        self.color = (for_flags >> 4) & 7
        self.sf = (for_flags >> 3) & 1
        self.size_color = for_flags & 7
        self.sreen_coolor = self.gif_arr[11]
        self.r = self.gif_arr[12]
        # print(self.ct, self.color, self.sf, self.size_color, self.sreen_coolor, self.r)
        array_shift = 13
        if self.ct:
            n = 2 ** (self.size_color + 1)
            self.global_color_table = [0 * i for i in range(n)]
            #print(len(self.global_color_table))
            for i in range(n):
                offset = 13 + i * 3
                (red, green, blue) = struct.unpack('BBB', self.gif_arr[offset: offset + 3])
                self.global_color_table[i] = (blue, green, red)
            #print(self.global_color_table)
            array_shift = 13 + n * 3
        #print(array_shift)

        num_of_img = 0

        while True:
            block_type = self.gif_arr[array_shift]

            if block_type == 0x21: #EXTENSION
                start_of_subblock = array_shift + 2
                #print(start_of_subblock, self.gif_arr[start_of_subblock])
                while self.gif_arr[start_of_subblock] != 0:
                    start_of_subblock += self.gif_arr[start_of_subblock] + 1
                    #print(start_of_subblock, self.gif_arr[start_of_subblock])
                array_shift = start_of_subblock + 1
            elif block_type == 0x2c: #IMAGE
                width = struct.unpack('H', self.gif_arr[array_shift + 5:array_shift + 7])[0]
                height = struct.unpack('H', self.gif_arr[array_shift + 7:array_shift + 9])[0]
                #print('imag', width, height)
                for_flags = self.gif_arr[array_shift + 9]
                ct = (for_flags >> 7) & 1
                if ct != 0:
                    local_pallete = []
                    colors = 1 << ((for_flags & 7) + 1)
                    # print('local_pallete ', for_flags & 7, colors)
                    for i in range(colors):
                        (red, green, blue) = struct.unpack('BBB', self.gif_arr[array_shift+10 + 3 * i : array_shift + 10 + 3 * i + 3])
                        local_pallete.append((blue, green, red))
                    # print(len(local_pallete))
                    array_shift += 3 * colors

                mc = self.gif_arr[array_shift + 10] # начальный размер LZV кода
                size_of_block = self.gif_arr[array_shift + 11]
                #print(mc)
                #start_of_subblock = array_shift + 2
                array_shift += 12
                decoder = LZWDecoder(mc + 1)

                while size_of_block > 0:
                    #print (array_shift, size_of_block)
                    decoder.feed(self.gif_arr, array_shift, size_of_block)
                    array_shift += size_of_block
                    size_of_block = self.gif_arr[array_shift]
                    array_shift += 1


                _bmp = bmp.Bmp(height,width)

                for i in range(height):
                    for j in range(width):
                        #print(i, j,(height - i - 1) * width + j,  width * i + j)
                        _bmp.graphics[(height - i - 1) * width + j] = self.global_color_table[decoder.values[width * i + j]]


                _bmp.write_to_file("test1_%d.bmp" % num_of_img) # выводим bmp
                num_of_img += 1


            elif block_type == 0x3b: #TRAILER
                break

def main():
    s = Gif()
    s.read_from_file('Yoda.gif')


if __name__ == "__main__":
    main()