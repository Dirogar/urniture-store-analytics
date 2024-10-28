import re


def natural_key(string):
    """Функция для разделения строки на части (буквы и числа) для
    натуральной сортировки"""
    return [int(text) if text.isdigit() else text.lower() for text in
            re.split(r'(\d+)', string)]
