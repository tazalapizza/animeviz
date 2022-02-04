import csv

with open("animelists_cleaned.csv", "r") as fin:
   with open('animelists_reduced.csv', 'w', encoding='UTF8', newline="") as fout:
      reader = csv.reader(fin)
      writer = csv.writer(fout)
      header = next(reader)
      header = [header[i] for i in [0, 1, 5]]
      writer.writerow(header)
      for r in reader:
         row = [r[i] for i in [0, 1, 5]]
         writer.writerow(row)