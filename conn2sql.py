import sqlite3
import random

# 创建数据库
def create_database_from_sql(sql_file, db_name):
    with open(sql_file, 'r') as file:
        sql_statements = file.read()

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executescript(sql_statements)
    conn.commit()
    conn.close()

# 数据写入数据库
#添加卡池信息
def insert_cardpool(text_file, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    with open(text_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            pool_no, pool_name,pool_up = line.strip().split(",")
            cursor.execute("INSERT INTO card_pool (pool_no,pool_name,pool_up) VALUES (?,?,?)",
                           (pool_no, pool_name,pool_up))         
    conn.commit()
    conn.close()
#添加卡牌信息
def insert_card(text_file, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    with open(text_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            card_no, card_name,card_kind,card_star= line.strip().split(",")
            cursor.execute("INSERT INTO card (card_no, card_name,card_kind,card_star) VALUES (?,?,?,?)",
                           (card_no, card_name,card_kind,card_star))         
    conn.commit()
    conn.close()
#添加卡池和卡牌信息
def insert_pool_card(text_file, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    with open(text_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            pool_name,card_name=line.strip().split(",")
            cursor.execute("INSERT INTO poolcard (pool_name, card_name) VALUES (?,?)",
                           (pool_name,card_name))         
    conn.commit()
    conn.close()

# 添加抽卡记录
def insert_draw_log(db_name,pool_name,card_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO draw_log (pool_name,card_name) VALUES (?,?)", (pool_name,card_name))
    
    conn.commit()
    conn.close()

#返回卡牌名
def get_cardname(pool_name, star, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT card_name FROM poolcard WHERE pool_name = ?", (pool_name,))
    pool_cards = cursor.fetchall()
    
    pool_cards = [card[0] for card in pool_cards]

    matching_star_cards = [card for card in pool_cards if get_card_star(card, conn) == star]

    if matching_star_cards:
        random_card = random.choice(matching_star_cards)
    else:
        random_card = None
    conn.close()

    return random_card

def get_card_star(card_name, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT card_star FROM card WHERE card_name = ?", (card_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
    
#将数据库的表输出为txt
def export_table_to_txt(table_name, db_name, txt_file):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    table_data = cursor.fetchall()
    conn.close()
    #写入文件
    with open(txt_file, 'w') as file:
        for row in table_data:
            row_str = "\t".join(str(value) for value in row)
            file.write(row_str + "\n")