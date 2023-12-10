from data.class_dbmanager import DBManager
from data.utils import get_data

db_manager = DBManager()

db_manager.create_tables()  # создание таблиц

employers_data, vacancies_data = get_data()

db_manager.save_employers_to_db(employers_data)
db_manager.save_vacancies_to_db(vacancies_data)

db_manager.get_companies_and_vacancies_count()
db_manager.get_avg_salary()
db_manager.get_all_vacancies()
db_manager.get_vacancies_with_higher_salary()
