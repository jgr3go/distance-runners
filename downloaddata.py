import csv
import requests
from bs4 import BeautifulSoup
import re

def main():
  with open('athlete_data.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(['Last', 'First', 'Country', 'Gender', 'Age', 'Weight (lbs)', 'Height (in)', 'Marathon', 'Half Marathon', '10K', '5K'])

    athletes = load()
    for ath in athletes:
      download(ath)
      write(ath, writer)

def load():
  athletes = []
  with open('athletes.csv', 'rb') as file:
    reader = csv.reader(file)
    next(reader, None) # skip header row
    for row in reader:
      athletes.append({
        'last': row[0],
        'first': row[1],
        'country': row[2],
        'gender': row[3],
        'races': {}
      })
  return athletes

def write(athlete, csv):
  a = athlete
  races = a['races']
  data = [a.get('last'), a.get('first'), a.get('country'), a.get('gender'), a.get('age'), a.get('weight'), a.get('height'),
          races.get('Marathon'), races.get('Half Marathon'), races.get('10K'), races.get('5K')]
  print(data)
  csv.writerow(data)

def download(athlete):
  download_olympic(athlete)
  download_iaaf(athlete)


def download_iaaf(athlete):
  events = ['5000', '5k', '10000', '10k', 'Half Marathon', 'Marathon']

  iaafurl = 'https://www.iaaf.org/athletes/search'
  params = {'name': '{0} {1}'.format(athlete['first'], athlete['last'])}
  res = requests.get(iaafurl, params=params)
  soup = BeautifulSoup(res.content, 'lxml')

  isAthlete = soup.find_all('meta', {'name': 'ContentType'})
  if (not isAthlete):
    print("WARNING: {0} {1} not found".format(athlete['first'], athlete['last']))
    return

  if isAthlete:
    tables = soup.select('#personalbests')
    for table in tables:
      trs = table.select('tr')
      for tr in trs:
        tds = tr.select('td')
        event = None
        time = None
        for td in tds:
          data = td.text.strip()

          if (event and time):
            continue
          if (event):
            time = data 
            continue

          if re.match('^(?:5000|10,*000|5 K|10 K)', data, re.I):
            if (data[0] == '5'):
              event = '5K'
            elif (data[0] == '1'):
              event = '10K'
          elif re.match('marathon', data, re.I):
            event = data

        if (event and time):
          prev = athlete['races'].get(event)
          if (prev is None or prev > time):
            athlete['races'][event] = time

    
def download_olympic(athlete):
  height = None
  weight = None
  age = None
  olympicurl = 'https://www.rio2016.com/en/search-athletes'
  params = {'q': '{0} {1}'.format(athlete['first'], athlete['last'])}
  res = requests.get(olympicurl, params=params)
  soup = BeautifulSoup(res.content, 'lxml')
  links = soup.find_all(href=re.compile('\/athlete\/'))
  if len(links):
    link = links[0]
    href = link['href']
    href = 'http://www.rio2016.com' + href
    
    res = requests.get(href)
    soup = BeautifulSoup(res.content, 'lxml')
    soup = soup.find('table', class_='about__table')
    abouts = soup.find_all('td', class_='about__col--data')
    for about in abouts:
      about = about.prettify('latin-1')
      match = re.search('(\d)\'\s*(\d+)[\'\"]', about)
      if (match):
        height = int(match.group(1)) * 12 + int(match.group(2))
        athlete['height'] = height
      match = re.search('\(Age (\d+)\)', about)
      if (match):
        age = match.group(1)
        athlete['age'] = age
      match = re.search('(\d+) lbs', about)
      if (match):
        weight = match.group(1)
        athlete['weight'] = weight


if __name__ == '__main__':
  main()