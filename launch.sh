#!/bin/bash

echo "🚀 Запуск системи 'Рій'..."

# Завантаження змінних із .env (якщо існує)
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Змінні середовища завантажено з .env"
else
    echo "⚠️  Файл .env не знайдено. Використовуються значення за замовчуванням."
fi

# Створення віртуального середовища, якщо його ще немає
if [ ! -d "venv" ]; then
    echo "📦 Створення віртуального середовища..."
    python3 -m venv venv
fi

# Активація віртуального середовища
source venv/bin/activate

# Встановлення залежностей
echo "📦 Встановлення залежностей..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧠 Запуск повної системи з GUI..."
python3 main.py

# Запуск swarm-системи (SwarmManager) напряму
echo "🧠 Запуск SwarmManager..."
python3 -c "
from core import config
from core.swarm_manager import SwarmManager

swarm = SwarmManager(config)
swarm.launch_swarm()
swarm.run_mission_loop()
"

