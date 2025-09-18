from allmath import UInt8192
from pympler.asizeof import asizeof #! pip install pympler

x = UInt8192(123456)

print(asizeof(x))
