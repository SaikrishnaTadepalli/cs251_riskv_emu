### Comming soon

- C++ Implementation with bindings in Python
- Expanded Architecture: Unified Data and Instruction Memory. L1, L2, L3 caching.
- Expanded ISA: Additional R & D type instructions.
- Assembler + WLP4(C) Compiler

# ARM Emulator

This is a basic ARM emulator written in Python. It emulates a simple ARM single cycle data path.

## Instructions and Restrictions

- **ADD**

  - **Instruction Format:** `ADD XA, XB, XC`
  - **Description:** Add the contents of `XB` and `XC` and stores the sum in `XA`

- **SUB**

  - **Instruction Format:** `SUB XA, XB, XC`
  - **Description:** Subtract the contents of `XC` from `XB` and stores the difference in `XA`

- **LDUR**

  - **Instruction Format:** `LDUR XA, [XB, IMM]`
  - **Description:** Loads the data from memory address `XB + IMM` into register `XA`
  - **Restrictions:**
    - Memory Access must be double-word aligned
    - Immediate value must be in the range [-256, 255]
  - **Example:** `LDUR X1, [X2, #24]` loads data from memory address `X2 + 24` into register `X1`

- **STUR**

  - **Instruction Format:** `STUR XA, [XB, IMM]`
  - **Description:** Stores the data in `XA` into memory address `XB + IMM`
  - **Restrictions:**
    - Memory Access must be double-word aligned
    - Immediate value must be in the range [-256, 255]
  - **Example:** `STUR X1, [X2, #24]` stores the data in `X1` into memory address `X2 + 24`

- **ADDI**

  - **Instruction Format:** `ADDI XA, XB, IMM`
  - **Description:** Add the contents of `XB` and `IMM` and stores the sum in `XA`
  - **Restrictions:**
    - Immediate value must be in the range [0, 4095]

- **SUBI**

  - **Instruction Format:** `SUBI XA, XB, IMM`
  - **Description:** Subtract the value `IMM` from `XB` and stores the difference in `XA`
  - **Restrictions:**
    - Immediate value must be in the range [0, 4095]

- **B**

  - **Instruction Format:** `B IMM`
  - **Description:** Unconditionally branches, incrementing the PC by an offset of `4 * IMM`
  - **Restrictions:**
    - Immediate value must be in the range [-33 554 432, 33 554 431]
  - **Example:** `B #28` sets the program counter to `PC + 4*28`

- **CBZ**

  - **Instruction Format:** `CBZ XA, IMM`
  - **Description:** Incrementing PC by an offset of `4 * IMM` if the content of `XA` is `0`, else moves to next instruction
  - **Restrictions:**
    - Immediate value must be in the range [-262144, 262143]
  - **Example:** `CBZ X1, #8` sets the program counter to `PC + 4*8` if `X1` is `0`, else it moves the program counter to the next instruction

- **CBNZ**
  - **Instruction Format:** `CBNZ XA, IMM`
  - **Description:** Incrementing PC by an offset of `4 * IMM` if the content of `XA` is not `0`, else moves to next instruction
  - **Restrictions:**
    - Immediate value must be in the range [-262144, 262143]
  - **Example:** `CBNZ X1, #8` sets the program counter to `PC + 4*8` if `X1` is not `0`, else it moves the program counter to the next instruction

## Basic Usage

1. Clone the repository: `git clone [URL]`
2. Navigate to the project directory: `cd src`
3. Run the emulator: `./main.py`. (Probably will need to do `chmod u+x main.py` first). This is a sample program.
4. To run your own program, import the CPU class and follow the below examples.

Basic Usage Example:

```python
from cpu import CPU

code1 = [
    # ... ARM Code here
    # (Array of strings, each string being 1 line of ARM code)
]

# DMem Configuration (pre-initialization)
dmem_config = '''
[16]=10
[24]=20
[32]=30
'''

# Registers Configuration (pre-initialization)
reg_config = '''
X10=16
X1=4
'''

# Initialize CPU object
cpu1 = CPU('Array Sum', code1, reg_config=reg_config, mem_config=dmem_config, randomize=False)

# Execute Program
cpu1.run()

# Step through program -> Use to debug
# cpu1.step()

# Set printing mode to decimal. (Hex by default)
cpu1.set_print_mode(hex_mode=False)

# Print CPU final state
print(cpu1)

# Assert Testing
assert(cpu2.get_reg_value('X5') == 5)  # X5 should have value 5
assert(cpu2.get_double_word(56) == 15) # [56] should contain value 15

```

Basic Grading Example:

```python
from cpu import CPU

code1 = [
    # ... ARM Code here
]

code2 = [
    # ... ARM Code here
]

cpu1 = CPU('Solution', code1)
cpu2 = CPU('Student Response', code2)

cpu1.run()
cpu2.run()

# CPU state equality
print(cpu1 == cpu2)

```

## API Functions

### `__init__(self, id, code, reg_config='', mem_config='', randomize=True)`

Instantiates a CPU object. By default, initializes the CPU to random values. This can be overridden to set specific values in registers and data memory.

- `id`: Identifier for the CPU object (use for debugging).
- `code`: Array of strings, each containing a line of ARM source code.
- `reg_config`: String containing configuration for registers
- `mem_config`: String containing configuration for data memory
- `randomize`: Boolean flag used to enable/disable randomizing non-configured CPU values.

Example1:

```python
code = [
    "ADDI X2,X12,#16",
    "STUR X2, [X1, #5]",
]

cpu1 = CPU("first cpu", code)
```

Example2:

```python
code = [
    "ADDI X2,X12,#16",
    "STUR X2, [X1, #5]",
]

# Dmem Values
dmem_config = '''
[16]=1
[24]=2
'''

# Register Values
reg_config = '''
X1=16
X2=5
'''

# __init__(self, code, reg_config = '', dmem_config = '', randomize = False)
cpu3 = CPU('cpu3', code3, reg_config=reg_config, mem_config=dmem_config, randomize=False)
```

### `run(self)`

Executes the program in it's entirety.

Example:

```python
cpu1 = CPU("first cpu", code)

cpu1.run()
```

### `step(self)`

Steps through every instruction of the program, printing the state every time.

Example:

```python
cpu1 = CPU("first cpu", code)

cpu1.step()
```

### `__eq__(cpu1, cpu2)`

Returns `True` if two CPU objects are equal, else `False`. Two CPUs are equal if their registers and data memory both have the same values.

- `cpu1`: CPU object instance
- `cpu2`: CPU object instance

Example:

```python
cpu1 = CPU("first", code1)
cpu1.run()

cpu2 = CPU("second", code2)
cpu2.run()

print(cpu1 == cpu2) # Checking Equality Here
```

Related:

- `__ne__(cpu1, cpu2)`
- `reg_eq(cpu1, cpu2)` - Returns `True` if both CPUs have the same Register values, else `False`
- `mem_eq(cpu1, cpu2)` - Returns `True` if both CPUs have the same Data Memory values, else `False`

### `__print__(self)`

Prints the state of the CPU.

Example:

```python
cpu1 = CPU("first", code1)
cpu1.run()

print(cpu1) # Printing Here
```

Related:

- `__str__(self)` - Returns a string containing the state of the CPU
- `set_print_mode(self, hex_mode: True)` - Use `hex_mode` boolean flag to set printing to decimal/hexadecimal

### `write_state(self, file_name)`

Writes the state of the CPU to a file.

- `file_name`: Name of the file that the state of the CPU is written to. Creates a new file in `file_name` doesn't exist.

Example:

```python
cpu1 = CPU("first", code1)
cpu1.run()

cpu1.write_state("my_cpu_state.txt") # Writing Here
```

### `get_reg_value(self, reg)`

Returns the value in a register.

- `reg`: String containing the name of the register whose value we wish to get.

Example:

```python
cpu1 = CPU("first", code1)
cpu1.run()

reg_val = cpu1.get_reg_value('X1') # Getting value in 'X1' here
```

### `set_reg_value(self, reg, value)`

Sets the value in a register.

- `reg`: String containing the name of the register whose value we wish to get.
- `value`: The new value we wish to place into the register

Example:

```python
cpu1 = CPU("first", code1)

cpu1.set_reg_value('X1', 100) # Setting 'X1' to 100 here
cpu1.set_reg_value('X2', 200) # Setting 'X2' to 200 here
cpu1.set_reg_value('X3', 300) # Setting 'X3' to 300 here

cpu1.run()
```

### `get_double_word(self, mem_index)`

Gets the double-word value at a memory index. Returns a 64-bit value from `mem[mem_index]` to `mem[mem_index + 7]` inclusive, where `mem[i]` is 8-bits of data.

- `mem_index`: Index from which we want to get the value from

Example:

```python
cpu1 = CPU("first", code1)
cpu1.run()

# Getting double-word starting at index 8 here
mem_val = cpu1.get_double_word(8)
```

### `set_double_word(self, mem_index, value)`

Sets the double word value starting at a memory index.

- `mem_index`: Index from which we want to get the value from
- `value`: The new value we want to place into the double word

Example:

```python
cpu1 = CPU("first", code1)

cpu1.set_double_word(24, 150) # Setting mem[24] to 150 here
cpu1.set_double_word(32, 250) # Setting mem[32] to 250 here
cpu1.set_double_word(40, 350) # Setting mem[40] to 350 here

cpu1.run()
```

Related:

- `set_mem_val(self, mem_index, value)` - Sets 1 byte of memory data to a certain value

### `randomize_cpu(self)`

Randomizes the values in the registers and data memory within a CPU.

Example:

```python
cpu1 = CPU("first", code1)

cpu1.randomize_cpu() # Randomizing here

cpu1.run()
```

Related:

- `randomize_register(self, reg_index)` - Randomizes value within a particular register
- `randomize_mem_byte(self, byte_index)` - Randomizes the value within a particular byte of memory
- `randomize_registers(self)` - Randomizes values within the registers
- `randomize_data_memory(self)` - Randomizes values within data memory
