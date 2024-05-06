import re

class ValidateARM():
    def extract_immediate_value(instruction):
        match = re.search(r'#(-?\d+)', instruction)
        if match:
            return int(match.group(1))
        return None

    def validate_immediate(immediate, lower_limit, upper_limit):
        return lower_limit <= immediate <= upper_limit

    def validate_instruction(instruction, patterns):
        for pattern, validator in patterns.items():
            match = re.match(pattern, instruction)
            if match:
                return validator(match)
        raise SyntaxError(f"{instruction} does not follow the instruction format")

    def validate_range(match, lower_limit, upper_limit, instruction):
        immediate = int(match.group(1))
        if not ValidateARM.validate_immediate(immediate, lower_limit, upper_limit):
            raise SyntaxError(f"Immediate value in {instruction} is out of range.")
        return True

    def validate_add_sub(match):
        return ValidateARM.validate_range(match, 0, 4095, match.group(0))

    def validate_ldur_stur(match):
        return ValidateARM.validate_range(match, -256, 255, match.group(0))

    def validate_cbnz_cbz(match):
        return ValidateARM.validate_range(match, -262144, 262143, match.group(0))

    def validate_b(match):
        return ValidateARM.validate_range(match, -33554432, 33554431, match.group(0))

    def validate_add(match):
        return True

    def validate_sub(match):
        return True

    def validate(instruction):
        instruction = instruction.upper()

        patterns = {
            r'^\s*ADDI\s+X([0-2]?[0-9]|30|31|ZR)\s*,*\s*X([0-2]?[0-9]|30|31|ZR)\s*,*\s*#(\d+)\s*$': ValidateARM.validate_add_sub,
            r'^\s*SUBI\s+X([0-2]?[0-9]|30|31|ZR)\s*,*\s*X([0-2]?[0-9]|30|31|ZR)\s*,*\s*#(\d+)\s*$': ValidateARM.validate_add_sub,
            r'^\s*LDUR\s+X([0-9]|1[0-9]|2[0-9]|30|31|ZR)\s*,*\s*\[\s*X([0-9]|1[0-9]|2[0-9]|30|31|ZR)\s*,*\s*#(-?\d+)\s*]\s*$': ValidateARM.validate_ldur_stur,
            r'^\s*STUR\s+X([0-9]|1[0-9]|2[0-9]|30|31|ZR)\s*,*\s*\[\s*X([0-9]|1[0-9]|2[0-9]|30|31|ZR)\s*,*\s*#(-?\d+)\s*]\s*$': ValidateARM.validate_ldur_stur,
            r'^\s*CBNZ\s+X([0-9]|1[0-9]|2[0-9]|30|31|ZR)\s*,*\s*#(-?\d+)\s*$': ValidateARM.validate_cbnz_cbz,
            r'^\s*CBZ\s+X([0-9]|1[0-9]|2[0-9]|30|31|ZR)\s*,*\s*#(-?\d+)\s*$': ValidateARM.validate_cbnz_cbz,
            r'^\s*B\s*\s*#(-?\d+)\s*$': ValidateARM.validate_b,
            r'^\s*ADD\s+X([0-2]?[0-9]|30|31|ZR)\s*,*\s*X([0-2]?[0-9]|30|31|ZR)\s*,*\s*X([0-2]?[0-9]|30|31|ZR)\s*$': ValidateARM.validate_add,
            r'^\s*SUB\s+X([0-2]?[0-9]|30|31|ZR)\s*,*\s*X([0-2]?[0-9]|30|31|ZR)\s*,*\s*X([0-2]?[0-9]|30|31|ZR)\s*$': ValidateARM.validate_sub,
        }

        for pattern, validator in patterns.items():
            if re.match(pattern, instruction):
                return validator(re.match(pattern, instruction))

        raise SyntaxError(f"{instruction} does not follow the instruction format")

    # Returns list of strings arm code from a file
    def read_file(filename: str):
        with open(filename, 'r') as file:
            lines = file.readlines()

        return [line.strip() for line in lines]

    # Takes a multiline string and returns a list of strings
    def split_string(arm_code: str):
        return list(filter(lambda x: x != "", arm_code.splitlines()))

    # Takes a list of strings arm code and validates it
    def validate_code(code):
        for line in code:
            try:
                ValidateARM.validate(line)
            except SyntaxError as e:
                print(e)
                raise SyntaxError()
        print('Arm Code Validated!')
