# A clean, categorized list of Python's **magic methods** (also known as dunder methods, short for “double underscore”) with short explanations for each. These are the hooks that let you customize how objects behave with built-in operations like arithmetic, comparison, iteration, and more

---

## Arithmetic Operators
These let objects behave like numbers.

| Method         | Purpose                                      |
|----------------|----------------------------------------------|
| `__add__`      | `a + b`                                      |
| `__sub__`      | `a - b`                                      |
| `__mul__`      | `a * b`                                      |
| `__matmul__`   | `a @ b` (matrix multiplication)              |
| `__truediv__`  | `a / b`                                      |
| `__floordiv__` | `a // b`                                     |
| `__mod__`      | `a % b`                                      |
| `__divmod__`   | `divmod(a, b)`                               |
| `__pow__`      | `a ** b` or `pow(a, b)`                      |
| `__lshift__`   | `a << b`                                     |
| `__rshift__`   | `a >> b`                                     |
| `__and__`      | `a & b`                                      |
| `__xor__`      | `a ^ b`                                      |
| `__or__`       | `a \| b`                                     |

### In-place versions (e.g. `a += b`)

| Method         | Purpose                                      |
|----------------|----------------------------------------------|
| `__iadd__`     | `a += b`                                     |
| `__isub__`     | `a -= b`                                     |
| `__imul__`     | `a *= b`                                     |
| `__imatmul__`  | `a @= b`                                     |
| `__itruediv__` | `a /= b`                                     |
| `__ifloordiv__`| `a //= b`                                    |
| `__imod__`     | `a %= b`                                     |
| `__ipow__`     | `a **= b`                                    |
| `__ilshift__`  | `a <<= b`                                    |
| `__irshift__`  | `a >>= b`                                    |
| `__iand__`     | `a &= b`                                     |
| `__ixor__`     | `a ^= b`                                     |
| `__ior__`      | `a \|= b`                                    |

---

## Comparison Operators
These let objects be compared.

| Method     | Purpose                     |
|------------|-----------------------------|
| `__eq__`   | `a == b`                    |
| `__ne__`   | `a != b`                    |
| `__lt__`   | `a < b`                     |
| `__le__`   | `a <= b`                    |
| `__gt__`   | `a > b`                     |
| `__ge__`   | `a >= b`                    |

---

## Type Conversion & Representation
These control how objects look and convert.

| Method       | Purpose                                 |
|--------------|-----------------------------------------|
| `__str__`    | `str(obj)` or `print(obj)`              |
| `__repr__`   | `repr(obj)` (unambiguous representation)|
| `__bytes__`  | `bytes(obj)`                            |
| `__format__` | `format(obj, spec)`                     |
| `__int__`    | `int(obj)`                              |
| `__float__`  | `float(obj)`                            |
| `__bool__`   | `bool(obj)`                             |
| `__complex__`| `complex(obj)`                          |

---

## Container Behavior
These let your act like a list, dict, etc.

| Method         | Purpose                                |
|----------------|----------------------------------------|
| `__len__`      | `len(obj)`                             |
| `__getitem__`  | `obj[key]`                             |
| `__setitem__`  | `obj[key] = value`                     |
| `__delitem__`  | `del obj[key]`                         |
| `__contains__` | `key in obj`                           |
| `__iter__`     | `for x in obj`                         |
| `__next__`     | `next(obj)`                            |
| `__reversed__` | `reversed(obj)`                        |

---

## Object Lifecycle
These control how an object is created and destroyed.

| Method       | Purpose                                  |
|--------------|------------------------------------------|
| `__new__`    | Called before `__init__`, creates object |
| `__init__`   | Initializes the object                   |
| `__del__`    | Called when object is deleted            |
| `__copy__`   | `copy.copy(obj)`                         |
| `__deepcopy__`| `copy.deepcopy(obj)`                    |

---

## Context Managers
These let an object work with `with` statements.

| Method       | Purpose                     |
|--------------|-----------------------------|
| `__enter__`  | Called at start of `with`   |
| `__exit__`   | Called at end of `with`     |

---

## Callable & Attribute Access
These let objects behave like functions or customize attribute access.

| Method         | Purpose                                |
|----------------|----------------------------------------|
| `__call__`     | `obj()` — makes object callable        |
| `__getattr__`  | Called when attribute not found        |
| `__setattr__`  | Called when setting an attribute       |
| `__delattr__`  | Called when deleting an attribute      |
| `__getattribute__`| Called for every attribute access   |

---

## Miscellaneous

| Method         | Purpose                                |
|----------------|----------------------------------------|
| `__sizeof__`   | `sys.getsizeof(obj)`                   |
| `__hash__`     | `hash(obj)`                            |
| `__index__`    | Used in slicing and indexing           |
| `__class__`    | Access the class of the object         |
