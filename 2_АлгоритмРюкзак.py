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

# Функция для проверки совместимости гипотез
def are_compatible(i, j):
    return THCompatibilityMatrix[i][j] == 1

# Функция для решения задачи о рюкзаке
def solve_knapsack():
    n = len(weight)
    sum_weights = int(sum(weight)) + 1
    dp = [[0] * sum_weights for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(sum_weights):
            if int(weight[i - 1]) > w:
                dp[i][w] = dp[i - 1][w]
            else:
                compatible = True
                for j in range(i):
                    if dp[j][w] == 1 and not are_compatible(i - 1, j - 1):
                        compatible = False
                        break
                if compatible:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - int(weight[i - 1])] + weight[i - 1])
                else:
                    dp[i][w] = dp[i - 1][w]

    max_weight = dp[n][sum_weights - 1]
    selected = [0] * n
    w = sum_weights - 1
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected[i - 1] = 1
            w -= int(weight[i - 1])

    return max_weight, selected

# Решаем задачу линейного программирования
max_weight, selected = solve_knapsack()


def save_data_to_file(file_path, data, max_weight, selected):
    with open(file_path, 'w') as file:
        # Записываем заголовок
        header = ','.join([f"TH{i}" for i in range(1, len(data[0]) + 1)])
        file.write(f",{header},sum(w)\n")

        # Записываем строки с данными
        for i, x_value in enumerate(selected, start=1):
            file.write(f"GH{i},")
            for val in data[i-1]:
                file.write(f"{val},")
            file.write(f"{x_value},{max_weight:.3f}\n")

# Пример использования
file_path_out = 'out.csv'
save_data_to_file(file_path_out, THCompatibilityMatrix, max_weight, selected)