import numpy as np

#Предобучение модели
teachNetwork = False

class NeuralNetwork:
    def __init__(self, num_features):
        # Initialize weights and bias randomly
        self.weights = np.random.rand(num_features)
        self.bias = np.random.rand()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x):
        # Forward pass through the network
        weighted_sum = np.dot(x, self.weights) + self.bias
        return self.sigmoid(weighted_sum)

    def train(self, inputs, targets, learning_rate, num_epochs):
        # Training the neural network
        for epoch in range(num_epochs):
            # Forward pass
            output = self.forward(inputs)

            # Compute loss
            loss = np.mean((output - targets) ** 2)

            # Backpropagation
            gradient = 2 * (output - targets) * output * (1 - output)
            self.weights -= learning_rate * np.dot(inputs.T, gradient)
            self.bias -= learning_rate * np.sum(gradient)

            # Print loss every 100 epochs
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

    def save_model(self, filename):
        # Save weights and bias to a file
        np.savez(filename, weights=self.weights, bias=self.bias)
        print("Model saved successfully.")

    def load_model(self, filename):
        # Load weights and bias from a file
        data = np.load(filename)
        self.weights = data['weights']
        self.bias = data['bias']
        print("Model loaded successfully.")

def load_data(matrix_file, weights_file):
    # Load TH matrix and weights from files
    TH_matrix = np.loadtxt(matrix_file, delimiter=' ')
    weights = np.loadtxt(weights_file)
    return TH_matrix, weights

def calculate_total_weight(weights, combination):
    total_weight = sum(weights[i] for i, selected in enumerate(combination) if selected)
    return total_weight

# Load data

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
TH_matrix, weights = load_data_from_file(file_path)
print(TH_matrix)

if teachNetwork:
    # Иницилизация
    model = NeuralNetwork(num_features=TH_matrix.shape[1])

    # Обучение
    learning_rate = 0.00001
    num_epochs = 1000
    model.train(TH_matrix, weights, learning_rate, num_epochs)

    # Созранение модели
    model.save_model("trained_model.npz")

# Загрузка
loaded_model = NeuralNetwork(num_features=TH_matrix.shape[1])
loaded_model.load_model("trained_model.npz")

# Тестирование
predictions = loaded_model.forward(TH_matrix)

# Поиск лучших результатов
best_indices = np.argsort(predictions)[-4:]
best_combinations = TH_matrix[best_indices]
best_weights = [calculate_total_weight(weights, combination) for combination in best_combinations]

def save_data_to_file(file_path, data, max_weight, selected):
    with open(file_path, 'w') as file:
        # Write header
        header = ','.join([f"TH{i}" for i in range(1, len(data[0]) + 1)])
        file.write(f",{header},sum(w)\n")

        # Write data rows
        for i, x_value in enumerate(selected, start=1):
            file.write(f"GH{i},")
            for val in data[i-1]:
                file.write(f"{val},")
            file.write(f"{x_value:.3f}\n")

# Пример использования
file_path_out = 'out.csv'
save_data_to_file(file_path_out, best_combinations, best_weights, predictions)