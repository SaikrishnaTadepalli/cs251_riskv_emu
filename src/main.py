#!/usr/bin/env python3

from cpu import CPU

# code1 = [
#     "ADD X1,X2,X3 ",
#     "SUB X1,X3,X5",
#     "ADDI X2,X12,#15",
#     "STUR X2, [X1, #8]",
#     "LDUR X4, [X1, #8]",
#     "SUBI X6,X4, #1"
# ]

# cpu1 = CPU('cpu1', code1)

# cpu1.run()

# print(cpu1)



# code2 = [
#     "ADDI X2,X12,#16",
#     "STUR X2, [X1, #5]",
#     "LDUR X4, [X1, #5]",
#     "SUBI X6,X4, #1"
# ]

# cpu2 = CPU('cpu2', code2)

# cpu2.run()

# print(cpu1 == cpu2)




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

cpu3 = CPU('cpu3 (sum array from mem)', code3)
cpu3.randomize_cpu()

print(cpu3)
input()

cpu3.set_double_word(0, 1)
cpu3.set_double_word(8, 2)
cpu3.set_double_word(16, 3)
cpu3.set_double_word(24, 4)
cpu3.set_double_word(32, 5)
cpu3.set_reg_value('X9', 60)

# print(cpu3)
cpu3.step()
# print(cpu3)

# print(cpu3.registers[0])
# print(cpu3.registers[1])
# print(cpu3.registers[2])
# print(cpu3.registers[2])