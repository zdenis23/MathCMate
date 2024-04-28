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

# Функция для проверки совместимости
def is_compatible(solution, new_element):
    for i, x in enumerate(solution):
        if x == 1 and THCompatibilityMatrix[i][new_element] == 0:
            return False
    return True

# Жадный алгоритм
solution = []
total_weight = 0
indices = sorted(range(len(weight)), key=lambda x: -weight[x])

for idx in indices:
    if is_compatible(solution, idx):
        solution.append(idx)
        total_weight += weight[idx]

# Вывод результатов
def save_data_to_file(file_path, data, selected_indices, total_weight):
    with open(file_path, 'w') as file:
        # Записываем заголовок
        header = ','.join([f"TH{i}" for i in range(1, len(data[0]) + 1)])
        file.write(f",{header},sum(w)\n")

        # Записываем строки с данными
        for i, idx in enumerate(selected_indices, start=1):
            file.write(f"GH{i},")
            for val in data[idx]:
                file.write(f"{val},")
            file.write(f"1,{total_weight:.3f}\n")

# Пример использования
file_path_out = 'out.csv'
save_data_to_file(file_path_out, THCompatibilityMatrix, solution, total_weight)