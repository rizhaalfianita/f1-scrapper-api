import service

res = service.get_year("https://www.formula1.com/en/results.html/2000/races.html")

service.save_to_json(res, "2000")