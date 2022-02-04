import csv

rows = []
with open("users_cleaned.csv", "r") as f:
   csvreader = csv.reader(f)
   header = next(csvreader)
   for row in csvreader:
      rows.append(row)

with open("countries.txt", "r") as f:
   t = f.read().splitlines()
   countries = [line.split(", ") for line in t]

rows.sort(key = lambda x: x[1])
countries.sort(key = lambda x: x[0])

result = []

ir = 0
ic = 0
while ic < len(countries):
   while rows[ir][1] != countries[ic][0]:
      ir += 1
   rows[ir][9] = countries[ic][1]
   result.append(rows[ir])
   ic += 1

with open('users_countries.csv', 'w', encoding='UTF8', newline="") as f:
   writer = csv.writer(f)
   writer.writerow(header)
   writer.writerows(result)