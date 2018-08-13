from mutator import Mutator

#sample_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1]
sample_data = 'abcdefghijklmnopqrstuvwxyz'

m1 = Mutator(sample_data)
m1.randomize_n_bytes(5)
print(m1.data)

m1 = Mutator(sample_data)
m1. remove_n_bytes(8)
print(m1.data)

m1 = Mutator(sample_data)
m1.remove_n_bytes_at(7, 3)
print(m1.data)

m1 = Mutator(sample_data)
m1.append_n_random_bytes(5)
print(m1.data)

bytes_list = bytearray(b'abc')
m1 = Mutator(sample_data)
m1.append_bytes(bytes_list)
print(m1.data)

m1 = Mutator(sample_data)
m1.insert_bytes(4, bytes_list)
print(m1.data)

print('===================================')
m1 = Mutator(sample_data)
m1.flip_bits()
print(m1.data)