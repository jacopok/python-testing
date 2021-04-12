import astropy.units as u
import numpy as np

class Continue(Exception):
    pass
continue_loop = Continue()  

def convert_unit(x):
    
    x = x.decompose()
    
    unit = x.unit
    unit_name = str(unit)
    
    eq_units = unit.find_equivalent_units(include_prefix_units=True)
    
    rating = np.inf
    for e in eq_units:
        try:
            e_name = str(e)
            for i in range(min(len(unit_name), len(e_name))):
                if e_name[-i-1] != unit_name[-i-1]:
                    raise continue_loop
            
            val = np.log(x.to(e).value)
            if val < 0:
                val = - 3 * val
            if val <= rating:
                correct_unit = e
                rating = val
        except Continue:
            continue
    
    return(x.to(correct_unit))
