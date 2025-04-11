from corpus import Corpus

class BaseFilter:
    def __init__(self,dirpath):
        self.dirpath = dirpath

        pass
    
    def decide(self):
        pass
    '''Vytvoření a nastavení vnitřních datových struktur třídy, 
    aby byly později využitelné metodou test().
    '''
    def train(self, dirpath):

        pass

    def test(self, dirpath):

        corpus = Corpus(dirpath)
        
        pass

    

    