def load_data_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines[:-1]:  # Пропускаем последнюю строку (weight)
        row = [int(x) for x in line.strip().split(',')]
        data.append(row)

    weight = [float(x) for x in lines[-1].strip().split(',')]

    return data, weight

# Пример использования
file_path = 'input_with_weights.csv'
THCompatibilityMatrix, weight = load_data_from_file(file_path)

# Функция для проверки совместимости двух гипотез
def are_compatible(i, j):
    return THCompatibilityMatrix[i][j] == 1

# Функция для поиска независимого множества с максимальной суммой весов
def find_max_weight_independent_set():
    n = len(weight)
    solutions = []

    # Функция для рекурсивного перебора
    def backtrack(idx, curr_soln, curr_weight):
        if idx == n:
            solutions.append((curr_soln.copy(), curr_weight))
            return

        # Включить текущую гипотезу
        curr_soln.append(idx)
        new_weight = curr_weight + weight[idx]
        for j in range(idx + 1, n):
            if are_compatible(idx, j):
                backtrack(j + 1, curr_soln, new_weight)
        curr_soln.pop()

        # Не включать текущую гипотезу
        backtrack(idx + 1, curr_soln, curr_weight)

    # Вызов рекурсивной функции для перебора
    backtrack(0, [], 0)

    # Сортировка решений по убыванию суммы весов
    solutions.sort(key=lambda x: x[1], reverse=True)

    return solutions

solutions = find_max_weight_independent_set()
# Вывод результатов
file_path = 'out.csv'

with open(file_path, 'w') as file:
    # Записываем заголовок
    header = ','.join([f"TH{i}" for i in range(1, len(THCompatibilityMatrix[0]) + 1)])
    file.write(f",{header},sum(w)\n")

    # Записываем строки с данными
    for i, (solution, sum_weights) in enumerate(solutions, start=1):
        solution_str = ','.join(['1' if j in solution else '0' for j in range(len(THCompatibilityMatrix))])
        file.write(f"GH{i},{solution_str},{sum_weights:.3f}\n")