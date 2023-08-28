import sqlite3
##############################################
def execute_sql_from_file(sql_file, conn):
    with open(sql_file, 'r') as file:
        sql_statements = file.read()
    cursor = conn.cursor()
    cursor.executescript(sql_statements)
    conn.commit()

# 连接到数据库（如果不存在则会创建）
conn = sqlite3.connect('card_database.db')
cursor = conn.cursor()

# 创建卡牌信息表（如果不存在）
cursor.execute_sql_from_file("data/card_pool.sql", conn)

# 从文本文件中读取数据并添加到数据库表中
with open('data/card_pool.txt', 'r') as file:
    for line in file:
        data = line.strip().split(',')  # 假设数据使用逗号分隔
        pool_no = data[0]
        pool_name = data[1]
        pool_up = data[2]

        # 将数据插入数据库表中
        cursor.execute('''
            INSERT INTO card_pool (pool_no,pool_name,pool_up)
            VALUES (int, char, char)
        ''', (pool_no, pool_name, pool_up))

# 提交更改并关闭连接
conn.commit()
conn.close()

print("数据已成功添加到数据库中。")