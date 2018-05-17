import csv

def store_to_csv(store_infos):
    f = open('./store.csv', 'w')
    csvWriter = csv.writer(f)

    for e in store_infos:
        csvWriter.writerow([e.getName(), e.getBranch(), e.getAddress(), e.getPhoneNum()])

    f.close()
