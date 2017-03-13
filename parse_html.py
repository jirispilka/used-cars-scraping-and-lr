"""
Parse hmlt files stored in the data dir.
Save the data into a csv file

@author: jirka
"""

import re
from bs4 import BeautifulSoup
import glob

DEBUG = False

data_dir = 'data_html_temp'
csv_file = 'octavia_cars_2017-03.csv'

files = glob.glob(data_dir + '/*.html')
files.sort()

print('Source files:')
print(files)
print(len(files))

cars = list()

for k, sfile in enumerate(files):

    print('processed files: {0}/{1}'.format(k, len(files)))

    with open(sfile, 'r') as fr:
        soup = BeautifulSoup(fr, 'lxml')

    # find individual ads
    for item in soup.find_all(id=re.compile('item.*')):

        a = item.find_all('a')

        sname = a[1].get_text()
        sname = sname.encode('utf-8')

        m = re.search("1.2|1.6|1.9|2.0", sname)

        sname = sname.replace(",", " ").replace(";", " ").strip()

        if m is None:
            displacement = ''
        else:
            sres = m.group(0)
            sres = sres.replace(",", ".").replace(":", ".").replace("/", ".")
            displacement = float(sres)

        price = year = mileage = 0
        # print item
        for k, dd in enumerate(item.find_all('dd')):

            if k == 0:

                price = dd.strong.get_text()
                price = price.replace(" ", "")
                price = int(price)
                if DEBUG:
                    print("price = {0}".format(price))

            elif k == 1:

                year = int(dd.get_text())
                if DEBUG:
                    print("year = {0}".format(year))

            elif k == 2:

                mileage = dd.get_text()
                ind = mileage.index('km')
                mileage = mileage[0:ind - 1]
                mileage = mileage.replace(" ", "")
                mileage = int(mileage)
                if DEBUG:
                    print("mileage = {0}".format(mileage))

            elif k == 3:

                stext = dd.get_text()
                stext = stext.encode('utf-8')
                stext = stext.replace(",", " ").replace(";", " ").strip()

                if DEBUG:
                    print("text = " + stext)
            # else:
            #     print dd

        cars.append([sname, displacement, year, mileage, price])

# write the file
with open(csv_file, 'w+') as fw:

    fw.write('text,displacement,year,mileage,price\n')

    for s, d, y, m, p in cars:
        fw.write('{0},{1},{2},{3},{4}\n'.format(s, d, y, m, p))

print('\n Done')

