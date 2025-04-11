class BinaryConfusionMatrix:
    def __init__(self, pos_tag= "SPAM", neg_tag="OK"):
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