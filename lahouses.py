from craigslist import CraigslistHousing
import csv
import sys


def writeCSVHeader(csvFile):
    with open(csvFile, 'w') as csvfile:
        fieldnames = ['id', 'name', 'url', 'datetime', 'price', 'where', 'has_image', 'has_map', 'geotag',
                      'lat', 'long', 'price_number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def writeCSV(cl_h, csvFile):
    recordCount = 0
    with open(csvFile, 'a') as csvfile:
        fieldnames = ['id', 'name', 'url', 'datetime', 'price', 'where', 'has_image', 'has_map', 'geotag',
                      'lat', 'long', 'price_number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for result in cl_h.get_results(sort_by='newest', geotagged=True):
            loc = result['geotag']
            price = result['price']
            if loc is None:
                continue
            else:
                try:
                    writer.writerow({'id': result['id'], 'name': result['name'],
                                     'url': result['url'], 'datetime': result['datetime'], 'price': result['price'],
                                     'where': result['where'], 'has_image': result['has_image'],
                                     'has_map': result['has_map'], 'geotag': result['geotag'],
                                     'lat': loc[0], 'long': loc[1], 'price_number': int(price[1:])})
                    sys.stdout.write("-")
                    sys.stdout.flush()
                    recordCount += 1
                except UnicodeEncodeError:
                    print("Unicode Error")
    print("\nRecords written: " + str(recordCount) + "\n")


# Define name of CSV file
file = 'lahouses.csv'

# Define site
site = 'losangeles'

# Define areas
# 'wst': westside-southbay-310
# 'sfv': san fernando valley
# 'lac': central LA 213/323
# 'sgv': san gabriel valley
# 'lgb': long beach / 562
# 'ant': antelope valley
areas = ['wst', 'sfv', 'lac', 'sgv', 'lgb', 'ant']

# Define categories
# 'reb': real estate by broker
# 'reo': real estate by owner
category = 'reb'

# Define max price
maxPrice = 1000000

# Get data and write to CSV file
# Write header
writeCSVHeader(file)
for area in areas:
    print(area + "\n")
    cl_h = CraigslistHousing(site=site, area=area, category=category, filters={
        'max_price': maxPrice, 'has_image': True, 'posted_today': True})
    writeCSV(cl_h, file)
