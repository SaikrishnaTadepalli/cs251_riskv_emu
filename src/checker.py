import json

class CPU_Validator():
    def __init__(self, state_path):
        with open(state_path, 'r') as file:
            rules_map = json.load(file)

        self.rules_map = rules_map
        print(self.rules_map)

    def validate_value(num, rule):
        return (num == rule["val"])

    def validate_range(num, rule):
        if (
            ("i_max" in rule and num > rule["i_max"]) or
            ("i_min" in rule and num < rule["i_min"]) or
            ("e_max" in rule and num >= rule["e_max"]) or
            ("e_min" in rule and num <= rule["e_min"])
        ):
            return False

        return True
    
    def validate_rule(num, rule):
        if rule["type"] == "value": res = CPU_Validator.validate_value(num, rule)
        elif rule["type"] == "value": res = CPU_Validator.validate_range(num, rule)
        
        return res == rule["result"]

    def validate_register(register_value, rules):
        for rule in rules:
            if CPU_Validator.validate_rule(register_value, rule) == False: 
                return False
        return True

    def validate_named_registers(cpu, rules):
        for rule in rules:
            register = rule["register"]
            reg_index = cpu.get_reg_index(register)
            reg_value = cpu.registers(reg_index)

            res = CPU_Validator.validate_register(reg_value, rule["rules"])

            if res == False: return False

        return True

    def validate_unnamed_registers(register_values, rules):
        for rule in rules:
            valid = False
            for i, register_val in enumerate(register_values):
                if CPU_Validator.validate_register(register_val, rule):
                    valid = True
                    register_values.pop(i)
                    break
            if valid == False: return False
        return True
            
    def validate_registers(cpu, rules):
        register_pool = {}
        for i, val in enumerate(cpu.registers()):
            register_pool[f"X{i}"] = val

        res1 = CPU_Validator.validate_named_registers(cpu, rules["named"])
        if res1 == False: return False

        for rule in rules["named"]:
            register_pool.pop(rule["register"])
        
        return CPU_Validator.validate_unnamed_registers(
            list(register_pool.values()), rules["unnamed"]
        )


    def validate(self, cpu):
        res = CPU_Validator.validate_registers(cpu, self.rules_map["registers"])
        if (res == False): return False

        


'''
{
    "X2": [
        {
            "type": "value",
            "val": 4,
            "result": false
        },
        {
            "type": "range",
            "i_max": 6,
            "e_min": 1,
            "result": true
        }
    ]
}
'''