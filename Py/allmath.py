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

	def __len__(self)->np.uint8:
		return np.uint8(1024)

	def __getitem__(self, index = np.uint32)-> MathF.allUIntsUnion:
		version, modeval, sign, chunkselect, endianness, indexvalue = Types.decode_index(index)
		version		 = np.uint8(version)
		modeval		 = np.uint8(modeval)
		sign		 = np.uint8(sign)
		chunkselect  = np.uint8(chunkselect)
		endianness	 = np.uint8(endianness)
		indexvalue	 = np.uint16(indexvalue)
		# mask = np.uint32(0)
		# for _ in range(modeval):
		# 	mask >>= 1
		# 	mask |= 0x8000
		# indexvalue |= (indexvalue & ~mask)
		if version == 1:
			match indexvalue:
				case _ if modeval == np.uint8(0)  and indexvalue >= np.uint16(8192): # just in case you dont rember the mode chart
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when bit indexing")
				case _ if modeval == np.uint8(1)  and indexvalue >= np.uint16(2048):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when nybble indexing")
				case _ if modeval == np.uint8(2)  and indexvalue >= np.uint16(1024):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when byte indexing")
				case _ if modeval == np.uint8(3)  and indexvalue >= np.uint16(512):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when Word indexing")
				case _ if modeval == np.uint8(4)  and indexvalue >= np.uint16(256):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when DWord indexing")
				case _ if modeval == np.uint8(5)  and indexvalue >= np.uint16(128):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when QWord indexing")
				case _ if modeval == np.uint8(6)  and indexvalue >= np.uint16(64):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when UInt128 indexing")
				case _ if modeval == np.uint8(7)  and indexvalue >= np.uint16(32):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when UInt256 indexing")
				case _ if modeval == np.uint8(8)  and indexvalue >= np.uint16(16):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when UInt512 indexing")
				case _ if modeval == np.uint8(9)  and indexvalue >= np.uint16(8):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when UInt1024 indexing")
				case _ if modeval == np.uint8(10) and indexvalue >= np.uint16(4):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when UInt2048 indexing")
				case _ if modeval == np.uint8(11) and indexvalue >= np.uint16(2):
					raise IndexError(f"Index {indexvalue} is out of range for type {type(self)} when UInt4096 indexing")
				case _: raise ValueError(f"Value not supported for version 1 indexing of {type(self)}")
			try:
				match modeval:
					case np.uint8(0): # bit indexing
						number = np.uint64(indexvalue) % 64
						element = self.chunks[indexvalue // 64]
						mask = np.uint64(1) << number
						return element & mask
					case np.uint8(1): # nybble indexing
						number = np.uint64(indexvalue) % 16
						element = self.chunks[indexvalue // 16]
						mask = np.uint64(0xF) << (number * 4) # shift is multiplied with the amount of return bits :3
						return element & mask
					case np.uint8(2): # byte indexing
						number = np.uint64(indexvalue) % 8
						element = self.chunks[indexvalue // 8]
						mask = np.uint64(0xFF) << (number * 8)
						return element & mask
					case np.uint8(3): # word indexing
						number = np.uint64(indexvalue) % 4
						element = self.chunks[indexvalue // 4]
						mask = np.uint64(0xFFFF) << (number * 16)
						return element & mask
					case np.uint8(4): # dword indexing
						number = np.uint64(indexvalue) % 2
						element = self.chunks[indexvalue // 2]
						mask = np.uint64(0xFFFFFFFF) << (number * 32)
						return element & mask
					case np.uint8(5): # qword / chunk indexing
						return self.chunks[indexvalue]
					#? further returns require lower biguints added, but ill set up for it now anyways
					case np.uint8(6): # UInt128 indexing
						value = Types.UInt128(0) #! Just realized these are gonna require recursive indexing... Fuck me. Hard.
						for i in range(2): #! also i cant explain this for some reason but like ik this is a hard requirement. trust me bro
							value[i] = self.chunks[(indexvalue * 2) + i]
						return value
					case np.uint8(7): # UInt256 indexing
						value = Types.UInt256(0)
						for i in range(4):
							value[i] = self.chunks[(indexvalue * 4) + i]
						return value
					case np.uint8(8): # UInt512 indexing
						value = Types.UInt512(0)
						for i in range(8):
							value[i] = self.chunks[(indexvalue * 8) + i]
						return value
					case np.uint8(9): # UInt1024 indexing
						value = Types.UInt1024(0)
						for i in range(16):
							value[i] = self.chunks[(indexvalue * 16) + i]
						return value
					case np.uint8(10): # UInt2048 indexing
						value = Types.UInt2048(0)
						for i in range(32):
							value[i] = self.chunks[(indexvalue * 32) + i]
						return value
					case np.uint8(11): # UInt4096 indexing
						value = Types.UInt4096(0)
						for i in range(64): #! I am actively convincing myself that this will actually work and i dont like it
							value[i] = self.chunks[(indexvalue * 64) + i]
						return value
					case _: raise ValueError(f"Indexing type not supported by version 1 indexing of {type(self)}")
			except IndexError: raise IndexError("Index value is out of bounds for index type")
		else: raise NotImplementedError("Version 2 has not been implemented for this version yet.")

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
		return self

	def __iadd__(self, other: Float8192)->Float8192:
		return self

	def __mul__(self, other: Float8192)->Float8192:
		return self

	def __imul__(self, other: Float8192)->Float8192:
		return self

	def __sub__(self, other: Float8192)->Float8192:
		return self

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


class Types:
	"""Simpler way to import and refer to types"""
	#? 64 bit
	UInt8192 = UInt8192
	UInt4096 = UInt4096
	UInt2048 = UInt2048
	UInt1024 = UInt1024
	UInt512 = UInt512
	UInt256 = UInt256
	UInt128 = UInt128
	Int8192 = Int8192
	Int4096 = Int4096
	Int2048 = Int2048
	Int1024 = Int1024
	Int512 = Int512
	Int256 = Int256
	Int128 = Int128
	Float8192 = Float8192
	Float4096 = Float4096
	Float2048 = Float2048
	Float1024 = Float1024
	Float512 = Float512
	Float256 = Float256
	Float128 = Float128
	#? 32 bit
	UInt8192H = UInt8192H
	UInt4096H = UInt4096H
	UInt2048H = UInt2048H
	UInt1024H = UInt1024H
	UInt512H = UInt512H
	UInt256H = UInt256H
	UInt128H = UInt128H
	Int8192H = Int8192H
	Int4096H = Int4096H
	Int2048H = Int2048H
	Int1024H = Int1024H
	Int512H = Int512H
	Int256H = Int256H
	Int128H = Int128H
	Float8192H = Float8192H
	Float4096H = Float4096H
	Float2048H = Float2048H
	Float1024H = Float1024H
	Float512H = Float512H
	Float256H = Float256H
	Float128H = Float128H


	def decode_index(index: np.uint32)->tuple[np.uint32,]:
		modeval: np.uint32 = index & 0x78000000 # 0b01111000000000000000000000000000
		version: np.uint32 = index & 0x80000000 # 0b1000...
		sign: np.uint32 = index & 0x40000
		chunkselect: np.uint32 = index & 0x20000
		endianness: np.uint32 = index & 0x10000
		indexvalue: np.uint32 = index & 0xFFFF
		return (version, modeval, sign, chunkselect, endianness, indexvalue)


class MathF:
	"""Functions and supporting variables, such as type unions/tuples"""

	#? Unions for type hinting
	#? Only indicate comptibility, thus all lower bit values are included too.
	#? Just the larger values are excludes, like np.int_, which can be either 32 or 64 bit, and therefore is excluded from intsUnion32

	#? Custom types
	bigUIntsUnion64 = Union[Types.UInt8192, Types.UInt4096, Types.UInt2048, Types.UInt1024, Types.UInt512, Types.UInt256, Types.UInt128]
	bigIntsUnion64 = Union[Types.Int8192, Types.Int4096, Types.Int2048, Types.Int1024, Types.Int512, Types.Int256, Types.Int128]
	bigFloatsUnion64 = Union[Types.Float8192, Types.Float4096, Types.Float2048, Types.Float1024, Types.Float512, Types.Float256, Types.Float128]
	bigUIntsUnion32 = Union[Types.UInt8192H, Types.UInt4096H, Types.UInt2048H, Types.UInt1024H, Types.UInt512H, Types.UInt256H, Types.UInt128H]
	bigIntsUnion32 = Union[Types.Int8192H, Types.Int4096H, Types.Int2048H, Types.Int1024H, Types.Int512H, Types.Int256H, Types.Int128H]
	bigFloatsUnion32 = Union[Types.Float8192H, Types.Float4096H, Types.Float2048H, Types.Float1024H, Types.Float512H, Types.Float256H, Types.Float128H]

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
	bigUInttypes64 = (Types.UInt8192, Types.UInt4096, Types.UInt2048, Types.UInt1024, Types.UInt512, Types.UInt256, Types.UInt128)
	uinttypes64 = (np.uint, np.uint16, np.uint32, np.uint64)
	bigInttypes64 = (Types.Int8192, Types.Int4096, Types.Int2048, Types.Int1024, Types.Int512, Types.Int256, Types.Int128)
	inttypes64 = (np.int_, np.int8, np.int16, np.int32, np.int64, int)
	bigFloattypes64 = (Types.Float8192, Types.Float4096, Types.Float2048, Types.Float1024, Types.Float512, Types.Float256, Types.Float128)
	floattypes64 = (np.float16, np.float32, np.float64)

	#? 32 Bit
	bigUInttypes32 = (Types.UInt8192H, Types.UInt4096H, Types.UInt2048H, Types.UInt1024H, Types.UInt512H, Types.UInt256H, Types.UInt128H)
	uinttypes32 = (np.uint8, np.uint16, np.uint32, np.uintc)
	bigInttypes32 = (Types.Int8192H, Types.Int4096H, Types.Int2048H, Types.Int1024H, Types.Int512H, Types.Int256H, Types.Int128H)
	inttypes32 = (np.int8, np.int16, np.int32, np.intc)
	bigFloattypes32 = (Types.Float8192H, Types.Float4096H, Types.Float2048H, Types.Float1024H, Types.Float512H, Types.Float256H, Types.Float128H)
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
		#? Casting to uint32s to avoid outbounding :3
		mode = np.uint32 (mode & 0xF) #? clamp mode to lower 4 bits with an and operation
		signed = np.uint32(signed & 0b1)
		littleEndian = np.uint32(littleEndian & 0b1)
		chunkselect = np.uint32(chunkselect & 0b1) if chunkselect is not None else None
		indexvalue = np.uint32(indexvalue & 0xFF)
		index |= (mode << 27) # bit magic sets bits 30-27 to mode
		#? This is an in-place bitwise or and a bitwise leftshift
		index |= (signed << 18)
		if chunkselect != None:
			index |= (chunkselect << 17)
		index |= (littleEndian << 16)
		mask = np.uint32(0) # build a mask for reserving bits in index value area/mask out indexvalue bits
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


