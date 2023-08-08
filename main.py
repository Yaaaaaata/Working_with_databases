from bd import DBManager
import psycopg2
from vacancies import fill_table


def check_table_empty():
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='vacancies',
        user='postgres',
        password='19Sonnik94'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vacancies")
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count == 0


if __name__ == "__main__":
    if check_table_empty():
        fill_table()

    db_manager = DBManager('localhost', '5432', 'vacancies', 'postgres', '19Sonnik94')

    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    print(companies_and_vacancies_count)

    all_vacancies = db_manager.get_all_vacancies()
    print(all_vacancies)

    avg_salary = db_manager.get_avg_salary()
    print(avg_salary)

    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    print(vacancies_with_higher_salary)

    vacancies_with_keyword = db_manager.get_vacancies_with_keyword('python')
    print(vacancies_with_keyword)
