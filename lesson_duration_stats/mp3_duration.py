import numpy as np
from pydub import AudioSegment
import os
import matplotlib.pyplot as plt

class data:

    def __init__(self, path, extension):
        self.path = path
        self.extension = extension

    @classmethod
    def default_init(cls):
        return(cls(path='data', extension='mp3'))

    @property
    def file_list(self):

        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.path):
            for file in f:
                if self.extension in file:
                    files.append(os.path.join(r, file))
        return(files)

    @property
    def lengths_array_seconds(self):

        second_lengths = []
        for f in self.file_list:
            audio = AudioSegment.from_file(f, self.extension)
            second_length = self.get_audio_length(audio)
            second_lengths.append(second_length)
        return(np.array(second_lengths))

    @property
    def lengths_array_minutes(self):
        return self.lengths_array_seconds / 60

    def plot_lengths(self):
        plt.hist(self.lengths_array_minutes)
        plt.xlabel("Duration (minutes)")
        plt.ylabel("Counts")
        plt.show()

    def analyze_histogram(self):
        if(len(self.lengths_array_seconds)<2):
            raise ValueError('Too few files to analyze')
            return None
        standard_dev = np.std(self.lengths_array_minutes)
        mean = np.mean(self.lengths_array_minutes)
        print(f'Standard Deviation = {standard_dev}')
        print(f'Mean = {mean}')


    @staticmethod
    def get_audio_length(audio):
        # might be changed later, to remove silence

        return(len(audio) / 1000) # pydub uses milliseconds

if __name__=='__main__':
    dat = data.default_init()
    dat.plot_lengths()
