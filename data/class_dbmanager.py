import os

import psycopg2
from dotenv import load_dotenv


class DBManager:
    """Класс для управления базой данных."""
    load_dotenv()

    def __init__(self):
        self.database = os.getenv('db_name')
        self.host = os.getenv('db_host')
        self.user = os.getenv('db_user')
        self.password = os.getenv('db_password')

        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password)

    def create_tables(self):
        """Создает таблицы employers и vacancies, если они не существуют."""
        query = """
            CREATE TABLE IF NOT EXISTS employers (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL);
            CREATE TABLE IF NOT EXISTS vacancies (name VARCHAR(255) NOT NULL, employer VARCHAR NOT NULL,
                salary INT, employer_id SERIAL REFERENCES employers(id), url TEXT)
        """
        with self.conn, self.conn.cursor() as cursor:
            cursor.execute(query)

    def get_companies_and_vacancies_count(self):
        """Возвращает список компаний и количество вакансий у каждой компании."""
        query = "SELECT employer, COUNT(*) AS vacancies_count FROM vacancies GROUP BY employer"
        with self.conn, self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return results

    def save_employers_to_db(self, data):
        """Сохраняет данные о работодателях в базу данных."""
        query = "INSERT INTO employers (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        with self.conn, self.conn.cursor() as cursor:
            cursor.executemany(query, data)

    def save_vacancies_to_db(self, data):
        """Сохраняет данные о вакансиях в базу данных."""
        query = "INSERT INTO vacancies (name, employer, salary, employer_id, url) VALUES (%s, %s, %s, %s, %s)"
        with self.conn, self.conn.cursor() as cursor:
            cursor.executemany(query, data)

    def get_all_vacancies(self):
        """Возвращает все вакансии из базы данных."""
        query = "SELECT * FROM vacancies"
        with self.conn, self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return results

    def get_avg_salary(self):
        """Возвращает среднюю зарплату всех вакансий, где зарплата указана."""
        query = "SELECT AVG(salary) AS avg_salary FROM vacancies WHERE salary IS NOT NULL"
        with self.conn, self.conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        return round(result[0]) if result[0] else None

    def get_vacancies_with_higher_salary(self):
        """Возвращает все вакансии, у которых зарплата выше средней зарплаты."""
        avg_salary = 62091
        query = "SELECT * FROM vacancies WHERE salary > %s"
        with self.conn, self.conn.cursor() as cursor:
            cursor.execute(query, (avg_salary,))
            results = cursor.fetchall()
        return results

    def get_vacancies_with_keyword(self, keyword: str):
        """Возвращает все вакансии, содержащие указанное ключевое слово в названии."""
        query = "SELECT * FROM vacancies WHERE name ILIKE %s"
        with self.conn, self.conn.cursor() as cursor:
            cursor.execute(query, ('%' + keyword + '%',))
            results = cursor.fetchall()
        return results
