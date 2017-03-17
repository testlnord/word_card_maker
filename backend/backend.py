import requests
from typing import Dict, List
from flask import Flask
from flask_restful import reqparse, Resource, Api
import settings

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('word', type=str, required=True, help='Word for translation cannot be blank')


def yandex_translate(word: str) -> str:
    params: Dict[str, str] = {'key': settings.API_KEY,
                              'lang': 'en-ru', 'text': word}
    response = requests.get("https://dictionary.yandex.net/api/v1/dicservice.json/lookup", params=params).json()
    return response['def'][0]['tr'][0]['text']


class Translator(Resource):
    def get(self):
        word: str = parser.parse_args()['word']
        return {'word': word, 'translation': yandex_translate(word)}

api.add_resource(Translator, '/dict/translation')

if __name__ == '__main__':
    app.run(debug=True)
