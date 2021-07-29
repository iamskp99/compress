u = input()
file = open(u, "rb")

byte = file.read(1)
c = []
while byte:
    q = byte
    int_val = int.from_bytes(q, "big")
    v = ((8-len(bin(int_val)[2:]))*"0")+bin(int_val)[2:]
    c.append(v)
    byte = file.read(1)

# print(sum(ans))
print(int("".join(c),2))
file.close()