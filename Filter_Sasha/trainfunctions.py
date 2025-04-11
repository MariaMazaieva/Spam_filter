import email
from email import policy
from email.parser import Parser
import re
import os
from trainingcorpus import TrainingCorpus

# datapath = 'path/1/'
class TrainFeatures:
    def __init__(self, raw_path):
        self.path_to_mail = raw_path #path to email
        self.count = 0
        # self.path_to_mail = os.path.realpath(raw_path)

    
    def process_directory(self): 
        # counter = 0
        for filename in os.listdir(self.path_to_mail):
            # if counter == 1:
            #     break 
            ''''''''
            if filename.startswith('!'):
                continue
            ''''''''
            file_path = os.path.join(self.path_to_mail, filename) 
            # print(f"Processing file: {file_path}")
            if os.path.isfile(file_path)  :
                
                email_body = self.fopen(file_path) 
                # preprocessed_body = self.preprocess_text(email_body) 
                # print(f"File: {filename}") 
                # print(f"Body: {preprocessed_body}\n")
                # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA----------\n")
               
                # break 

 
    
    def fopen(self):
        counter = 0
        for filename in os.listdir(self.path_to_mail):
            

            # if counter == 1:
            #     break 
            
            ''''''''
            if filename.startswith('!'):
                continue
            ''''''''
            file_path = os.path.join(self.path_to_mail, filename) 
            # # print(f"Processing file: {file_path}")
            # if os.path.isfile(file_path)  :
                
            #     email_body = self.fopen(file_path) 

            print(f"File name: {file_path}")
            if not os.path.exists(file_path):
                print(f"File does not exist: {file_path}")
                return ""
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    msg = email.message_from_file(f, policy=policy.default)
            except Exception as e:
                print(f"Error reading email file: {e}")
                # return ""
            
            print(f"Is email multipart? {msg.is_multipart()}")
            
            body_content = ""
            
            if not msg.is_multipart():
                # pass
                # # Handle non-multipart messages
                body_content = msg.get_payload(decode=True)
                # try:
                #     body_content = msg.get_content()
                #     charset = msg.get_content_charset() or 'utf-8'  # Fallback to 'iso-8859-1'
                #     if charset.lower() == 'default':
                #         charset = 'utf-8'  # Override invalid charset
                #     body_content = body_content.encode('utf-8').decode(charset, errors='ignore')
                #     # print(f"Non-multipart body content: {body_content}")
                # except Exception as e:
                #     print(f"Error decoding non-multipart content: {e}")
                    # continue
            # return body_content
        
        # Handle multipart messages
            if msg.is_multipart():
                for part in msg.iter_parts():
                    content_type = part.get_content_type()
                    content_disposition = part.get_content_disposition()
                    payload = part.get_payload(decode=True)  # Decode content
                    charset = part.get_content_charset() or 'utf-8'
                    
                    # if charset.lower() == 'default':
                    #     charset = 'utf-8'  # Override invalid charset
                    
                    decoded_content = ""
                    if payload:
                        try:
                            decoded_content = payload.decode(charset, errors='ignore')
                        except Exception as e:
                            print(f"Error decoding charset {charset}: {e}")
                    
                    print(f"Content type: {content_type}")
                    # print(f"Part content disposition: {content_disposition}")
                    # print(f"Decoded part content: {decoded_content}")
                    
                    if content_disposition is None and content_type in ['text/plain', 'text/html']:
                        body_content += decoded_content
        
                    print(f"Text body: {body_content} \n")
            counter +=1
            if counter == 15:
                break 

        return body_content


    
    def preprocess_text(self, text): 
        text = text.lower() 
        # text = re.sub(r'\d+', '', text) 
        # text = re.sub(r'\s+', ' ', text) 
        # text = re.sub(r'[^\w\s]', '', text) 
        return text
    
    def print_body_parts(self, spams): 
        for name, email_body in spams: 
            processed_body = self.preprocess_text(email_body) 
            print(f"Email: {name}") 
            print(f"Body: {processed_body}\n")

    
# if __name__== '__main__':
#   corpus = TrainingCorpus('path/1/') 
#   processor = TrainFeatures('path/1/'   ) 
#   counter = 0
# #   processor.process_directory()
#   for filename in os.listdir('path/1/'): 
#     processor.process_directory()
#     if counter == 1:
#         break
#     file_path = os.path.join('path/1/', filename) 
#     email_body = processor.fopen(file_path) 
#     # text = email_body
#     # tokens = re.findall(r'[a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}|https?://\S+|\b\w+\b', text.lower())
#     # print(tokens)
#     print(f"Email Body from {filename}: {email_body}\n") 
#     counter +=1
  
#   spams = list(corpus.spams()) 
# #   print(processor.process_directory())
    


    