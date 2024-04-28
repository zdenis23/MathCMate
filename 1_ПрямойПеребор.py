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


def is_compatible(solution):
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            if solution[i] == 1 and solution[j] == 1 and THCompatibilityMatrix[i][j] == 0:
                return False
    return True

def generate_solutions(weight):
    solutions = []
    n = len(weight)
    for i in range(2 ** n):
        solution = [int(x) for x in bin(i)[2:].zfill(n)]
        if is_compatible(solution):
            sum_weights = sum(weight[j] * solution[j] for j in range(n))
            solutions.append((solution, sum_weights))
    return solutions

solutions = generate_solutions(weight)
solutions.sort(key=lambda x: x[1], reverse=True)

print("#hypotheses\n")
print(f"Final Global hypotheses (GH) total number: {len(solutions)}\n")
print("TH1 TH2 TH3 TH4 TH5 TH6 TH7 TH8 TH9 TH10 TH11 TH12 sum(w)")
print("___ ___ ___ ___ ___ ___ ___ ___ ___ ____ ____ ____ ________\n")

for i, (solution, sum_weights) in enumerate(solutions[:8], start=1):
    print(f"GH{i} {' '.join(str(sol) for sol in solution)} {sum_weights:.3f}")