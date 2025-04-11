import os
import random
from basefilter import BaseFilter

class NaiveFilter(BaseFilter):
    def createAnswer(self, datapath):
        for filename in os.listdir(datapath):
            if filename.startswith('!'):
                continue
            filepath = os.path.join(datapath, filename)
            if os.path.isfile(filepath):
                yield filename, 'OK'

    def decide(self, datapath):
        my_dict = {}
        for keys, values in self.createAnswer(datapath):
            my_dict[keys] = values
        return my_dict

class ParanoidFilter(BaseFilter):
    def createAnswer(self, datapath):
        for filename in os.listdir(datapath):
            if filename.startswith('!'):
                continue
            filepath = os.path.join(datapath, filename)
            if os.path.isfile(filepath):
                yield filename, 'SPAM'

    def decide(self, datapath):
        my_dict = {}
        for keys, values in self.createAnswer(datapath):
            my_dict[keys] = values
        return my_dict

class RandomFilter(BaseFilter):
    def createAnswer(self, datapath):
        for filename in os.listdir(datapath):
            if filename.startswith('!'):
                continue
            filepath = os.path.join(datapath, filename)
            if os.path.isfile(filepath):
                answer = random.choice(['OK', 'SPAM'])
                yield filename, answer

    def decide(self, datapath):
        my_dict = {}
        for keys, values in self.createAnswer(datapath):
            my_dict[keys] = values
        return my_dict
    