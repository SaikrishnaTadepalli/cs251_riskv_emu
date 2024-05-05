#!/usr/bin/env python3

from cpu import CPU
from validator import ValidateARM 

# Sum values from array
code3 = [
    "ADDI X0, X31, #5", 
    "ADD X2, X31, XZR", 
    "ADDI X8, X31, #0", 
    "LDUR X1, [X8, #0]",
    "ADD X2, X2, X1",   
    "SUBI X0, X0, #1",  
    "ADDI X8, X8, #8",  
    "CBNZ X0, #-4",    
]

ValidateARM.validate_code(code3)

# Dmem Values
dmem_config = '''
[16]=1
[24]=2
[32]=3
[40]=4
[48]=5
'''

# Register Values
reg_config = '''
X1=16
X2=5
'''

# __init__(self, code, reg_config = '', dmem_config = '', randomize = False)
cpu3 = CPU('cpu3', code3, reg_config=reg_config, mem_config=dmem_config, randomize=False)

print(cpu3)