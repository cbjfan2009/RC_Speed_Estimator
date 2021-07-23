#from SQLAlchemy import *
import mysql_connector
estimator_db = mysql_connector.connect(
    host='localhost',
    user="devMatt",
    password="D3V3l0pm3ntS3rV3rcbjfan2009")

print(estimator_db)