words = []

with open('copy.txt') as file:
  for line in file:
    word = line.split('/')[0]
    words.append(word)

vowels = ['a', 'e', 'i', 'o', 'u']

shapes = {}

for word in words:
  shape = ''
  for letter in word:
    if letter in vowels:
      shape = shape + 'v'
    else:
      shape = shape + 'c'
  
  if shape in shapes:
    shapes[shape].append(word)
  else:
    shapes[shape] = [word]

def solve(string):
  initial = string[0]
  final = string[-1]
  vcs = string[1:-1]
  if initial in vowels:
    vcs = 'v' + vcs
  else:
    vcs = 'c' + vcs
  if final in vowels:
    vcs = vcs + 'v'
  else:
    vcs = vcs + 'c'

  words = shapes[vcs]
  sol=[]
  for w in words:
    if (w[0] == initial and w[-1] == final):
      sol.append(w)
  return(sol)