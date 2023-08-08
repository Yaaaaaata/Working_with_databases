import requests
import psycopg2


def get_vacancies():
    """
    Получает список вакансий с сайта hh.ru.

    Returns:
        Список вакансий.
    """
    url = 'https://api.hh.ru/vacancies'
    regions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    params = {
        "per_page": 100,
        "page": 0
    }
    headers = {
        "User-Agent": "api-test-agent",
    }

    all_vacancies = []

    for region in regions:
        params['area'] = region
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        total_pages = data['pages']

        for page in range(0, total_pages):
            params['page'] = page
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            all_vacancies += data['items']

    vacancies = []
    required_companies = ['AliExpress Россия', 'ANABAR', 'hotellab.io', 'CoMagic.dev',
                          'Effective Mobile', 'Hammer Systems', 'Blue underlined link', 'iFuture',
                          'amoCRM', 'Jaxel', 'Konica Minolta', 'MedMundus', 'Positron - Студия Грохотова', 'ROIburo',
                          'Twinby', 'Spider Group', 'Апэрбот', 'Виста', 'Девелоника', 'КСЕНЬЕВСКИЙ ПРИИСК', 'МДО',
                          'Мэврика', 'Новео', 'Перспективный стартап', 'ПИКАССО', 'Полезный Софт', 'РУ-Ю',
                          'Цифровые привычки', 'Телеком-Инжиниринг']

    for vacancy in all_vacancies:
        employer_name = vacancy['employer']['name']
        if employer_name in required_companies:
            vacancies.append(vacancy)

    return vacancies


def fill_table():
    """
    Заполняет таблицу vacancies в базе данных данными о вакансиях.

    Returns:
        Отсортированный список вакансий из таблицы.
    """
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='vacancies',
        user='postgres',
        password='19Sonnik94'
    )
    cursor = conn.cursor()

    vacancies = get_vacancies()

    for vacancy in vacancies:
        employer_name = vacancy['employer']['name']
        vacancy_name = vacancy['name']
        salary = vacancy.get('salary')
        if salary is not None:
            salary_from = salary.get('from')
            salary_to = salary.get('to')
            salary_currency = salary.get('currency')
        else:
            salary_from = None
            salary_to = None
            salary_currency = None
        vacancy_link = vacancy['alternate_url']
        cursor.execute(
            "INSERT INTO vacancies (company_name, vacancy_name, salary_from, salary_to, salary_currency, vacancy_link) VALUES (%s, %s, %s, %s, %s, %s)",
            (employer_name, vacancy_name, salary_from, salary_to, salary_currency, vacancy_link))

    cursor.execute("SELECT * FROM vacancies ORDER BY company_name ASC")
    sorted_vacancies = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return sorted_vacancies


if __name__ == "__main__":
    fill_table()
