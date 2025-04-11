from collections import Counter
import re

from trainingcorpus import TrainingCorpus
from improved_corpus import ImprovedCorpus

COUNT = 30

class EmailAnalysis:
    def __init__(self, name, body, status = None):
        self.name = name #name of the file with the email
        self.body = body #the text of the mail
        self.status = status #if it has a status like OK or SPAM, if not - None
        self.spam_possibility = 0 # the possibility to be SPAM out of (2)
        self.ham_possibility = 0 # the possibility to be HAM out of (1)
       
        # self.spam_word_counter  = Counter ({ 
        # "free", "win", "winner", "congratulations", "prize", "cash", "reward", "bonus",
        # "jackpot", "lottery", "money", "fortune", "million", "savings", "claim",
        # "investment", "loan", "guaranteed", "profit", "debit",
        # "act now", "limited time", "hurry", "exclusive", "don't miss", "click here",
        # "urgent", "immediate", "important", "deadline", "risk-free", "no obligation",
        # "final notice", "get started", "apply now", "bank account", "transfer", "credit card", "paypal",
        # "update account", "confidential", "verification", "password",
        # "secure transaction", "claim your prize", "refund","discount", "sale", "special offer", 
        # "lowest price", "best rates", "order now",
        # "affordable", "luxury", "cheap", "bargain", "promotion", "gift", "coupons",
        # "buy now", "weight loss", "anti-aging", "free trial", "subscription", "membership", "newsletter",
        # "testimonials", "satisfaction", 
        # })
        # self.ham_word_counter  = Counter ({
            
        # })
        

        self.spam_words = Counter({
            "free", "win", "winner", "congratulations", "prize", "cash", "reward", "bonus",
            "lottery", "money", "million", "click here", "buy now", "exclusive", "offer",
            "hurry", "urgent", "limited time", "order now", "guaranteed"
        })

        self.ham_words = Counter({
            "hello", "regards", "business", "please", "meeting", "discussion", "schedule",
            "agenda", "team", "project", "details", "attached","report", "update", "deadline", "talk soon", "you soon"
        })
        
    def reset_possibilities(self):
        """
        Reset spam and ham possibilities for a fresh email analysis.
        """
        self.spam_possibility = 0
        self.ham_possibility = 0

    def find_suspicious_words(self):
        '''
        Check for suspicious words and adjust spam scores
        '''
        for word in self.spam_words:
            if word in self.body.lower():
                self.spam_possibility += 5

    def find_ham_indicators(self):
        '''
        Check for ham-like words and adjust ham scores
        '''
        new_text = self.clean_html(self.body)
        for word in self.ham_words:
            if word in  new_text:
                self.ham_possibility += 10


    

    def clean_html(self, html_text):
        '''
        Clean HTML content and tokenize the resulting plain text.
        '''
        
        # if isinstance(html_text, bytes):
        #     html_text = html_text.decode('utf-8', errors='ignore')
        clean_text = re.sub(r'<[^>]+>', '', html_text)
        clean_text = re.sub(r'[^\w\s%$@&!?-]', '', clean_text)  # Remove punctuation
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Normalize whitespace
        clean_text = clean_text.lower()
        tokens = re.findall(r'[a-zA-Z._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}|https?://\S+|\b[a-zA-Z0-9%$@&!?-]+\b', clean_text)
        return tokens

    def len_of_email(self): # splits body into words 

        length = len(self.body.split())
        # print(f"{length=} {self.status=}\n ")
        return length
    
    def len_of_words(self):
        words = re.sub(r'<[^>]+>', '', self.body)
        words = words.split()
        len_words = len(words)

        # print(f"{len_words=} {self.status=}\n ")

        return len_words
    

    # def count_probability(self):
    #     common_words = self.frequency()
    #    # self.calculate_spam_words_in_text()
    #     '''Spam possib'''
    #     self.find_suspicious_words() 
    #     if self.exclamation_mark_finder() > 5: # if there are a lot of '!'
    #         self.spam_possibility += 10
    #     '''Ham possib'''
    #     if self.find_personal_pronoun() >= 3:
    #         self.ham_possibility += 3
    #     return common_words

    def count_url(self):
        text = self.body
        url_pattern = r'https?://[^\s]+'  # Regex to match URLs starting with http or https
        urls = re.findall(url_pattern, text)
        return len(urls)
    

    def count_probability(self):
        '''
        Updates spam and ham probabilities its body content characteristics 
        '''
        self.reset_possibilities()

        common_words = self.frequency()
        self.find_suspicious_words()
        self.find_ham_indicators()
        self.find_suspicious_phrases()  # Call the new method for phrase detection
        counter_url = self.count_url()
        # Count special characters
        special_chars = self.count_special_characters()

        # Adjust spam possibility based on excessive punctuation
        if special_chars['!'] > 5:  # Excessive exclamation marks
            self.spam_possibility += 6
        if special_chars['?'] > 3:  # Excessive question marks
            self.spam_possibility += 5
        if special_chars['-'] > 8:  # Excessive hyphens
            self.spam_possibility += 5
        if special_chars['$'] > 2:  # Excessive hyphens
            self.spam_possibility += 5
        if special_chars[';'] > 8:  # Excessive hyphens
            self.spam_possibility += 3
        if counter_url >5:
            self.spam_possibility += 3

        if len(self.body.split()) < 20:
            self.spam_possibility += 5


        # Adjust ham possibility based on personal pronouns
        if self.find_personal_pronoun() >= 3:
            self.ham_possibility += 12

        return common_words
    
    def count_special_characters(self):
        '''
        Counts amount of  special characters (?, !, -) in the email body
        '''
        special_chars = {'?': 0, '!': 0, '-': 0,'%': 0,'$': 0,';': 0}
        for char in self.body:
            if char in special_chars:
                special_chars[char] += 1
        return special_chars
    

    # def words_in_ham(self):
        # '''
        # Checks if wrods are in ham counter

        # '''
        # new_text = self.clean_html(self.body)
        
    #     for word in new_text:
    #         if word in self.ham_words:
    #             self.ham_possibility +=5
        



    '''Common part for all the emails behind the status'''

    def frequency(self): # Counts frequencies of words and returns most common words
        new_text = self.clean_html(self.body)
        counter = Counter(new_text) 
        return counter.most_common(COUNT)
    

    def exclamation_mark_finder(self): # Counts exclamation mark
        ex_mark_count = 0
        for c in str(self.body):
            if c == '!':
                ex_mark_count += 1
        return ex_mark_count
    
    # def exclamation_mark_finder(self): # Counts exclamation mark
    #     ex_mark_count = 0
    #     for c in str(self.body):
    #         if c == '!' or c == '&' or c == '?' or c == '-' or c == '%':
    #             ex_mark_count += 1
    #     return ex_mark_count

    def find_suspicious_words(self): 
        body_str = self.body
        body_str = body_str.lower()
        for words in self.spam_words:
            if words in body_str:
                self.spam_possibility += 6
                
        

    def find_personal_pronoun(self): # Counts number of personal pronouns
        personal_pronouns = {'i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours'}
        words = self.clean_html(self.body)
        personal_count = sum(1 for word in words if word in personal_pronouns)
    
        return personal_count
    

    def find_suspicious_phrases(self):
        """
        Detects specific suspicious phrases in the email body and adjusts spam possibility.
        """
        suspicious_phrases = [
            "click here", "buy now", "act now", "limited time",
            "hurry", "exclusive offer", "don't miss", "risk-free",
            "claim your prize", "free trial", "order now", "get started",
            "apply now", "win big", "special offer", "best rates",
            "guaranteed", "weight loss", "save money", "congratulations"
        ]

        body_lower = self.body.lower()  # Convert the body to lowercase for case-insensitive matching
        for phrase in suspicious_phrases:
            if phrase in body_lower:
                # print(f"Suspicious phrase found: {phrase}")  # Debugging output
                self.spam_possibility += 10  # Increase spam possibility for each detected phrase



    

# if __name__== '__main__':

#     dir = 'path/1/'
#     # corpus = TrainingCorpus(dir)
#     # # corpus = ImprovedCorpus(dir)
#     # # email_content = corpus.emails()
#     # spams = list(corpus.spams())
#     # hams = list(corpus.hams())
#     # email_content = hams + spams

#     corpus = TrainingCorpus(dir)
#     spams = list(corpus.spams())
#     hams = list(corpus.hams())
#     counter_spam = 0
#     counter_ham = 0
#     length_spam = 0
#     length_ham = 0
#     len_w_spam = 0
#     len_w_ham = 0

#     for each_spam in spams:
#         analysis = EmailAnalysis(each_spam[0], each_spam[1], 'SPAM')
#         print("File:",analysis.name)
#         length_spam +=analysis.len_of_email()
#         len_w_spam += analysis.len_of_words()
#         counter_spam +=1
#     for each_ham in hams:
#         analysis = EmailAnalysis(each_ham[0], each_ham[1], 'OK')
#         print("File:",analysis.name)
#         length_ham += analysis.len_of_email()
#         len_w_ham += analysis.len_of_words()
#         counter_ham+=1

#     ava_len__spam = length_spam/counter_spam
#     ava_len_ham = length_ham/counter_ham
#     print(f"{counter_ham=} {counter_spam=}\n")
#     print(f"{ava_len_ham=} {ava_len__spam=}\n") 
#     print(f"{(len_w_ham/counter_ham)=} {(len_w_spam/counter_spam)=}\n") 

#     # for fname, fbody in email_content:
#     #     email = EmailAnalysis(fname, fbody)

#     #     print("File:", email.name)
#     #     print(email.len_of_email())
#         # print(email.clean_html(email.body))
#         # print("Click here index:", email.find_suspicious_words())
#         # print("Most common words:", email.frequency())
#         # #print("Sim sentences:", email.similar_sentences())
#         # print("Exclamination mark frequency:", email.exclamation_mark_finder())
#         # print("Lenth is :", email.len_of_email())

#         # print()
        