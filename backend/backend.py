import requests
from typing import Dict
from flask import Flask
from flask_restful import reqparse, Resource, Api, abort
from flask_jwt import JWT, jwt_required, current_identity
import settings
from database import database_methods
import user_methods


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('word', type=str, required=True, help='Word for translation cannot be blank')
parser.add_argument('translation', type=str)
parser.add_argument('context', type=str)
parser.add_argument('deck', type=str)

langparser = reqparse.RequestParser()
langparser.add_argument('lang', type=str, required=True, help='Language cannot be blank')

methods = database_methods.DatabaseMethods(settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, settings.DB_NAME,
                                           settings.DB_PORT)


def authenticate(username, password):
    user: user_methods.User = methods.retrieve_user(username, password)
    if user:
        return user


def identity(payload):
    user_id = payload['identity']
    user: user_methods.User = methods.retrieve_user_by_id(user_id)
    if user:
        return user

app.config['SECRET_KEY'] = settings.SECRET_KEY
jwt = JWT(app, authenticate, identity)


def yandex_translate(word: str, lang: str) -> str:
    params: Dict[str, str] = {'key': settings.API_KEY,
                              'lang': lang, 'text': word}
    response = requests.get("https://dictionary.yandex.net/api/v1/dicservice.json/lookup", params=params).json()
    return response['def'][0]['tr'][0]['text']


class Translator(Resource):
    decorators = [jwt_required()]

    def get(self):
        word: str = parser.parse_args()['word']
        return {'word': word, 'translation': yandex_translate(word, methods.get_language_by_id(current_identity.id))}


class Cards(Resource):
    decorators = [jwt_required()]

    def post(self):
        word: str = parser.parse_args()['word']
        translation: str = parser.parse_args()['translation']
        context: str = parser.parse_args()['context']
        deck: str = parser.parse_args().get('deck', None)
        if deck is None:
            methods.insert_card(word, translation, context, " ".join([current_identity.username, "deck"]))
        else:
            has_rights = methods.check_if_user_has_deck(current_identity.id, deck)
            if not has_rights:
                abort(400)
            methods.insert_card(word, translation, context, deck)

        return {'word': word, 'translation': translation, 'context': context}


class Language(Resource):
    decorators = [jwt_required()]

    def post(self):
        lang: str = langparser.parse_args()['lang']
        methods.set_language(current_identity.username, lang)

        return {'lang': lang}

api.add_resource(Translator, '/dict/translation')
api.add_resource(Cards, '/cards/add')
api.add_resource(Language, '/settings/language')

if __name__ == '__main__':
    app.run(debug=True, port=settings.SERVER_PORT, host=settings.SERVER_HOST)
