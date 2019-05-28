import numpy as np
from pydub import AudioSegment
import os
import matplotlib.pyplot as plt

path = 'data'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.mp3' in file:
            files.append(os.path.join(r, file))

second_lengths = []

for f in files:
    print("Analyzing " + f)
    audio = AudioSegment.from_mp3(f)
    second_length = len(audio) / 1000 # pydub 
    second_lengths.append(second_length)
    print(f"{second_length} seconds")

minute_lengths = np.array(second_lengths) / 60

plt.hist(minute_lengths)
plt.xlabel("Duration (minutes)")
plt.ylabel("Counts")

if(len(minute_lengths)>2):
    print(f'Standard Deviation = {np.std(minute_lengths)}')
    print(f'Mean = {np.mean(minute_lengths)}')
