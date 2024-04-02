from ai_utils.patterns import chat_bot_data
from random import choice
import re
from ai_utils.ai_model_predict import AIModelPredict
from ai_utils.patterns import incomplete_responses

class ResponseModel:
    def __init__(self):
        self.response = AIModelPredict()
        
    def get_response(self, query):
        query_alpha = re.sub(r'[^a-zA-Z\s]', '', query.lower())
        for item in chat_bot_data:
            patterns = item.get('patterns', [])
            responses = item.get('responses', [])
            for pattern in patterns:
                if query_alpha == pattern:
                # if re.search(pattern, query_alpha, re.IGNORECASE):
                    return choice(responses)
        if len(query) < 5:
            return choice(incomplete_responses)
        return self.response.predict(query)
