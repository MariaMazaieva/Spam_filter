import os
from getemail import GetBody
class ImprovedCorpus:
    def __init__(self, filepath):
        self.fpath = filepath

    def emails(self):
        for file_name in os.listdir(self.fpath):
            if file_name.startswith('!'):
                continue
            file_path = os.path.join(self.fpath, file_name)
            if os.path.isfile(file_path):
                file_body = GetBody(file_path)
                f_body = file_body.fopen(file_path)
                yield file_name, f_body
    
if __name__ == '__main__':
    dir = 'spam-data-12-s75-h25/1/'
    corp = ImprovedCorpus(dir)
    
    emails_list = list(corp.emails())
    
    for file_name, body in corp.emails():
        print(f"File: {file_name}")
        print(f"Body:\n{body}\n")