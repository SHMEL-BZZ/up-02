"""
Модуль конкуренции видов - модель данных и бизнес-логика
"""

import random
import csv
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Rat:
    """Класс крысы"""
    def __init__(self, species):
        self.species = species
        self.hostility = random.random()
        self.hunger = 0

    
    def to_dict(self):
        """Преобразует состояние крысы в словарь (для сохранения в CSV/JSON)"""
        return {
            'species': self.species,
            'hostility': round(self.hostility, 3),
            'hunger': self.hunger,
        }


class Cell:
    """Класс клетки поля"""
    def __init__(self):
        self.rats = []
        self.rye = False
    
    def to_dict(self):
        """Преобразует состояние клетки в словарь для сохранения"""
        return {
            'rats': [r.to_dict() for r in self.rats],
            'rye': self.rye
        }
