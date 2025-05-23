import random
import time

class NRainhas:
    def __init__(self, n):
        self.n = n
        self.board = self.random_board()
        self.steps = []

    def random_board(self):
        # Coloca uma rainha em cada coluna, em linhas aleatórias
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def heuristic(self, board):
        # Conta o número de pares de rainhas que se atacam
        conflicts = 0
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(self, board):
        neighbors = []
        for col in range(self.n):
            for row in range(self.n):
                if board[col] != row:
                    neighbor = board.copy()
                    neighbor[col] = row
                    neighbors.append(neighbor)
        return neighbors

    def hill_climb(self):
        current = self.board
        current_h = self.heuristic(current)
        self.steps.append((current.copy(), current_h))

        while True:
            neighbors = self.get_neighbors(current)
            neighbor = min(neighbors, key=lambda b: self.heuristic(b))
            neighbor_h = self.heuristic(neighbor)

            if neighbor_h >= current_h:
                # Chegou em um platô ou ótimo local
                break
            current = neighbor
            current_h = neighbor_h
            self.steps.append((current.copy(), current_h))

        self.board = current
        return current

    def solve(self):
        solution = self.hill_climb()
        return solution, self.heuristic(solution), self.steps

def print_board(board):
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

if __name__ == "__main__":
    for n in [8, 10, 15, 20]:
        print(f"\nSolucionando para n = {n}")
        solver = NRainhas(n)
        start_time = time.time()
        solution, heuristic, steps = solver.solve()
        end_time = time.time()

        print(f"Estado inicial: {steps[0][0]} | Heurística: {steps[0][1]}")
        print(f"Estado final: {solution} | Heurística: {heuristic}")
        print(f"Tempo: {end_time - start_time:.4f} segundos")
        print(f"Passos realizados: {len(steps)-1}")

        if n <= 20:
            print("\nConfiguração final do tabuleiro:")
            print_board(solution)