# pylint: disable=line-too-long, invalid-name, import-error, multiple-imports, unspecified-encoding, broad-exception-caught, trailing-whitespace, no-name-in-module, unused-import

import resource_calculator
import sys, os

HOW_TO_USE = """
1. Enter the name and amount (like this: Comp_Name Amount) of the component you want to calculate the cost of.
2. When entering amount, you can use simple math signs (+, -, *, /), but without brackets.
3. You can enter multiple components.
4. Enter !all to get names of all the components.
5. Enter 0 to get cost."""
BRAKES = "\n--------------------------------------------------------\n"
SUPPORTED_MATH_SIGNS = {'+':lambda r, l: r+l, 
                        '-':lambda r, l: r-l, 
                        '*':lambda r, l: r*l, 
                        '/':lambda r, l: r/l}


def calculate_cost(calc:resource_calculator.ResourceCalculator, id, count, cost={}): # omg i love recursion
    if calc.is_primary(id):
        if id in cost:
            cost[id] += count
        else:
            cost[id] = count
        
        return 
    else:
        components = calc.get_craft_components(id)
        
        for i in components.keys():
            calculate_cost(calc, i, count*components[i], cost)
        
        return 

def parce_math(string:str, sign:str):
    index = string.rfind(sign)
    
    part_r, part_l = string[:index], string[index+1:]
    
    for i in SUPPORTED_MATH_SIGNS.keys():
        rf = part_l.rfind(i)
        if rf not in (-1, 0):
            part_l = parce_math(part_l, i)
            break
    
    for i in SUPPORTED_MATH_SIGNS.keys():
        rf = part_r.rfind(i)
        if rf not in (-1, 0):
            part_r = parce_math(part_r, i)
            break

    return SUPPORTED_MATH_SIGNS[sign](int(part_r), int(part_l))
    

def main():
    print("DEV DATA: " + sys.executable)
    print(f"HOW TO USE: {HOW_TO_USE}")
    
    config_name = 'resources.json'
    
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    calc = resource_calculator.ResourceCalculator(os.path.join(application_path, config_name))
    
    a = input()
    
    cost = {}
    
    while a != "0":
        if a.replace(" ", "") == "!all":
            print(BRAKES)
            
            for i in calc.get_all_components_ids():
                comp_names = calc.get_all_component_names(i)
                print(f"{comp_names[0]} (or {','.join(comp_names[1:])})")
            
            print(BRAKES)
            
            a = input()
            continue
            
        
        try:
            res = " ".join(a.split(" ")[:-1])
            count = a.split(" ")[-1]
        except ValueError:
            print(f"Invalid input: {a}")
            a = input()
            continue
        
        
        for i in SUPPORTED_MATH_SIGNS.keys():
            rf = count.rfind(i)
            if rf not in (-1, 0):
                count = parce_math(count, i)
                break
                
        count = int(count)
        
        
        id = calc.get_component_by_name(res)
        
        if id is None:
            a = input()
            continue
        
        cost_out = calculate_cost(calc, id, count, cost)
        
        a = input()
    
    print(BRAKES)
    for i in cost.keys():
        print(f"{calc.get_component_name_by_id(i)}: {cost[i]}")
    
    input("Press Enter to exit...")
        

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Some error occured:", e)
        input("Press Enter to exit...")