import csv
# import json
# import datetime
import sqlite3
from FileOperator import FileOperator
import bisect


# database manipulation class
class SqlDatabase:
    def create_database(self, filename: str):
        conn = sqlite3.connect(f'{filename}.sqlite')
        cur = conn.cursor()
        cur.executescript('''
        DROP TABLE IF EXISTS Flight;

        CREATE TABLE Flight (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            flight_number TEXT,
            date TIME,
            position TEXT,
            in_or_out    INTEGER,
            takeoff_time INTEGER,
            landing_time INTEGER
        );
        ''')
        return conn

    def writeday(self, filename: str, day: dict):
        conn = sqlite3.connect(f'{filename}.sqlite')
        cur = conn.cursor()
        cur.executescript('''
                DROP TABLE IF EXISTS Days;

                CREATE TABLE Days (
                    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    position INTEGER,
                    times TEXT
                );
                ''')

        for key, val in day.items():
            cur.execute('''INSERT OR IGNORE INTO Days (position, times) VALUES ( ?, ? )''', (key, str(val), ))

            conn.commit()


# Data clear class
class Time:
    # String to time
    def str2min(self, string: str) -> int:
        hour, minute = string.strip().split(':')
        return int(hour) * 60 + int(minute)

    # Time to string
    def min2str(self, minute: int) -> str:
        hour, min = str(minute // 60), str(minute % 60)
        if minute % 60 == 0:
            min = '00'
        string = hour + ':' + min
        return string

    # in = 0, out = 1
    def in_and_out(self, string: str) -> int:
        if string == '进':
            string = 0
        else:
            string = 1
        return string

    # insert data into database ({filename}.sqlite)
    def worktime(self, da: list, conn) -> list:
        for index, lines in enumerate(da):
            flight_number = lines[6]
            date = lines[4]
            position = lines[8]
            in_or_out = self.in_and_out(lines[2])
            takeoff_time = lines[14]
            landing_time = lines[17]

            if flight_number is None or date is None or position is None or in_or_out is None or\
                    takeoff_time is None or landing_time is None:
                continue

            print(flight_number, date, position, in_or_out, takeoff_time, landing_time)

            conn.cursor().execute('''INSERT OR IGNORE INTO Flight (flight_number, date, position, in_or_out, 
                takeoff_time, landing_time) VALUES ( ?, ?, ?, ?, ?, ? )''',
                                  (flight_number, date, position, in_or_out, takeoff_time, landing_time, ))

            conn.commit()

            da[index] = [lines[4], lines[8], self.in_and_out(lines[2]), lines[14], lines[17]]
        return da

    # build one day occupied time list
    def select_day(self, filename: str, day: str, pos: str) -> list:
        conn = sqlite3.connect(f'{filename}.sqlite')
        cur = conn.cursor()
        cur.execute('''
            SELECT in_or_out, takeoff_time, landing_time FROM Flight where date like ( ? ) and position like ( ? )''',
                    (day, pos, ))
        data = cur.fetchall()

        times, timesin, timesout = [], [], []
        for line in data:
            if line[0]:
                bisect.insort(timesout, line[1])
            else:
                bisect.insort(timesin, line[2])

        if timesin[0] > timesout[0]:
            times.append(['0:00', timesout[0]])
            for i, (t1, t2) in enumerate(zip(timesin[:-1], timesout[1:])):
                times.append([t1, t2])
            if timesin[-1] > timesout[-1]:
                times.append([timesin[-1], '23:59'])

        elif len(timesin) == len(timesout):
            for i, (t1, t2) in enumerate(zip(timesin, timesout)):
                times.append([t1, t2])
        else:
            for i, (t1, t2) in enumerate(zip(timesin[:-1], timesout)):
                times.append([t1, t2])
            times.append([timesin[-1], '23:59'])

        return times


    # def linear(self, da: list) -> list:
    #     da.sort(key=lambda x: x[0])
    #     print(type(da))


# Main function
def main():
    # open file
    fhand = FileOperator()
    with fhand.openfile('20220801-20220810.csv', 3, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        cur = SqlDatabase()
        time = Time()
        # read data
        # data = ([line for line in csv_reader if line[8].startswith('2') or line[8].startswith('1') or
        #          line[8].startswith('C')])
        # time.worktime(data, cur.create_database('20220801-20220810', '20220801-20220810'))

        # build one day occupied time dict{position: list}
        dic = {}
        for pos in [position for position in range(210, 232 + 1)]:
            day = time.select_day('20220801-20220810', '2022-08-05', str(pos))
            dic[pos] = dic.get(pos, day)

        # write dict into database
        cur.writeday('2022-08-05', dic)

        # write file
        # with open('20220801-20220810-new.csv', 'w', newline='') as new_file:
        #     csv_writer = csv.writer(new_file, delimiter=',')
        #     csv_writer.writerows(data)


# Main function
if __name__ == '__main__':
    main()
