import numpy as np
#from pydub import AudioSegment
from mutagen.mp3 import MP3
import os
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

class data:

    def __init__(self, path, extension):
        self.path = path
        self.extension = extension

    @classmethod
    def default_init(cls):
        return(cls(path='data', extension='mp3'))

    @property
    def file_dict(self):

        first_parts = []
        other_parts = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.path):
            for file in f:
                if self.extension in file:
                    split_name = file.split('_')
                    if(len(split_name) == 2):
                        first_parts.append(os.path.join(r, file))
                    elif(len(split_name) == 3):
                        other_parts.append(os.path.join(r, file))
                    else:
                        raise ValueError('Unexpected file in data directory')

        get_date = lambda string: string.split('_')[1].split('.')[0]

        file_dict = {}
        for file in first_parts:
            day = get_date(file)
            parts_list = [file]
            for file2 in other_parts:
                if(get_date(file2) == day):
                    parts_list.append(file2)
            file_dict[day] = parts_list

        return(file_dict)

    @property
    def total_lengths_array(self):

        day_lengths = []
        for key, filelist in self.file_dict.items():
            #audio = AudioSegment.from_file(f, self.extension)
            lengths = []
            for name in filelist:
                second_length = self.get_audio_length(name)
                lengths.append(second_length)
            day_lengths.append(np.sum(np.array(lengths)))
        return(np.array(day_lengths) / 60)

    @property
    def separate_lengths_array(self):

        first_parts = []
        second_parts = []
        for key, filelist in self.file_dict.items():
            #audio = AudioSegment.from_file(f, self.extension)
            lengths = []
            if(len(filelist) == 1):
                length = self.get_audio_length(filelist[0])
                if(length>50*60):
                    # then the whole two-hour lesson was recorded, so...
                    first_parts.append(length/2)
                    second_parts.append(length/2)
                else:
                    first_parts.append(length)
            else:
                first_parts.append(self.get_audio_length(filelist[0]))
                second_parts.append(self.get_audio_length(filelist[1]))

        return((np.array(first_parts)/60, np.array(second_parts)/60))

    def plot_total_lengths(self):
        plt.hist(self.total_lengths_array)
        plt.xlabel("Duration (minutes)")
        plt.ylabel("Counts")
        plt.vlines(90, 0, 4, label = 'Proper lesson time')
        plt.legend()
        plt.show()

    def plot_separate_lengths(self):
        first_parts, second_parts = self.separate_lengths_array
        means = [np.mean(x) for x in [first_parts, second_parts]]
        maximums = [np.max(first_parts), np.max(second_parts), 45]
        minimums = [np.min(first_parts), np.min(second_parts), 45]
        bins = np.linspace(min(minimums), max(maximums), num=10)
        plt.hist([first_parts, second_parts], bins, alpha=0.5,
        label=[f"First parts, mean = {means[0]:.1f}min" , f"Second parts, mean = {means[1]:.1f}min"])

        plt.xlabel("Duration (minutes)")
        plt.ylabel("Counts")
        plt.vlines(45, 0, 2, label = 'Proper lesson time')
        plt.legend()
        plt.show()

    def analyze_histogram(self):
        if(len(self.total_lengths_array)<2):
            raise ValueError('Too few files to analyze')
            return None
        standard_dev = np.std(self.total_lengths_array)
        mean = np.mean(self.total_lengths_array)
        print(f'Standard Deviation = {standard_dev}')
        print(f'Mean = {mean}')


    @staticmethod
    def get_audio_length(name):
        # might be changed later, to remove silence

        #return(len(audio) / 1000) # pydub uses milliseconds
        audio = MP3(name)
        return(audio.info.length)


if __name__=='__main__':
    dat = data.default_init()
    #dat.plot_total_lengths()
    dat.plot_separate_lengths()
