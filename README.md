# all.mathematics  
Literally all of math in one file  

Note our usage of other libraries when applicable :3  

## Python Implementation  

### Table of Contents  

- [all.mathematics](#allmathematics)
  - [Python Implementation](#python-implementation)
    - [Table of Contents](#table-of-contents)
    - [License](#license)
    - [System requirements](#system-requirements)
    - [Version Notices](#version-notices)
    - [Types](#types)
    - [Values](#values)
    - [Structure](#structure)
    - [Memory management](#memory-management)
      - [Data size / memory usage](#data-size--memory-usage)
      - [Notes](#notes)
      - [Overhead](#overhead)
      - [Total RAM usage by type](#total-ram-usage-by-type)

---  

### License  

This library is covered by the GNU LGPL v3.0 license    
Read the provided license here: [License](/LICENSE)  
Check the official GNU site here: [www.gnu.org/](https://www.gnu.org/licenses/lgpl-3.0.html)  

GNU LGPL v3.0 is patent-protective and copyleft, covering the developers and contributors from being sued by terminating protections for users should they try to sue.  
The copyleft is what enforces the library to remain under LGPL 3.0, but is weak in the sense that it does not enforce itself onto any works using the library.  
This means you can use this for a project covered by, say, Apache 2.0, MIT, CC0, etc. so long as the license is not strongly copyleft, and you keep the library license the same etc.  

### System requirements  

- Python ≥3.10 (32 or 64-bit)  
- NumPy ≥1.20.0  

NB! Note on 32-bit systems:  
32-bit Python should be able to run this library, but memory limitations (~2-3 GB) make it unsuitable for very  
large arrays or high-precision computation. I recommend using 64-bit Python 3.12+ for either of these usecases if you can.  

There is explicit support for 32-bit, because i know a lot of people in developing / poorer areas that work with  
computer science and programming. I wanted this to be usable by everyone.  
However, if you use a 32-bit version, you will need to manage memory more carefully. I will not limit the power  
of the library for the majority who use 64-bit versions, but 32-bit users will not be excluded either.  

### Version Notices  

This is version 1.  
V2 will have a whole set of new values and such, although do not worry, its designed for retro compatibility.  
My estimate for the largest value storable in v2 is a UInt2097152, or roughly 256kB for one value :3c  

### Types  

- 64 Bit
  - UInt
    - UInt8192
    - UInt4096
    - UInt2048
    - UInt1024
    - UInt512
    - UInt256
    - UInt128
  - Int
    - Int8192
    - Int4096
    - Int2048
    - Int1024
    - Int512
    - Int256
    - Int128
  - Float
    - Float8192
    - Float4096
    - Float2048
    - Float1024
    - Float512
    - Float256
    - Float128
- 32 Bit
  - UInt
    - UInt8192H
    - UInt4096H
    - UInt2048H
    - UInt1024H
    - UInt512H
    - UInt256H
    - UInt128H
  - Int
    - Int8192H
    - Int4096H
    - Int2048H
    - Int1024H
    - Int512H
    - Int256H
    - Int128H
  - Float
    - Float8192H
    - Float4096H
    - Float2048H
    - Float1024H
    - Float512H
    - Float256H
    - Float128H

### Values  

- Fixed size  
  - np.ndarray within
    - Custom dunder modules
  - Initial value: 0
  - Chunks of np.uint64, np.int32 etc.

- Indexing  
  - Indexing bigtypes returns bytes as `np.uint8`  
  - Single index
    - `obj[ np.uint32 ]` / `obj.__getitem__( np.uint32 )`  
    - Regular index behaviour  
    - Return type is a plain `np.uint8`  
  - Slices  
    - `obj[ np.uint32|None : np.uint32|None : np.uint32|None ]` / `obj.__getitem__( slice( np.uint32|None, np.uint32|None, np.uint32|None ))`  
    - Default arguments values are all `None`  
    - Regular slice behaviour - includes start, excludes stop  
      If unspecified, slices from `0` to `len(obj)` in steps of `1`  
    - Return type is `np.ndarray[np.uint8]`  
  - Ellipses  
    - Not supported cant bother just use a slice  

- Logic
  - Per now uses other types' logic for most things  
- ...  

### Structure  

The bigtypes are in essence wrappers around a set of variables, typically a `np.ndarray` and some extra bits.  

- 64 bit compatible types  
  - Unsigned Integers  
    1. Type wrapper  
       1. `__slots__`  
          1. `chunks`  
       2. chunks (`ndarray`)  
          1. Zero-initialized `np.uint64`s  
          Count = typesize / 8 / 8  

          2. `dtype=np.uint64`  
  - Signed Integers  
    1. Type wrapper  
       1. `__slots__`  
          1. `chunks`  
          2. `sign_chunk`  
       2. chunks (`ndarray`)  
          1. Zero-initialized `np.uint64`s  
          Count = ( typesize / 8 / 8 ) - 1  

          2. `dtype=np.uint64`  
       3. sign_chunk (`np.int64`)  
          1. Zero-initialized  
  - Floating Point Numbers
    1. Type wrapper  
       1. `__slots__`  
          1. `mantissa`  
          2. `mantissa_signed`  
          3. `exponent`  
       2. mantissa (`ndarray`)  
          1. Zero-initialized `np.uint64`s  
          Count = ( typesize / 8 / 8 ) - 1  

          2. `dtype=np.uint64`  
       3. mantissa_signed (`np.int64`)  
          1. Zero-initialized  
       4. exponent (`np.uint16`)  
          1. Initialized to a keyword argument, `precision`, which defaults to `16`  
- 32 bit compatible types  
  - Unsigned Integers  
    1. Type wrapper  
       1. `__slots__`  
          1. `chunks`  
       2. chunks (`ndarray`)  
          1. Zero-initialized `np.uint32`s  
          Count = typesize / 8 / 4  

          2. `dtype=np.uint32`  
  - Signed Integers  
    1. Type wrapper  
       1. `__slots__`  
          1. `chunks`  
          2. `sign_chunk`  
       2. chunks (`ndarray`)  
          1. Zero-initialized `np.uint32`s  
          Count = ( typesize / 8 / 4 ) - 1  

          2. `dtype=np.uint32`  
       3. sign_chunk (`np.int32`)  
          1. Zero-initialized  
  - Floating Point Numbers
    1. Type wrapper  
       1. `__slots__`  
          1. `mantissa`  
          2. `mantissa_signed`  
          3. `exponent`  
       2. mantissa (`ndarray`)  
          1. Zero-initialized `np.uint32`s  
          Count = ( typesize / 8 / 4 ) - 1  

          2. `dtype=np.uint32`  
       3. mantissa_signed (`np.int32`)  
          1. Zero-initialized  
       4. exponent (`np.uint16`)  
          1. Initialized to a keyword argument, `precision`, which defaults to `16`  

Example type structure: `Types.Float128`;  

```py
class Float128:
  __slots__ = ['mantissa', 'mantissa_signed', 'exponent']

  def __init__(self, value: int|Types.uintsUnion64|Types.uintsUnion32 = 0, *, 
      precision: int|Types.uintsUnion64|Types.uintsUnion32 = 16):
    self.mantissa = np.uint64(0)
    self.mantissa_signed = np.int64(0)
    self.exponent = np.uint16(precision)
```

Example type structure: `Types.Int2048H`;  

```py
class Int2048H:
  __slots__ = ['chunks', 'signed_chunk']

  def __init__(self, value: int|Types.uintsUnion32 = 0):
    self.chunks = np.zeros(63, dtype=np.uint32)
    self.signed_chunk = np.int32(0)
```

### Memory management  

Refer to these tables for most cases. Additional information is found below.  

Default type sizes:  

|   Type    |   Size in RAM    |
|:---------:|:----------------:|
|    int    |  ~28-36 bytes +  |
|   bool    |       -"-        |

#### Data size / memory usage  

> This does not include overhead like metadata, structure, tags, or padding. See below for overhead and total sizes.  

| Type              | Data size in bits | Data size in bytes | Cleartext |  
|:------------------|:------------------|:-------------------|----------:|  
| `Types.UInt8192`  | 8192              | 1024               |      1 kB |  
| `Types.UInt4096`  | 4096              | 512                |     512 B |  
| `Types.UInt2048`  | 2048              | 256                |     256 B |  
| `Types.UInt1024`  | 1024              | 128                |     128 B |  
| `Types.UInt512`   | 512               | 64                 |      64 B |  
| `Types.UInt256`   | 256               | 32                 |      32 B |  
| `Types.UInt128`   | 128               | 16                 |      16 B |  
| `np.uint64`       | 64                | 8                  |       8 B |  
| `np.uint`         | 64 / 32           | 8 / 4              | 8 B / 4 B |  
| `np.uint32`       | 32                | 4                  |       4 B |  
| `np.uintc`        | 32                | 4                  |       4 B |  
| `np.uint16`       | 16                | 2                  |       2 B |  
| `np.uint8`        | 8                 | 1                  |       1 B |  
| `Types.Int8192`   | 8192              | 1024               |      1 kB |  
| `Types.Int4096`   | 4096              | 512                |     512 B |  
| `Types.Int2048`   | 2048              | 256                |     256 B |  
| `Types.Int1024`   | 1024              | 128                |     128 B |  
| `Types.Int512`    | 512               | 64                 |      64 B |  
| `Types.Int256`    | 256               | 32                 |      32 B |  
| `Types.Int128`    | 128               | 16                 |      16 B |  
| `np.int64`        | 64                | 8                  |       8 B |  
| `np.int`          | 64 / 32           | 8 / 4              | 8 B / 4 B |  
| `np.int32`        | 32                | 4                  |       4 B |  
| `np.intc`         | 32                | 4                  |       4 B |  
| `np.int16`        | 16                | 2                  |       2 B |  
| `np.int8`         | 8                 | 1                  |       1 B |  
| `Types.Float8192` | 8208              | 1026               |      1 kB |  
| `Types.Float4096` | 4112              | 514                |     514 B |  
| `Types.Float2048` | 2064              | 258                |     258 B |  
| `Types.Float1024` | 1040              | 130                |     130 B |  
| `Types.Float512`  | 528               | 66                 |      66 B |  
| `Types.Float256`  | 272               | 34                 |      34 B |  
| `Types.Float128`  | 144               | 18                 |      18 B |  
| `np.float128`     | 128               | 16                 |      16 B |  
| `np.float96`      | 96                | 12                 |      12 B |  
| `np.float64`      | 64                | 8                  |       8 B |  
| `np.float32`      | 32                | 4                  |       4 B |  
| `np.float16`      | 16                | 2                  |       2 B |  

#### Notes  

The bigfloat types use an equivalent bigint and a fitting pointer: e.g. a `Float8192` uses an `Int8192` and a `np.uint16`  
The memory usage is equivalent to these two separately; thus 1 kB + 2 B = 1026 B ≅ 1 kB  
This just allows for a different convention than IEEE 754: Namely that the bit count is the bit count of the MANTISSA.  
The actual biggest value storable is thus any value fitting in the bigint, and decimal values down to a precision of: the bitcount - 1.  
The exponent is also just the plain value instead of being biased  

Everything else follows IEEE standards, simply due to being superstructures utilizing numpy's value types and arrays.  

These bigfloats thus represent, e.g. a `Float8192`, between ∓4095.0 and like 0.000...01;  
 \- an arbitrary variable precision between 8191 and 0 bits.  
This is accomplished as described above by considering the value to be Mantissa/2^Exponent+{decimal value}  
That allows for the exponent to define an arbitrary precision, default is 16 bits.  
In exchange, the exponent cannot be negative, as theres a metaphorical 'slice' from MSB to the exponent, which gives the integer portion,  
and one from the exponent to LSB, giving the decimal section.  

> This is a keyword argument when creating the float, and i hope to have a way to encode a precision in assignment values ready for version 2.   
> or yk, make a function or special value for it idfk yet  

#### Overhead  

Below is a table of the estimated memory usage of the overhead and metadata of types :D  

| Type                               | Overhead size 64-bit | Overhead size 32-bit |  
|:-----------------------------------|---------------------:|---------------------:|  
| bigints                            |                 ~44B |              ~24-28B |  
| biguints                           |                 ~40B |              ~20-24B |  
| bigfloats                          |                 ~48B |              ~24-28B |  
| NumPy scalars (uint64, int8, etc.) |              ~32-40B |              ~24-28B |  
| NumPy arrays (`np.ndarray`)        |             ~96-144B |             ~64-100B |

This is the overhead for just the element itself. Bigtypes contain several values, each of which have overhead of their own.  

#### Total RAM usage by type  

This includes the data and overhead for every element in the super structure as well.  
This is what you should check to see the actual memory usage of the objects you create - simply tally up UwU  

| Type         |                    Memory usage conjecture |                                                                                                       Equation |  
|:-------------|-------------------------------------------:|---------------------------------------------------------------------------------------------------------------:|  
| `UInt8192`   |                   1024 + 40 + 144 = 1208 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt4096`   |                     512 + 40 + 144 = 696 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt2048`   |                     256 + 40 + 144 = 440 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt1024`   |                     128 + 40 + 144 = 312 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt512`    |                      64 + 40 + 144 = 248 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt256`    |                      32 + 40 + 144 = 216 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt128`    |                      16 + 40 + 144 = 200 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `Int8192`    |          8 + 40 + 1016 + 44 + 144 = 1248 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int4096`    |            8 + 40 + 504 + 44 + 144 = 736 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int2048`    |            8 + 40 + 248 + 44 + 144 = 480 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int1024`    |            8 + 40 + 120 + 44 + 144 = 352 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int512`     |             8 + 40 + 56 + 44 + 144 = 288 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int256`     |             8 + 40 + 24 + 44 + 144 = 256 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int128`     |               8 + 40 + 8 + 44 + 40 = 140 B |                                          int raw + int overhead + uint raw + instance overhead + uint overhead |  
| `Float8192`  | 2 + 40 + 8 + 40 + 1016 + 44 + 144 = 1300 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float4096`  |   2 + 40 + 8 + 40 + 504 + 44 + 144 = 778 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float2048`  |   2 + 40 + 8 + 40 + 248 + 44 + 144 = 522 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float1024`  |   2 + 40 + 8 + 40 + 120 + 44 + 144 = 394 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float512`   |    2 + 40 + 8 + 40 + 56 + 44 + 144 = 330 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float256`   |    2 + 40 + 8 + 40 + 24 + 44 + 144 = 298 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float128`   |      2 + 40 + 8 + 40 + 8 + 44 + 40 = 182 B |       exponent raw + exponent overhead + int raw + int overhead + uint raw + instance overhead + uint overhead |  
| `UInt8192H`  |                   1024 + 24 + 100 = 1148 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt4096H`  |                     512 + 24 + 100 = 636 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt2048H`  |                     256 + 24 + 100 = 380 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt1024H`  |                     128 + 24 + 100 = 252 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt512H`   |                      64 + 24 + 100 = 188 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt256H`   |                      32 + 24 + 100 = 156 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `UInt128H`   |                      16 + 24 + 100 = 140 B |                                                             ndarray raw + instance overhead + ndarray overhead |  
| `Int8192H`   |          4 + 28 + 1020 + 28 + 100 = 1180 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int4096H`   |            4 + 28 + 508 + 28 + 100 = 668 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int2048H`   |            4 + 28 + 252 + 28 + 100 = 412 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int1024H`   |            4 + 28 + 124 + 28 + 100 = 284 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int512H`    |             4 + 28 + 60 + 28 + 100 = 220 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int256H`    |             4 + 28 + 28 + 28 + 100 = 188 B |                                    int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Int128H`    |              4 + 28 + 12 + 28 + 28 = 100 B |                                          int raw + int overhead + uint raw + instance overhead + uint overhead |  
| `Float8192H` | 2 + 24 + 4 + 24 + 1020 + 28 + 100 = 1208 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float4096H` |   2 + 24 + 4 + 24 + 508 + 28 + 100 = 696 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float2048H` |   2 + 24 + 4 + 24 + 252 + 28 + 100 = 440 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float1024H` |   2 + 24 + 4 + 24 + 124 + 28 + 100 = 312 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float512H`  |    2 + 24 + 4 + 24 + 60 + 28 + 100 = 248 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float256H`  |    2 + 24 + 4 + 24 + 28 + 28 + 100 = 216 B | exponent raw + exponent overhead + int raw + int overhead + ndarray raw + instance overhead + ndarray overhead |  
| `Float128H`  |     2 + 24 + 4 + 24 + 12 + 28 + 28 = 122 B |       exponent raw + exponent overhead + int raw + int overhead + uint raw + instance overhead + uint overhead |  

Note that this is in bytes, and assumes the highest amount if theres a range of possibilities.  
The realistic memory usage will later be measured with pympler. Until then, these amounts should be assumed.  
