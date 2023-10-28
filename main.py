import service

all_years = service.get_all_year("https://www.formula1.com/en/results.html/2023/races.html")

service.save_to_json(all_years, "F1_all_year")