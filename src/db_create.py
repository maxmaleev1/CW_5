from typing import Any
import psycopg2


class DBCreate:
    """Создает базу данных, подключение к ней, и таблицы"""
    def __init__(self, **params: dict[str, Any]) -> None:
        """Инициализирует подключение к базе данных"""
        self.db_name = params.get("db_name")
        self.params = params
        try:
            self.conn = psycopg2.connect(
                dbname="postgres",
                user=self.params.get("user"),
                password=self.params.get("password"),
                host=self.params.get("host", "localhost"),  # Значение по умолчанию
                port=self.params.get("port", 5432),  # Значение по умолчанию
            )
            self.conn.autocommit = True
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных PostgreSQL: {e}")
            raise

        self.create_database()
        self.create_tables()

    def create_database(self) -> None:
        """Создает базу данных"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
                cur.execute(f"CREATE DATABASE {self.db_name}")

        except psycopg2.Error as e:
            print(f"Ошибка при создании базы данных: {e}")
            raise

        finally:
            self.conn.close()

    def create_tables(self) -> None:
        """Создает таблицы в базе данных"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.params.get("user"),
                password=self.params.get("password"),
                host=self.params.get("host", "localhost"),  # Значение по умолчанию
                port=self.params.get("port", 5432),  # Значение по умолчанию
            )
            # Подключение к новой базе
            self.conn.autocommit = True

            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE employer (
                        employer_id int UNIQUE PRIMARY KEY,
                        employer_name VARCHAR(100),
                        employer_url VARCHAR(100)
                    )
                """
                )

                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        vacancy_name VARCHAR(100),
                        vacancy_url VARCHAR(100),
                        city VARCHAR(50),
                        salary INT,
                        employer_id INT,
                        FOREIGN KEY (employer_id) REFERENCES employer(employer_id)
                    )
                """
                )

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
            raise
        finally:
            self.conn.commit()
            self.conn.close()

    def insert_data_to_db(self, vacancies: list[dict]) -> None:
        """Заполняет данные в таблицы базы данных"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.params.get("user"),
                password=self.params.get("password"),
                host=self.params.get("host", "localhost"),  # Значение по умолчанию
                port=self.params.get("port", 5432),  # Значение по умолчанию
            )
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                for vacancy in vacancies:
                    try:
                        employer = vacancy.get("employer")
                        if employer:
                            employer_id = employer.get("id")
                            employer_name = employer.get("name")
                            employer_url = employer.get("alternate_url")

                            cur.execute(
                                """
                                INSERT INTO employer (employer_id, employer_name, employer_url)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (employer_id) DO NOTHING
                                RETURNING employer_id
                                """,
                                (employer_id, employer_name, employer_url),
                            )

                            result = cur.fetchone()
                            if result:
                                employer_id = result[0]

                        else:
                            print(f"Данные о работодателе отсутствуют для вакансии {vacancy.get('id')}")
                            continue

                        salary_from = vacancy.get("salary", {}).get("from")
                        salary_to = vacancy.get("salary", {}).get("to")
                        salary = salary_from if salary_from is not None else salary_to
                        address = vacancy.get("address")
                        city = address.get("city") if address else None

                        cur.execute(
                            """
                            INSERT INTO vacancies (vacancy_name, vacancy_url, city, salary, employer_id)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (
                                vacancy.get("name"),
                                vacancy.get("alternate_url"),
                                city,
                                salary,
                                employer_id,
                            ),
                        )

                    except psycopg2.Error as e:
                        print(f"Ошибка при обработке вакансии {vacancy.get('id')}: {e}")
                        continue
                    except KeyError as e:
                        print(f"KeyError: отсутствует ключ {e} в вакансии {vacancy.get('id')}")
                        continue
                    except TypeError as e:
                        print(f"TypeError: неверный тип данных в вакансии {vacancy.get('id')}: {e}")
                        continue
                    except Exception as e:
                        print(f"Неизвестная ошибка при обработке вакансии {vacancy.get('id')}: {e}")
                        continue

        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных для вставки данных: {e}")
            raise
        finally:
            self.conn.commit()
            self.conn.close()