import sys

def run_length_encode(input_data):
    encoded = []
    count = 0
    prev = "-1"
    for data in input_data:
        if data == prev:
            count += 1

        else:
            if prev != "-1":
                #Adding 152 to the ASCII values to deal with the integers.
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


file_source = input()
file = open(file_source,'r')
data_for_run_length_encode = []

for line in file:
    for character in line:
        data_for_run_length_encode.append(character)


#Test Run
w = run_length_encode(data_for_run_length_encode)
now = run_length_decode(w)
for x in now:
    sys.stdout.write(x)