packed = bytearray(b'\x81\xa9pico_data\x00')
p_length = bytearray(len(packed).to_bytes(1, 'big'))


# packed = bytearray(umsgpack.dumps(payload))

# get the length of the packed bytearray and convert that to a
# byte array


# append the length to the packed bytarray
p_length.extend(packed)
# packed = p_length.extend(packed)
packed = bytes(p_length)
print(packed)
# ly = bytearray(len(b).to_bytes(1, 'big'))
# ly.extend(bytearray(b))
# m = bytes(ly)
# print(m)
