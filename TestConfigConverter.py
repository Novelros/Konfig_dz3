import unittest
from ConfigConverter import ConfigConverter  # Импортируем ваш класс ConfigConverter

class TestConfigConverter(unittest.TestCase):
    def setUp(self):
        self.converter = ConfigConverter()

    def test_basic_string_conversion(self):
        input_json = '{"name": "Alice"}'
        expected_output = 'dict(\nname = @"Alice"\n)'
        self.assertEqual(self.converter.parse_and_convert(input_json), expected_output)

    def test_basic_number_conversion(self):
        input_json = '{"age": 30}'
        expected_output = 'dict(\nage = 30\n)'
        self.assertEqual(self.converter.parse_and_convert(input_json), expected_output)

    def test_nested_dict_conversion(self):
        input_json = '{"user": {"name": "Bob", "age": 25}}'
        expected_output = 'dict(\nuser = dict(\nname = @"Bob",\nage = 25\n)\n)'
        self.assertEqual(self.converter.parse_and_convert(input_json), expected_output)

    def test_list_conversion(self):
        input_json = '{"tags": ["tag1", "tag2"]}'
        expected_output = 'dict(\ntags = dict(\n  0 = @"tag1",\n  1 = @"tag2"\n)\n)'
        self.assertEqual(self.converter.parse_and_convert(input_json), expected_output)

    def test_complex_structure(self):
        input_json = '{"title": "Hello World", "content": "This is a post.", "tags": ["example", "test"], "likes": 100}'
        expected_output = 'dict(\ntitle = @"Hello World",\ncontent = @"This is a post.",\ntags = dict(\n  0 = @"example",\n  1 = @"test"\n),\nlikes = 100\n)'
        self.assertEqual(self.converter.parse_and_convert(input_json), expected_output)

    def test_error_on_invalid_key(self):
        input_json = '{"user-name": "Charlie"}'  # Некорректное имя ключа должно вызвать ошибку
        with self.assertRaises(ValueError):
            self.converter.parse_and_convert(input_json)

    def test_error_on_unsupported_type(self):
        input_json = '{"data": {"key": null}}'  # Значение None не поддерживается
        with self.assertRaises(ValueError):
            self.converter.parse_and_convert(input_json)

if __name__ == '__main__':
    unittest.main()