# sudoku.py

import random

class SudokuBoard:
    def __init__(self, size):
        self.size = size  # Tamanho do tabuleiro (n)
        self.board = [[0]*size for _ in range(size)]  # Inicializa o tabuleiro vazio
        self.solution = [[0]*size for _ in range(size)]  # Inicializa o tabuleiro de solução vazio

    def generate_board(self):
        # Gera um tabuleiro Sudoku válido
        self._fill_board()
        self._remove_numbers()

    def _fill_board(self):
        # Preenche o tabuleiro com uma solução válida
        self._fill_diagonal_subgrids()
        self._solve_sudoku()

    def _fill_diagonal_subgrids(self):
        # Preenche os subgrids diagonais com números válidos
        subgrid_size = int(self.size ** 0.5)
        for i in range(0, self.size, subgrid_size):
            self._fill_subgrid(i, i)

    def _fill_subgrid(self, start_row, start_col):
        # Preenche um subgrid de tamanho sqrt(n) x sqrt(n) com números válidos
        subgrid_size = int(self.size ** 0.5)
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)
        idx = 0
        for i in range(subgrid_size):
            for j in range(subgrid_size):
                self.board[start_row + i][start_col + j] = nums[idx]
                idx += 1

    def _solve_sudoku(self):
        # Implementação para resolver o Sudoku
        if not self._solve():
            raise ValueError("Sudoku não tem solução válida.")

    def _solve(self):
        # Implementação principal para resolver o Sudoku utilizando backtracking
        empty_cell = self._find_empty()
        if not empty_cell:
            # Se não há mais células vazias, copia o tabuleiro atual para a solução
            self.solution = [row[:] for row in self.board]
            return True
        
        row, col = empty_cell
        for num in range(1, self.size + 1):
            if self._is_valid(num, row, col):
                self.board[row][col] = num
                if self._solve():
                    return True
                self.board[row][col] = 0  # Backtracking
        return False

    def _find_empty(self):
        # Encontra a próxima célula vazia no tabuleiro
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

    def _is_valid(self, num, row, col):
        # Verifica se é válido inserir 'num' na posição (row, col)
        # Verifica linha
        if num in self.board[row]:
            return False
        # Verifica coluna
        for r in range(self.size):
            if self.board[r][col] == num:
                return False
        # Verifica subgrid
        subgrid_size = int(self.size ** 0.5)
        start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
        for r in range(start_row, start_row + subgrid_size):
            for c in range(start_col, start_col + subgrid_size):
                if self.board[r][c] == num:
                    return False
        return True

    def _remove_numbers(self):
        # Remove aleatoriamente números para criar o jogo inicial
        cells_to_remove = random.sample(range(self.size * self.size), k=self.size * self.size // 2)
        for idx in cells_to_remove:
            row = idx // self.size
            col = idx % self.size
            self.board[row][col] = 0  # Marca a célula como vazia

    def get_sudoku_to_play(self):
        return self.board

    def get_solution(self):
        return self.solution
