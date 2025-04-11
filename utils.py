
'''budeme potřebovat při učení filtru (pokud jej budeme učit) a při hodnocení úspěšnosti filtrů.
Vstupy:	  cesta k textovému souboru (v našem případě to budou typicky soubory !truth.txt a !prediction.txt)
Výstupy:  dictionary obsahující pro každý název souboru identifikátor SPAM nebo OK
'''
#filepath_truth, filepath_prediction
def read_classification_from_file(filepath):
    slovnik = dict()
    with open(filepath,'rt',encoding = 'utf-8') as f:
        text = f.readlines()
        for line  in text:
            line = line.strip().split() #line has two iems: email and index
            email,index = line
            slovnik[email] = index
            
    return slovnik 





'''
eng_to_cz = {'cat': 'kocka', 'dog': 'pes', 'house': 'dum' }
for eng, cz in eng_to_cz.items():
    print(eng, ',', cz)
'''