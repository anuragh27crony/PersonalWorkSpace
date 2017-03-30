from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def fetch_auth_token():
    secret_code = request.args.get("code")
    return_response = 'Empty Response'
    if secret_code:
        client_id = 'e5e9aee8a7421ce5447e'
        client_secret = '76941c55c06fa973cc5958a84b0f2a988c3c7c56'
        url = 'https://github.com/login/oauth/access_token?client_id=' + client_id + '&client_secret=' + client_secret + '&code=' + secret_code

        response = requests.post(url=url, headers={'Accept': 'application/json'})
        response_json = response.json()
        print(response.text)
        print(response_json)
        flask_response = jsonify(response_json)
        flask_response.headers["Access-Control-Allow-Origin"] = "https://teletrax.github.io"
        flask_response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"

        return flask_response

    return return_response


if __name__ == '__main__':
    app.run()
