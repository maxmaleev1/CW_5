from configparser import ConfigParser


employer_id = [
    "80",
    "1740",
    "4181",
    "4219",
    "1373",
    "39305",
    "3388",
    "15478",
    "4233",
    "3809",
]

def config(filename: str = "src/database.ini", section: str = "postgresql") -> dict:
    """
    Читает конфигурационный файл и извлекает параметры для подключения к базе данных.
    Метод ищет в файле конфигурации секцию, указанную в параметре `section` (по умолчанию "postgresql"),
    и извлекает все параметры, определенные в этой секции
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # Проверка чтения файла с конфигурацией
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file.".format(section, filename))
    return db