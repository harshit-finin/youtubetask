import csv

with open('in.csv','r',errors='ignore') as csv_file:
  csv_reader = csv.reader(csv_file)
	
  for line in csv_reader:
    city = line[0]
    lat = line[1]
    lng = line[2]
    print(f'{city} {lat} {lng}')