# Is is possible to write a word by concatenating note names?

#%%

from tqdm import tqdm

allowed_words = []
allowed_combinations = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                        'do', 're', 'mi', 'fa', 'sol', 'la', 'si', 
                        'sharp', 'flat']

def check_word(word):  
  while len(word) > 0:
    changed = False
    for ac in allowed_combinations:
      if word[:len(ac)] == ac:
        word = word[len(ac):]
        changed = True
    
    if not changed:
      return False
  
  return True

#%%

with open('words_alpha.txt') as file:
  for line in tqdm(file):
    word = line.split('/')[0].replace('\n', '').lower()
    if check_word(word):
      allowed_words.append(word)
        
# %%
