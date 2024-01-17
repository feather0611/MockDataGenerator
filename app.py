import random
from datetime import datetime, timedelta
import pymysql

conn = pymysql.connect(
    host="YOUR_HOST",
    user="YOUR_ACCOUNT",
    password="YOUR_PASSWORD",
    database="YOUR_DATABASE",
)
cursor = conn.cursor(pymysql.cursors.DictCursor)

# for i in range(1000):
#     username = f"user_{i+1:04d}"
#     create_time = datetime.now() - timedelta(days=random.randint(1, 550), hours=random.randint(0, 24), minutes=random.randint(0, 60), seconds=random.randint(0, 60))
#     cursor.execute(
#         "INSERT INTO member (username, create_time) VALUES (%s, %s)",
#         (username, create_time),
#     )

for _ in range(5000):
    member_pk = random.randint(1, 1000)
    cursor.execute(
        f"SELECT pk, member_fk, borrow_time, create_time FROM borrow_fee WHERE member_fk = {member_pk} ORDER BY create_time DESC"
    )
    borrow_data = cursor.fetchall()

    cursor.execute(f"SELECT pk, create_time FROM member WHERE pk = {member_pk}")
    member_data = cursor.fetchone()

    type = 1
    borrow_fee = round(random.uniform(1, 10000), 2)
    create_time = member_data["create_time"] + timedelta(
        days=random.randint(0, 15),
        hours=random.randint(0, 24),
        minutes=random.randint(0, 60),
        seconds=random.randint(0, 60),
    )
    borrow_time = 1
    if len(borrow_data) != 0:
        type = 2
        create_time = borrow_data[0]["create_time"] + timedelta(
            days=random.randint(0, 15),
            hours=random.randint(0, 24),
            minutes=random.randint(0, 60),
            seconds=random.randint(0, 60),
        )
        borrow_time = borrow_data[0]["borrow_time"] + 1
    print(member_pk, type, borrow_fee, borrow_time, create_time)
    # 插入交易資料
    cursor.execute(
        f"INSERT INTO borrow_fee (member_fk, type, borrow_fee, borrow_time, create_time) VALUES ({member_pk}, {type}, {borrow_fee}, {borrow_time}, '{create_time}');"
    )

# 提交交易資料變更
conn.commit()

# 關閉資料庫連接
cursor.close()
conn.close()
