from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

list = {}
white_wines = []
red_wines = []
another_drink = []
event1 = datetime.datetime(year=1920, month=1, day=1, hour=0)
event2 = datetime.datetime.now()
delta = event2.year-event1.year
if 11 <= delta <= 20:
    years = "лет"
elif delta % 10 == 2 or delta % 10 == 3 or delta % 10 == 4:
    years = "года"
elif delta % 10 == 1:
    years = "год"
else:
    years = "лет"

excel_data_df = pandas.read_excel('wine2.xlsx', sheet_name='Лист1', na_values='nan', keep_default_na=False, usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка'])
drinks = excel_data_df.to_dict(orient='records')
print(drinks)
for drink in drinks:
    if drink['Категория'] == "Белые вина":
        white_wines.append(drink)
    elif drink['Категория'] == "Красные вина":
        red_wines.append(drink)
    else:
        another_drink.append(drink)
list["Белые вина"] = white_wines
list["Красные вина"] = red_wines
list["Напитки"] = another_drink

pprint(list)                       




rendered_page = template.render(
    number_of_years=years,
    year=delta,
    caps=list,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
