# all.mathematics  
Literally all of math in one file  

Note our usage of other libraries when applicable :3  

## Python Implementation  

---  

### Types:  

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
    - This is purely a memory savings optimization. See the chart below for my reason to do this.  

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

  - Slice
  - Ellipses  
- Logic
  - Per now uses other types' logic for most thing like len()
- ...  
