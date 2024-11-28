import json
import sys
import re


class ConfigConverter:
    def __init__(self):
        self.constants = {}

    def convert_value(self, value, indent_level=0):
        """Конвертирует значение из JSON в учебный конфигурационный язык."""
        indent = '  ' * indent_level  # Определяем текущий уровень отступа
        if isinstance(value, dict):
            return self.convert_dict(value, indent_level)
        elif isinstance(value, str):
            if value.isdigit():  # Если строка является числом
                return value  # Число как строка
            return f'@"{value}"'  # Оборачиваем строку в кавычки
        elif isinstance(value, (int, float)):
            return str(value)  # Числовые значения
        elif isinstance(value, list):
            return self.convert_list(value, indent_level)  # Обработка списков
        else:
            raise ValueError(f"Неподдерживаемый тип: {type(value)}")

    def convert_list(self, lst, indent_level):
        """Конвертирует список из JSON в учебный конфигурационный язык."""
        items = []
        for index, item in enumerate(lst):
            converted_item = self.convert_value(item, indent_level + 2)  # Увеличиваем уровень отступа
            items.append(f"{'  ' * (indent_level + 1)}{index} = {converted_item}")

        return f"{'  ' * indent_level}dict(\n" + ",\n".join(items) + f"\n{'  ' * indent_level})"

    def convert_dict(self, d, indent_level):
        """Конвертирует словарь из JSON в учебный конфигурационный язык."""
        items = []
        for key, value in d.items():
            if not re.match(r'^[a-zA-Z]+$', key):
                raise ValueError(f"Некорректное имя ключа: {key}")
            converted_value = self.convert_value(value, indent_level)
            items.append(f"{'  ' * indent_level}{key} = {converted_value}")

        return f"dict(\n" + ",\n".join(items) + f"\n{'  ' * indent_level})"

    def parse_and_convert(self, input_json):
        """Парсит JSON и конвертирует его в формат конфигурационного языка."""
        parsed_data = json.loads(input_json)
        return self.convert_dict(parsed_data, 0)


def main():
    converter = ConfigConverter()

    # Читаем JSON из стандартного ввода
    try:
        input_json = sys.stdin.read()
        output = converter.parse_and_convert(input_json)
        print(output)
    except json.JSONDecodeError as e:
        print(f"Ошибка разбора JSON: {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()