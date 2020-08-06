from bitarray import bitarray
a = bitarray()            # create empty bitarray
a.append(0)
a.extend([1, 1, 0])
a = list(a)
print(a)
