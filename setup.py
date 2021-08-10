import sqlite3
import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hash_passwd = pwd_context.hash("admin")
date = datetime.date.today()
str = f"insert into users (id, name, account, email, passwd, department, manager, hr, on_job, off_job, status) values (\'1\', \'admin\',\'admin\', \'admin@gmail.com\', \'{hash_passwd}\', \'admin\', \'True\', \'True\', \'{date}\', \'{date}\', \'0\')"

db = sqlite3.connect("attendance/attendance.db")
cursor = db.cursor()
cursor.execute(str)
cursor.close()
db.commit()
db.close()