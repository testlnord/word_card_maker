import requests
from typing import Dict, List
from flask import Flask
from flask_restful import reqparse, Resource, Api
import settings
from database import database_methods

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('word', type=str, required=True, help='Word for translation cannot be blank')
parser.add_argument('translation', type=str)
parser.add_argument('context', type=str)


def yandex_translate(word: str) -> str:
    params: Dict[str, str] = {'key': settings.API_KEY,
                              'lang': 'en-ru', 'text': word}
    response = requests.get("https://dictionary.yandex.net/api/v1/dicservice.json/lookup", params=params).json()
    return response['def'][0]['tr'][0]['text']


class Translator(Resource):
    def get(self):
        word: str = parser.parse_args()['word']
        return {'word': word, 'translation': yandex_translate(word)}


class Cards(Resource):
    def post(self):
        word: str = parser.parse_args()['word']
        translation: str = parser.parse_args()['translation']
        context: str = parser.parse_args()['context']
        database_methods.insert_card(word, translation, context, 'Public deck')
        return {'word': word, 'translation': translation, 'context': context}

api.add_resource(Translator, '/dict/translation')
api.add_resource(Cards, '/cards/add')

if __name__ == '__main__':
    app.run(debug=True)
