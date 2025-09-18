from allmath import Types
from pympler.asizeof import asizeof #! pip install pympler

x = 0xF
for _ in range(2047):
    x <<= 4
    x |= 0xF

print(x)

print(x.bit_length())

y = Types.UInt8192(x)

print(asizeof(y))

print(repr(y))

print(str(y))

print(int(y._to_int()).bit_length())

print(y.chunks[0]) if type(y) not in Types.floattypes64 else print(y.mantissa[0])

print(y.chunks[-1]) if type(y) not in Types.floattypes64 else print(y.mantissa[-1])

