
# database/db.py
import sqlite3
from datetime import datetime

DB_NAME = "data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS debtor_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            debtor_name TEXT NOT NULL,
            card_category INTEGER NOT NULL,
            cards_count INTEGER NOT NULL,
            total_amount INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usercard TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS User_card1000 (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        card TEXT UNIQUE
    )
    """)
    try:
        cur.execute("ALTER TABLE User_card1000 ADD COLUMN used INTEGER DEFAULT 0")
        cur.execute("ALTER TABLE User_card500 ADD COLUMN used INTEGER DEFAULT 0")
        cur.execute("ALTER TABLE User_card300 ADD COLUMN used INTEGER DEFAULT 0")
        cur.execute("ALTER TABLE User_card200 ADD COLUMN used INTEGER DEFAULT 0")
    except:
        pass  

    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS User_card500 (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        card TEXT UNIQUE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS User_card300 (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        card TEXT UNIQUE
    )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS User_card200 (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        card TEXT UNIQUE
    )
    """)
    ####################################################3
    cur.execute("""
            CREATE TABLE IF NOT EXISTS debt_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL
            
    )
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS cash_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL
           
        )

    """)
    
    

    conn.commit()
    conn.close()

def add_card(usercard):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO user_cards (usercard) VALUES (?)",
        (usercard,)
    )

    conn.commit()
    conn.close()
def get_cards_desc():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT usercard 
        FROM user_cards
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_total(tab):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT SUM(amount) FROM {tab}")
    total = cur.fetchone()[0] or 0
    conn.close()
    return total


def count_available_cards(table_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE used = 0")
    count = cur.fetchone()[0]

    conn.close()
    return count

def buy_cards(table_name, quantity):
    conn = get_connection()
    cur = conn.cursor()

    # 1️⃣ جلب الكروت غير المستخدمة
    cur.execute(f"""
        SELECT ID, card 
        FROM {table_name}
        WHERE used = 0
        ORDER BY ID ASC
        LIMIT ?
    """, (quantity,))

    cards = cur.fetchall()

    if not cards:
        conn.close()
        return [], "❌ لا يوجد كروت متاحة"

    # 2️⃣ استخراج IDs
    ids = [str(c[0]) for c in cards]

    # 3️⃣ تحديث الكروت إلى مستخدمة
    cur.execute(
        f"UPDATE {table_name} SET used = 1 WHERE ID IN ({','.join(['?']*len(ids))})",
        ids
    )

    conn.commit()
    conn.close()

    # 4️⃣ إرجاع الكروت فقط
    return [c[1] for c in cards], "✅ تم البيع بنجاح"


def add_amount(amount,tabl_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO {tabl_name} (amount)
        VALUES (?)
    """, (
        amount,

    ))

    conn.commit()
    conn.close()

def add_card_to_table(table_name, card):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"INSERT INTO {table_name} (card) VALUES (?)", (card,))
    
    conn.commit()
    conn.close()


def insert_debtor_sale(debtor_name, card_category, cards_count):
    total_amount = int(card_category) * int(cards_count)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO debtor_sales 
        (debtor_name, card_category, cards_count, total_amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        debtor_name,
        card_category,
        cards_count,
        total_amount,
        datetime.now().strftime("%y-%m-%d  %H:%M")
    ))

    conn.commit()
    conn.close()
def print_all_user_card(table_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT 
            id,card
           
        FROM {table_name}
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    if not rows:
        return "لا توجد بيانات"
    else:
        return rows
    conn.close()
        

def print_all_debtor_sales():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            id,
            debtor_name,
            card_category,
            cards_count,
            total_amount,
            created_at
        FROM debtor_sales
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    print("📋 سجل عمليات الدَّين:")
    print("-" * 50)

    for row in rows:
        print(
            f"ID: {row[0]} | "
            f"المدين: {row[1]} | "
            f"الفئة: {row[2]} | "
            f"عدد الكروت: {row[3]} | "
            f"الإجمالي: {row[4]} | "
            f"التاريخ: {row[5]}"
        )

    if not rows:
        print("لا توجد بيانات.")

def filter_debtors(e):
    keyword = debtor_input.value.strip()
    debtor_list_view.controls.clear()

    if not keyword:
        page.update()
        return

    # 👇 جلب الأسماء من قاعدة البيانات
    results = db.search_debtors_by_name(keyword)

    for name in results:
        debtor_list_view.controls.append(
            ft.ListTile(
                title=ft.Text(name),
                on_click=lambda ev, n=name: select_debtor(n)
            )
        )

    page.update()
def search_debtors_by_name(keyword):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT debtor_name
        FROM debtor_sales
        WHERE debtor_name LIKE ?
        GROUP BY debtor_name
        ORDER BY debtor_name
    """, (f"{keyword}%",))

    results = [row[0] for row in cur.fetchall()]
    conn.close()

    return results
def delete_all_debtor_sales():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM debtor_sales")

    conn.commit()
    conn.close()
    print("تم حذف جميع عمليات الدَّين")
    
def delet_usercard(table_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"DELETE FROM {table_name}")
    cur.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

    conn.commit()
    conn.close()
    print("تم حذف جميع عمليات الدَّين")

def count_cards(table_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]

    conn.close()
    return count

def get_debtors_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT debtor_name, SUM(total_amount)
        FROM debtor_sales
        WHERE debtor_name != ''
        GROUP BY debtor_name
        ORDER BY SUM(total_amount) DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def get_debtor_details(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, card_category, cards_count, total_amount, created_at
        FROM debtor_sales
        WHERE debtor_name = ?
        ORDER BY created_at DESC
    """, (name,))

    data = cursor.fetchall()
    conn.close()
    return data
def delete_debtor(name):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM debtor_sales WHERE debtor_name=?", (name,))
    conn.commit()
    conn.close()

def get_last_debtor_sale():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT debtor_name, card_category, cards_count, total_amount
        FROM debtor_sales
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    return row  # None إذا لا توجد بيانات


conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()
print_all_debtor_sales()
