from flask import Flask, jsonify, request



# name - имя текущ. модуля (проекта с кодом) питона

app = Flask(__name__)

client = app.test_client()


@app.route('/getHelloWorld', methods=['GET'])
def get_HelloWord():
    return "Hello World!"


@app.route('/', methods=['GET'])
def get_HelloWordMain():
    return """
    Main page!
    
    Very simple calculator is realized here. Template for executing: 'num1.operation(num2) = result'
    Available operations:
    \n\t'+' - plus;
    \n\t'-' - minus;
    \n\t'*' - multiply;
    \n\t'/' - division    
    """

# http://127.0.0.1:5000/getWord?var=someWord


@app.route('/calc', methods=['GET'])
def get_calc():
    num1 = float(request.args.get('num1', '1'))
    num2 = float(request.args.get('num2', '1'))
    operation = request.args.get('operation', '+')

    if operation == 'plus':
        result = num1 + num2
        sign = '+'
    elif operation == 'minus':
        result = num1 - num2
        sign = '-'
    elif operation == 'multiply':
        result = num1 * num2
        sign = '*'
    elif operation == 'division':
        try:
            result = num1 / num2
        except ZeroDivisionError:
            return 'Division on zero! Try another numbers'
        sign = '/'

    return f"Operation {num1} {sign} {num2} = {str(result)}"


if __name__ == '__main__':
    app.run()
    # app.run(debug=True, port=5000)
