import spacy, re
from ai_utils import patterns
from ai_utils.keywords import dummy_data_keywords
from ai_models.fake import FakeAIModel
from ai_models.texts import Text
from ai_models.wikipedia import WikiPedia
from . import keywords
from ai_models import *
from faker import Faker
from ai_models.fake import FakeAIModel

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class AIModelPredict:
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(FakeAIModel)
        self.text = Text()
        self.wiki = WikiPedia()

    def is_question(self, query):
        doc = nlp(query)
        if doc[0].lower_ in keywords.question_words:
            return True
        if len(doc) > 0 and doc[-1].text == "?":
            return True
        return False
    
    def is_sents(self, query, count):
        sents_count = 0
        for sent in nlp(query).sents:
            sents_count += 1
        return sents_count <= count

    def is_fake_data(self, query):
            doc = nlp(query)
            key_word = False
            root_word = False
            root_child = False
            verb_present = False 
            
            for token in doc:
                if token.text.lower() in keywords.dummy_data_keywords:
                    # print('key_word')
                    key_word = True
                    break
                
            for token in doc:
                if token.dep_ == "ROOT" and token.lemma_.lower() in keywords.related_dummy_data_root_words:
                    # print('root_word')
                    root_word = True
                    for child in token.children:
                        if child.text.lower() in keywords.dummy_data_child_keywords or child.text.lower() in [pattern.replace('_', ' ') for pattern in patterns.fake_possible_methods]:
                        #    print('root_child')
                           root_child = True
                           break   
                                
            for token in doc:
                if token.pos_ == "VERB":
                    # print('verb_present')
                    verb_present = True
                    break
                
            result = (int(key_word) + int(root_word) + int(root_child) + int(verb_present)) / 4
            return result,

    def is_text_data(self, query):
        score = 0
        pattern = r'\n+'
        user_query = text = ''
        source = ''
        result = re.split(pattern, query)
        if len(result) > 1:
            score += 0.15                         
            user_query = result[-1]
            sents_count = 0
            for sent in nlp(user_query).sents:
                sents_count += 1
            if sents_count <= 2:
                score += 0.35                         
            text = '\n'.join(result[:-1])      
            for token in nlp(user_query):
                token_text = token.text.lower()
                if token_text in keywords.bullet_point_keywords:
                    score += 0.50
                    source = "bullet_point"
                    break
                elif token_text in keywords.sentence_summary_keywords:
                    score += 0.50
                    source = "sentence_summary"
                    break
                elif token_text in keywords.text_description_keywords:
                    score += 0.50
                    source = "text_description"
                    break
                elif token_text in keywords.sentiment_analysis_keywords:
                    score += 0.50
                    source = "sentiment_analysis"
                    break
                elif token_text in keywords.add_title_keywords:
                    score += 0.50
                    source = "add_title"
                    break
        return score, user_query, text, source

    def is_asking_datetime(self, query):
        score = 0
        if self.is_question(query):
            score += 0.25
        if self.is_sents(query, 1):
            score += 0.25

        for token in nlp(query):
            if token.text.lower() in keywords.all_datetime_keywords:
                score += 0.5
                break
        return score,
    
    def predict(self,query):
        result_text = self.is_text_data(query)
        if result_text[0] == 1:
            response = self.text.get_response(result_text)
            # print('response',response)
            return response
        result_fake = self.is_fake_data(query)
        if result_fake[0] == 1:
            response = self.fake.get_response((query, self.fake))
            return response
        
        sources = {
            'result_fake' : {
                    'score' : result_fake[0],
                    'arg' :(query, self.fake),
                    'attr' : self.fake
                } ,
            'result_text' : {
                    'score' : result_text[0],
                    'arg' :result_text,
                    'attr' : self.text
                } 
        }
        
        max_score = 0
        max_score_model = None
        check_score = 0.7
        for key, value in sources.items():
            if value['score'] >= check_score and value['score'] > max_score:
                max_score_model = value
        
        if max_score_model:
            print(max_score_model)
            return max_score_model['attr'].get_response(max_score_model['arg'])        
        
                
        return self.wiki.get_response(query)
        
            
                    
