import re
import random

# import instr as Instr
from instr import Instr
from validator import ValidateARM

# number of bytes in data memory
MEMSIZE = 256 

class CPU:
    def __init__(self, 
                 id: any, 
                 code: list[str], 
                 reg_config: str = "", 
                 mem_config: str = "", 
                 randomize: bool = True
                ) -> None:
        # Validate Arm Code
        ValidateARM.validate_code(code)

        self.id = id
        self.pc = 0

        self.code = code

        self.registers = [0] * 32
        self.data_mem = [0] * MEMSIZE
        self.print_mode_hex = True

        if randomize: self.randomize_cpu()
        if reg_config != "": self.config_reg(reg_config)
        if mem_config != "": self.config_mem(mem_config)

    def str_hex(self) -> str:
        def twos_complement_hex(number, num_bits):
            # Calculate the two's complement
            if number < 0: 
                number = (1 << num_bits) + number
            
            # Convert to hexadecimal
            hex_str = hex(number & ((1 << num_bits) - 1))
            
            # Pad with zeros if needed
            hex_str = hex_str[2:].zfill(num_bits // 4)
            hex_str = hex_str.upper()
            
            return ' '.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])
        
        def pad_hex(num, length):
            return twos_complement_hex(num, length * 4)

        def pad_left(data, length, char=' '): 
            data_str = str(data)
            if len(data_str) >= length: return data_str[:length]
            else: return char * (length - len(data_str)) + data_str


        res = f"\nCPU ID: {self.id} {'-' * (65 - len(str(self.id)))}\n\n"
        
        res += f"PC = {self.pc}\n\n"

        res += f"Registers:\n"
        for i in range(0, 16):
            res += f"\t{pad_left(f'X{i}', 4)}: {pad_hex(self.registers[i], 16)}\t||   {pad_left(f'X{i + 16}', 3)}: {pad_hex(self.registers[i + 16], 16)}\n"
        
        res += "\nData Memory:\n"
        for i in range(0, MEMSIZE // 2, 8):
            c_w = MEMSIZE // 2
            c1, c2 = c_w * 0, c_w * 1

            d_hex = lambda x: pad_hex(self.data_mem[x], 2)

            res += f"\t{pad_left(c1 + i, 4)}: {d_hex(c1 + i + 0)} {d_hex(c1 + i + 1)} {d_hex(c1 + i + 2)} {d_hex(c1 + i + 3)} {d_hex(c1 + i + 4)} {d_hex(c1 + i + 5)} {d_hex(c1 + i + 6)} {d_hex(c1 + i + 7)}"
            res += f"   ||  {pad_left(c2 + i, 4)}: {d_hex(c2 + i + 0)} {d_hex(c2 + i + 1)} {d_hex(c2 + i + 2)} {d_hex(c2 + i + 3)} {d_hex(c2 + i + 4)} {d_hex(c2 + i + 5)} {d_hex(c2 + i + 6)} {d_hex(c2 + i + 7)}"
            res += "\n"

        res += f"\n{'-' * 74}\n\n"

        return res
        
    def str_dec(self) -> str:
        def pad_left(data, length, char=' '): 
            data_str = str(data)
            if len(data_str) >= length: return data_str[:length]
            else: return char * (length - len(data_str)) + data_str

        def dec_to_twos_comp(n):
            if n > 0x7FFFFFFFFFFFFFFF:
                return -1 * ((n ^ (0xFFFFFFFFFFFFFFFF)) +1)
            return n

        res = f"\nCPU ID: {self.id} {'-' * (65 - len(str(self.id)))}\n\n"
        
        res += f"PC = {self.pc}\n\n"

        res += f"Registers:\n"
        for i in range(0, 16):
            num1 = dec_to_twos_comp(self.registers[i])
            num2 = dec_to_twos_comp(self.registers[i + 16])
            res += f"\t{pad_left(f'X{i}', 4)}: {pad_left(num1, 23)}\t||   {pad_left(f'X{i + 16}', 3)}: {pad_left(num2, 23)}\n"
        
        res += "\nData Memory:\n"
        for i in range(0, MEMSIZE // 2, 8):
            c_w = MEMSIZE // 2
            c1, c2 = c_w * 0, c_w * 1
            
            num1, num2 = 0, 0
            for j in range(8):
                num1, num2 = num1 << 8, num2 << 8
                num1 += self.data_mem[c1 + i + j]
                num2 += self.data_mem[c2 + i + j]

            num1 = dec_to_twos_comp(num1)
            num2 = dec_to_twos_comp(num2)
            
            res += f"\t{pad_left(c1 + i, 4)}: {pad_left(num1, 23)}\t||   "
            res += f"{pad_left(c2 + i, 4)}: {pad_left(num2, 23)}\n"

        res += f"\n{'-' * 74}\n\n"

        return res
    
    def set_print_mode(self, hex_mode: bool = True) -> None:
        self.print_mode_hex = hex_mode
    
    def __str__(self) -> str:
        if self.print_mode_hex: 
            return self.str_hex()
        else:
            return self.str_dec()

    def __print__(self) -> None:
        print(str(self))

    def reg_eq(cpu1, cpu2) -> bool:
        for R1, R2 in zip(cpu1.registers, cpu2.registers):
            if R1 != R2: return False
        return True
    
    def mem_eq(cpu1, cpu2) -> bool:
        for M1, M2 in zip(cpu1.data_mem, cpu2.data_mem):
            if M1 != M2: return False
        return True

    def __eq__(cpu1, cpu2) -> bool:
        return CPU.reg_eq(cpu1, cpu2) and CPU.mem_eq(cpu1, cpu2)

    def __ne__(cpu1, cpu2) -> bool:
        return CPU.__eq__(cpu1, cpu2) == False

    def write_state(self, file_name: str) -> None:
        cpu_str = str(self)

        f = open(file_name)
        f.write(cpu_str)
        f.close()

    def config_reg(self, reg_config: str) -> None:
        reg_config_list = list(filter(lambda x: x != "", reg_config.splitlines()))
        
        # Regex for: 'X', some number, '=', some number
        inp_pattern = r'X\d+=-?\d+'
        for config in reg_config_list:
            formatted_config = config.replace(" ", "").upper()

            if bool(re.match(inp_pattern, formatted_config)) == False:
                error_msg = f'''
                Invalid reg_config rule.
                Recieved: {config}.
                Expected Pattern: 'XA=VAL'.
                Example: 'X1=4'.
                '''
                raise ValueError(error_msg)
            
            reg, val = formatted_config.split('=')
            value = int(val)
            
            self.set_reg_value(reg, value)

    def config_mem(self, mem_config: str) -> None:
        mem_config_list = list(filter(lambda x: x != "", mem_config.splitlines()))

        # Regex for: '[', some number, ']', '=', some number
        inp_pattern = r'\[\d+\]=-?\d+'
        
        for config in mem_config_list:
            formatted_config = config.replace(" ", "").upper()

            if bool(re.match(inp_pattern, formatted_config)) == False:
                error_msg = f'''
                Invalid mem_config rule.
                Recieved rule: '{config}'.
                Expected Pattern: '[MEM]=VAL'.
                Example: '[8]=32'.
                '''
                raise ValueError(error_msg)
            
            mem, val = formatted_config.split('=')
            
            mem = mem.replace('[', '')
            mem = mem.replace(']', '')

            mem_index = int(mem)
            value = int(val)

            self.set_double_word(mem_index, value)
            
    def get_cur_instr(self) -> str:
        i = (self.pc // 4)
        if i >= len(self.code):
            error_msg = f'''
            PC value out of bounds. 
            Expected PC < {len(self.code) * 4}. Recieved PC = {self.pc}.
            (Expected i < {len(self.code)}. Recieved i = {i}.)'
            '''
            raise IndexError(error_msg)
        return self.code[self.pc // 4].upper()

    def get_reg_index(reg: str) -> int:
        reg = reg.upper()

        error_msg = f'''
            Invalid register. Recieved '{reg}'.
        '''

        if reg == 'XZR': 
            return 31

        if len(reg) < 2: 
            raise ValueError(error_msg)
        
        if reg[0] != 'X':
            raise ValueError(error_msg)
        
        try:
            reg_num = int(reg[1:])
        except ValueError:
            raise ValueError(error_msg)
    
        if reg_num < 0 or reg_num > 31: 
            raise ValueError(error_msg)

        return reg_num
    
    def get_immediate_value(imm: str) -> int:
        error_msg = f'''
            Invalid immediate value. Recieved '{imm}'.
        '''

        if len(imm) <= 1 or imm[0] != '#':
            raise ValueError(error_msg)
        
        try:
            imm_num = int(imm[1:])
        except ValueError:
            raise ValueError(error_msg)

        return imm_num
    
    def validate_double_word_index(self, mem_index: int) -> None:
        if (mem_index % 8) != 0:
            error_msg = f'''
            Invalid double word index.
            Recieved mem_index: [{mem_index}].
            mem_index must be double-word aligned.
            '''
            raise ValueError(error_msg)

        if mem_index + 7 >= len(self.data_mem):
            error_msg = f'''
            Invalid double word index.
            Index out of bounds. 
            Recieved: {mem_index}.
            Maximum Accepted: {len(self.data_mem) - 8}
            '''
            raise ValueError(error_msg)
    
    def get_reg_value(self, reg: str) -> int:
        reg_index = CPU.get_reg_index(reg)
        return self.registers[reg_index]
    
    def set_reg_value(self, reg: str, value: int) -> None:
        reg_index = CPU.get_reg_index(reg)
        self.set_register_val(reg_index, value)
    
    def get_double_word(self, mem_index: int) -> int:
        self.validate_double_word_index(mem_index)
        
        res = 0
        for i in range(8):
            res <<= 8
            res += self.data_mem[mem_index + i]
        return res
    
    def set_double_word(self, mem_index: int, value: int) -> None:
        self.validate_double_word_index(mem_index)
        for i in range(7, -1, -1):
            temp = value & 0xFF
            value >>= 8
            self.set_mem_val(mem_index + i, temp)

    def set_register_val(self, reg_index: int, value: int) -> None:
        if reg_index < 0 or reg_index >= len(self.registers):
            error_msg = f'''
            Invalid Register Index. Recieved {reg_index}.
            '''
            raise IndexError(error_msg)
        
        self.registers[reg_index] = value

    def set_mem_val(self, mem_index: int, value: int) -> None:
        if mem_index < 0 or mem_index >= MEMSIZE:
            error_msg = f'''
            Invalid Memory Index. Recieved {mem_index}.
            '''
            raise IndexError(error_msg)
        
        self.data_mem[mem_index] = value

    def randomize_register(self, reg_index: int) -> None:
        rand_val = random.randrange(2 ** 64)
        self.set_register_val(reg_index, rand_val)

    def randomize_mem_byte(self, byte_index: int) -> None:
        rand_val = random.randrange(2 ** 8)
        self.set_mem_val(byte_index, rand_val)

    def randomize_registers(self) -> None:
        for i in range(len(self.registers) - 1):
            self.randomize_register(i)

    def randomize_data_memory(self) -> None:
        for i in range(len(self.data_mem)):
            self.randomize_mem_byte(i)

    def randomize_cpu(self) -> None:
        self.randomize_registers()
        self.randomize_data_memory()
    
    def run_instr(self) -> None:
        # Get current Instruction
        instr_values = Instr.extract(self.get_cur_instr())
        
        # Seperate Instruction and Instruction Args
        instr, args = instr_values.instr, instr_values.args

        def run_r_type() -> None:
            try:
                XA, XB, XC = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'XB', 'XC'].
                '''
                raise ValueError(error_msg)

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            XC = CPU.get_reg_index(XC)

            if instr == Instr.ADD:
                # Compute value to be put in XA
                new_val = self.registers[XB] + self.registers[XC]
            elif instr == Instr.SUB:
                # Compute value to be put in XA
                new_val = self.registers[XB] - self.registers[XC]
            else:
                error_msg = f'''
                Unknown R-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)
            
            # Place new value in XA
            self.set_register_val(XA, new_val)
            
            # Increment PC to next instruction
            self.pc += 4

        def run_d_type() -> None:
            try:
                XA, XB, IMM = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'XB', 'IMM'].
                '''
                raise ValueError(error_msg)

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            IMM = CPU.get_immediate_value(IMM)

            #Enforcing IMM bounds
            if not (-256 <= IMM <= 255):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected -256 <= IMM <= 255.
                '''
                raise ValueError(error_msg)
            
            mem_index = self.registers[XB] + IMM

            # Memory Access must be double word aligned
            if (mem_index % 8 != 0):
                error_msg = f'''
                Memory Access invalid during D-type instruction.
                Recieved access index = {mem_index}.
                Access Index must be double-word aligned.
                '''
                raise ValueError(error_msg)

            if instr == Instr.LDUR:
                mem_value = self.get_double_word(mem_index)
                self.set_register_val(XA, mem_value)
            elif instr == Instr.STUR:
                reg_val = self.registers[XA]
                self.set_double_word(mem_index, reg_val)
            else:
                error_msg = f'''
                Unknown D-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)
            
            # Increment PC to next instruction
            self.pc += 4

        def run_i_type() -> None:
            try:
                XA, XB, IMM = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'XB', 'IMM'].
                '''
                raise ValueError(error_msg)

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            IMM = CPU.get_immediate_value(IMM)

            # Enforcing IMM bounds
            if not (0 <= IMM <= 4095):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected 0 <= IMM <= 4095.
                '''
                raise ValueError(error_msg)

            if instr == Instr.ADDI:
                # Compute value to be put in XA
                new_val = self.registers[XB] + IMM
            elif instr == Instr.SUBI:
                # Compute value to be put in XA
                new_val = self.registers[XB] - IMM
            else:
                error_msg = f'''
                Unknown I-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)
            
            # Place new value in XA
            self.set_register_val(XA, new_val)
            
            # Increment PC to next instruction
            self.pc += 4

        def run_b_type() -> None:
            try:
                IMM = args[0]
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['IMM'].
                '''
                raise ValueError(error_msg)
            
            IMM = CPU.get_immediate_value(IMM)

            # Enforcing IMM bounds
            if not (-33554432 <= IMM <= 33554431):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected -33 554 432 <= IMM <= 33 554 431.
                '''
                raise ValueError(error_msg)

            # Set new PC value
            self.pc += 4 * IMM

        def run_cb_type() -> None:
            try:
                XA, IMM = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'IMM'].
                '''
                raise ValueError(error_msg)
            
            XA = CPU.get_reg_index(XA)
            IMM = CPU.get_immediate_value(IMM)

            # Enforcing IMM bounds
            if not (-262144 <= IMM <= 262143):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected -262 144 <= IMM <= 262 143.
                ''' 
                raise ValueError(error_msg)
            
            step = 1
            if instr == Instr.CBZ:
                if self.registers[XA] == 0: step = IMM
            elif instr == Instr.CBNZ:
                if self.registers[XA] != 0: step = IMM
            else:
                error_msg = f'''
                Unknown CB-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)

            # Set new PC value
            self.pc += 4 * step

        if instr in Instr.R_TYPE: run_r_type()
        elif instr in Instr.D_TYPE: run_d_type()
        elif instr in Instr.I_TYPE: run_i_type()
        elif instr in Instr.B_TYPE: run_b_type()
        elif instr in Instr.CB_TYPE: run_cb_type()
        else:
            error_msg = f'''
            Invalid Instruction.
            Recieved '{self.get_cur_instr()}' where:
                - 'instr' is '{instr}'
                - 'args' is {args}
            '''
            raise ValueError(error_msg)

    def run(self) -> None:
        while self.pc < len(self.code) * 4:
            self.run_instr()
    
    def step(self) -> None:
        print(f"Executing {'=' * 64}\n")
        print("Initial State: ")
        print(self)
        while self.pc < len(self.code) * 4:
            input()
            print("Instructions:")
            for i, instr in enumerate(self.code):
                line = f"\t{f'{i * 4: >3}'}: " + f"{instr: <25}"
                if i == (self.pc // 4): line += "\t<<< Just Executed"
                print(line)
            self.run_instr()
            print(self)
        print(f"Finished {'=' * 65}")
