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
