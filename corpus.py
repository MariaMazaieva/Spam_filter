import os 
class Corpus:
    def __init__(self,dirpath):
        self.dirpath = dirpath
    
    def emails(self):
        names_files = os.listdir()
        for name in names_files:
            if name.startswith("!"):
                continue
            filepath = os.path.join(self.dirpath, name)
            with open(filepath, "rt", encoding= "UTF-8") as f:
                text = f.read()
                yield filepath, text 
                











# Create corpus from a directory
corpus = Corpus('/path/to/directory/with/emails')
count = 0
# Go through all emails and print the filename and the message body
for fname, body in corpus.emails():
    print(fname)
    print(body)
    print('-------------------------')
    count += 1
print('Finished: ', count, 'files processed.')