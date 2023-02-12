import csv

from django.test import TestCase

import os

from .dlp_component.slack_.data_search.text import SlackTextDataSearch
from .dlp_component.slack_.data_search.files import (
    CsvFileDataSearch,
    TxtFileDataSearch,

    SlackFilesDataSearch,
)
from .models import ReTemplate


class SlackTextDataSearchTestCase(TestCase):
    def setUp(self):
        ReTemplate.objects.create(pattern=r'\b123\b')

    def test_text_find_data(self):
        re_template = ReTemplate.objects.get(pattern=r'\b123\b')

        text_1 = 'Hello! How are you?'
        text_2 = '123 1234'

        slack_text_data_search_1 = SlackTextDataSearch(text_1)
        text_data_1 = slack_text_data_search_1.find_data(re_template.rpattern)

        slack_text_data_search_2 = SlackTextDataSearch(text_2)
        text_data_2 = slack_text_data_search_2.find_data(re_template.rpattern)

        self.assertEqual(text_data_1, [])
        self.assertEqual(text_data_2, ['123'])


class SlackFileDataSearchTestCase(TestCase):
    def setUp(self):
        ReTemplate.objects.create(pattern=r'\b12345\b')

        with open('test_1.txt', 'w') as f:
            f.write('1234567890\n0987654321')

        with open('test_2.txt', 'w') as f:
            f.write('12345\n1234567890')

        with open('test_3.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Name', 'Number'])
            writer.writerow(['Test name 1', '123'])
            writer.writerow(['Test name 2', '12345'])

    def test_text_find_data(self):
        re_template = ReTemplate.objects.get(pattern=r'\b12345\b')

        with open('test_1.txt', 'rb') as f:
            file_bytes_1 = f.read()

        with open('test_2.txt', 'rb') as f:
            file_bytes_2 = f.read()

        with open('test_3.csv', 'rb') as f:
            file_bytes_3 = f.read()

        file_data_search_1 = TxtFileDataSearch(
            file_bytes_1,
            'test_1.txt',
            'txt',
        )
        file_data_search_2 = TxtFileDataSearch(
            file_bytes_2,
            'test_2.txt',
            'txt',
        )
        file_data_search_3 = CsvFileDataSearch(
            file_bytes_3,
            'test_3.csv',
            'csv',
        )
        file_data_search_list = [
            file_data_search_1,
            file_data_search_2,
            file_data_search_3,
        ]

        files_data_search = SlackFilesDataSearch(file_data_search_list)
        data = files_data_search.find_data(re_template.rpattern)

        self.assertNotIn(file_data_search_1, data)
        self.assertIn(file_data_search_2, data)
        self.assertIn(file_data_search_3, data)

        os.remove('test_1.txt')
        os.remove('test_2.txt')
        os.remove('test_3.csv')
