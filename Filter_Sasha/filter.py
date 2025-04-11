import os
from collections import Counter
from trainingcorpus import TrainingCorpus
from emailanalysis import EmailAnalysis
from improved_corpus import ImprovedCorpus
import math

class MyFilter:

    def __init__(self):
        self.was_training = False
        self.spam_words = Counter()  
        self.ham_words = Counter()  
        self.spam_possibility = 0
        self.ham_possibility = 0
        self.average_spam = 0
        self.average_ham = 0

    def train(self, path_to_truth):
        self.was_training = True
        self.path_to_truth= path_to_truth
        corpus = TrainingCorpus(path_to_truth)
        spams = list(corpus.spams())
        hams = list(corpus.hams())
        counter_spam = 0
        length_spam = 0
        len_w_spam = 0
        counter_ham = 0
        length_ham = 0
        len_w_ham = 0
        for each_spam in spams:
            analysis = EmailAnalysis(each_spam[0], each_spam[1], 'SPAM')
            self.spam_words.update(analysis.frequency()) # returns most common words in file
            counter_spam += 1
            length_spam +=analysis.len_of_email() # length of a body email part with only split()
            len_w_spam += analysis.len_of_words() # length of a split and HTML clean email
        self.average_spam = len_w_spam/counter_spam
        
        for each_ham in hams:
            analysis = EmailAnalysis(each_ham[0], each_ham[1], 'OK')
            self.ham_words.update(analysis.frequency()) # returns most common words in file
            counter_ham += 1
            length_ham +=analysis.len_of_email() # length of a body email part with only split()
            len_w_ham += analysis.len_of_words() # length of a split and HTML clean email
        self.average_ham = len_w_ham/counter_ham

    '''function adds spam words to the counter and decides SPAM or OKay '''
    def decide(self, email_body, analysis):
        words = analysis.clean_html(email_body)
        summa_spam =  sum(self.spam_words.values()) + len(self.spam_words)
        summa_ham =  sum(self.ham_words.values()) + len(self.ham_words)
        for word in words:
            
            if summa_spam != 0:
                spam_prob = (self.spam_words[word] + 1) / (summa_spam )
        
            if summa_ham != 0:
                ham_prob = (self.ham_words[word] + 1) / (summa_ham)
            
            if spam_prob != 0:
                self.spam_possibility += math.log(spam_prob)

            if ham_prob != 0:
                self.ham_possibility += math.log(ham_prob)

        length_difference_spam = analysis.len_of_words() - self.average_spam
      
        length_difference_ham = analysis.len_of_words() - self.average_ham
        
        if(length_difference_spam >= length_difference_ham):
            self.spam_possibility +=40
        else:
            self.ham_possibility += 6


        # Feature-based adjustments
        self.spam_possibility += analysis.spam_possibility
        self.ham_possibility += analysis.ham_possibility

        # Final decision
        if self.spam_possibility > self.ham_possibility:
            return 'SPAM'
        else:
            return 'OK'
        
        
    def common_words_in_spam_ham(self, array_of_words):
        if array_of_words:
            spam_count = 0
            ham_count = 0
            for word in array_of_words:
                for spam_w in self.spam_words:
                    if word == spam_w:
                        spam_count += 1
                for ham_w in self.ham_words:
                    if word == ham_w:
                        ham_count += 1
            self.spam_possibility += spam_count/len(array_of_words) 
            self.ham_possibility += ham_count/len(array_of_words)
        
    def general_spam_check(self):
        if self.spam_possibility > self.ham_possibility:
            return 'SPAM'
        else:
            return 'OK'
     
    def test(self, path_to_pred):
        corpus = ImprovedCorpus(path_to_pred) # returns body 
        emails = corpus.emails() # returns name and body of a file 
        predictions = {}

        for email in emails:
            email_name, email_body = email

            analysis = EmailAnalysis(email_name, email_body)
            common_words = analysis.count_probability()
            if self.was_training:
                self.common_words_in_spam_ham(common_words)
            self.spam_possibility += analysis.spam_possibility
            self.ham_possibility += analysis.ham_possibility

            if self.was_training:
                prediction = self.decide(email_body, analysis)
            else:
                prediction = self.general_spam_check()
            
            predictions[email_name] = prediction

            self.spam_possibility = 0
            self.ham_possibility = 0

        filepath = os.path.join(path_to_pred, "!prediction.txt")
        with open(filepath, "w", encoding='utf-8') as f:
            for email_name, prediction in predictions.items():
                f.write(f"{email_name} {prediction}\n")


if __name__ == '__main__':
    filter = MyFilter()
    
    filter.train('path/1/')
    filter.test('path/2/')