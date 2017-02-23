#######################################################################################################################
#                                                                                                                     #
#                                MIS40570: Analytics Research and Implementation                                      #
#                                                                                                                     #
#                                 ARI Programming Assignment - Airline Seating                                        #
#                                           Due Date: Feburary 24, 2017                                               #
#                                   Author: Deepak Kumar Gupta and Shruti Goyal                                       #
#                                               16200660             16200726                                         #
#                                                                                                                     #
#######################################################################################################################


# Run this code G:\Pycharm_programs\ARI\code>python seat_assign_16200660_16200726.py airline_seating.db bookings.csv


import sys
import unittest
import sqlite3
import pandas as pd
import numpy as np

######################################################################################################################
#                                                                                                                     #
#                                         Functions Reading Values from Files and DB                                  #
#                                                                                                                     #
#######################################################################################################################
                                        #Acceting booking csv file name as second system argument
db = 'airline_seating.db'
filename = 'bookings.csv'



#This function read nrows and seat_config from rows_cols table in Database
# seat_col storing the columns in aircraft seat map by calculating length of seat_config variable


def read_seat_config():
    conn = sqlite3.connect(db)                                                               #Connecting to the database
    cur = conn.cursor()
    row_data = cur.execute('''SELECT * FROM rows_cols''')               #Reading nrows, seat_config from rows_cols table
    for row in row_data:
        nrows = row[0]
        seat_config = row[1]
        seat_col = len(seat_config)
    valid_nrows_seat_config(nrows,seat_config)
    return nrows, seat_config, seat_col


def read_rows_in_booking(filename):                          #Function calculating the number of record in booking file
    df = pd.read_csv(filename, header=None)
    return len(df)

class read_booking(object):
    def __init__(self,n,filename):
        self.n =n
        self.filename = filename

    def read(self):
        df = pd.read_csv(filename,header=None)
        self.passenger_name =df.loc[self.n,0]                                 #Setting Index to 1 as index starts from 0
        self.no_of_passenger=df.loc[self.n,1]  #Reading passenger name and no. of passenger from booking file one by one
        return self.passenger_name, self.no_of_passenger




######################################################################################################################
#                                                                                                                    #
#                                         Seat Map - Controlling Seats and Booking                                   #
#                                         ----------------------------------------                                   #
#  Description: This function read the seating configuration of a aircraft from database file, based on which this   #
#               generate seat map i.e creating numpy matrix of given nrow and seat_config                            #
#                                                                                                                    #
#  Values: 0 is empty seat and 1 is occupied seat                                                                    #
#                                                                                                                    #
#  Example: For trained data, we have nrows := 15 & seat_config ='ACDF', by using numpy we have created matrix of    #
#            15 rows x 4 cols, and assigned 0 as default value.                                                      #
#######################################################################################################################

def generate_seat_map():
    nrows, seat_config, seat_col = read_seat_config()
    valid_nrows_seat_config(nrows, seat_config)
    seats = np.zeros(shape=(nrows, seat_col))
    seats_name = np.chararray(shape=(nrows, seat_col), itemsize=15)
    return seats,seats_name



######################################################################################################################
#                                                                                                                     #
#                                         Validity Functions                                                          #
#                                                                                                                     #
#######################################################################################################################

'''
Function Name: check_overbooking()
Description: This function first find the total number of passengers from the booking list, if booking is more than
the number of available seats in a aircraft then program will exit(0). However, program should accept all passenger till
it is has no space to accommodate any new passenger.
'''


def check_overbooking():
    nrows, seat_config, seat_col = read_seat_config()
    passenger_total = 0
    for i in range(nrows):
        passenger_name, no_of_passenger = read_booking.read(i, filename)
        passenger_total += no_of_passenger
    if passenger_total > (seat_col * nrows):
        print("Cannot Proceed: No. of Passenger can't be more than no. of available seats")
        exit(0)


def is_empty_booking_list(passenger_name,no_of_passenger):
    for i in range(nrows):
        if passenger_name == "" or no_of_passenger == 0 or no_of_passenger == " ":
            print("Cannot Proceed: Passenger Information is Missing")
            exit(0)


def is_no_of_passenger_invalid_entry(no_of_passenger):
    if no_of_passenger <=0 or isinstance(no_of_passenger, str):
        print("Cannot Proceed: No_of_Passenger entry is invalid")
        exit(0)


def seats_not_full(empty_seat_row):
    if sum(empty_seat_row) != 0:
        return True


def valid_nrows_seat_config(nrows,seat_config):
    if isinstance(nrows,str) or isinstance(seat_config,int):
        print("Cannot Proceed: Invalid value of nrows or seat_config")
        exit(1)

def call_validity_functions(passenger_name,no_of_passenger):
    is_empty_booking_list(passenger_name, no_of_passenger)
    is_no_of_passenger_invalid_entry(no_of_passenger)
#######################################################################################################################
#                                                                                                                     #
#                                         Seat Tracker Functions                                                      #
#                                                                                                                     #
#######################################################################################################################


def create_seat_tracker():
    empty_seat_row = []
    for i in range(nrows):
        empty_seat_row.append(seat_col)
    return empty_seat_row


def update_seat_tracker(empty_seat_row, row):
    val = empty_seat_row[row]
    empty_seat_row[row] = val - 1
    return empty_seat_row


def total_available_seats(empty_seat_row):
    total_seats= sum(empty_seat_row)
    return total_seats


#######################################################################################################################
#                                                                                                                     #
#                                         Seat Encoder Function                                                       #
#                                                                                                                     #
#######################################################################################################################


def seats_encoder(row, col):
    row_number = row + 1
    seat_number = seat_config[col]
    seat = str(row_number) + seat_number
    return seat, row_number, seat_number

#######################################################################################################################
#                                                                                                                     #
#                                         Database Functions                                                          #
#                                                                                                                     #
#######################################################################################################################

# Reference: http://www.sqlitetutorial.net/sqlite-python/update/


def update_seats(conn, seating):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    #sql = ''' UPDATE seating
    #           SET name = ?
    #           WHERE row = ? AND seat = ?'''

    sql = ''' INSERT INTO seating (name, row,seat) VALUES (? , ? ,? );'''
    cur = conn.cursor()
    try:
        cur.execute(sql, seating)
        print(seating[0], "seat ->", str(seating[1])+seating[2])
    except sqlite3.IntegrityError:
        print("Database Error: Seat already checked in by some Passenger")


def update_metrics(conn, metrics):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE metrics
              SET passengers_refused = ? ,
               passengers_separated = ?'''
    cur = conn.cursor()
    cur.execute(sql, metrics)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db)
        return conn
    except EnvironmentError as e:
        print(e)

    return None


#######################################################################################################################
#                                                                                                                     #
#                                         Case 1 : Single Seat Allocation                                             #
#                                                                                                                     #
#######################################################################################################################

class single_seat(object):

    def __init__(self,passenger_name,no_of_passenger):
        self.passenger_name = passenger_name
        self.no_of_passenger=no_of_passenger

    def single_seat_allocation(self):
        for i in range(nrows):
            for j in range(seat_col):
                if seats[i][j] == 0.0:
                    seats[i][j] = 1.0
                    seats_name[i][j] = self.passenger_name.split(" ")[0]
                    update_seat_tracker(empty_seat_row, i)
                    seat, row_number, seat_number = seats_encoder(i, j)
                    conn = create_connection(db)
                    with conn:
                        update_seats(conn, (self.passenger_name,row_number, seat_number))
                    return i, j


#######################################################################################################################
#                                                                                                                     #
#                                         Case 2 : Seat Allocation                                                    #
#                           no_of_passenger > 1 or no_of_passenger <= seat_col                                        #
#                                                                                                                     #
#######################################################################################################################
class groupSeatCaseTwo(object):

    def __init__(self,passenger_name,no_of_passenger):
        self.passenger_name = passenger_name
        self.no_of_passenger = no_of_passenger

    def group_seat_available_row(self):
        for i in range(nrows):
            if empty_seat_row[i] >= self.no_of_passenger:
                return i

    def group_seat_check(self):
        row = self.group_seat_available_row()
        temp = []
        for j in range(seat_col):
            if seats[row][j] == 0:
                temp.append(j)
        return temp, row

    def group_seat_allot(self):
        temp, row = self.group_seat_check()
        seat_allocated = []
        for i in range(self.no_of_passenger):
            col = temp[i]
            seat_allocated.append(col)
            seats[row][col] = 1
            seats_name[row][col] = self.passenger_name.split(" ")[0]
            update_seat_tracker(empty_seat_row, row)
            seat, row_number, seat_number = seats_encoder(row, col)
            conn = create_connection(db)
            with conn:
                update_seats(conn, (self.passenger_name, row_number, seat_number))
        return seat_allocated, row

    def is_seats_in_a_row(self):
        for i in range(nrows):
            if empty_seat_row[i] >= self.no_of_passenger:
                return True


#######################################################################################################################
#                                                                                                                     #
#                                         Case 3 : Seat Allocation                                                    #
#                                        no_of_passenger > seat_col                                                   #
#                                                                                                                     #
#######################################################################################################################

class group_seat_case_three(object):
    def __init__(self,passenger_name,no_of_passenger):
        self.passenger_name = passenger_name
        self.no_of_passenger = no_of_passenger

    def group_seat_allot_case3(self):
        no_of_rows = self.no_of_passenger // seat_col
        remaining_seats = self.no_of_passenger % seat_col
        grouptwoObj = groupSeatCaseTwo(self)
        for i in range(no_of_rows):
            grouptwoObj.group_seat_allot(self.passenger_name, seat_col)
        grouptwoObj.group_seat_allot(self.passenger_name, remaining_seats)


#######################################################################################################################
#                                                                                                                     #
#                                         Main Function Call and Body                                                 #
#                                                                                                                     #
#######################################################################################################################
def __main__(db,filename):

    passenger_refused = 0.0
    passenger_seated_away = 0
    total_booking = read_rows_in_booking(filename)
    for n in range(total_booking):
        readBookingObj = read_booking(n, filename)
        passenger_name, no_of_passenger = readBookingObj.read()
        single_seatObj = single_seat(passenger_name,no_of_passenger)
        gsctwoObj= groupSeatCaseTwo(passenger_name,no_of_passenger)
        group_seat_case_threeObj= group_seat_case_three(passenger_name,no_of_passenger)

        if seats_not_full(empty_seat_row) and total_available_seats(empty_seat_row) >= no_of_passenger:

            #Case 1 calling starts here
            if no_of_passenger == 1:
                i, j = single_seatObj.single_seat_allocation()

            #Case 2 calling starts here
            elif no_of_passenger > 1 and no_of_passenger <= seat_col:
                Flag = gsctwoObj.is_seats_in_a_row()

                if total_available_seats(empty_seat_row) > no_of_passenger and Flag == True:
                    # And each row has only 1 seat then allocate separately
                    gsctwoObj.group_seat_allot()
                elif total_available_seats(empty_seat_row) >= no_of_passenger:
                    for i in range(no_of_passenger):
                        single_seatObj.single_seat_allocation()
                        passenger_seated_away += 1.0

            #Case 3 calling starts here
            elif no_of_passenger > seat_col:

                if total_available_seats(empty_seat_row) > no_of_passenger:
                    group_seat_case_threeObj.group_seat_allot_case3()
                elif total_available_seats(empty_seat_row) == no_of_passenger:
                    for i in range(no_of_passenger):
                        single_seatObj.single_seat_allocation()
                        passenger_seated_away += 1.0

        elif total_available_seats(empty_seat_row) == 0:
            print("Flight is Fully Booked ", passenger_name)
            passenger_refused += no_of_passenger

        elif seats_not_full(empty_seat_row) and total_available_seats(empty_seat_row) < no_of_passenger:
            print("Can't Accommodate You", passenger_name)

            passenger_refused += no_of_passenger
            continue
        else:
            print("System Error")
            exit(0)
    print("Passenger Refused So Far", passenger_refused)                        #Total no. of Passenger Refused checkin
    print("Passenger Seated Away", passenger_seated_away)          #Total no. of Passenger seating away from their group
    conn = create_connection(db)
    with conn:                                     #updating count of passenger refused and seated away in metrics table
        update_metrics(conn, (passenger_refused, passenger_seated_away))
    print("-----------------------Seat Map of Fully Booked Plan is -----------------------")
    for i in range(nrows):
        try:
            rows = seats_name[i].center(10, fillchar=' ').decode("utf-8")
            row_no = str(i + 1)
            print(row_no, rows)
        except UnicodeDecodeError:
            print("Unicode Error: try to run from python environment ")
    return passenger_seated_away, passenger_refused

nrows, seat_config, seat_col = read_seat_config()
seats,seats_name = generate_seat_map()
empty_seat_row = create_seat_tracker()


class test_after_total_seats(unittest.TestCase):

    def __init__(self,testname, db, filename):
        super(test_after_total_seats, self).__init__(testname)
        self.db = db
        self.filename = filename

    def test_total_available_seats(self):
        seats_available = total_available_seats(empty_seat_row)
        self.assertEqual(seats_available,0)

    def test_passenger_refused(self):
        passenger_seated_away ,passenger_refused= __main__(self.db,self.filename)
        self.assertEqual(passenger_refused,180)

    def test_passenger_refused2(self):
        passenger_seated_away ,passenger_refused= __main__(self.db,self.filename)
        self.assertEqual(passenger_refused,180)

    def test_read_seat_config(self):
        nrows, seat_config, seat_col = read_seat_config()
        self.assertEqual(nrows,15,msg="Reading Correct Rows")
if __name__ == '__main__':
    if len(sys.argv) > 1:
        db = sys.argv[1]
        filename = sys.argv[2]
        __main__(db,filename)

        print("-------------------Testing Data-------------------")
        suite = unittest.TestSuite()
        suite.addTest(test_after_total_seats("test_total_available_seats",db,filename))
        suite.addTest(test_after_total_seats("test_passenger_refused",db,filename))
        suite.addTest(test_after_total_seats("test_passenger_refused2", 'test.db','test_bookings.csv'))
        suite.addTest(test_after_total_seats("test_read_seat_config", db, filename))
        unittest.TextTestRunner().run(suite)
    else:
        print("Enter valid *.db and *.csv filenames.")