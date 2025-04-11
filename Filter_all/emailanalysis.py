from collections import Counter
import re

class EmailAnalysis:
    '''The class to analyze emails on'''
    def __init__(self, name, body, status = None):
        self.name = name #name of the file with the email
        self.body = body #the text of the mail
        self.status = status #if it has a status like OK or SPAM, if not - None
        self.spam_possibility = 0 # the possibility to be SPAM out of (2)
        self.ham_possibility = 0 # the possibility to be HAM out of (1)
       
        self.spam_words  = Counter ({ 
        "free", "win", "winner", "congratulations", "prize", "cash", "reward", "bonus",
        "jackpot", "lottery", "money", "fortune", "million", "savings", "claim",
        "investment", "loan", "guaranteed", "profit", "debit", "visa","mastercard",
        "act now", "limited time", "hurry", "exclusive", "don't miss", "click here",
        "urgent", "immediate", "important", "deadline", "risk-free", "no obligation",
        "final notice", "get started", "apply now", "bank account", "transfer", "credit card", "paypal",
        "update account", "confidential", "verification", "password",
        "secure transaction", "claim your prize", "refund","discount", "sale", "special offer", 
        "lowest price", "best rates", "order now", "anti-aging", "free trial",
        "affordable", "luxury", "cheap", "bargain", "promotion", "gift", "coupons",
        "buy now", "weight loss", "porn","sex", "subscription", "membership", "newsletter",
        "testimonials", "satisfaction", 
        })

        self.ham_words = Counter({
            "hello", "regards", "business", "please", "meeting", "discussion", "schedule",
            "agenda", "team", "project", "details", "attached",  "deadline", "talk soon", "you soon", "thank",
            "please", "sorry", "regards", "welcome", "appreciate", "sincerely",
            "hello", "hi", "meeting", "update", "confirm",
            "project", "invoice", "document", "report", "plan",
            "information", "details", "attached", "included", "example",
            "mom", "dad", "family", "home", "friend", "school", "weekend", "vacation",
            "dear", "good", "morning", "thanks"
        })
        
    def len_of_email(self):
        return len(self.body.split()) # splits body into words 
    
    def count_of_words(self):
        '''
        Counts clean words in the text
        '''
        words = re.sub(r'<[^>]+>', '', self.body)
        words = words.split()
        return len(words)
    

    def reset_possibilities(self):
        '''
        Reset spam and ham possibilities for a fresh email analysis.
        '''
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
                self.ham_possibility += 5

    def clean_html(self, html_text):
        '''
        Clean HTML content and tokenize the resulting plain text.
        '''
        clean_text = re.sub(r'<[^>]+>', '', html_text) # Remove html commands
        clean_text = re.sub(r'[^\w\s%$@&!?-]', '', clean_text)  # Remove punctuation
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Normalize whitespace
        clean_text = clean_text.lower() # Make all letters lowercase
        tokens = re.findall(r'[a-zA-Z._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}|https?://\S+|\b[a-zA-Z0-9%$@&!?-]+\b', clean_text)
        return tokens # Return words and numbers
    
    def count_probability(self):
        '''
        Updates spam and ham probabilities its body content characteristics 
        '''
        self.reset_possibilities()

        # common_words = self.frequency()
        self.find_suspicious_words()
        self.find_ham_indicators()
        counter_url = self.count_url()
        # Count special characters
        special_chars = self.count_special_characters()

        # Adjust spam possibility based on excessive punctuation
        if special_chars['!'] > 5:  # Excessive exclamation marks
            self.spam_possibility += 5
        if special_chars['?'] > 3:  # Excessive question marks
            self.spam_possibility += 5
        if special_chars['-'] > 8:  # Excessive hyphens
            self.spam_possibility += 8
        if special_chars['$'] > 2:  # Excessive hyphens
            self.spam_possibility += 4
        if special_chars[';'] > 8:  # Excessive hyphens
            self.spam_possibility += 3

        if counter_url >5:
            self.spam_possibility += 2

        # Adjust ham possibility based on personal pronouns
        if self.find_personal_pronoun() >= 3:
            self.ham_possibility += 6
        return self.spam_possibility, self.ham_possibility
    
    def count_special_characters(self):
        '''
        Counts amount of  special characters (?, !, -) in the email body
        '''
        special_chars = {'?': 0, '!': 0, '-': 0,'%': 0,'$': 0,';': 0}
        for char in self.body:
            if char in special_chars:
                special_chars[char] += 1
        return special_chars
                
    def count_url(self):
        '''
        Counts urls in the email
        '''
        text = self.body
        url_pattern = r'https?://[^\s]+'  # Regex to match URLs starting with http or https
        urls = re.findall(url_pattern, text)
        return len(urls)

    def find_personal_pronoun(self): # Counts number of personal pronouns
        personal_pronouns = {'i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours'}
        words = self.clean_html(self.body)
        personal_count = sum(1 for word in words if word in personal_pronouns)
    
        return personal_count
    