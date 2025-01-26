import requests
from src.config import employer_id


class HeadHunterAPI:
    """
    Выполняет загрузку вакансий с API HeadHunter, проверку последних на наличие обязательных полей
    (ЗП и адреса) и их валидацию
    """

    def __init__(self) -> None:
        """
        Инициализирует объект для работы с API HeadHunter.
        Устанавливает базовый URL для запросов, заголовки, параметры поиска вакансий и выполняет
        загрузку вакансий и их валидацию
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": None, "page": 0, "per_page": 100, "employer_id": employer_id}
        self.__vacancies: list = []
        self._load_vacancies()
        self._validate_vacancy()

    @property
    def vacancies(self) -> list:
        """Возвращает список вакансий"""
        return self.__vacancies

    def _load_vacancies(self) -> None:
        """Загружает вакансии с API HeadHunter в количестве указанных страниц (2000 вакансий (20 страниц))"""
        while self.__params["page"] != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code != 200:
                raise requests.HTTPError(f"Ошибка при запросе к API: статус {response.status_code}")

            vacancies = response.json().get("items", [])

            self.__vacancies.extend(vacancies)

            # Обеспечиваем, что self.params["page"] всегда целое число
            current_page = self.__params["page"]
            if isinstance(current_page, int):  # Проверка на тип
                self.__params["page"] = current_page + 1

    def _validate_vacancy(self) -> None:
        """Удаляет вакансии, если ЗП или адрес не указаны"""
        for vacancy in self.__vacancies.copy():
            if vacancy["salary"] is None or vacancy["address"] is None:
                self.__vacancies.remove(vacancy)