import csv
import re


def main():
  athletes = load()
  athletes = sorted(athletes, key=lambda athlete: athlete.get('last'))
  write(athletes)

def load():
  files = ['5k_men.csv', '5k_women.csv', '10k_men.csv', '10k_women.csv',
            'marathon_men.csv', 'marathon_women.csv']
  athletes = []
  athDict = {}

  for file in files:
    gender = re.match('women', file)
    if (gender):
      gender = 'F'
    else:
      gender = 'M'

    with open(file, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        uniq = row[0] + row[1] + row[2]
        if (athDict.get(uniq)):
          continue

        athletes.append({
          'last': row[0],
          'first': row[1],
          'country': row[2],
          'gender': gender
        })
        athDict[uniq] = 1

  return athletes

def write(athletes):
  with open('athletes.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(['Last', 'First', 'Country', 'Gender'])

    for a in athletes:
      writer.writerow([a['last'], a['first'], a['country'], a['gender']])

if __name__ == '__main__':
  main()