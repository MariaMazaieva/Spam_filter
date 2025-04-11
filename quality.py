from utils import read_classification_from_file
from confmat import BCM
import os

def compute_quality_for_corpus(corpus_dir):
    truth_f = os.path.join(corpus_dir, "!truth.txt")
    pred_f = os.path.join(corpus_dir, "!prediction.txt")

    truth = read_classification_from_file(truth_f)
    pred =read_classification_from_file(pred_f)

    bcm = BCM(pos_tag = "SPAM",neg_tag = "OK")
    bcm.compute_from_dicts(truth, pred)
    return quality_score(bcm.tp, bcm.tn, bcm.fp,bcm.fn)


def quality_score(tp, tn, fp, fn ):
    return (tp + tn)/( tp + tn + 10 * fp + fn)