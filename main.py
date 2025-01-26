from src.config import config
from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.db_create import DBCreate


def main() -> None:
    config()
    hh = HeadHunterAPI()
    params = config()
    db = DBCreate(**params)
    # Вставка данных о вакансиях в базу данных
    db.insert_data_to_db(hh.vacancies)
    # Подключение к базе данных через DBManager
    db_headhunter = DBManager(**params)


    print("\nЗДРАВСТВУЙТЕ. ПРЕДЛАГАЮ РАССМОТРЕТЬ ВАКАНСИИ КОМПАНИЙ ИЗ ТОП-10 2023г.:\n")
    print("КОЛИЧЕСТВО ВАКАНСИЙ В КОМПАНИЯХ:\n")
    companies_vacancies = db_headhunter.get_companies_and_vacancies_count()
    if companies_vacancies:
        for company, count_vacancies in companies_vacancies:
            print(f"Компания:   {company}")
            print(f"Вакансий:   {count_vacancies}\n")
    else:
        print("\nВАКАНСИИ НЕ НАЙДЕНЫ\n")


    print("\nВСЕ ВАКАНСИИ:\n")
    vacancies = db_headhunter.get_all_vacancies()
    if vacancies:
        for vacancy in vacancies:
            employer_name, city, vacancy_name, salary, vacancy_url = vacancy
            print(f"Город:      {city}")
            print(f"Компания:   {employer_name}")
            print(f"Вакансия:   {vacancy_name}")
            print(f"ЗП:         {salary} руб.")
            print(f"Ссылка:     {vacancy_url}\n")
    else:
        print("\nНЕ УДАЛОСЬ ПОЛУЧИТЬ ИНФОРМАЦИЮ О ВСЕХ ВАКАНСИЯХ\n")


    print("\nСРЕДНЯЯ ЗП ПО ВАКАНСИЯМ:\n")
    avg_salary = db_headhunter.get_avg_salary()
    if avg_salary:
        for vacancy_name, avg in avg_salary:
            print(f"Вакансия:     {vacancy_name}")
            print(f"Средняя ЗП:   {round(avg, 2)} руб.\n")
    else:
        print("\nНЕ УДАЛОСЬ ПОЛУЧИТЬ ИНФОРМАЦИЮ О СРЕДНЕЙ ЗП\n")

    print("\nВАКАНСИИ С ЗП ВЫШЕ СРЕДНЕЙ:\n")
    high_salary_vacancies = db_headhunter.get_vacancies_with_higher_salary()
    if high_salary_vacancies:
        for vacancy in high_salary_vacancies:
            employer_name, city, vacancy_name, salary, vacancy_url = vacancy
            print(f"Город:      {city}")
            print(f"Компания:   {employer_name}")
            print(f"Вакансия:   {vacancy_name}")
            print(f"Ссылка:     {vacancy_url}")
            print(f"ЗП:         {salary} руб.\n")
    else:
        print("\nНЕ УДАЛОСЬ ПОЛУЧИТЬ ИНФОРМАЦИЮ О ВАКАНСИЯХ С ЗП ВЫШЕ СРЕДНЕЙ\n")


    while input("\nХОТИТЕ ПОИСКАТЬ ВАКАНСИИ ПО КЛЮЧЕВОМУ СЛОВУ? (да/нет): ") == "да":
        keyword_for_searching = input("ВВЕДИТЕ КЛЮЧЕВОЕ СЛОВО ДЛЯ ПОИСКА ВАКАНСИЙ: ")
        if keyword_for_searching:
            search_results = db_headhunter.get_vacancies_with_keyword(keyword_for_searching)
            if search_results:
                for vacancy in search_results:
                    employer_name, city, vacancy_name, salary, vacancy_url = vacancy
                    print()
                    print(f"Город:      {city}")
                    print(f"Вакансия:   {vacancy_name}")
                    print(f"ЗП:         {salary} руб.")
                    print(f"Компания:   {employer_name}")
                    print(f"Ссылка:     {vacancy_url}")
            else:
                print("\nВАКАНСИИ С ВВЕДЕННЫМ КЛЮЧЕВЫМ СЛОВОМ НЕ НАЙДЕНЫ\n")
    print('\nВЫПОЛНЕНИЕ ПРОГРАММЫ ЗАВЕРШЕНО. УДАЧНОГО ТРУДОУСТРОЙСТВА!')


if __name__ == "__main__":
    main()