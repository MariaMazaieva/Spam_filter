import os
import re
import math
from collections import defaultdict
from trainingcorpus import TrainingCorpus
from emailanalysis import EmailAnalysis
from improved_corpus import ImprovedCorpus

SPAM = 1
OK = 0

class MyFilter:
    def __init__(self):
        self.spam_word_counts = defaultdict(int) # Stores the spam words with their frequency
        self.ham_word_counts = defaultdict(int) # Stores the ham words with their frequency
        self.was_training = False # To know if there was training or not
        self.spam_word_total = 0 # The total amount of spam words
        self.ham_word_total = 0 # The total amount of ham words
        self.spam_email_count = 0 # The total amount of spam emails in the training
        self.ham_email_count = 0 # The total amount of spam emails in the training
        self.spam_possibility = 0 # Possibility that the email is spam
        self.ham_possibility = 0 # Possibility that the email is ok
        self.average_spam = 0
        self. average_ham = 0
    
    '''
    Special func for loading SPAM and Ham emails
    Functon loads  emails  in data array 
    returns array of emails named: data
    '''
    def load_data(self,directory):
        data = []
        training_corpus = TrainingCorpus(directory)
        count_ham = 0
        count_spam = 0
        count_words_ham = 0
        count_words_spam = 0
        
        # Loading spam emials using trainning_corpus 
        for filename, email_body in training_corpus.spams():
            analysis = EmailAnalysis(filename, email_body, 'SPAM')
            count_spam+=1
            count_words_spam += analysis.count_of_words()
            
            data.append((self.clean_text(email_body), filename, SPAM))  # 1 is SPAM

        # Loading ham emials using trainning_corpus
        for filename, email_body in training_corpus.hams():
            analysis = EmailAnalysis(filename, email_body, 'OK')
            count_ham+=1
            count_words_ham += analysis.count_of_words()
            data.append((self.clean_text(email_body), filename, OK))  # 0 is OK

        self.average_spam = (count_words_spam)/count_spam
        self.average_ham = (count_words_ham)/count_ham

        return data

    
    '''
    Functon devides text into words
    returns text.split
    '''
    def tokenize(self,text): #Divide text by spaces
        return text.lower().split()
    


    '''
    Trainnig is mostly based on common words in spam and ham like emails.
    - Takes in consideration emails length
    - Upgrates dictinaries
    - Tokanize words 
    - Return: None 
    '''
    def train(self, train_directory):
       
        self.was_training = True
        
        data = self.load_data(train_directory)
        for email_body, filename, label in data: # tuple (text, filename, lable)
            analysis = EmailAnalysis(filename, email_body)
            words = self.tokenize(email_body)

            if label == SPAM: 
                self.spam_email_count += 1
                for word in words:
                    self.spam_word_counts[word] += 1
                    analysis.spam_words.update(word)
                    self.spam_word_total += 1
            else:  # Ham
                self.ham_email_count += 1
                for word in words:
                    self.ham_word_counts[word] += 1
                    analysis.ham_words.update(word)
                    self.ham_word_total += 1

            length_difference_spam = analysis.count_of_words() - self.average_spam
      
            length_difference_ham = analysis.count_of_words() - self.average_ham
        
            if(length_difference_spam > length_difference_ham):
                self.spam_possibility +=10
            else:
                self.ham_possibility += 13



    def predict(self, cleaned_body):
        
        words = self.tokenize(cleaned_body)
        summa  = self.spam_email_count + self.ham_email_count #the total amount of emails in training

        spam_score=0
        ham_score = 0

        if summa !=0: 
            spam_score = math.log(self.spam_email_count / (summa))
            ham_score = math.log(self.ham_email_count / (summa))
       
        spam_words = self.spam_word_total + len(self.spam_word_counts)
        ham_words = self.ham_word_total + len(self.ham_word_counts)

        for word in words:
            if spam_words !=0:
                spam_word_prob = (self.spam_word_counts[word] + 1) / (spam_words)
                spam_score += math.log(spam_word_prob)

            if ham_words !=0:
                ham_word_prob = (self.ham_word_counts[word] + 1) / (ham_words)
                ham_score += math.log(ham_word_prob)

        
        spam_score += (self.spam_possibility )
        ham_score += (self.ham_possibility)


        return SPAM if spam_score > ham_score else OK

    """
    Tests the classifier and generates predictions for emails in the test directory.
    """
    def test(self, test_directory):
        
        corpus = ImprovedCorpus(test_directory)
        emails = corpus.emails()  # returns name and body of a file
        predictions = {}

        for email_name, email_body in emails:
            # Reset possibilities for each email
            spam_possibility = 0
            ham_possibility = 0

            # Preprocess and analyze the email
            cleaned_body = self.clean_text(email_body)
            analysis = EmailAnalysis(email_name, email_body)
            self.spam_possibility, self.ham_possibility = analysis.count_probability()

            # If training was performed, use probabilities; otherwise, rely on heuristics
            if self.was_training:
                spam_possibility += analysis.spam_possibility
                ham_possibility += analysis.ham_possibility
                prediction = self.predict(cleaned_body)
            else:
                spam_possibility += analysis.spam_possibility
                ham_possibility += analysis.ham_possibility
                prediction = 'SPAM' if spam_possibility > ham_possibility else 'OK'

            predictions[email_name] = "SPAM" if prediction == SPAM else "OK"

        # Save predictions to !prediction.txt
        prediction_filepath = os.path.join(test_directory, "!prediction.txt")
        os.makedirs(test_directory, exist_ok=True)
        with open(prediction_filepath, "w", encoding="utf-8") as f:
            for filename, prediction in predictions.items():
                f.write(f"{filename} {prediction}\n")

    
    '''
    Functon 'cleans' our text from html, punctuation and removes whitespaces
    returns text with all lower letters 
    '''
    def clean_text(self,text):
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation ,.!? ect
        text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
        return text.lower() #making everything with lower letters


                    
        
if __name__ == "__main__":

    filter = MyFilter()
    
    #filter.train('path/1/')
    filter.test('path/2/')
