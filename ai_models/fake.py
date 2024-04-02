from faker.providers import BaseProvider
import random, re, spacy
from ai_utils.patterns import fake_possible_methods, dummy_data_not_available_responses
from ai_utils.keywords import dummy_data_keywords
from jinja2 import Template

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class FakeAIModel(BaseProvider):
    def ipv4_address(self):
        octets = [str(self.random_int(min=0, max=255)) for _ in range(4)]
        return ".".join(octets)

    def ipv6_address(self):
        hextets = [format(self.random_int(min=0, max=65535), "x") for _ in range(8)]
        return ":".join(hextets)
    
    def aadhaar_card_number(self):
        aadhaar_number = self.random_int(min=1000_0000_0000, max=9999_9999_9999)
        return f"{aadhaar_number}"


    def get_method_data(self, method, count, faker_obj):
        data = {
            'title' : f'{random.choice(dummy_data_keywords[:4])} {method.title()} data',
            'values' : []
        }
        if hasattr(faker_obj, method.replace(' ', '_')):
            method_function = getattr(faker_obj, method.replace(' ', '_'))
            for i in range(count):
                data['values'].append(method_function())
            return True, data 
        else:
            data['values'].append(random.choice(dummy_data_not_available_responses))
        return False, random.choice(dummy_data_not_available_responses)
            
        
    def get_response(self, data):
        query, faker_obj = data
        data = {
            'title' : f'Here is ',
            'values' : []
        }
        methods = self.predict_method(query)
        if len(methods) == 0:
            print('No methods')
            return random.choice(dummy_data_not_available_responses)
        counts = self.get_count(query)
        diff = len(methods) - len(counts)
        if diff > 0:
            counts.extend([1] * diff)
        for method, count in zip(methods, counts):
            success, response = self.get_method_data(method.lower(), count, faker_obj)
            if success:
                data['values'].append(response)
                data['title'] += f' {count if count > 1 else ""} {method.title()},'
            else:
                data['values'].append(random.choice(dummy_data_not_available_responses))
        data['title'] = data['title'][:-1]
        return self.format_response(data) 
        
            
    def format_response(self, gpt_response):
        response = """"""
        if (isinstance(gpt_response, dict)):
            response += f"<b>{gpt_response['title']}</b>"
        else:    
            response += f"<b>{gpt_response}</b>"
        for index, value in enumerate(gpt_response['values']):
            if (isinstance(value, dict)):
                response += f"<br></br>{index+1}. {self.format_response(value)}"
            else:    
                response += f"<div>{index+1}. {value}</div>"
        return response
        with open('fake_template.html', 'r') as file:
            template_content = file.read()
            print(type(template_content))
        
        template = Template(template_content)
        html_code = template.render(data=gpt_response)
        return html_code

                
        

    def predict_method(self,query):
        doc = nlp(query)
        singularized_text = []
        for token in doc:
            if token.pos_ == "NOUN" and not token.tag_.startswith("NNP"):
                singularized_text.append(token.lemma_)
            else:
                singularized_text.append(token.text)
        query = " ".join(singularized_text)

        pattern = r"\b(?:{})\b".format("|".join(re.escape(method.replace('_', ' ')) for method in fake_possible_methods))
        matches = re.findall(pattern, query, re.IGNORECASE)
        return matches

    def get_count(self,query):
        pattern = r"\b\d+\b"
        numbers = re.findall(pattern, query, re.IGNORECASE)
        return [int(number) for number in numbers]
