import csv;
import os;
FILENAME = 'legendinisdb.txt'

def read_db():
    if os.path.exists(FILENAME):
      db = file(FILENAME, "r+")
    else:
      db = file(FILENAME, "w+")

    
    messagereader = csv.reader(db, delimiter=',')
    list = [];
    for k in messagereader:
        tripple = [k[0], k[1], k[2]]
        list.append(tripple);
    return list;

def write_db(user, time, message):
    with open(FILENAME, "a") as myfile:
      myfile.write(user + ',' + time + ',' + message + "\n");
      myfile.close();


if __name__ == '__main__':
    db = read_db()
    write_db("marius", "2014-10-15 08:10", "drinking beer")
    for entry in db:
        print entry
