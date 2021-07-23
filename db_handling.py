import mysql.connector

db = mysql.connector.connect(
   host='localhost',
   user='devMatt',
   password='D3V3l0pm3ntS3rV3rcbjfan2009',
   database='webapp_user_input')

dbcursor = db.cursor()

class users(db.Model):
   id = db.Column('user', db.Integer, primary_key = True)
   motkv = db.Column(db.Float)
   batvolt = db.Column(db.Float)
   pinion = db.Column(db.Float)
   spur = db.Column(db.Float)
   fgratio = db.Column(db.Float)
   wheeldiam = db.Column(db.Float)

def __init__(self, id, motkv, batvolt, pinion, spur, fgratio, wheeldiam):
   self.id = id
   self.motkv = motkv
   self.batvolt = batvolt
   self.pinion = pinion
   self.spur = spur
   self.fgratio = fgratio
   self.wheeldiam = wheeldiam


#use this type of syntax to insert new data into the table
#sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
#val = ("John", "Highway 21")
#mycursor.execute(sql, val)

sql = "INSERT INTO webapp_user_input (ip, motkv, batvolt, pinion, spur, fgratio, wheeldiam) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val = [
   ('204.210.165.122', 2400, 16.8, 16, 54, 3.92, 2.5)
]
dbcursor.execute(sql,val)

db = db.commit()




