import re
# 4 * x**3 - 10 * x - 3
def derivative(func, symbol="x"):
    """
    
    @params:
        func:
        symbol:
    @returns:
        derv_func:
    """
    func = func.replace(" ", "")
    array = re.split(r"[+-]", func) # split on + or -
    new_array = []
    for term in array:
        idx_mult = term.find("*")
        if idx_mult != -1:
            if term[idx_mult-1] == "*" or term[idx_mult+1] == "*":
                koeff = 1
                
            else:
                koeff = term[0]

        else:
            koeff = 1

        idx_exp = term.find("**")
        if idx_exp != -1:
            exp = term[idx_exp+2:len(term)]
        else:
            exp = 1

        if term.find(symbol) != -1: 
            new_koeff = int(exp)*int(koeff)
            new_exp = int(exp)-1
            new_const = 0
            
            new_term = str(new_koeff) + "*" + symbol + "**" + str(new_exp)

            new_array.append(new_term)

    derv_func = ""
    for term in new_array:
        derv_func += term + "+"

    return derv_func[:-1] 


