"""
config_loader.py — Завантаження YAML-конфігурацій для системи.
"""

import yaml
import os


def load_config(path: str) -> dict:
    """
    Завантажує YAML-конфігурацію з вказаного шляху.

    :param path: Шлях до конфігураційного файлу
    :return: Дані конфігурації як словник
    :raises FileNotFoundError, yaml.YAMLError
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл конфігурації не знайдено: {path}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Помилка YAML-парсингу: {e}")

    if not isinstance(config, dict):
        raise ValueError("Формат конфігурації має бути словником (dict)")

    return config
