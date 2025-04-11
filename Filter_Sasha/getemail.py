import email
from email import policy

# datapath = 'spam-data-12-s75-h25/1/'
class GetBody:
    def __init__(self, raw_path):
        self.path_to_mail = raw_path #path to email
    
 
    '''Function returns 'body' part of an email'''
    def fopen(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            msg = email.message_from_file(f,policy=policy.default)
            
        body_content = ""
        
        if not msg.is_multipart(): #check if file has multipul parts 

            payload = msg.get_payload(decode=True)
            if payload:
                body_content = payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore')

        if msg.is_multipart():
            for part in msg.iter_parts():
                content_type = part.get_content_type()
                content_disposition = part.get_content_disposition()
                payload = part.get_payload(decode=True)  # Decode content
                charset = part.get_content_charset() or 'utf-8' # Detect encoding 

                decoded_content = ""
                if payload:
                    try:
                        decoded_content = payload.decode(charset, errors='ignore') # Decode message 
                    except Exception as e:
                        print(f"Error decoding charset {charset}: {e}")
                
                if content_disposition is None and content_type in ['text/plain', 'text/html']:
                    body_content += decoded_content


        # print("Body type:", type(body_content))
        return body_content



    