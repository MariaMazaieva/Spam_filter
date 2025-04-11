import os
import re
import math
from collections import defaultdict
from trainingcorpus import TrainingCorpus
from emailanalysis import EmailAnalysis
from improved_corpus import ImprovedCorpus

SPAM = 1
OK = 0

'''
Functon 'cleans' our text from html, punctuation and removes whitespaces
returns text with all lower letters 
'''
def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation ,.!? ect
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text.lower() #making everything with lower letters


'''
Functon devides text into words
returns text.split
'''
def tokenize(text): #Divide text bz spaces
    return text.lower().split()


'''
Special func for loading SPAM and Ham emails
Functon loads  emails  in data array 
returns array of emails named: data
'''

def load_data(directory):
    data = []
    training_corpus = TrainingCorpus(directory)

    # Loading spam emials using trainning_corpus 
    for filename, email_body in training_corpus.spams():
        data.append((clean_text(email_body), filename, SPAM))  # 1 is SPAM

    # Loading ham emials using trainning_corpus
    for filename, email_body in training_corpus.hams():
        data.append((clean_text(email_body), filename, OK))  # 0 is OK

    return data

# def load_data_general(path_to_pred):
#     data = []
#     corpus = ImprovedCorpus(path_to_pred)
#     training_corpus = TrainingCorpus(path_to_pred)
#     emails = corpus.emails()
    
#     # Load spam emails
#     for filename, email_body in training_corpus.spams():
#         data.append((clean_text(email_body), filename, SPAM))  # 1 for SPAM

#     # Load ham emails
#     for filename, email_body in training_corpus.hams():
#         data.append((clean_text(email_body), filename, OK))  # 0 for OK

#     return data



#  
class MyFilter:
    def __init__(self):
        self.spam_word_counts = defaultdict(int)
        self.ham_word_counts = defaultdict(int)
        self.was_training = False
        self.spam_word_total = 0
        self.ham_word_total = 0
        self.spam_email_count = 0
        self.ham_email_count = 0
        self.spam_possibility = 0
        self.ham_possibility = 0

    def train(self, train_directory):
        '''
        Trainnig is mostly based on common words in spam and ham like emails.
        - Takes in consideration emails length
        - Upgrates dictinaries
        - Tokanize words 
        - Return: None 
        '''
        self.was_training = True
        
        data = load_data(train_directory)
        for email_body, filename, label in data: # tuple (text, filename, lable)
            analysis = EmailAnalysis(filename, email_body)
            words = tokenize(email_body)

            length_difference_spam = analysis.len_of_words() - self.average_spam
      
            length_difference_ham = analysis.len_of_words() - self.average_ham
        
            if(length_difference_spam >= length_difference_ham):
                self.spam_possibility +=7
            else:
                self.ham_possibility += 15

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





    def predict(self, cleaned_body):
        
        words = tokenize(cleaned_body)
        summa  = self.spam_email_count + self.ham_email_count


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

            
            

        
        


        return 1 if spam_score > ham_score else 0


    def general_spam_check(self):
        if self.spam_possibility > self.ham_possibility:
            return 'SPAM'
        else:
            return 'OK'
        

    
        

    def test(self, test_directory):
        """
        Tests the classifier and generates predictions for emails in the test directory.
        """
        corpus = ImprovedCorpus(test_directory)
        emails = corpus.emails()  # returns name and body of a file
        predictions = {}

        for email_name, email_body in emails:
            # Reset possibilities for each email
            spam_possibility = 0
            ham_possibility = 0

            # Preprocess and analyze the email
            cleaned_body = clean_text(email_body)
            analysis = EmailAnalysis(email_name, email_body)
            analysis.count_probability()

            # If training was performed, use probabilities; otherwise, rely on heuristics
            if self.was_training:
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

        # print(f"Predictions saved to {prediction_filepath}")


                    



        
if __name__ == "__main__":
    # # Paths to training and testing directories
    # train_directory = "path/1"
    # test_directory = "path/2"

    # # Load training data
    # train_data = load_data(train_directory)

    # # Train the classifier
    # classifier = MyFiler()
    # classifier.train(train_data)

    # # Load testing data
    # test_data = load_data(test_directory)

    # # Evaluate the classifier on the test data
    # accuracy = evaluate(classifier, test_data)

    # # Generate predictions for the testing data
    # predictions = {}
    # for text, filename, label in test_data:
    #     prediction = classifier.predict(text)
    #     predictions[filename] = "SPAM" if prediction == 1 else "OK"




    # prediction_filepath = os.path.join(test_directory, "!prediction.txt")
    # with open(prediction_filepath, "w", encoding="utf-8") as f:
    #     for filename, prediction in predictions.items():
    #         f.write(f"{filename} {prediction}\n")

    filter = MyFilter()
    
    #filter.train('path/1/')
    filter.test('path/2/')




    # def decide(self, email_body, analysis):
    #     words = analysis.clean_html(email_body)
    #     summa_spam =  sum(self.spam_words.values()) + len(self.spam_words)
    #     summa_ham =  sum(self.ham_words.values()) + len(self.ham_words)
    #     for word in words:
            
    #         if summa_spam != 0:
    #             spam_prob = (self.spam_words[word] + 1) / (summa_spam )
        
    #         if summa_ham != 0:
    #             ham_prob = (self.ham_words[word] + 1) / (summa_ham)
            
    #         if spam_prob != 0:
    #             self.spam_possibility += math.log(spam_prob)

    #         if ham_prob != 0:
    #             self.ham_possibility += math.log(ham_prob)

    #     length_difference_spam = analysis.len_of_words() - self.average_spam
      
    #     length_difference_ham = analysis.len_of_words() - self.average_ham
        
    #     if(length_difference_spam >= length_difference_ham):
    #         self.spam_possibility +=15
    #     else:
    #         self.ham_possibility += 6


    #     # Feature-based adjustments
    #     self.spam_possibility += analysis.spam_possibility
    #     self.ham_possibility += analysis.ham_possibility

    #     # Final decision
    #     if self.spam_possibility > self.ham_possibility:
    #         return 'SPAM'
    #     else:
    #         return 'OK'