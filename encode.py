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


def encode():
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

    return