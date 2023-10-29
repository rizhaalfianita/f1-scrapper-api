from flask import Flask, request, jsonify
import service

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Welcome to Formula 1 API, created by Fahrendra Khoirul Ihtada and Rizha Alfianita"

@app.route('/season/<int:year>', methods=['GET'])
def get_season(year):
    try:
        link_year = f"https://www.formula1.com/en/results.html/{year}/races.html"
        res = service.get_year(link_year)
        print("DONEEE")
        if res == []:
            return "Year not found : F1 only available from 1950 to current year"
        return jsonify(res)
    except Exception as e:
        return jsonify(error=str(e)), 500  # Return the error message with a 500 status code


@app.route('/all-season', methods=['GET'])
def get_all_season():
    try:
        res = service.list_all_year("https://www.formula1.com/en/results.html/2023/races.html")  
        return jsonify(res)
    except Exception as e:
        return jsonify(error=str(e)), 500  # Return the error message with a 500 status code


if __name__ == '__main__':
    app.config['TIMEOUT'] = 20  # Set timeout to 10 seconds
    app.run(debug=False, host='0.0.0.0',port=10000)
