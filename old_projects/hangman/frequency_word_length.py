from collections import defaultdict, Counter, OrderedDict

words_by_length = defaultdict(list)

with open('copy.txt') as file:
  for line in file:
    word = line.split('/')[0].replace('\n', '')
    words_by_length[len(word)].append(word)

distribution = defaultdict(Counter)

for length, words in words_by_length.items():
  for word in words:
    for char in word:
      distribution[length][char.lower()] += 1
      
for length in distribution:
  distribution[length] = OrderedDict(sorted(distribution[length].items()))
