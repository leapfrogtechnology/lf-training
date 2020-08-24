import pandas as pd
import requests
import yaml
import json
from bs4 import BeautifulSoup

def weather(soup):
    week = soup.find(id='seven-day-forecast-body')
    items = week.find_all(class_='tombstone-container')
    temperatures = [item.find(class_='temp').get_text() for item in items[1:]]
    period_names = [item.find(class_='period-name').get_text() for item in items]
    period_names.pop(0)
    short_descriptions = [item.find(class_='short-desc').get_text() for item in items]
    short_descriptions.pop(0)
    weather_stuff = pd.DataFrame(
        {'Period': period_names,
         'Short_descriptions': short_descriptions,
         'temperatures': temperatures,
        })
    return weather_stuff

def full_weather(soup):
    full = soup.find(id='detailed-forecast-body')
    newitems=full.find_all(class_='row')
    label = [newitem.find(class_='col-sm-2 forecast-label').get_text() for newitem in newitems]
    full_descriptions =  [newitem.find(class_='col-sm-10 forecast-text').get_text() for newitem in newitems]
    full_weather_stuff = pd.DataFrame(
        {
            'Period': label,
            'Full_descriptions': full_descriptions,
        })
    return full_weather_stuff

def to_csv(weather_stuff,full_weather_stuff):
    weather_stuff.to_csv('./outputs/weather.csv')
    full_weather_stuff.to_csv('./outputs/fullweather.csv')

def to_json(weather_stuff,full_weather_stuff):    
    weather_stuff.to_json('./outputs/weather.json')
    full_weather_stuff.to_json('./outputs/fullweather.json')

def to_yml(weather_stuff,full_weather_stuff):
    with open('./outputs/weather.yml', 'w') as file:
        yaml.dump({'result': json.loads(weather_stuff.to_json(orient='records'))}, file, default_flow_style=False)
    with open('./outputs/fullweather.yml', 'w') as file:
        yaml.dump({'result': json.loads(full_weather_stuff.to_json(orient='records'))}, file, default_flow_style=False)

def to_xml(weather_stuff,full_weather_stuff):
    def xmlfunc(row):
        xml = ['<item>']
        for field in row.index:
            xml.append('  <field name="{0}">{1}</field>'.format(field, row[field]))
        xml.append('</item>')
        return '\n'.join(xml)
    with open('outputs/weather.xml', 'w') as f:
        print('\n'.join(weather_stuff.apply(xmlfunc, axis=1)), file=f)
    with open('outputs/fullweather.xml', 'w') as f:
        print('\n'.join(full_weather_stuff.apply(xmlfunc, axis=1)), file=f)



def main():
    url = 'https://forecast.weather.gov/MapClick.php?lat=34.05361000000005&lon=-118.24549999999999#.XziR9XVfikA'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    sweather = weather(soup)
    fweather = full_weather(soup)
    to_csv(sweather,fweather)
    to_json(sweather,fweather)
    to_yml(sweather,fweather)
    to_xml(sweather,fweather)


if __name__ == "__main__":
    main()
