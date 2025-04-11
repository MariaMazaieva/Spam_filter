import os
from getemail import GetBody

class TrainingCorpus:
    def __init__(self, datapath):
        self.datapath = datapath
        self.truth_path = os.path.join(datapath, "!truth.txt")
        self.truth_dict = self._load_truth()

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

    def spams(self):
        for filename in os.listdir(self.datapath):
            if filename.startswith("!"):
                continue
            if self.is_spam(filename):
                filepath = os.path.join(self.datapath, filename)
                email = GetBody(filepath)
                yield filename, email.fopen(filepath)

    def hams(self): # returns filename,
        for filename in os.listdir(self.datapath):
            if filename.startswith("!"):
                continue
            if self.is_ham(filename):
                filepath = os.path.join(self.datapath, filename)
                email = GetBody(filepath)
                yield filename, email.fopen(filepath)

if __name__ == "__main__":
    datapath = "spam-data-12-s75-h25/1/"
    corpus = TrainingCorpus(datapath)

    spams = list(corpus.spams())
    hams = list(corpus.hams())

    print(f"Found {len(spams)} spams and {len(hams)} hams.")
    print("First spam:", spams[0] if spams else "None")
    print("First ham:", hams[0] if hams else "None")
