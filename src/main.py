#!/usr/bin/env python3

from cpu import CPU

# Sum array problem:
# - Array will be setup in dmem
# - X1 points to base of array
# - X2 has the length of the array
# - X3 points to the last item in the array. Place the result after this

code1 = [
'ADD X4, XZR, XZR',  # Use X4 as scratch register for sum - set it to 0
'LDUR X5, [X1, #0]', # Use X5 as scratch register to hold current array value
'ADD X4, X4, X5',    # Add current array value to running sum
'ADDI X1, X1, #8',   # Increment Array Pointer (use X1)
'SUBI X2, X2, #1',   # Decrement counter (use X2)
'CBNZ X2, #-4',      # If counter is not 0, go to next array item
'STUR X4, [X3, #8]', # Store result 1 place after the last item in the array
]

# Memory Values (pre-initialization)
dmem_config = '''
[16]=1
[24]=2
[32]=3
[40]=4
[48]=5
'''

# Register Values (pre-initialization)
reg_config = '''
X1=16
X2=5
X3=48
'''

# Initialize CPU object.
cpu1 = CPU('Array Sum Example', code1, reg_config, dmem_config)

# CPU prints in hexadecimal by default. Set to decimal.
cpu1.set_print_mode(hex_mode=False) 

# Run ARM code
cpu1.run()

# Steps through ARM code. Use for Debugging.
# cpu1.step() 

# Print CPU state.
print(cpu1)

# Testing Expected Values
assert(cpu1.get_reg_value('X1') == 56) # X1 should point to the address of the last item
assert(cpu1.get_reg_value('X2') == 0)  # X2 should be 0
assert(cpu1.get_reg_value('X4') == 15) # X4 should contain sum: 55
assert(cpu1.get_reg_value('X5') == 5)  # X5 should have the value of the last array item
assert(cpu1.get_double_word(56) == 15) # [96] should contian the sum: 55