from flask import Flask
from flask_restful import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api(app)


class Quote(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(ai_quotes), 200
        for quote in ai_quotes:
            if (quote["id"] == id):
                return f'{quote.get("author")} once said: {quote.get("quote")}', 200
        return "Quote not found", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('author')
        parser.add_argument('quote')
        params = parser.parse_args()
        for quote in ai_quotes:
            # Если цитата существует то выдаем код 400
            if (id == quote["id"]):
                return f"Quote with id {id} already exists", 400
            # POST-метод принимает ID цитаты.
            # Затем, используя reqparse, он получил автора и цитату из запроса, сохранив их в словаре params.
            quote = {
                "id": int(id),
                "author": params['author'],
                'quote': params['quote']
            }
            ai_quotes.append(quote)
            return quote, 201

    def put(self, id):
        # PUT-метод берет ID и input и парсит параметры цитаты, используя reqparse
        parser = reqparse.RequestParser()
        parser.add_argument('author')
        parser.add_argument('quote')
        params = parser.parse_args()
        # Если цитата с указанным ID существует, метод обновит ее с новыми параметрами,
        # а затем выведет обновленную цитату с кодом 200. Если цитаты с указанным ID еще нет, будет создана новая запись с кодом 201.
        for quote in ai_quotes:
            if (id == quote["id"]):
                quote["author"] = params["author"]
                quote["quote"] = params["quote"]
                return quote, 200

        quote = {
            "id": id,
            "author": params["author"],
            "quote": params["quote"]
        }

        ai_quotes.append(quote)
        return quote, 201

    def delete(self, id):
        global ai_quotes
        # Перебираем список цитат и удаляем нужную
        ai_quotes = [qoute for qoute in ai_quotes if qoute["id"] != id]
        return f"Quote with id {id} is deleted.", 200


api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>", "/ai_quotes/", "/ai_quotes")
if __name__ == '__main__':
    app.run(debug=True)
