import psycopg2

conn = psycopg2.connect(database=, user=, password=)


def create_db_structure(cursor):
    """
    Создание таблиц
    """
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client(
    client_id INTEGER PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    lastname VARCHAR(80) NOT NULL,
    e_mail VARCHAR(100) NOT NULL UNIQUE
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phone_number(
    phone_id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES client(client_id),
    phone VARCHAR(70)
    );
    """)
    conn.commit()

def find_client(cursor, name=None, lastname=None, e_mail=None, phone=None):
    """
    Поиск клиента
    """
    cursor.execute("""
    SELECT * FROM client c 
    JOIN phone_number p ON c.client_id = p.client_id 
    WHERE name=%s or lastname=%s or e_mail=%s or phone=%s;
    """, (name, lastname, e_mail, phone))
    return print(cursor.fetchall())

class Client:
    def __init__(self, client_id, name, lastname, e_mail, phone=None):
        self.client_id = client_id
        self.name = name
        self.lastname = lastname
        self.e_mail = e_mail
        self.phone = phone

    def add_new_client(self, cursor):
        """
        Добавление нового клиента
        """
        cursor.execute("""
        INSERT INTO client(client_id, name, lastname, e_mail) VALUES(%s, %s, %s, %s);
        """, (self.client_id , self.name, self.lastname, self.e_mail))
        cursor.execute("""
        INSERT INTO phone_number(client_id, phone) VALUES(%s, %s);
        """, (self.client_id, self.phone))
        conn.commit()

    def add_phone(self,cursor, new_phone):
        """
        Добавляет телефон для существующего клиента
        """
        cursor.execute("""
        INSERT INTO phone_number(client_id, phone) VALUES(%s, %s);
        """, (self.client_id, new_phone))
        return conn.commit()

    def update_client(self, cursor, name1=None, lastname1=None, e_mail1=None, phone1=None):
        """
        Изменяет данные о клиенте
        """
        cursor.execute("""
        UPDATE client SET name=%s, lastname=%s, e_mail=%s
        WHERE client_id=%s;
        """, (name1,lastname1, e_mail1, self.client_id))
        if phone1 != None:
            cursor.execute("""
            UPDATE phone_number SET phone=%s WHERE client_id=%s;
            """, (phone1, self.client_id))
        conn.commit()

    def del_client_phone(self, cursor, phone:str):
        """
        Удаляет телефон клиента
        """
        cursor.execute("""
        DELETE FROM phone_number WHERE client_id=%s and phone=%s;
        """, (self.client_id, phone))
        conn.commit()

    def del_client(self, cursor):
        """
        Удаляет клиента
        """
        cursor.execute("""
        DELETE FROM phone_number WHERE client_id=%s;
        """, (self.client_id,))
        cursor.execute("""
        DELETE FROM client WHERE client_id=%s;
        """, (self.client_id,))
        conn.commit()


with conn.cursor() as cur:
    create_db_structure(cur)
    client1 = Client(1, 'Alex', 'Petrov', 'petr@mail.ru', 921764)
    client1.add_new_client(cur)
    client2 = Client(2, 'Egor', 'Ivanov', 'ivan@gmail.com', 123123)
    client2.add_new_client(cur)
    client1.add_phone(cur, 456456)
    client1.update_client(cur, 'Ivan', 'Ivanov', 'ivanpetr@mail.ru')
    client1.del_client_phone(cur, '456456')
    client2.del_client(cur)
    find_client(cur, 'Ivan', 'Ivanov', 'ivanpetr@mail.ru', '921764')

conn.close()