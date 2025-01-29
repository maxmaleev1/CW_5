from typing import Any
import psycopg2


class DBManager:
    """
    Класс для работы с базой данных для извлечения информации (город, вакансия, ЗП, компания, ссылка) о вакансиях и компаниях:
    - Получение списка всех компаний и количества вакансий у каждой компании
    - Получение списка всех вакансий
    - Получение средней ЗП по вакансиям
    - Получение вакансий с ЗП выше средней
    - Получение вакансий, содержащих ключевое слово
    """
    def __init__(self, **params: dict[str, Any]) -> None:
        """Инициализирует объект DBManager с параметрами для подключения к базе данных"""
        self.db_name = params.get("db_name")
        self.params = params

    def connect(self) -> Any:
        """Устанавливает соединение с базой данных"""
        # Проверяем, что все необходимые параметры присутствуют
        required_params = ["host", "user", "password", "port"]
        for param in required_params:
            if param not in self.params:
                raise ValueError(f"Отсутствует обязательный параметр: {param}")
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.params.get("user"),
                password=self.params.get("password"),
                host=self.params.get("host", "localhost"),  # Значение по умолчанию
                port=self.params.get("port", 5432),  # Значение по умолчанию
            )
            return conn
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных {self.db_name}: {e}")

    def get_companies_and_vacancies_count(self) -> Any:
        """Получает список всех компаний и количества вакансий у каждой компании"""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT employer.employer_name, COUNT(vacancy_id) FROM vacancies
                        JOIN employer ON employer.employer_id = vacancies.employer_id
                        GROUP BY employer_name
                        ORDER BY COUNT(vacancy_id) DESC
                        """
                    )
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print(f"Ошибка при получении количества вакансий по компаниям: {e}")

    def get_all_vacancies(self) -> Any:
        """Получает список всех вакансий"""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT employer.employer_name, vacancies.city, vacancies.vacancy_name, vacancies.salary, vacancies.vacancy_url
                        FROM vacancies
                        JOIN employer ON employer.employer_id = vacancies.employer_id
                        ORDER BY vacancies.salary DESC
                        """
                    )
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print(f"Ошибка при получении всех вакансий: {e}")

    def get_avg_salary(self) -> Any:
        """Получает среднюю ЗП по вакансиям"""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT vacancies.vacancy_name, AVG(vacancies.salary) FROM vacancies
                        GROUP BY vacancies.vacancy_name
                        ORDER BY AVG(vacancies.salary) DESC
                        """
                    )
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print(f"Ошибка при получении средней зарплаты: {e}")

    def get_vacancies_with_higher_salary(self) -> Any:
        """Получает вакансии с ЗП выше средней"""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT employer.employer_name, vacancies.city, vacancies.vacancy_name, vacancies.salary, vacancies.vacancy_url
                        FROM vacancies
                        JOIN employer ON employer.employer_id = vacancies.employer_id
                        WHERE salary > (SELECT AVG(salary) FROM vacancies)
                        ORDER BY vacancies.salary DESC                      
                        """
                    )
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Получает вакансии, содержащие ключевое слово"""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT employer.employer_name, vacancies.city, vacancies.vacancy_name, vacancies.salary, vacancies.vacancy_url
                        FROM vacancies
                        JOIN employer ON employer.employer_id = vacancies.employer_id
                        WHERE vacancy_name LIKE %s
                        ORDER BY vacancies.salary DESC
                        """,
                        (f"%{keyword}%",),  # Параметр передается как кортеж
                    )
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print(f"Ошибка при получении вакансий с ключевым словом {keyword}: {e}")