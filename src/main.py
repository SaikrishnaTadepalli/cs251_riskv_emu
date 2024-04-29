#!/usr/bin/env python3

import emu
import checker

code1 = [
    "ADD X1,X2,X3 ",
    "SUB X1,X3,X5",
    "ADDI X2,X12,#4095",
    "STUR X2, [X1, #8]",
    "LDUR X4, [X1, #8]",
    "SUBI X6,X4, #1"
]

cpu1 = emu.CPU(0, code1)

code2 = [
    "ADDI X2,X12,#16",
    "STUR X2, [X1, #5]",
    "LDUR X4, [X1, #5]",
    "SUBI X6,X4, #1"
]

cpu2 = emu.CPU(0, code2)

cpu1.run()
cpu2.run()

print(cpu1)

# print(cpu1 == cpu2)

c = checker.CPU_Validator("./schema.json")

print(c.rules_map)