# -----------------------------------------------------------------------------
# This file is part of DVPDEVS/all.mathematics
#
# Copyright (C) 2025 DVP-F/Carnx00 and thebroskialex
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.
# -----------------------------------------------------------------------------

#TODO: #82 Make all bools into np.uint8

from __future__ import annotations # Treat type hints as strings/future types. this gets rid of 60+ errors per class
import numpy as np
from typing import Union, Literal, Final
from dataclasses import dataclass, fields

# Meta Immutability classes
class _ConstMeta(type): 
	__slots__ = ()
	def __setattr__(cls, name, value): raise TypeError(f"{cls.__name__} is immutable")
	def __delattr__(cls, name): raise TypeError(f"{cls.__name__} is immutable")
class _ImmutableConstMeta(_ConstMeta):
	def __init__(cls, *args, **kwargs):
		for base in cls.__mro__[1:]: 
			if isinstance(type(base), _ImmutableConstMeta): raise TypeError("Const classes cannot be subclassed")
		super().__init__(*args, **kwargs)


# Custom type for storing 1024 byte unsigned integers
class UInt8192:
	"""This is a fixed-size unsigned 8192-bit integer type. It IMMEDIATELY takes 1KB of ram."""

#TODO: #83 Change type hints to be realistc/useful

	MAX = (1 << 1024) -1

	__slots__ = ['chunks']

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
			res |= int(self.chunks[i])
		return res

	def __repr__(self):
		return f"UInt8192({self._to_int()})"

	def bit_length(self):
		return np.uint16(8192)

	def __len__(self)->np.uint8:
		return np.uint8(1024)

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

# TODO: #78 UINT
	def __truediv__(self, other: UInt8192)->Float8192: #I am unsure how this will be done with the current methods of doing arithmetic - Smol
		return self									# Whenever ive finished floats, we can use them. although itruediv may have to cast into float - DVP

# TODO: #77 UINT 
	def __itruediv__(self, other: UInt8192)->Float8192:
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

# TODO: #76 UINT 
	def __pow__(self, other: UInt8192)->UInt8192:
		return self

# TODO: #75 UINT 
	def __ipow__(self, other: UInt8192)->UInt8192:
		return self

#? pos and neg seem wasted tbh.

	def __and__(self, other: UInt8192)->UInt8192:
		new = UInt8192(0)
		for i in range(len(self.chunks)): #! Very temp!!
			new.chunks[i] = self.chunks[i] & other.chunks[i] # basic logic im gonna need
		return new

	def __or__(self, other: UInt8192)->UInt8192:
		new = UInt8192(0)
		for i in range(len(self.chunks)): #! Very temp!!
			new.chunks[i] = self.chunks[i] | other.chunks[i] # basic logic im gonna need
		return new

	def __xor__(self, other: UInt8192)->UInt8192:
		new = UInt8192(0)
		for i in range(len(self.chunks)): #! Very temp!!
			new.chunks[i] = self.chunks[i] ^ other.chunks[i] # basic logic im gonna need
		return new

# TODO: #69 UINT 
	def __lshift__(self, amount: UInt8192)->UInt8192:
		new = UInt8192(0); held = np.uint64
		# whole_words = amount // 64
		# bit_shift   = amount % 64
		# # Step 1: shift whole words
		# if whole_words > 0:
		# 	new = np.concatenate([np.zeros(whole_words, dtype=np.uint64), new])
		# # Step 2: shift bits inside each word + propagate carries
		# if bit_shift > 0:
		# 	shifted = new << bit_shift
		# 	carries = new >> (64 - bit_shift)
		# 	# add carries into next word
		# 	shifted[1:] |= carries[:-1]
		# 	new = shifted

		...

		return new

# TODO: #68 UINT 
	def __rshift__(self, amount: UInt8192)->UInt8192:
		new = UInt8192(0); held = np.uint64
		# whole_words = amount // 64
		# bit_shift   = amount % 64
		# # Step 1: shift whole words (drop LSB words)
		# if whole_words > 0:
		# 	if whole_words >= len(new):
		# 		return np.zeros_like(new, dtype=np.uint64)
		# 	new = new[whole_words:]
		# # Step 2: shift bits inside each word + propagate carries downward
		# if bit_shift > 0:
		# 	shifted = new >> bit_shift
		# 	carries = new << (64 - bit_shift)
		# 	# carry from word i goes into word i-1
		# 	shifted[:-1] |= carries[1:]
		# 	new = shifted
		# # pad MSB side to maintain fixed length
		# if whole_words > 0:
		# 	pad = np.zeros(whole_words, dtype=np.uint64)
		# 	new = np.concatenate([new, pad])

		...

		return new


	def __iand__(self, other: UInt8192)->UInt8192:
		for i in range(len(self.chunks)): #! Very temp!!
			self.chunks[i] = self.chunks[i] & other.chunks[i] # basic logic im gonna need
		return self

	def __ior__(self, other: UInt8192)->UInt8192:
		for i in range(len(self.chunks)): #! Very temp!!
			self.chunks[i] = self.chunks[i] | other.chunks[i] # basic logic im gonna need
		return self

	def __ixor__(self, other: UInt8192)->UInt8192:
		for i in range(len(self.chunks)): #! Very temp!!
			self.chunks[i] = self.chunks[i] ^ other.chunks[i] # basic logic im gonna need
		return self

# TODO: #64 UINT 
	def __ilshift__(self, amount: UInt8192)->UInt8192:
		return self

# TODO: #63 UINT 
	def __irshift__(self, amount: UInt8192)->UInt8192:
		return self

	def __eq__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

# TODO: #62 UINT 
	def __ne__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

# TODO: #61 UINT 
	def __lt__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

# TODO: #60 UINT 
	def __le__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

# TODO: #59 UINT 
	def __gt__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

# TODO: #58 UINT 
	def __ge__(self, other: UInt8192)->bool:
		for i in range(128):
			if int(self.chunks[i]) != int(other.chunks[i]):
				return False
		return True

# TODO: #57 UINT 
	def __del__(self)->UInt8192:
		return self

# TODO: #56 UINT 
	def __int__(self)->int:
		return self._to_int()

# TODO: #54 UINT 
	def __bool__(self)->bool:
		return True if self._to_int() != 0 else False

# TODO: #55 UINT
	def __str__(self)->str:
		return repr(self).removesuffix(')').removeprefix('UInt8192(')

# TODO: #53 UINT 
	def __bytes__(self)->bytes:
		return self._to_int().to_bytes(128, 'little')

# TODO: #52 UINT 
	def __getitem__(self,
			index: np.uint32 | slice[np.uint32|None,np.uint32|None,np.uint32|None]
			)-> np.uint8|np.ndarray[np._AnyShapeT,np.uint8]:
		"""
		Return a single `np.uint8` or a generic 1D `np.ndarray(shape=tuple[int], dtype=np.uint8)`
		"""
		if type(index) == np.uint32:
			if index > Types._MAX_INDEX_BY_TYPE.UInt8192:
				raise IndexError(f'Index {index} is out of range for UInt8192')
			else:
				number :np.uint64 = np.uint64(index) % 8 # which byte
				element :np.uint64 = self.chunks[index // 8] # which chunk
				return np.uint8((element >> (number * 8)) & 0xFF) # extract and return
		elif type(index) == slice:
			# can be improved later but for now imma use a generator
			arr :list[np.uint8]= []
			for idx in range(
					0 if not index[0] else index[0],
					self.chunks.__len__()*8 if not index[1] else index[1],
					1 if not index[2] else index[2]
				): arr.append(self.__getitem__(np.uint32(idx)))
			return np.arr(arr, np.uint8)

# TODO: #51 UINT 
	def __setitem__(self, indexer: 
			np.uint32 |
			slice[np.uint32|None,np.uint32|None,np.uint32|None],
			value: Types.allUIntsUnion
			)-> Types.allUIntsUnion:
		if type(indexer) == np.uint32:
			index = indexer
			check = Types.index_validate(index)
			if check[0] == np.uint8(1):
				m : tuple[np.uint8, None|IndexError] = Types.index_match(index, "UInt8192")
				if m[0] == np.uint8(1):
					version, modeval, sign, chunkselect, endianness, indexvalue = Types.index_decode(index)
					version		= np.uint8(version)
					modeval		= np.uint8(modeval)
					sign		= np.uint8(sign)
					chunkselect = np.uint8(chunkselect)
					endianness	= np.uint8(endianness)
					indexvalue	= np.uint16(indexvalue)
					try:
						# generate masks
						_len = np.uint64(0)
						for _ in range(modeval):
							_len |= 1; _len << 1
						vmask = np.uint64(indexvalue)
						...
					except IndexError as e: raise IndexError("Unknown failure when indexing") from e 
				else: raise m[1]
			else: 
				if check[1] is not None: raise check[1]
				else: raise ValueError(check[0])

# TODO: #50 UINT 
	def __contains__(self, other: Types.allUIntsUnion|list[np.uint32]|tuple[np.uint32] = None)->bool:
		if other == None: raise TypeError("No value to check for was given")
		elif type(other) in (list, tuple):
			other = Types.UInt8192(0)
			... #? basically index but the index value is the value were looking for instead of the position we're looking for D:
			#? Gotta do this to check:
			if ... == other: return True
			other <<= ('some value based on other`s index type') 
		else: # assume we good, index per chunk and comp to `other`
			other = np.uint64(int(other))
			for i in range(len(self.chunks)):
				if self.chunks[i] == other: return True   
			return False

# TODO: #49 UINT 
	def __copy__(self)->UInt8192:
		return Types.UInt8192(int(self)) #! https://docs.python.org/3/library/copy.html

	def __sizeof__(self)->int:
		"""Return actual size of the object in memory, or a conjecture of its size in memory"""
		try:
			from pympler.asizeof import asizeof
			return asizeof(self)
		except Exception|ImportError|ImportWarning:
			return np.uint8(1208) #? See Memory Management in README.md for more info about this

# Custom type for storing 1024 byte floats
class Float8192:
	"""This is a fixed-size signed 8192-bit float type. It IMMEDIATELY takes 1KB of ram."""

	MAX = (1 << 1024) -1
	__slots__ = ['mantissa', 'mantissa_signed', 'exponent']

	def __init__(self, value: int|Types.uintsUnion64|Types.uintsUnion32 = 0, *, precision: int|Types.uintsUnion64|Types.uintsUnion32 = 16):
		self.mantissa = np.zeros(127, dtype=np.uint64)
		self.mantissa_signed = np.int64(0)
		self.exponent = np.uint16(precision)
		self._from_float(value)

	def _from_float(self, value: int = 0):
		i=0
		while value > 0 and i < 128:
			self.mantissa[i] = value & 0xFFFFFFFFFFFFFFFF
			value >>= 64
			i += 1

# TODO: #47 FLOAT
	def _to_int(self)->int:
		return self

# TODO: #46 FLOAT
	def __repr__(self):
		return f"Float8192({''})"

# TODO: #45 FLOAT
	def __add__(self, other: Float8192)->Float8192:
		return self

# TODO: #44 FLOAT
	def __iadd__(self, other: Float8192)->Float8192:
		return self

# TODO: #43 FLOAT
	def __mul__(self, other: Float8192)->Float8192:
		return self

# TODO: #42 FLOAT
	def __imul__(self, other: Float8192)->Float8192:
		return self

# TODO: #41 FLOAT
	def __sub__(self, other: Float8192)->Float8192:
		return self

# TODO: #40 FLOAT
	def __isub__(self, other: Float8192)->Float8192:
		return self

# TODO: #39 FLOAT
	def __truediv__(self, other: Float8192)->Float8192:
		return self

# TODO: #38 FLOAT
	def __itruediv__(self, other: Float8192)->Float8192:
		return self

# TODO: #37 FLOAT
	def __floordiv__(self, other: Float8192)->Float8192:
		return self

# TODO: #36 FLOAT
	def __ifloordiv__(self, other: Float8192)->Float8192:
		return self

# TODO: #35 FLOAT
	def __mod__(self, other: Float8192)->Float8192:
		return self

# TODO: #34 FLOAT
	def __imod__(self, other: Float8192)->Float8192:
		return self

# TODO: #33 FLOAT
	def __pow__(self, other: Float8192)->Float8192:
		return self

# TODO: #32 FLOAT
	def __ipow__(self, other: Float8192)->Float8192:
		return self

#? again no use for pos and neg i suspect

# TODO: #28 FLOAT
	def __abs__(self)->Float8192:
		return self

# TODO: #29 FLOAT
	def __and__(self)->Float8192:
		return self

# TODO: #27 FLOAT
	def __or__(self)->Float8192:
		return self

# TODO: #26 FLOAT
	def __xor__(self)->Float8192:
		return self

# TODO: #25 FLOAT
	def __lshift__(self)->Float8192:
		return self

# TODO: #24 FLOAT
	def __rshift__(self)->Float8192:
		return self

# TODO: #23 FLOAT
	def __iand__(self)->Float8192:
		return self

# TODO: #22 FLOAT
	def __ior__(self)->Float8192:
		return self

# TODO: #21 FLOAT
	def __ixor__(self)->Float8192:
		return self

# TODO: #20 FLOAT
	def __ilshift__(self)->Float8192:
		return self

# TODO: #19 FLOAT
	def __irshift__(self)->Float8192:
		return self

# TODO: #18 FLOAT
	def __eq__(self, other: Float8192)->bool:
		return True

# TODO: #17 FLOAT
	def __ne__(self, other: Float8192)->bool:
		return True

# TODO: #16 FLOAT
	def __lt__(self, other: Float8192)->bool:
		return True

# TODO: #15 FLOAT
	def __le__(self, other: Float8192)->bool:
		return True

# TODO: #14 FLOAT
	def __gt__(self, other: Float8192)->bool:
		return True

# TODO: #13 FLOAT
	def __ge__(self, other: Float8192)->bool:
		return True

# TODO: FLOAT
	def __del__(self)->Float8192:
		return self

# TODO: #12 FLOAT
	def __int__(self)->int:
		chunk_size = self.mantissa.itemsize * 8
		value = 0
		for i in range(len(self.mantissa) - 1, -1, -1):
			value = (value << chunk_size) | int(self.mantissa[i])
		return value if getattr(self, "sign", 1) >= 0 else -value

# TODO: #11 FLOAT
	def __bool__(self)->bool:
		...

# TODO: #10 FLOAT
	def __str__(self)->str:
		res = ''
		for i in range(128):
			...
		return res

# TODO: #9 FLOAT
	def __bytes__(self)->bytes:
		return self

# TODO: #8 FLOAT
	def __len__(self)->int:
		chunk_size = self.mantissa.itemsize * 8
		for i in range(len(self.mantissa)-1, -1, -1):
			chunk = int(self.mantissa[i])
			if chunk != 0:
				return i * chunk_size
		return 0

# TODO: #7 FLOAT
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

# TODO: #6 FLOAT
	def __getitem__(self)-> Types.uintsUnion64:
		return self

# TODO: #5 FLOAT
	def __setitem__(self)->Float8192:
		return self

# TODO: #4 FLOAT
	def __contains__(self)->bool:
		return self

# TODO: #3 FLOAT
	def __copy__(self)->Float8192:
		return self

# TODO: #2 FLOAT
	def __sizeof__(self)->int:
		return self


class Convert:
	"""Conversion mainly between bases and types"""

	def b05_to_b10_uint(encoded: Types.uintsUnion32|Types.uintsUnion64 = 0, max_precision: Types.uintsUnion32 = 16) -> tuple[Types.uintsUnion32|Types.uintsUnion64, Types.uintsUnion32]:
		"""Convert a decimal fraction encoded in binary fixed-point as base 0.5 into a uint of the decimal digits and the number of digits\n
		(To avoid losing leading zeros)"""
		
		if encoded == 0:
			return encoded, np.uint8(1)
		bitcount = len(encoded)
		denomINATOR = type(encoded)(1) << bitcount #? stupid but works actually
		numerator = encoded
		p10 = type(encoded)(1)
		for d in range(1, max_precision +1):
			p10 *= 10
			if (numerator * p10) % denomINATOR == 0: #! wont work until dunder methods have been added (mod)
				return (numerator * p10) // denomINATOR, d #! wont work until dunder methods have been added (floordiv)
		#? best guess approximation in case nothing better is found :|
		return (numerator * p10) // denomINATOR, max_precision #! wont work until dunder methods have been added (floordiv)

# TODO: #79 Rewrite to use np types
	def b10_uint_to_b05(encoded_digits: Types.uintsUnion32|Types.uintsUnion64 = 0, max_precision: Types.uintsUnion32 = 16) -> tuple[Types.uintsUnion32|Types.uintsUnion64, Types.uintsUnion32]:
		"""Convert base-10 decimal digits into a binary fixed-point encoded uint where each bit is 0.5^n"""

		if encoded_digits == 0:
			return type(encoded_digits)(0), type(encoded_digits)(1)
		decimal_digit_count = len(encoded_digits)
		power_10 = 10 ** decimal_digit_count
		for bits in range(1, int(max_precision) + 1):
			multiplier = 1 << bits
			if (int(encoded_digits) * multiplier) % power_10 == 0:
				b05 = (int(encoded_digits) * multiplier) // power_10
				return type(encoded_digits)(b05), type(encoded_digits)(bits)
		#? fallback approximation
		multiplier = 1 << int(max_precision)
		b05 = (int(encoded_digits) * multiplier) // power_10
		return type(encoded_digits)(b05), type(encoded_digits)(max_precision)



class Types:
	"""Simpler way to import, refer, check and hint to types"""
	#? 64 bit
	UInt8192 = UInt8192
	# UInt4096 = UInt4096
	# UInt2048 = UInt2048
	# UInt1024 = UInt1024
	# UInt512 = UInt512
	# UInt256 = UInt256
	# UInt128 = UInt128
	# Int8192 = Int8192
	# Int4096 = Int4096
	# Int2048 = Int2048
	# Int1024 = Int1024
	# Int512 = Int512
	# Int256 = Int256
	# Int128 = Int128
	Float8192 = Float8192
	# Float4096 = Float4096
	# Float2048 = Float2048
	# Float1024 = Float1024
	# Float512 = Float512
	# Float256 = Float256
	# Float128 = Float128
	#? 32 bit
	# UInt8192H = UInt8192H
	# UInt4096H = UInt4096H
	# UInt2048H = UInt2048H
	# UInt1024H = UInt1024H
	# UInt512H = UInt512H
	# UInt256H = UInt256H
	# UInt128H = UInt128H
	# Int8192H = Int8192H
	# Int4096H = Int4096H
	# Int2048H = Int2048H
	# Int1024H = Int1024H
	# Int512H = Int512H
	# Int256H = Int256H
	# Int128H = Int128H
	# Float8192H = Float8192H
	# Float4096H = Float4096H
	# Float2048H = Float2048H
	# Float1024H = Float1024H
	# Float512H = Float512H
	# Float256H = Float256H
	# Float128H = Float128H

	#? Unions for type hinting
	#? Only indicate compatibility, thus all lower bit values are included too.
	#? Just the larger values are excluded, like np.int_, which can be either 32 or 64 bit, and therefore is excluded from intsUnion32
	#? Custom types
	# bigUIntsUnion64	 = Union[UInt8192,         UInt4096,   		UInt2048,   	 UInt1024,   	  UInt512,    		UInt256,          UInt128	]
	# bigIntsUnion64	 = Union[Int8192,          Int4096,    		Int2048,    	 Int1024,    	  Int512,     		Int256,           Int128	]
	# bigFloatsUnion64 = Union[Float8192,        Float4096,  		Float2048,  	 Float1024,  	  Float512,   		Float256,         Float128	]
	# bigUIntsUnion32	 = Union[UInt8192H,        UInt4096H,  		UInt2048H,  	 UInt1024H,  	  UInt512H,   		UInt256H,         UInt128H	]
	# bigIntsUnion32	 = Union[Int8192H,         Int4096H,   		Int2048H,   	 Int1024H,   	  Int512H,    		Int256H,          Int128H	]
	# bigFloatsUnion32 = Union[Float8192H,       Float4096H, 		Float2048H, 	 Float1024H, 	  Float512H,  		Float256H,        Float128H	]
	#? Native and numpy types
	# intsUnion64		 = Union[int,              np.int_,    		np.int8,    	 np.int16,   	  np.int32,   		np.int64,         np.intc	]
	# uintsUnion64	 = Union[np.uint,          np.uint8,   		np.uint16,  	 np.uint32,  	  np.uint64,  		np.uintc					]
	# floatsUnion64	 = Union[float,            np.float16, 		np.float32, 	 np.float64, 	  np.float96, 		np.float128					]
	# intsUnion32		 = Union[np.int8,          np.int16,   		np.int32,   	 np.intc														]
	# uintsUnion32	 = Union[np.uint8,         np.uint16,  		np.uint32,  	 np.uintc														]
	# floatsUnion32	 = Union[np.float16,       np.float32																						]
	#? Combos
	# allIntsUnion32	 = Union[bigIntsUnion32,   intsUnion32																						]
	# allIntsUnion64	 = Union[bigIntsUnion64,   intsUnion64																						]
	# allUIntsUnion32	 = Union[bigUIntsUnion32,  uintsUnion32																						]
	# allUIntsUnion64	 = Union[bigUIntsUnion64,  uintsUnion64																						]
	# allUIntsUnion	 = Union[allUIntsUnion32,  allUIntsUnion64																					]
	# allIntsUnion	 = Union[allIntsUnion32,   allIntsUnion64																					]
	# allIntUIntsUnion = Union[allIntsUnion,     allUIntsUnion																					]
	# allFloatsUnion32 = Union[bigFloatsUnion32, floatsUnion32																					]
	# allFloatsUnion64 = Union[bigFloatsUnion64, floatsUnion64																					]
	# allBit32Union		 = Union[allIntsUnion32,   allUIntsUnion32, allFloatsUnion32																]
	# allBit64Union		 = Union[allIntsUnion64,   allUIntsUnion64, allFloatsUnion64																]
	# allBigTypesUnion = Union[bigIntsUnion32,   bigIntsUnion64,  bigUIntsUnion32, bigUIntsUnion64, bigFloatsUnion32, bigFloatsUnion64			]

	#? Tuples for type checking
	#? Custom types
	# bigInttypes64	 = (	 Int8192,    	   Int4096,    		Int2048,    	 Int1024,    	  Int512,    	  	Int256,    		  Int128	)
	# bigUInttypes64	 = (	 UInt8192,   	   UInt4096,   		UInt2048,   	 UInt1024,   	  UInt512,   	  	UInt256,   		  UInt128	)
	# bigFloattypes64	 = (	 Float8192,  	   Float4096,  		Float2048,  	 Float1024,  	  Float512,  	  	Float256,  		  Float128	)
	# bigInttypes32	 = (	 Int8192H,   	   Int4096H,   		Int2048H,   	 Int1024H,   	  Int512H,   	  	Int256H,   		  Int128H	)
	# bigUInttypes32	 = (	 UInt8192H,  	   UInt4096H,  		UInt2048H,  	 UInt1024H,  	  UInt512H,  	  	UInt256H,  		  UInt128H	)
	# bigFloattypes32	 = (	 Float8192H, 	   Float4096H, 		Float2048H, 	 Float1024H, 	  Float512H, 	  	Float256H, 		  Float128H	)
	#? Native/numpy types
	inttypes64		 = (	 np.int_,    	   np.int8,    		np.int16,   	 np.int32,   	  np.int64,  	  	int							)
	uinttypes64		 = (	 np.uint,    	   np.uint16,  		np.uint32,  	 np.uint64														)
	floattypes64	 = (	 np.float16, 	   np.float32, 		np.float64		 																)
	inttypes32		 = (	 np.int8,    	   np.int16,   		np.int32,   	 np.intc														)
	uinttypes32		 = (	 np.uint8,   	   np.uint16,  		np.uint32,  	 np.uintc														)
	floattypes32	 = (	 np.float16, 	   np.float32, 		np.float64																		)

	#? repurpose this
	@dataclass(frozen=True, slots=True) # OOooOoOoooOohhhhHHHHHhHhhH so fancy you are now.
	class _MAX_INDEX_BY_TYPE(metaclass=_ImmutableConstMeta): # Make Immutable (unless you try WAY too hard but then its your problem)
		# Declared initialized ∴ Enum
		UInt8192   :Final[np.uint32] = 8191
		UInt4096   :Final[np.uint32] = 4095
		UInt2048   :Final[np.uint32] = 2047
		UInt1024   :Final[np.uint32] = 1023
		UInt512    :Final[np.uint32] = 511
		UInt256    :Final[np.uint32] = 255
		UInt128    :Final[np.uint32] = 127
		Int8192    :Final[np.uint32] = 8191
		Int4096    :Final[np.uint32] = 4095
		Int2048    :Final[np.uint32] = 2047
		Int1024    :Final[np.uint32] = 1023
		Int512     :Final[np.uint32] = 511
		Int256     :Final[np.uint32] = 255
		Int128     :Final[np.uint32] = 127
		Float8192  :Final[np.uint32] = 8191
		Float4096  :Final[np.uint32] = 4095
		Float2048  :Final[np.uint32] = 2047
		Float1024  :Final[np.uint32] = 1023
		Float512   :Final[np.uint32] = 511
		Float256   :Final[np.uint32] = 255
		Float128   :Final[np.uint32] = 127
		UInt8192H  :Final[np.uint32] = 8191
		UInt4096H  :Final[np.uint32] = 4095
		UInt2048H  :Final[np.uint32] = 2047
		UInt1024H  :Final[np.uint32] = 1023
		UInt512H   :Final[np.uint32] = 511
		UInt256H   :Final[np.uint32] = 255
		UInt128H   :Final[np.uint32] = 127
		Int8192H   :Final[np.uint32] = 8191
		Int4096H   :Final[np.uint32] = 4095
		Int2048H   :Final[np.uint32] = 2047
		Int1024H   :Final[np.uint32] = 1023
		Int512H    :Final[np.uint32] = 511
		Int256H    :Final[np.uint32] = 255
		Int128H    :Final[np.uint32] = 127
		Float8192H :Final[np.uint32] = 8191
		Float4096H :Final[np.uint32] = 4095
		Float2048H :Final[np.uint32] = 2047
		Float1024H :Final[np.uint32] = 1023
		Float512H  :Final[np.uint32] = 511
		Float256H  :Final[np.uint32] = 255
		Float128H  :Final[np.uint32] = 127

class MathF:
	"""Functions and supporting variables"""

	def frexp(bigint: Types.bigIntsUnion64|Types.bigIntsUnion32)->tuple[np.ndarray[int, np.uint64|np.uint32], int]:
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
		'bit'		:0b00000, # np.uint8
		'nybble'	:0b00001, # np.uint8
		'byte'		:0b00010, # np.uint8
		'word'		:0b00011, # np.uint16
		'dword'		:0b00100, # np.uint32
		'qword'		:0b00101, # np.uint64
		'uint128'	:0b00110, # Types.UInt128
		'uint256'	:0b00111, # Types.UInt256
		'uint512'	:0b01000, # Types.UInt512
		'uint1024'	:0b01001, # Types.UInt1024
		'uint2048'	:0b01010, # Types.UInt2048
		'uint4096'	:0b01011, # Types.UInt4096
		#! and more is coming in later versions
	}



