import os
class Corpus:
    def __init__(self, filepath):
        self.fpath = filepath

    def emails(self):
        for file_name in os.listdir(self.fpath):
            if file_name.startswith('!'):
                continue
            file_path = os.path.join(self.fpath, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rt", encoding="utf-8") as f:
                    file_body = f.read()
                    yield file_name, file_body
    
