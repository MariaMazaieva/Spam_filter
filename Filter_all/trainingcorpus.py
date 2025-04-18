import os
from getemail import GetBody

class TrainingCorpus:
    '''The corpus for training. Reads !truth.txt gile and separates spams and hams'''
    def __init__(self, datapath):
        self.datapath = datapath
        self.truth_path = os.path.join(datapath, "!truth.txt")
        self.truth_dict = self._load_truth() #the dict formed based on the !truth.txt file

    def _load_truth(self):
        truth_dict = {}
        with open(self.truth_path, "rt", encoding="utf-8") as f:
            for line in f:
                filename, label = line.strip().split()
                truth_dict[filename] = label
        return truth_dict

    def get_class(self, filename) -> str:
        return self.truth_dict.get(filename, None)

    def is_ham(self, filename) -> bool:
        return self.get_class(filename) == "OK"

    def is_spam(self, filename) -> bool:
        return self.get_class(filename) == "SPAM"

    def spams(self): #generates spam emails by returning name of the spam file and it's content 
        for filename in os.listdir(self.datapath):
            if filename.startswith("!"):
                continue
            if self.is_spam(filename):
                filepath = os.path.join(self.datapath, filename)
                email = GetBody(filepath)
                yield filename, email.fopen(filepath)

    def hams(self): #generates ham emails by returning name of the spam file and it's content
        for filename in os.listdir(self.datapath):
            if filename.startswith("!"):
                continue
            if self.is_ham(filename):
                filepath = os.path.join(self.datapath, filename)
                email = GetBody(filepath)
                yield filename, email.fopen(filepath)

