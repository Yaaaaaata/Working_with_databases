import psycopg2


class DBManager:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cursor.execute("SELECT company_name, COUNT(*) AS vacancy_count FROM vacancies GROUP BY company_name")
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        self.cursor.execute("SELECT company_name, vacancy_name, salary_from, salary_to, salary_currency, vacancy_link FROM vacancies")
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cursor.execute("SELECT AVG(salary_from) AS avg_salary FROM vacancies WHERE salary_from IS NOT NULL")
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        self.cursor.execute("SELECT company_name, vacancy_name, salary_from, salary_to, salary_currency, vacancy_link FROM vacancies WHERE salary_from > %s", (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        self.cursor.execute("SELECT company_name, vacancy_name, salary_from, salary_to, salary_currency, vacancy_link FROM vacancies WHERE vacancy_name ILIKE %s", ('%' + keyword + '%',))
        return self.cursor.fetchall()
