import sys
import heapq


def run_length_encode(input_data):
    encoded = []
    count = 0
    prev = "-1"
    for data in input_data:
        if data == prev:
            count += 1

        else:
            if prev != "-1":
                # Adding 152 to the ASCII values to deal with the integers.
                if (prev >= '0') and (prev <= '9'):
                    prev = chr(152+ord(prev))

                if count == 1:
                    encoded.append(prev)

                else:
                    encoded.append(str(count))
                    encoded.append(prev)

            prev = data
            count = 1

    if count == 1:
        encoded.append(prev)

    else:
        encoded.append(str(count))
        encoded.append(prev)

    return encoded

def run_length_decode(input_data):
    decoded = []
    i = 0
    while i < len(input_data):
        data = input_data[i]
        if (data >= '0') and (data <= '9'):
            counter = int(data)
            original_data = input_data[i+1]
            if ord(original_data) >= 200:
                original_data = chr(ord(original_data)-152)

            while counter > 0:
                decoded.append(original_data)
                counter -= 1

            i = i+2

        else:
            if ord(data) >= 200:
                decoded.append(chr(ord(data)-152))

            else:
                decoded.append(data)

            i = i+1

    return decoded



def huffman_encode(heap):
    # Make Tree
    while len(heap) > 1:
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)

        for value in low[1:]:
            value[1] = '0' + value[1]

        for value in high[1:]:
            value[1] = '1' + value[1]

        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])

    return heap[0][1:]


def frequency_calculator(input_data):
    # This returns an array containing frequency of the character and character itself and the path from the root (or the huffman code)

    d = {}
    for i in input_data:
        if i in d:
            d[i] += 1

        else:
            d[i] = 1

    array = []
    for i in d:
        array.append([d[i],[i,'']])

    return array


def add_extra(data):
    needed = 8-(len(data)%8)
    data = data+("0"*needed)
    return data


def to_huffman_encoded(encoded_data,encode_map):
    arr = []
    for i in encoded_data:
        arr.append(encode_map[i])

    return "".join(arr)


def get_bytearray(encodedtext):
    bt = bytearray()
    for i in range(0, len(encodedtext), 8):
        byte = encodedtext[i:i + 8]
        bt.append(int(byte, 2))

    return bt


def encode():
    print("Enter the address of your input.txt file : ")
    file_source = input()
    file = open(file_source, 'r')
    data_for_run_length_encode = []

    for line in file:
        for character in line:
            data_for_run_length_encode.append(character)

    encoded_data = run_length_encode(data_for_run_length_encode)
    heap = frequency_calculator(encoded_data)
    heapq.heapify(heap)
    huffman_codes = huffman_encode(heap)
    hash_map = {}
    encode_map = {}
    for x in huffman_codes:
        ele = x[0]
        val = x[1]
        hash_map[val] = ele
        encode_map[ele] = val

    print("Enter the address of your output.bin file : ")
    output_file = input()
    output = open(output_file, 'wb')
    huffman_encoded = to_huffman_encoded(encoded_data,encode_map)
    fully_encoded = add_extra(huffman_encoded)
    print("Fully  encoded  ")
    print(" ")
    print(fully_encoded)
    b_array = get_bytearray(fully_encoded)
    output.write(b_array)


encode()