import re
import csv

def main():
  athletes = []
  files = ['5k_men', '5k_women', '10k_men', '10k_women',
            'marathon_men', 'marathon_women']
  for fil in files:
    with open('{0}.dat'.format(fil), 'rb') as file:
      for line in file:
        dat = re.match('\d+ \d+ ([A-Z\'\-]+) ([^\d]+) ([A-Z]{3}).*', line)
        if dat is not None:
          last_name = dat.group(1).title()
          first_name = dat.group(2)
          country = dat.group(3)
          athletes.append([last_name, first_name, country])

    with open('{0}.csv'.format(fil), 'wb') as file:
      writer = csv.writer(file)
      for a in athletes: 
        writer.writerow(a)


if __name__ == "__main__":
  main()