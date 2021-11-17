#%%

class Test():

    @staticmethod
    def method(x):
        """
        docstring
        """
        print(x)

    def with_self(self, x):
        
        print(x)

# %%
t = Test()

t.method('3')
# %%
Test.method('3')
# %%

Test.with_self('t', 'x')
# %%
