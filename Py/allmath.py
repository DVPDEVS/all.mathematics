from __future__ import annotations # Treat type hints as strings/future types. this gets rid of 60+ errors per class
import numpy as np
from typing import Union

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
		return len(str(self))*64 if type(self) == 0 else 0

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
	"""Functions and supporting variables, such as type unions/tuples"""

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
	allUIntsUnion = Union[allUIntsUnion32, allUIntsUnion64]
	allIntsUnion = Union[allIntsUnion32, allIntsUnion64]
	allIntUIntsUnion = Union[allIntsUnion, allUIntsUnion]
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
	bigUInttypes32 = (UInt8192H, UInt4096H, UInt2048H, UInt1024H, UInt512H, UInt256H, UInt128H)
	uinttypes32 = (np.uint8, np.uint16, np.uint32, np.uintc)
	bigInttypes32 = (Int8192H, Int4096H, Int2048H, Int1024H, Int512H, Int256H, Int128H)
	inttypes32 = (np.int8, np.int16, np.int32, np.intc)
	bigFloattypes32 = (Float8192H, Float4096H, Float2048H, Float1024H, Float512H, Float256H, Float128H)
	floattypes32 = (np.float16, np.float32, np.float64)


	def frexp(bigint: MathF.bigIntsUnion64|MathF.bigIntsUnion32)->tuple[np.ndarray[int, np.uint64|np.uint32], int]:
		"""Convert a bigint type (this library's int and uint types) to a floating point type. Returns the mantissa and exponent, not an object."""
		bitcount = len(bigint) #? ngl i barely know what this does
		if bitcount == 0:
			return bigint, 0
		chunk_size = bigint.chunks.itemsize * 8
		max_bits = len(bigint.chunks) * chunk_size
		shift = max_bits - bitcount
		normalized = bigint << shift
		exponent = bitcount
		return normalized, exponent

	indexmodes = {
		'bit'		:0b00000,
		'nybble'	:0b00001,
		'byte'		:0b00010,
		'word'		:0b00011,
		'dword'		:0b00100,
		'qword'		:0b00101,
		'uint128'	:0b00110,
		'uint256'	:0b00111,
		'uint512'	:0b01000,
		'uint1024'	:0b01001,
		'uint2048'	:0b01010,
		'uint4096'	:0b01011,
		#! and more is coming in later versions
	}

	def indexgen(mode: MathF.uintsUnion32 = 2, indexvalue: MathF.uintsUnion32 = 0, *, 
			#! btw best for memory reasons to use the smalles uints you can, so here i'd pass np.uint8 for mode
			signed: bool|np.uint8 = 0, 
			littleEndian: bool|np.uint8 = 1,
			chunkselect: bool|np.uint8|None = None, 
			version2: bool|np.uint8 = 0) -> np.uint32:
		"""Generates an index value `np.uint32` for indexing bigint/biguint types"""
		index = np.uint32(0)
		#? clamp mode to lower 4 bits with an and operation
		mode = np.uint32 (mode & 0xF)
		signed = np.uint32(signed & 0b1)
		littleEndian = np.uint32(littleEndian & 0b1)
		chunkselect = np.uint32(chunkselect & 0b1) if chunkselect is not None else None
		indexvalue = np.uint32(indexvalue & 0xFF)
		index |= (mode << 27) # bit magic sets bits 30-27 to mode
		#? This is an in-place bitwise or and a bitwise leftshift
		index |= ((signed) << 18)
		if chunkselect != None:
			index |= ((chunkselect & 0b1) << 17)
		index |= ((littleEndian & 0b1) << 16)
		mask = 0 # build a mask for reserving bits in index value area/mask out indexvalue bits
		for _ in range(mode):
			mask >>= 1 # right shift once
			mask |= 0x8000 # this ors in one high bit (0b1000...)
		index |= (indexvalue & ~mask) # mask out ignored bits, just in case
		""" 
		An example of an index which may be constructed with this:
		mode = 3 [word]
		signed = True [Negative value]
		indexvalue = 391
		==
		0b 0001 1000 0000 0101 0000 0001 1000 0111
		Bit 31 is locked as this is version 1								(0)
		Bits 30-27 are the mode value clamped to 4 bits						(001 1)
		Bits 26-19 are reserved 											0s
		Bit 18 is the sign flag, indicating that this is a negative value 	(1)
		Bit 17 is the chunk selection flag, set to 							0
		Bit 16 is the endian indicator, set to little 						(1)
		Bits 15-13 were masked out from the indexvalue 						(0s)
		Bits 12-0 are our index 											(0 0001 1000 0111) (391)
		//
		Another example:
		mode = 0
		signed = False
		indexvalue = 6753
		==
		0b 0000 0000 0000 0001 0001 1010 0110 0001
		even then, in version one, the index is limited to certain max values. In this case, none of the
		first 3 digits in the index matter, as the highest value accepted is 8191, while 16 bits can
		supply 65535, and 13 bits = 0x1fff = 0b 0001 1111 1111 1111 = 8191
		"""
		return np.uint32(index)


