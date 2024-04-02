import spacy, re
from collections import Counter
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    
class BulletPoints:
    
    def calculate_bullet_points_count(self, no_bullet_points, text):
        frequecy = 400
        if no_bullet_points:
            return no_bullet_points
        return len(text)//frequecy if len(text)//frequecy else 1
    
    def get_bullet_points(self, text, no_bullet_points = None):
        words = []
        bullet_points = []
        cleaned_text = re.sub(r'\[\d+\]', '', text).replace('.\n', '. ')
        tokens = nlp(cleaned_text)
        
        for token in tokens:
            if not token.is_stop and token.pos_ != 'PUNCT':
                words.append(token.text)
        
        res = Counter(words)
        common_words = [ tup[0] for tup in res.most_common(self.calculate_bullet_points_count(no_bullet_points, text))]
        points = cleaned_text.split('. ')
        for word in common_words:
            for point in points:
                if word in point and point not in bullet_points:
                    bullet_points.append({'heading' : word, "point":point.strip()})
                    break
        return bullet_points
    
    def get_point_counts(self, user_query):
        pattern = r"\b\d+\b"
        numbers = re.findall(pattern, user_query, re.IGNORECASE)
        print(numbers)
        if len(numbers):
            return int(numbers[0])
        return None
    
    def get_response(self, user_query, text):
        point_counts = self.get_point_counts(user_query)
        response = self.get_bullet_points(text, point_counts)
        return self.format_response(response)
    
        
    def format_response(self, gpt_response):
        response = """</br><b>Here is Buttet Points</b>"""
        for index, point in enumerate(gpt_response):
            response = response + f"<br></br><b>{index+1}. {point['heading']}</b> → {point['point']}"
        return response
        
    
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Summary:
    def extractive_summarization(self, text, num_sentences=3):
        sentences = sent_tokenize(text)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        ranked_sentences = sorted(((similarity_matrix[i, j], i, j) for i in range(len(sentences)) for j in range(len(sentences))), reverse=True)
        selected_sentences = sorted([sentences[idx] for _, _, idx in ranked_sentences[:num_sentences or 3]])
        return ' '.join(selected_sentences)

    def get_lines_counts(self, user_query):
            pattern = r"\b\d+\b"
            numbers = re.findall(pattern, user_query, re.IGNORECASE)
            if len(numbers):
                return int(numbers[0])
            return None
    
    def get_response(self, user_query, text):
        line_counts = self.get_lines_counts(user_query)
        response = self.extractive_summarization(text, line_counts)
        return self.format_response(response)
    
        
    def format_response(self, gpt_response):
        response = """</br><b>Here is Brief Summary</b>"""
        return response + f"</br>{gpt_response}"
        
    
import nltk
nltk.download('stopwords')
from rake_nltk import Rake


class Keywords:
    def keyword_extraction(self, text, num_keywords=5):
        r = Rake()
        r.extract_keywords_from_text(text)
        try:
            keywords = r.get_ranked_phrases()[:num_keywords or 10]
        except:
            keywords = r.get_ranked_phrases()
        return set([keyword for keyword in keywords if str(keyword).replace('_', '').replace('-', '').isalnum()])

    def get_key_counts(self, user_query):
        pattern = r"\b\d+\b"
        numbers = re.findall(pattern, user_query, re.IGNORECASE)
        if len(numbers):
            return int(numbers[0])
        return None
    
    def get_response(self, user_query, text):
        key_counts = self.get_key_counts(user_query)
        response = self.keyword_extraction(text, key_counts)
        return self.format_response(response)
    
        
    def format_response(self, gpt_response):
        response = """</br><b>Here is Some titles to your text</b>"""
        for index, title in enumerate(gpt_response):
            response = response + f"<br></br><b>{index+1}. {title}</b>"
        return response
    
    
class Describe:
    
    def __init__(self):
        self.features = [{
            'length' : ['length', 'total length', 'total count', 'character count', 'total character count', 'total character'],
            'words' : ['total words','total word', '']
        }]
        
    def describe(self, text, user_query = None):
        doc = nlp(text)
        total_characters = str(len(text))
        tokens = [token.text for token in doc]
        word_count = str(len(tokens))
        unique_word_count = str(len(set(tokens)))
        total_tokens = str(len(tokens))
        most_common_words = ", ".join([word for word, _ in Counter([token.text for token in doc if not token.is_stop]).most_common(5)])
        average_word_length = str(sum(len(token) for token in tokens) / len(tokens)) if len(tokens) > 0 else '0'
        named_entities = ", ".join([f"{ent.text} ({ent.label_})" for ent in doc.ents])
        analysis = {
            "Total Characters": total_characters,
            "Word Count": word_count,
            "Unique Word Count": unique_word_count,
            "Total Tokens": total_tokens,
            "Most Common Words": most_common_words,
            "Average Word Length": average_word_length,
            "Named Entities": named_entities,
        }

        return analysis
    
    def get_key_counts(self, user_query):
        pattern = r"\b\d+\b"
        numbers = re.findall(pattern, user_query, re.IGNORECASE)
        if len(numbers):
            return int(numbers[0])
        return None
    
    def get_response(self, user_query, text):
        key_counts = self.get_key_counts(user_query)
        response = self.describe(text)
        return self.format_response(response)
    
        
    def format_response(self, gpt_response):
        response = """</br><b>Here is text analysis</b>"""
        for index, key in enumerate(gpt_response.keys()):
            response = response + f"<br></br><b>{index+1}. {key}</b> → {gpt_response[key]}"
        return response

    
class Text:
    
    def get_response(self, result_text):
        score, user_query, text, source = result_text
        self.model = None
        if source == 'bullet_point':
            self.model = BulletPoints()
        elif source == 'add_title':
            self.model = Keywords()            
        elif source == 'sentence_summary':
            self.model = Summary()            
        elif source == 'text_description':
            self.model = Describe()    
        
        return self.model.get_response(user_query, text)    
                    