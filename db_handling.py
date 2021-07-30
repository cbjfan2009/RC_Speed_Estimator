import mysql.connector
import psycopg2
mysqldb = mysql.connector.connect(
   host='localhost',
   user='devMatt',
   password='D3V3l0pm3ntS3rV3rcbjfan2009',
   database='webapp_user_input'
   )

# dbcursor = mysqldb.cursor()

# class users(db.Model):
#   id = db.Column('user', db.Integer, primary_key = True)
#   motkv = db.Column(db.Float)
#   batvolt = db.Column(db.Float)
#   pinion = db.Column(db.Float)
#   spur = db.Column(db.Float)
#   fgratio = db.Column(db.Float)
#   wheeldiam = db.Column(db.Float)

# def __init__(self, user, motkv, batvolt, pinion, spur, fgratio, wheeldiam):
#   self.user = user
#   self.motkv = motkv
#   self.batvolt = batvolt
#   self.pinion = pinion
#   self.spur = spur
#   self.fgratio = fgratio
#   self.wheeldiam = wheeldiam


# use this type of syntax to insert new data into the table
# sql = "INSERT INTO tablename (column1name, column2name) VALUES (%s, %s)"
# val = ("column1", "column2")
# mycursor.execute(sql, val)

# sql = "INSERT INTO *TABLENAME* (--these are the SQL table column names-- User, Motor_kV, Batt_Volt, Pinion, Spur, Final_Ratio, Wheel_Rad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
sql = "INSERT INTO speed_estimation_inputs (User, Motor_kV, Batt_Volt, Pinion, Spur, Final_Ratio, Wheel_Rad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = [
   ('204.210.165.122', 2400, 16.8, 16, 54, 3.92, 2.5),
   ('204.210.165.123',3500, 12.6, 16, 54, 3.92, 2.5),
   ('204.210.165.124', 4200, 8.4, 12, 54, 3.92, 2.5)
]
# proves I am connected to the database
# dbcursor.execute('SHOW TABLES')
# for x in dbcursor:
#   print(x)

# this will execute the sql data write, but needs commit after
# dbcursor.executemany(sql, val)

# db = db.commit()


# def sql_query():
#   dbcursor = db.cursor()
#   sql_data = dbcursor.execute('SELECT * FROM speed_estimation_inputs')
#   return sql_data


#POSTGRES PRACTICE



# postgresql connection
# postgres://vlinujzpemehpy:81bb09e53a2532c52b6a8696ebf0497b253e0a0516f0c1c741d5ceae3e10806e@ec2-54-211-160-34.compute-1.amazonaws.com:5432/df5p5d20v6pbf9
pgdb = psycopg2.connect(
   host='ec2-54-211-160-34.compute-1.amazonaws.com',
   user='vlinujzpemehpy',
   password='81bb09e53a2532c52b6a8696ebf0497b253e0a0516f0c1c741d5ceae3e10806e',
   port='5432',
   database='df5p5d20v6pbf9'
   )
pgcursor = pgdb.cursor()


def check_connection():
   pgcursor.execute("select version()")
   data = pgcursor.fetchone()
   print("Connection established to: ", data)


def create_table():
   sql = '''CREATE TABLE estimation_data 
   ("User" text PRIMARY KEY,
    Motor_kV integer,
     Batt_Volt decimal,
      Pinion integer,
       Spur integer,
        Final_Ratio decimal,
         Wheel_Rad decimal);'''
   pgcursor.execute(sql)
   pgdb.commit()


def pg_add_data(sql,val):
   pgcursor.executemany(sql, val)
   pgdb.commit()


def pg_query():
   pass

# can run this once to verify login credentials work
# check_connection()

# create table in the database
# create_table()



pgsql = '''INSERT INTO estimation_data 
   ("User", Motor_kV, Batt_Volt, Pinion, Spur, Final_Ratio, Wheel_Rad)
   VALUES (%s, %s, %s, %s, %s, %s, %s);'''
pgval = [
      ('204.210.165.130', 4000, 16.8, 14, 50, 3.75, 2.25),
      ('204.210.165.126', 1800, 22.2, 18, 52, 4.0, 2.75),
      ('204.210.165.155', 3500, 8.4, 13, 54, 3.92, 2.0),
      ('204.210.165.230', 1000, 29.6, 18, 52, 3.75, 3.0),
      ('204.210.170.126', 800, 29.6, 18, 52, 4.0, 3.2),
      ]

pg_add_data(pgsql, pgval)

pgdb.close()