#%%

def fizzbuzz(N):
    """Print integers from 1 to N, substituting multiples of 3 with "Fizz",
    multiples of 5 with "Buzz" and multiples of 15 with "FizzBuzz".

    Args:
        N (int): maximum number to print
    """
    
    for i in range(1, N+1):
        out = ''
        
        if i % 3 == 0:
            out += 'Fizz'
        if i % 5 == 0:
            out += 'Buzz'
        if out == '':
            out = i

        print(out)
# %%

fizzbuzz(100)
# %%
