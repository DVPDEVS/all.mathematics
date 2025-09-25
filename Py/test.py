from allmath import Types
from pympler.asizeof import asizeof #! pip install pympler
import copy

tested = Types.UInt8192

x = 0xF
# for _ in range(2047):
for _ in range(1647):
	x <<= 4
	x |= 0xF

print(x)

y = copy.copy(x)

print(y)

# print(x.bit_length())

# y = tested(x)

# print(asizeof(y))

# print(repr(y))

# print(str(y))

# try:
#     print(y.bit_length())
# finally: pass

# print(y.chunks[0])

# print(y.chunks[-1])

# print(y + tested(126))

# y += tested(12894723848934723)
# print(y)

# print(y - tested(126))

# y -= tested(12894723848934723)
# print(y)
