from functools import lru_cache

class MyClass():

    def __init__(self, data):
        
        self.data = data

    @property    
    def slow_attribute(self):
        return self._slow_attribute(self.data)
        
    @staticmethod
    @lru_cache
    def _slow_attribute(data):

        # long computation, using data

        return sum(data)

from time import perf_counter_ns

def print_time_and_value_of_computation(c):
    
    t1 = perf_counter_ns()    
    val = c.slow_attribute
    t2 = perf_counter_ns()

    print(f'Time taken: {(t2 - t1)/1000} microseconds')
    print(f'Value: {val}')


c = MyClass(range(10_000))

print_time_and_value_of_computation(c)
print_time_and_value_of_computation(c)

print('Changing the dataset!')
c.data = range(20_000)

print_time_and_value_of_computation(c)
print_time_and_value_of_computation(c)

print('Going back to the original dataset!')
c.data = range(10_000)

print_time_and_value_of_computation(c)