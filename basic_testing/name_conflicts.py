#%%

class Test():

    def __init__(self):
        self.x = 1
    
    @property
    def x(self):
        return 2
        

# %%
t = Test()
t.x
# %%
