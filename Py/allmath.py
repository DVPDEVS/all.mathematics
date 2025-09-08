from __future__ import annotations # Treat type hints as strings/future types. this gets rid of 60+ errors per class
import numpy as np
from typing import Union

from fontTools.ttLib.tables.otConverters import UInt8

# Custom type for storing 1024 byte unsigned integers
class UInt8192:
	"""This is a fixed-size unsigned 8192-bit integer type. It IMMEDIATELY takes 1KB of ram."""

	MAX = (1 << 1024) -1

#! Avoiding subclassing int for the fine control applicable now :3
#? (Im gonna have to create every magic method manually)
#	def __new__(cls, value)->UInt1024:
#		try:
#			ivalue = int(value)
#		except Exception as e:
#			raise TypeError(f"Cannot convert from {type(value)} to UInt1024") from e
#		if ivalue < 0 or ivalue > cls.MAX:
#			raise ValueError(f"Value is out of range for UInt1024 (0...{cls.MAX})")
#		return super().__new__(cls,value)

	def __init__(self, value: int = 0):
		self.chunks = np.zeros(128, dtype=np.uint64)
		self._from_int(value)

	def _from_int(self, value: int = 0):
		i=0
		while value > 0 and i < 128:
			self.chunks[i] = value & 0xFFFFFFFFFFFFFFFF
			value >>= 64
			i += 1

	def _to_int(self)->int:
		res = 0
		for i in reversed(range(128)):
			res <<= 64
			res |= self.chunks[i]
		return res

	def __repr__(self):
		return f"UInt1024({self._to_int()})"

	def __add__(self, other: UInt8192)->UInt8192:
		res = UInt8192()
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) + int(other.chunks[i]) + carry
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return res

	def __iadd__(self, other: UInt8192)->UInt8192:
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) + int(other.chunks[i]) + carry
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return self

	def __mul__(self, other: UInt8192)->UInt8192:
		res = UInt8192()
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) * int(other.chunks[i]) + carry
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return res

	def __imul__(self, other: UInt8192)->UInt8192:
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) * int(other.chunks[i]) + carry
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return self

	def __sub__(self, other: UInt8192)->UInt8192:
		res = UInt8192()
		for i in range(128):
			total = int(self.chunks[i]) - int(other.chunks[i])
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return res

	def __isub__(self, other: UInt8192)->UInt8192:
		for i in range(128):
			total = int(self.chunks[i]) - int(other.chunks[i])
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return self

	def __truediv__(self, other: UInt8192)->UInt8192: #I am unsure how this will be done with the current methods of doing arithmetic - Smol
		return self

	def __itruediv__(self, other: UInt8192)->UInt8192:
		return self

	def __floordiv__(self, other: UInt8192)->UInt8192:
		res = UInt8192()
		for i in range(128):
			try:
				total = int(self.chunks[i]) // int(other.chunks[i])
			except ZeroDivisionError:
				total = 0
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return res

	def __ifloordiv__(self, other: UInt8192)->UInt8192:
		for i in range(128):
			try:
				total = int(self.chunks[i]) // int(other.chunks[i])
			except ZeroDivisionError:
				total = 0
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return self

	def __mod__(self, other: UInt8192)->UInt8192:
		res = UInt8192()
		for i in range(128):
			try:
				total = int(self.chunks[i]) % int(other.chunks[i])
			except ZeroDivisionError:
				total = 0
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return res

	def __imod__(self, other: UInt8192)->UInt8192:
		for i in range(128):
			try:
				total = int(self.chunks[i]) % int(other.chunks[i])
			except ZeroDivisionError:
				total = 0
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return self

	def __pow__(self, other: UInt8192)->UInt8192:
		return self

	def __ipow__(self, other: UInt8192)->UInt8192:
		return self

	def __neg__(self)->UInt8192:
		return self

	def __pos__(self)->UInt8192:
		return self

	def __abs__(self)->UInt8192:
		for i in range(128):
			total=abs(int(self.chunks[i]))
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return self

	def __and__(self)->UInt8192:
		return self

	def __or__(self)->UInt8192:
		return self

	def __xor__(self)->UInt8192:
		return self

	def __lshift__(self)->UInt8192:
		return self

	def __rshift__(self)->UInt8192:
		return self

	def __iand__(self)->UInt8192:
		return self

	def __ior__(self)->UInt8192:
		return self

	def __ixor__(self)->UInt8192:
		return self

	def __ilshift__(self)->UInt8192:
		return self

	def __irshift__(self)->UInt8192:
		return self

	def __eq__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

	def __ne__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

	def __lt__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

	def __le__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

	def __gt__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

	def __ge__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

	def __del__(self)->UInt8192:
		return self

	def __int__(self)->int:
		return self._to_int()

	def __bool__(self)->bool:
		return True if self._to_int() != 0 else False

	def __str__(self)->str:
		res = ''
		for i in range(128):
			res += str(int(self.chunks[i]))
		return res

	def __bytes__(self)->bytes:
		return self._to_int().to_bytes(128, 'little')

	def __len__(self)->int:
		return len(str(self))*64 if type(self) ==  else 0

	def __getitem__(self)-> Union[np.bool_, np.uint8, np.uint16, np.uint32, np.uint64]:
		...

	def __setitem__(self)->UInt8192:
		return self

	def __contains__(self)->bool:
		return self

	def __copy__(self)->UInt8192:
		return self

	def __sizeof__(self)->int:
		return self

# Custom type for storing 1024 byte floats
class Float8192:
	"""This is a fixed-size signed 8192-bit float type. It IMMEDIATELY takes 1KB of ram."""

	MAX = (1 << 1024) -1

	def __init__(self, value: int = 0):
		self.sign = 1
		self.mantissa = np.zeros(128, dtype=np.uint64)
		self.exponent = np.int16(0)
		self._from_float(value)

	def _from_float(self, value: int = 0):
		i=0
		while value > 0 and i < 128:
			self.mantissa[i] = value & 0xFFFFFFFFFFFFFFFF
			value >>= 64
			i += 1

	def _to_int(self)->int:
		return self

	def __repr__(self):
		return f"Float8192({''})"

	def __add__(self, other: Float8192)->Float8192:
		return res

	def __iadd__(self, other: Float8192)->Float8192:
		return self

	def __mul__(self, other: Float8192)->Float8192:
		return res

	def __imul__(self, other: Float8192)->Float8192:
		return self

	def __sub__(self, other: Float8192)->Float8192:
		return res

	def __isub__(self, other: Float8192)->Float8192:
		return self

	def __truediv__(self, other: Float8192)->Float8192:
		return self

	def __itruediv__(self, other: Float8192)->Float8192:
		return self

	def __floordiv__(self, other: Float8192)->Float8192:\
		return self

	def __ifloordiv__(self, other: Float8192)->Float8192:\
		return self

	def __mod__(self, other: Float8192)->Float8192:
		return self

	def __imod__(self, other: Float8192)->Float8192:
		return self

	def __pow__(self, other: Float8192)->Float8192:
		return self

	def __ipow__(self, other: Float8192)->Float8192:
		return self

	def __neg__(self)->Float8192:
		return self

	def __pos__(self)->Float8192:
		return self

	def __abs__(self)->Float8192:
		return self

	def __and__(self)->Float8192:
		return self

	def __or__(self)->Float8192:
		return self

	def __xor__(self)->Float8192:
		return self

	def __lshift__(self)->Float8192:
		return self

	def __rshift__(self)->Float8192:
		return self

	def __iand__(self)->Float8192:
		return self

	def __ior__(self)->Float8192:
		return self

	def __ixor__(self)->Float8192:
		return self

	def __ilshift__(self)->Float8192:
		return self

	def __irshift__(self)->Float8192:
		return self

	def __eq__(self, other: Float8192)->bool:
		return True

	def __ne__(self, other: Float8192)->bool:
		return True

	def __lt__(self, other: Float8192)->bool:
		return True

	def __le__(self, other: Float8192)->bool:
		return True

	def __gt__(self, other: Float8192)->bool:
		return True

	def __ge__(self, other: Float8192)->bool:
		return True

	def __del__(self)->Float8192:
		return self

	def __int__(self)->int:
		chunk_size = self.mantissa.itemsize * 8
		value = 0
		for i in range(len(self.mantissa) - 1, -1, -1):
			value = (value << chunk_size) | int(self.mantissa[i])
		return value if getattr(self, "sign", 1) >= 0 else -value

	def __bool__(self)->bool:
		...

	def __str__(self)->str:
		res = ''
		for i in range(128):
			...
		return res

	def __bytes__(self)->bytes:
		return self

	def __len__(self)->int:
		chunk_size = self.mantissa.itemsize * 8
		for i in range(len(self.mantissa)-1, -1, -1):
			chunk = int(self.mantissa[i])
			if chunk != 0:
				return i * chunk_size
		return 0

	def _normalize(self):
		bitcount = len(self.mantissa)
		if bitcount == 0:
			self.exponent = 0
			self.sign = 1
			return
		max_bits = len(self.mantissa) * 8 * self.mantissa.itemsize
		shift = max_bits - bitcount
		if shift > 0:
			self.mantissa <<= shift
			self.exponent -= 1

	def __getitem__(self)-> Union[np.bool_, np.uint8, np.uint16, np.uint32, np.uint64]:
		...

	def __setitem__(self)->Float8192:
		return self

	def __contains__(self)->bool:
		return self

	def __copy__(self)->Float8192:
		return self

	def __sizeof__(self)->int:
		return self



class MathF:


	bit64types = (UInt8192, UInt4096, UInt2048, UInt1024, UInt512, UInt256, UInt128, Int8192, Int4096, Int2048, Int1024, Int512, Int256, Int128,
	Float8192, Float4096, Float2048, Float1024, Float512, Float256, Float128)

	bit32types = (UInt8192H, UInt4096, UInt2048H, UInt1024H, UInt512H, UInt256H, UInt128H, Int8192H, Int4096H, Int2048H, Int1024H, Int512H, Int256H, Int128H,
	Float8192H, Float4096H, Float2048H, Float1024H, Float512H, Float256H, Float128H)


	#? Unions for type hinting
	#? Only indicate comptibility, thus all lower bit values are included too.
	#? Just the larger values are excludes, like np.int_, which can be either 32 or 64 bit, and therefore is excluded from intsUnion32

	#? Custom types
	bigUIntsUnion64 = Union[UInt8192, UInt4096, UInt2048, UInt1024, UInt512, UInt256, UInt128]

	bigIntsUnion64 = Union[Int8192, Int4096, Int2048, Int1024, Int512, Int256, Int128]

	bigFloatsUnion64 = Union[Float8192, Float4096, Float2048, Float1024, Float512, Float256, Float128]

	bigUIntsUnion32 = Union[UInt8192H, UInt4096H, UInt2048H, UInt1024H, UInt512H, UInt256H, UInt128H]

	bigIntsUnion32 = Union[Int8192H, Int4096H, Int2048H, Int1024H, Int512H, Int256H, Int128H]

	bigFloatsUnion32 = Union[Float8192H, Float4096H, Float2048H, Float1024H, Float512H, Float256H, Float128H]

	#? Native and numpy types
	intsUnion64 = Union[int, np.int_, np.int8, np.int16, np.int32, np.int64, np.intc]

	uintsUnion64 = Union[np.uint, np.uint8, np.uint16, np.uint32, np.uint64, np.uintc]

	floatsUnion64 = Union[float, np.float16, np.float32, np.float64, np.float96, np.float128]

	intsUnion32 = Union[np.int8, np.int16, np.int32, np.intc]

	uintsUnion32 = Union[np.uint8, np.uint16, np.uint32, np.uintc]

	floatsUnion32 = Union[np.float16, np.float32]

	#! Unionized unions get flattened, so this does actually work.
	allIntsUnion32 = Union[bigIntsUnion32, intsUnion32]

	allIntsUnion64 = Union[bigIntsUnion64, intsUnion64]

	allUIntsUnion32 = Union[bigUIntsUnion32, uintsUnion32]

	allUIntsUnion64 = Union[bigUIntsUnion64, uintsUnion64]

	allFloatsUnion32 = Union[bigFloatsUnion32, floatsUnion32]

	allFloatsUnion64 = Union[bigFloatsUnion64, floatsUnion64]

	bit32Union = Union[bigIntsUnion32, bigUIntsUnion32, bigFloatsUnion32, intsUnion32, uintsUnion32, floatsUnion32]

	bit32Union = Union[bigIntsUnion64, bigUIntsUnion64, bigFloatsUnion64, intsUnion64, uintsUnion64, floatsUnion64]


	#? Tuples for type checking

	#? 64 Bit
	bigUInttypes64 = (UInt8192, UInt4096, UInt2048, UInt1024, UInt512, UInt256, UInt128)

	uinttypes64 = (np.uint, np.uint16, np.uint32, np.uint64)

	bigInttypes64 = (Int8192, Int4096, Int2048, Int1024, Int512, Int256, Int128)

	inttypes64 = (np.int_, np.int8, np.int16, np.int32, np.int64, int)

	bigFloattypes64 = (Float8192, Float4096, Float2048, Float1024, Float512, Float256, Float128)

	floattypes64 = (np.float16, np.float32, np.float64)

	#? 32 Bit
	bigUInttypes32 = (UInt8192, UInt4096, UInt2048, UInt1024, UInt512, UInt256, UInt128)

	uinttypes32 = (np.uint8, np.uint16, np.uint32, np.uintc)

	bigInttypes32 = (Int8192, Int4096, Int2048, Int1024, Int512, Int256, Int128)

	inttypes32 = (np.int8, np.int16, np.int32, np.intc)

	bigFloattypes32 = (Float8192, Float4096, Float2048, Float1024, Float512, Float256, Float128)

	floattypes32 = (np.float16, np.float32, np.float64)


	def frexp(bigint: MathF.bigIntsUnion64|MathF.bigIntsUnion32)->tuple[np.ndarray[int, np.uint64|np.uint32], int]:
		"""Convert a bigint type (this library's int and uint types) to a floating point type. Returns the mantissa and exponent, not an object."""
		bitcount = len(bigint)
		if bitcount == 0:
			return bigint, 0
		chunk_size = bigint.chunks.itemsize * 8
		max_bits = len(bigint.chunks) * chunk_size
		shift = max_bits - bitcount
		normalized = bigint << shift
		exponent = bitcount
		return normalized, exponent

