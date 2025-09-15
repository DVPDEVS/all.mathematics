# all.mathematics  
Literally all of math in one file  

Note our usage of other libraries when applicable :3  

## Python Implementation  

### Table of Contents  

- [all.mathematics](#allmathematics)
  - [Python Implementation](#python-implementation)
    - [Table of Contents](#table-of-contents)
    - [Types](#types)
    - [Values](#values)
    - [Memory management](#memory-management)
      - [Notes](#notes)
      - [Overhead](#overhead)
      - [Total RAM usage by type](#total-ram-usage-by-type)

---  

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
  - Index
    - Uses a 32 bit value of any type, simplest defined in hex or bin
    - Table of structure, as default Little Endian (LE) 
      - Indexes depend on a declaration in Mode Denotion to define which one is applicable.

      | Bit addresses | Use             | Return size in bits | Return size in bytes | Expected Values |
      |---------------|-----------------|---------------------|----------------------|-----------------|
      | 31            | Version flag    | -                   | -                    | 0 ... 1         |
      | 30 ... 27     | Mode denotion   | -                   | -                    | 0 ... 11        |
      | 26 ... 19     | Reserved        | -                   | -                    | 0 ... 511       |
      | 18 ... 16     | Flags           | -                   | -                    | 0 ... 11        |
      | 18            | Sign            | -                   | -                    | 0 ... 1         |
      | 17            | Chunk Selection | -                   | -                    | 0 ... 1         |
      | 16            | Endianness      | -                   | -                    | 0 ... 1         |
      | 15 ... 0      | Bit index       | 1                   | 1/8                  | 0 ... 8191      |
      | 14 ... 0      | Nybble index    | 4                   | 1/2                  | 0 ... 2047      |
      | 13 ... 0      | Byte index      | 8                   | 1                    | 0 ... 1023      |
      | 12 ... 0      | Word index      | 16                  | 2                    | 0 ... 511       |
      | 11 ... 0      | DWord index     | 32                  | 4                    | 0 ... 255       |
      | 10 ... 0      | Qword index     | 64                  | 8                    | 0 ... 127       |
      | 9  ... 0      | UInt128 index   | 128                 | 16                   | 0 ... 63        |
      | 8  ... 0      | UInt256 index   | 256                 | 32                   | 0 ... 31        |
      | 7  ... 0      | UInt512 index   | 512                 | 64                   | 0 ... 15        |
      | 6  ... 0      | UInt1024 index  | 1024                | 128                  | 0 ... 7         |
      | 5  ... 0      | UInt2048 index  | 2048                | 256                  | 0 ... 3         |
      | 4  ... 0      | UInt4096 index  | 4096                | 512                  | 0 ... 1         |
      | 3  ... 0      | NotImplemented  | -                   | -                    | 0               |
      | 2  ... 0      | NotImplemented  | -                   | -                    | 0               |
      | 1  ... 0      | NotImplemented  | -                   | -                    | 0               |
      | 0             | NotImplemented  | -                   | -                    | 0               |

    - The Mode denotion bits say what kind of value youre indexing to, and thus what size value should be expected in LSBs
      - Additionally this will influence the reserved bits used for the actual index values
      - Also note bit 31 is always 0 for these version 1 values. In later versions this can be used for an alternate set of modes.
    
      | Value (bits 31...27) | Value in decimal | Type     | Reserved bits for index value |
      |----------------------|------------------|----------|-------------------------------|
      | 0b00000              | 0                | Bit      | 15 ... 0                      |
      | 0b00001              | 1                | Nybble   | 14 ... 0                      |
      | 0b00010              | 2                | Byte     | 13 ... 0                      |
      | 0b00011              | 3                | Word     | 12 ... 0                      |
      | 0b00100              | 4                | DWord    | 11 ... 0                      |
      | 0b00101              | 5                | Qword    | 10 ... 0                      |
      | 0b00110              | 6                | UInt128  | 9  ... 0                      |
      | 0b00111              | 7                | UInt256  | 8  ... 0                      |
      | 0b01000              | 8                | UInt512  | 7  ... 0                      |
      | 0b01001              | 9                | UInt1024 | 6  ... 0                      |
      | 0b01010              | 10               | UInt2048 | 5  ... 0                      |
      | 0b01011              | 11               | UInt4096 | 4  ... 0                      |
      | 0b01100...0b01111    | 12-15            | Reserved | 0                             |
  
  - The returned values from indexing/slicing will be the corresponding value, such as a big uint type, a np.uint8 for small values, etc.
    - This is purely a memory savings optimization. See the chart below for my reason to do this. I also have a chart further down at [Memory management](#memory-management) which covers memory management in more detail.  

    | Type      | Size in RAM      |
    |-----------|------------------|
    | int       | ~28-36 bytes +   |
    | bool      | int subclass     |
    | np.uint8  | 1 byte           |
    | np.uint16 | 2 bytes          |
    | np.uint32 | 4 bytes          |
    | np.uint64 | 8 bytes          |
    | np.uint   | 4-8 bytes (auto) |
    | np.uintc  | 4 bytes          |

  - Slice and Ellipses  
    The custom types are designed to support the following kinds of indexing:  

  |  Structure                                 |  Type    | Function call                                       | Treated as                    |  
  |:-------------------------------------------|:---------|:----------------------------------------------------|:------------------------------|  
  | `obj[ np.uint32 ]`                         | Index    | `obj.__getitem__( np.uint32 )`                      | `x`                           |  
  | `obj[ np.uint32 : ]`                       | Slice    | `obj.__getitem__( slice( uint32, None, None))`      | `x -> max`                    |  
  | `obj[ : np.uint32 ]`                       | Slice    | `obj.__getitem__( slice( None, uint32, None))`      | `min -> x`                    |  
  | `obj[ np.uint32 : np.uint32 ]`             | Slice    | `obj.__getitem__( slice( uint32, uint32, None))`    | `x -> y`                      |  
  | `obj[ np.uint32 : np.uint32 : ]`           | Slice    | `obj.__getitem__( slice( uint32, uint32, None))`    | `x -> y`                      |  
  | `obj[ np.uint32 : : np.uint32 ]`           | Slice    | `obj.__getitem__( slice( uint32, None, uint32))`    | `x -> max, in steps of z`     |  
  | `obj[ : np.uint32 : np.uint32 ]`           | Slice    | `obj.__getitem__( slice( None, uint32, uint32))`    | `min -> x, in steps of y`     |  
  | `obj[ : np.uint32 : ]`                     | Slice    | `obj.__getitem__( slice( None, uint32, None))`      | `min -> x`                    |  
  | `obj[ np.uint32 : np.uint32 : ]`           | Slice    | `obj.__getitem__( slice( uint32, None, None))`      | `x -> max`                    |  
  | `obj[ np.uint32 : np.uint32 : np.uint32 ]` | Slice    | `obj.__getitem__( slice( uint32, None, None))`      | `x -> max`                    |  
  | `obj[ : : ]`                               | Slice    | `obj.__getitem__( slice( None, None, None))`        | `raise ValueError`            |  
  | `obj[ : ]`                                 | Slice    | `obj.__getitem__( slice( None, None, None))`        | `raise ValueError`            |  
  | `obj[ ... ]`                               | Ellipses | `obj.__getitem__( Ellipses )`                       | `min -> max`                  |  
  | `obj[ ..., np.uint32 ]`                    | Ellipses | `obj.__getitem__(( Ellipses, uint32 ))`             | `min -> x`                    |  
  | `obj[ np.uint32, ... ]`                    | Ellipses | `obj.__getitem__(( uint32, Ellipses ))`             | `x -> max`                    |  
  | `obj[ np.uint32, ..., np.uint32 ]`         | Ellipses | `obj.__getitem__(( uint32, Ellipses, uint32 ))`     | `x -> y`                      |  
  | `obj[ ..., np.uint32, ... ]`               | Ellipses | `obj.__getitem__(( Ellipses, uint32, Ellipses ))`   | `min -> max (must include x)` |  
  | `obj[ ..., np.uint32, np.uint32 ]`         | Ellipses | `obj.__getitem__(( Ellipses, uint32, uint32 ))`     | `min -> y (must include x)`   |  
  | `obj[ np.uint32, np.uint32, ... ]`         | Ellipses | `obj.__getitem__(( uint32, uint32, Ellipses ))`     | `x -> y`                      |  
  | `obj[ np.uint32, ..., ... ]`               | Ellipses | `obj.__getitem__(( uint32, Ellipses ))`             | `x -> max`                    |  
  | `obj[ ..., ..., ... ]`                     | Ellipses | `obj.__getitem__(( Ellipses, Ellipses, Ellipses ))` | `min -> max`                  |  
  | `obj[ ..., ... ]`                          | Ellipses | `obj.__getitem__(( Ellipses, Ellipses ))`           | `min -> max`                  |  

  - Helper function  

    Theres a helper function, `Types.index_encode()` which i heavily suggest using.  
    It mainly takes two arguments, w/o keywords, `mode` and `indexvalue`.  
    From this a `np.uint32` is dynamically created and returned.  
    Contained are the default settings (keyword arguments):  

    - `sign = False | 0`  
    - `littleEndian = True | 1` (translates to endianness, which is little (1) by default)  
    - `version2 = False | 0`  

    and your input values, in the exact structure specified in documentation.  
    `mode` defaults to 2, that is, byte indexing, and `indexvalue` to 0, thus the first byte/8 bits of the big type's value.  
- Logic
  - Per now uses other types' logic for most things  
- ...  

### Memory management  

Refer to these tables for most cases. additional information is found below.  

| Type              | Memory usage in bits | Memory usage in bytes | Cleartext |  
|:------------------|:---------------------|:----------------------|----------:|  
| `Types.UInt8192`  | 8192                 | 1024                  | 1 kB      |  
| `Types.UInt4096`  | 4096                 | 512                   | 512 B     |  
| `Types.UInt2048`  | 2048                 | 256                   | 256 B     |  
| `Types.UInt1024`  | 1024                 | 128                   | 128 B     |  
| `Types.UInt512`   | 512                  | 64                    | 64 B      |  
| `Types.UInt256`   | 256                  | 32                    | 32 B      |  
| `Types.UInt128`   | 128                  | 16                    | 16 B      |  
| `np.uint64`       | 64                   | 8                     | 8 B       |  
| `np.uint`         | 64 / 32              | 8 / 4                 | 8 B / 4 B |  
| `np.uint32`       | 32                   | 4                     | 4 B       |  
| `np.uintc`        | 32                   | 4                     | 4 B       |  
| `np.uint16`       | 16                   | 2                     | 2 B       |  
| `np.uint8`        | 8                    | 1                     | 1 B       |  
| `Types.Int8192`   | 8192                 | 1024                  | 1 kB      |  
| `Types.Int4096`   | 4096                 | 512                   | 512 B     |  
| `Types.Int2048`   | 2048                 | 256                   | 256 B     |  
| `Types.Int1024`   | 1024                 | 128                   | 128 B     |  
| `Types.Int512`    | 512                  | 64                    | 64 B      |  
| `Types.Int256`    | 256                  | 32                    | 32 B      |  
| `Types.Int128`    | 128                  | 16                    | 16 B      |  
| `np.int64`        | 64                   | 8                     | 8 B       |  
| `np.int`          | 64 / 32              | 8 / 4                 | 8 B / 4 B |  
| `np.int32`        | 32                   | 4                     | 4 B       |  
| `np.intc`         | 32                   | 4                     | 4 B       |  
| `np.int16`        | 16                   | 2                     | 2 B       |  
| `np.int8`         | 8                    | 1                     | 1 B       |  
| `Types.Float8192` | 8208                 | 1026                  | 1 kB      |  
| `Types.Float4096` | 4112                 | 514                   | 514 B     |  
| `Types.Float2048` | 2064                 | 258                   | 258 B     |  
| `Types.Float1024` | 1040                 | 130                   | 130 B     |  
| `Types.Float512`  | 528                  | 66                    | 66 B      |  
| `Types.Float256`  | 272                  | 34                    | 34 B      |  
| `Types.Float128`  | 144                  | 18                    | 18 B      |  
| `np.float128`     | 128                  | 16                    | 16 B      |  
| `np.float96`      | 96                   | 12                    | 12 B      |  
| `np.float64`      | 64                   | 8                     | 8 B       |  
| `np.float32`      | 32                   | 4                     | 4 B       |  
| `np.float16`      | 16                   | 2                     | 2 B       |  

#### Notes  

The bigfloat types use an equivalent bigint and a fitting pointer: e.g. a `Float8192` uses an `Int8192` and a `np.uint16`  
The memory usage is equivalent to these two separately; thus 1 kB + 2 B = 1026 B ≅ 1 kB  
This just allows for a different convention than IEEE 754: Namely that the bit count is the bit count of the MANTISSA.  
The actual biggest value storable is thus any value fitting in the bigint, and decimal values down to a precision of: the bitcount - 1.  
The exponent is also just the plain value instead of being biased  

Everything else follows IEEE standards, simply due to being superstructures utilizing numpy's value types and arrays.  

These bigfloats thus represent, e.g. a `Float8192`, between ∓8191.0 and 0.000...01; an arbitrary variable precision of between 8191 and 0 bits.  
This is accomplished as described above by considering the value to be Mantissa/2^Exponent+{decimal value}  
That allows for the exponent to define an arbitrary precision, default is 16 bits.  
In exchange, the exponent cannot be negative, as theres a metaphorical 'slice' from MSB to the exponent, which gives the integer portion,  
and one from the exponent to LSB, giving the decimal section.  

> This is a keyword argument when creating the float, and i hope to have a way to encode a precision in assignment values ready for version 2.   
> or yk, make a function or special value for it idfk yet  

#### Overhead  

Below is a table of the estimated memory usage of the overhead and metadata of elements of the types :D  

| Type                               | Overhead size 64-bit | Overhead size 32-bit |  
|:-----------------------------------|---------------------:|---------------------:|  
| bigfloats                          | ~48B                 | ~24-28B              |  
| bigints, biguints                  | ~40B                 | ~20-24B              |  
| NumPy scalars (uint64, int8, etc.) | ~32-40B              | ~24-28B              |  
| NumPy arrays (`np.ndarray`)        | ~96-144B             | ~64-100B             |  

Note that this does in fact not include overhead from the contained variables, such as an ndarray with actually data in it.  
You need to count the overhead of the contained objects, too.  

#### Total RAM usage by type  

This includes the data and overhead for every element in the super structure as well.  
This is what you should check to see the actual memory usage of the objects you create - simply tally up UwU  

| Type                            | Memory usage                        |  
|:--------------------------------|------------------------------------:|  
| UInt8192                        | 1024 + 40 + 144 + 40 * 128 = 6328 B |  

<!-- This is summing up overhead for the contained elements, stored data, and overhead for the type itself -->
