import numpy as np

# Custom type for storing 1024 byte unsigned integers
class UInt1024:
	"""This is a fixed-size unsigned 8192-bit integer type. It IMMEDIATELY takes 1GB of ram."""

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

	def __add__(self, other: UInt1024)->UInt1024:
		res = UInt1024()
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) + int(other.chunks[i]) + carry
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return res

	def __iadd__(self, other: UInt1024)->UInt1024:
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) + int(other.chunks[i]) + carry
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return self

	def __mul__(self, other: UInt1024)->UInt1024:
		res = UInt1024()
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) * int(other.chunks[i]) + carry
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return res

	def __imul__(self, other: UInt1024)->UInt1024:
		carry = 0
		for i in range(128):
			total = int(self.chunks[i]) * int(other.chunks[i]) + carry
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
			carry = total >> 64
		if carry != 0: raise OverflowError
		return self

	def __sub__(self, other: UInt1024)->UInt1024:
		res = UInt1024()
		for i in range(128):
			total = int(self.chunks[i]) - int(other.chunks[i])
			res.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return res

	def __isub__(self, other: UInt1024)->UInt1024:
		for i in range(128):
			total = int(self.chunks[i]) - int(other.chunks[i])
			self.chunks[i] = total & 0xFFFFFFFFFFFFFFFF
		return self

	def __truediv__(self, other: UInt1024)->UInt1024:
		return self

	def __itruediv__(self, other: UInt1024)->UInt1024:
		return self

	def __floordiv__(self, other: UInt1024)->UInt1024:\
		return self

	def __ifloordiv__(self, other: UInt1024)->UInt1024:\
		return self

	def __mod__(self, other: UInt1024)->UInt1024:
		return self

	def __imod__(self, other: UInt1024)->UInt1024:
		return self

	def __pow__(self, other: UInt1024)->UInt1024:
		return self

	def __ipow__(self, other: UInt1024)->UInt1024:
		return self

	def __neg__(self)->UInt1024:
		return self

	def __pos__(self)->UInt1024:
		return self

	def __abs__(self)->UInt1024:
		return self

	def __and__(self)->UInt1024:
		return self

	def __or__(self)->UInt1024:
		return self

	def __xor__(self)->UInt1024:
		return self

	def __lshift__(self)->UInt1024:
		return self

	def __rshift__(self)->UInt1024:
		return self

	def __iand__(self)->UInt1024:
		return self

	def __ior__(self)->UInt1024:
		return self

	def __ixor__(self)->UInt1024:
		return self

	def __ilshift__(self)->UInt1024:
		return self

	def __irshift__(self)->UInt1024:
		return self

	def __eq__(self)->bool:
		return self

	def __ne__(self)->bool:
		return self

	def __lt__(self)->bool:
		return self

	def __le__(self)->bool:
		return self

	def __gt__(self)->bool:
		return self

	def __ge__(self)->bool:
		return self

	def __new__(self)->UInt1024:
		return self

	def __del__(self)->UInt1024:
		return self

	def __int__(self)->int:
		return self

	def __bool__(self)->bool:
		return self

	def __str__(self)->str:
		return self

	def __bytes__(self)->bytes:
		return self

	def __len__(self)->int:
		return self

	def __getitem__(self)->np.uint64:
		return self

	def __setitem__(self)->UInt1024:
		return self

	def __contains__(self)->bool:
		return self

	def __copy__(self)->UInt1024:
		return self

	def __sizeof__(self)->int:
		return self

# Custom type for storing 1024 byte floats


