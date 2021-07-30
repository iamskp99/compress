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
                # This means that frequency will be treated as normal int character and
                # the integer will have different characters which have higher ASCII
                # value.This will help us to deal with confusion with integer as a character and
                # integer as frequency.
                if (prev >= '0') and (prev <= '9'):
                    prev = chr(152+ord(prev))

                if count == 1:
                    encoded.append(prev)

                else:
                    for x in str(count):
                        encoded.append(x)

                    encoded.append(prev)

            prev = data
            count = 1

    if count == 1:
        encoded.append(prev)

    else:
        for x in str(count):
            encoded.append(x)

        encoded.append(prev)

    return encoded


def run_length_decode(input_data):
    decoded = []
    i = 0
    while i < len(input_data):
        data = input_data[i]
        if (data >= '0') and (data <= '9'):
            val = []
            while i < len(input_data):
                x = input_data[i]
                if (x >= '0') and (x <= '9'):
                    val.append(x)
                    i = i+1

                else:
                    break

            counter = int("".join(val))
            original_data = input_data[i]
            if ord(original_data) >= 200:
                original_data = chr(ord(original_data)-152)

            while counter > 0:
                decoded.append(original_data)
                counter -= 1

        else:
            if ord(data) >= 200:
                decoded.append(chr(ord(data)-152))

            else:
                decoded.append(data)

        i = i+1

    return decoded


def huffman_encode(heap):
    # This will generate all the huffman codes of all the characters.
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
    # This function adds extra zeroes at the end of encoded data
    # to make it multiple of 8. Also,we add head which is the count
    # of zeroes added at the end.
    needed = 8-(len(data)%8)
    head = ("0"*len(bin(needed)[2:]))+bin(needed)[2:]
    data = data+("0"*needed)
    data = head+data
    return data


def to_huffman_encoded(encoded_data,encode_map):
    # Huffman encoded string is generated.
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


def encode_the_map(length,hash_map):
    # This function encodes the hash map.
    val = bin(length)[2:]
    val = ((8-(len(val)%8))*"0")+val
    result = [val]
    for data in hash_map:
        code = data
        ele = hash_map[data]
        zeroes_to_be_added = 8-(len(code)%8)
        new_code = ("0"*zeroes_to_be_added)+code
        length_bytes_to_be_read = len(new_code)//8
        character_data = ord(ele)
        new_code_length_bytes_to_be_read = ((8-len(bin(length_bytes_to_be_read)[2:]))*"0")+bin(length_bytes_to_be_read)[2:]
        new_character_data = ((8-len(bin(character_data)[2:]))*"0")+bin(character_data)[2:]
        new_zeroes_to_be_added = ((8-len(bin(zeroes_to_be_added)[2:]))*"0")+bin(zeroes_to_be_added)[2:]
        result.append(new_zeroes_to_be_added)
        result.append(new_code_length_bytes_to_be_read)
        result.append(new_code)
        result.append(new_character_data)

    return "".join(result)


def encode():
    # The text files are encoded in this format :
    # [zeroes added to the last][length of the table]
    # Now, the data is stored in this format
    # [zeroes before the code][Length of the bytes to read][Actual huffman code][Actual ASCII code]
    # Zeroes before the code is the amount of zeroes added before actual huffman code
    # This is all stored in binary format

    print("Enter the address of your encode.txt file : ")
    file_source = input()
    print("")
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
    print("")
    output = open(output_file, 'wb')
    huffman_encoded = to_huffman_encoded(encoded_data,encode_map)
    partially_encoded = add_extra(huffman_encoded)
    map_to_be_added = encode_the_map(len(huffman_codes),hash_map)
    fully_encoded = map_to_be_added+partially_encoded
    b_array = get_bytearray(fully_encoded)
    output.write(b_array)
    return


def make_hash_map(file_address):
    # This function will decode hash map
    file = open(file_address, "rb")
    flag = 0
    num = 1  # Garbage value
    i = 0
    hash_map = {}
    byte = file.read(1)
    while i < num and byte:
        if flag == 0:
            flag = 1
            q = byte
            int_val = int.from_bytes(q, "big")
            v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
            num = int(v,2)
            byte = file.read(1)

        else:
            q = byte
            int_val = int.from_bytes(q, "big")
            v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
            zeroes_before = int(v, 2)
            byte = file.read(1)
            q = byte
            int_val = int.from_bytes(q, "big")
            v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
            length_of_bytes = int(v,2)
            byte = file.read(1)
            arr = []
            cnt = 0
            while cnt < length_of_bytes and byte:
                q = byte
                int_val = int.from_bytes(q, "big")
                v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
                arr.append(v)
                cnt += 1
                byte = file.read(1)

            extracted_code = "".join(arr)
            code = extracted_code[zeroes_before:]
            q = byte
            int_val = int.from_bytes(q, "big")
            v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
            ascii = int(v, 2)
            hash_map[code] = chr(ascii)
            byte = file.read(1)
            i = i+1

    file.close()
    return hash_map


def file_read(file_address):
    file = open(file_address, "rb")
    flag = 0
    num = 1  # Garbage value
    i = 0
    ans = []
    byte = file.read(1)
    while i < num and byte:
        if flag == 0:
            flag = 1
            q = byte
            int_val = int.from_bytes(q, "big")
            v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
            num = int(v, 2)
            byte = file.read(1)

        else:
            byte = file.read(1)
            q = byte
            int_val = int.from_bytes(q, "big")
            v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
            length_of_bytes = int(v, 2)
            byte = file.read(1)
            cnt = 0
            while cnt < length_of_bytes and byte:
                cnt += 1
                byte = file.read(1)

            byte = file.read(1)
            i = i + 1

    byte = file.read(1)
    q = byte
    int_val = int.from_bytes(q, "big")
    v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
    head = int(v, 2)
    byte = file.read(1)
    while byte:
        q = byte
        int_val = int.from_bytes(q, "big")
        v = ((8 - len(bin(int_val)[2:])) * "0") + bin(int_val)[2:]
        byte = file.read(1)
        ans.append(v)

    coded_text = "".join(ans)
    coded_text = coded_text[0:len(coded_text)-head]
    file.close()
    return coded_text


def get_text_array(code,hash_map):
    ans = []
    s = ""
    for i in code:
        s = s + i
        if s in hash_map:
            ans.append(hash_map[s])
            s = ""

    return ans


def decode():
    print("Enter the address of your decode.txt file : ")
    file_source = input()
    print("")
    decode_file = open(file_source, 'a')
    print("Enter the address of your output.bin file : ")
    u = input()
    print("")
    hash_map = make_hash_map(u)
    code = file_read(u)
    result = get_text_array(code,hash_map)
    ans = run_length_decode(result)
    for i in ans:
        decode_file.write(i)

    return


print("Enter 0 if you want to compress a file or 1 if you want to de-compress it :")
choice = int(input())
print("")
if choice == 0:
    encode()

if choice == 1:
    decode()