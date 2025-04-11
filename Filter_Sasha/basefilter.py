import os
class BaseFilter:
    
    def train(self, datapath):
        pass

    def decide(self, datapath):
        raise NotImplementedError("The method decide should be implemented")

    def test(self, datapath):
        # Cesta k adresáři s maily. (Adresář nebude obsahovat soubor !truth.txt.)
        # Vytvoří v zadaném adresáři soubor !prediction.txt.
        filepath = os.path.join(datapath, "!prediction.txt")
        with open(filepath, "w+", encoding='utf-8') as f:
            data = (self.decide(datapath))
            for key, value in data.items():
                f.write(f"{key} {value}\n")
        