# !pip install wikipedia
from wikipedia import wikipedia
from ai_utils.patterns import chatbot_responses, incomplete_responses
from rake_nltk import Rake
from ai_utils import keywords
import re
import spacy

try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Downloading and installing 'en_core_web_md' model...")
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

class WikiPedia:
    def __init__(self):
        self.keyword = None
        self.page_name = None
        self.page_content = None
        
    def keyword_extraction(self, text):
        r = Rake()
        r.extract_keywords_from_text(text)
        keyword = r.get_ranked_phrases()[:1]
        if len(keyword):
            self.keyword = keyword[0]
            return self.keyword

    def search_page(self):
        self.page_name = wikipedia.search(self.keyword)[:1]
        if self.page_name == []:
            self.page_name = None

    def calculate_similarity(self, sentence1, sentence2):
        score = 0
        sent1_words = set(sentence1.lower().split())
        sent2_words = set(sentence2.lower().split())
        return len(sent1_words.intersection(sent2_words))/len(sent1_words)


    def search_content(self, query):
        try:
            pattern = "|".join(keywords.full_info_keywords)
            regex = re.compile(pattern)
            if bool(regex.search(query)):
                self.page_content = wikipedia.page(self.page_name).summary
            else:
                content = wikipedia.page(self.page_name).content
                sents = [sent.text for sent in nlp(content).sents]
                max_score = 0
                sentence1 = None
                max_score2 = 0
                sentence2 = None
                for sent in sents:
                    similarity_score = self.calculate_similarity(query, sent)
                    if similarity_score > max_score:
                        max_score = similarity_score
                        sentence1 = sent
                    if similarity_score > max_score2 and similarity_score < max_score :
                        max_score2 = similarity_score
                        sentence2 = sent
                if sentence1 and sentence2:
                    self.page_content = sentence1 + ' ' + sentence2
                elif sentence1:
                    self.page_content = sentence1
                elif sentence2:
                    self.page_content = sentence2
                else:
                    self.page_content = wikipedia.page(self.page_name).summary                    
        except wikipedia.DisambiguationError:
            pass


    def get_response(self, query):
        try:
            self.keyword_extraction(query)
            self.search_page()
            self.search_content(query)
            return self.page_content
        except:
            # print(self.keyword, self.page_name)
            return get_random_response(self.keyword or '')
        
    
    
import random

# Responses for various topics
responses = (
    "I'm not sure about that in the field of <b>{topic}</b>. Would you like me to look it up for you?",
    "That's an interesting question. Unfortunately, I don't have information on that topic in <b>{topic}</b>.",
    "I'm sorry, I don't have knowledge about that particular subject within the realm of <b>{topic}</b>.",
    "I'm afraid I don't have the answer to that question right now in <b>{topic}</b>.",
    "Hmm, I'm not familiar with that. Is there something else I can assist you with in the field of <b>{topic}</b>?",
    "I'm still learning! Unfortunately, I don't have information on that topic yet in <b>{topic}</b>.",
    "I'm sorry, I don't have that information at the moment. Is there anything else you'd like to know in the field of <b>{topic}</b>?",
    "I'm not equipped with knowledge on that topic in <b>{topic}</b>. Would you like me to try and find more information?",
    "It seems like I haven't been trained on that subject yet in <b>{topic}</b>. I apologize for the inconvenience.",
    "I'm not sure I understand the question correctly. Are you asking about <b>{topic}</b>?",
    "I'm sorry, that's beyond my current capabilities in <b>{topic}</b>.",
    "I'm not familiar with <b>{topic}</b>. Could you provide more context or information?",
    "I'm afraid I'm not programmed to respond to inquiries about <b>{topic}</b>.",
    "I don't have information on <b>{topic}</b> at the moment. Is there anything else you'd like to discuss?",
    "I'm sorry, I can't provide assistance regarding <b>{topic}</b> at this time.",
    "I'm still learning and haven't covered <b>{topic}</b> yet. Is there another topic you'd like to inquire about?",
    "I don't have any data on <b>{topic}</b> right now. Would you like me to search for more information?",
    "I'm not familiar with <b>{topic}</b>. Let me know if there's anything else I can help you with.",
    "Unfortunately, I'm not equipped to handle questions about <b>{topic}</b>.",
    "I'm sorry, I don't have any information available regarding <b>{topic}</b>."
)
def get_random_response(topic):
    """
    Get a random response related to the specified topic.
    
    Parameters:
        topic (str): The topic name.
    
    Returns:
        str: A random response related to the topic.
    """
    if not topic:
        return random.choice(chatbot_responses)
    response = random.choice(responses)
    return response.format(topic=topic)
