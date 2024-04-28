#!/bin/bash

# Массив команд
#commands=("python 1_ПрямойПеребор.py", "python 2_АлгоритмРюкзак.py", "python 3_Жадный_алгоритм.py", "python 4_LogisticRegression.py")


# Список команд


# Массив команд


# Массив команд
commands=(
    "python3 1_ПрямойПеребор.py"
    "python3 2_АлгоритмРюкзак.py"
    "python3 3_Жадный_алгоритм.py"
    "python3 4_LogisticRegression.py"
    "python3 5_Алгоритм_поиска_независимого_множества_в_графе.py"

)

# Проходим по каждой команде
for cmd in "${commands[@]}"; do
    # Замеряем время начала выполнения команды в микросекундах
    start_time=$(date +%s%N)
    

    # Выполняем команду
    eval "$cmd"

    # Замеряем время окончания выполнения команды в микросекундах
    end_time=$(date +%s%N)
    

    # Вычисляем время выполнения команды в микросекундах
    execution_time=$((($end_time - $start_time) / 1000000000 ))

    # Выводим результат
    echo "Command \"$cmd\" executed in $execution_time seconds"
done