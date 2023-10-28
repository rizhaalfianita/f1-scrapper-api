from flask import Flask, request, jsonify
import service

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Welcome to Formula 1 API, created by Fahrendra Khoirul Ihtada and Rizha Alfianita"

@app.route('/season/<int:year>', methods=['GET'])
def get_season(year):
    link_year = f"https://www.formula1.com/en/results.html/{year}/races.html"
    res = service.get_year(link_year)
    if res == []:
        return "Year not found : F1 only available from 1950 to current year"
    return jsonify(res)


@app.route('/all-season', methods=['GET'])
def get_all_season():
    res = service.list_all_year("https://www.formula1.com/en/results.html/2023/races.html")
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=False, port=5000)