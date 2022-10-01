from ast import arg
from email.policy import default
from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import argparse
import os
import pandas
import collections
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape





def years(count_of_years):
    if 11 <= count_of_years <= 20:
        years = "лет"
    elif count_of_years % 10 == 2 or count_of_years % 10 == 3 or count_of_years % 10 == 4:
        years = "года"
    elif count_of_years % 10 == 1:
        years = "год"
    else:
        years = "лет"
    return years     

def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')    
    year_of_foundation = datetime.datetime(year=1920, month=1, day=1, hour=0)
    present_year = datetime.datetime.now()
    count_of_years = present_year.year-year_of_foundation.year
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", default="wine3.xlsx")
    parser.add_argument("-sheet_name", default="Лист1")                   
    args = parser.parse_args()
    excel_data_df = pandas.read_excel(args.file, sheet_name=args.sheet_name, na_values='nan', keep_default_na=False)
    drinks = excel_data_df.to_dict(orient='records')

    dict_of_lists = collections.defaultdict(list) 

    for drink in drinks:
        dict_of_lists[drink["Категория"]].append(drink)    
    wines = dict_of_lists.items()

    rendered_page = template.render(
        number_of_years=count_of_years,
        year=years(count_of_years ),
        wines=wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()




if __name__ == "__main__":
    main()