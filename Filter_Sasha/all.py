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
    return quality_score(my_dict['tp'], my_dict['tn'], my_dict['fp'], my_dict['fn'])

def read_classification_from_file(filepath):
    my_dict = {}
    with open(filepath, "rt", encoding='utf-8') as f:
        for line in f:
            key_value = line.split()
            if len(key_value) == 2:
                my_dict[key_value[0]] = key_value[1]

    return my_dict

def write_classification_to_file(filepath, my_dict):
    with open(filepath, "wt", encoding='utf-8') as f:
        for key, value in my_dict.items():
            print(key, value, file=f)

class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def as_dict(self):
        return dict(tp=self.tp, tn=self.tn, fp=self.fp, fn=self.fn)
    
    def update(self, truth, pred):
        if truth not in {self.pos_tag, self.neg_tag}:
            raise ValueError(f"Invalid truth value: {truth}.")
        if pred not in {self.pos_tag, self.neg_tag}:
            raise ValueError(f"Invalid prediction value: {pred}.")

        if pred == self.pos_tag:
            if pred == truth:
                self.tp += 1
            else:
                self.fp += 1
        elif pred == self.neg_tag:
            if pred == truth:
                self.tn += 1
            else:
                self.fn += 1
    
    def compute_from_dicts(self, truth_dict, pred_dict):
        for email_id in truth_dict:
            self.update(truth=truth_dict[email_id], pred=pred_dict[email_id])