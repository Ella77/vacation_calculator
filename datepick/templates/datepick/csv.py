import csv


f= open('output.csv','w',encoding = 'utf-8', newline ='')
wr = csv.writer(f)
wr.writerow([1, "김정수"], False)
wr.writerow([2,"박상미", True])
f.close()