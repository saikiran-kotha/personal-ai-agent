from app.vectorstore import DocumentQA
from app.tasks import get_time, get_weather

class PersonalAgent:
    def __init__(self):
        self.doc_qa = DocumentQA()

    def run(self, query):
        if "time" in query.lower():
            return get_time()
        elif "weather" in query.lower():
            return get_weather()
        else:
            return self.doc_qa.answer_query(query)
