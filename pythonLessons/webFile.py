from flask import Flask, jsonify, request


app = Flask(__name__)
client = app.test_client()
movieList = [
    {
        'title': 'The Light',
        'description': 'Very important stuff'
    },
    {
        'title': 'Driver',
        'description': "Gosling didn't die in the end"
    }
]


@app.route('/getHelloWorld', methods=['GET'])
def get_HelloWorld():
    return "Hello World!"


@app.route('/', methods=['GET'])
def get_HelloWorldMain():
    return "Main page!"


@app.route('/getList', methods=['GET'])
def get_List():
    return jsonify(movieList)


@app.route('/getList', methods=['POST'])
def update_List():
    newMovie = request.json
    movieList.append(newMovie)
    return jsonify(movieList)


if __name__ == '__main__':
    app.run()