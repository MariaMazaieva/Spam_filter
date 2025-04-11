import os

from utils import read_classification_from_file
from confmat import BinaryConfusionMatrix

def quality_score(tp, tn, fp, fn):
    q = (tp + tn)/(tp + tn + 10*fp + fn)
    return q

def compute_quality_for_corpus(corpus_dir):
    truth_dict = read_classification_from_file(os.path.join(corpus_dir, '!truth.txt'))
    pred_dict = read_classification_from_file(os.path.join(corpus_dir, '!prediction.txt'))
    bcm = BinaryConfusionMatrix()
    bcm.compute_from_dicts(truth_dict, pred_dict)
    my_dict = bcm.as_dict()
    print("result\n")
    return quality_score(my_dict['tp'], my_dict['tn'], my_dict['fp'], my_dict['fn'])

if __name__ =='__main__':
    # print(result")
    result = compute_quality_for_corpus('spam-data-12-s75-h25/2')
    print(result)       