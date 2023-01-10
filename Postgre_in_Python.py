import psycopg2

def create_db_structure(cursor):
    """
    Создание таблиц
    """
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS client(
            client_id INTEGER PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            lastname VARCHAR(80) NOT NULL,
            Email VARCHAR(100) NOT NULL UNIQUE
            );
                """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS phone_number(
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(client_id),
            phone VARCHAR(70)
            );
                """)


def find_client(cursor):
    """
    Поиск клиента
    """
    param = input('Введите название столбца для поиска \n'
                  '(имя, фамилия, email, телефон): ')
    column = {'имя': 'name', 'фамилия': 'lastname', 'email': 'Email',
              'телефон': 'phone'}
    column_1 = column[param]
    value = input('Введите значение для поиска: ')
    cursor.execute(f"""SELECT * FROM client c 
                    JOIN phone_number p ON c.client_id = p.client_id 
                    WHERE {column_1}=%s;
                    """, (value,))
    return print(cursor.fetchall())



class Client:
    def __init__(self, client_id, name, lastname, Email, phone=None):
        self.client_id = client_id
        self.name = name
        self.lastname = lastname
        self.Email = Email
        self.phone = phone

    def add_new_client(self, cursor):
        """
        Добавление нового клиента
        """
        cursor.execute("""
                INSERT INTO client(client_id, name, lastname, Email)
                VALUES(%s, %s, %s, %s);
                """, (self.client_id, self.name, self.lastname, self.Email))
        cursor.execute("""
                INSERT INTO phone_number(client_id, phone)
                VALUES(%s, %s);
                """, (self.client_id, self.phone))

    def add_phone(self, cursor, new_phone):
        """
        Добавляет телефон для существующего клиента
        """
        cursor.execute("""
                INSERT INTO phone_number(client_id, phone) VALUES(%s, %s);
                """, (self.client_id, new_phone))

    def update_client(self, cursor):
        """
        Изменяет данные о клиенте
        """
        param = input('Введите название столбца который хотите изменить \n'
                      '(имя, фамилия, email, телефон): ')
        column = {'имя': 'name', 'фамилия': 'lastname', 'email': 'Email',
                  'телефон': 'phone'}
        column_1 = column[param]
        value = input('Введите значение на которое хотите изменить: ')
        if column_1 != 'phone':
            cursor.execute(f"""
                UPDATE client SET {column_1}=%s WHERE client_id=%s;
                """, (value, self.client_id))
        else:
            cursor.execute(f"""
                UPDATE phone_number SET {column_1}=%s WHERE client_id=%s;
                """, (value, self.client_id))

    def del_client_phone(self, cursor, phone: str):
        """
        Удаляет телефон клиента
        """
        cursor.execute("""
                DELETE FROM phone_number WHERE client_id=%s and phone=%s;
                """, (self.client_id, phone))

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

if __name__ == "__main__":
    with psycopg2.connect(database='client_db', user='postgres', password='576504') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    DROP TABLE phone_number;
                    DROP TABLE client;
                    """)
            create_db_structure(cur)
            client1 = Client(1, 'Alex', 'Petrov', 'petr@mail.ru', 921764)
            client1.add_new_client(cur)
            client2 = Client(2, 'Egor', 'Ivanov', 'ivan@gmail.com', 123123)
            client2.add_new_client(cur)
            client1.add_phone(cur, 456456)
            client1.update_client(cur)
            client1.del_client_phone(cur, '456456')
            client2.del_client(cur)
            find_client(cur)

    conn.close()
