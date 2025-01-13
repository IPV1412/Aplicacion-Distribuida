def print_board(board):
    """Muestra el tablero en consola."""
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("--+---+--")


def check_winner(board):
    """Comprueba si hay un ganador."""
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return None


def is_draw(board):
    """Comprueba si el tablero está lleno."""
    return " " not in board


def handle_move(board, position, player):
    """Procesa el movimiento del jugador."""
    if board[position] == " ":
        board[position] = player
        winner = check_winner(board)
        if winner:
            return {"status": "WIN", "winner": winner, "board": board}
        elif is_draw(board):
            return {"status": "DRAW", "board": board}
        else:
            return {"status": "CONTINUE", "board": board}
    return {"status": "INVALID", "board": board}


# Lógica principal del juego
def main():
    board = [" " for _ in range(9)]
    turn = "X"
    game_over = False

    print("¡A Jugar Gato!")
    print_board(board)

    while not game_over:
        print(f"\nTurno del jugador {turn}.")
        try:
            position = int(input("Ingresa una posición (0-8): "))
            if position < 0 or position > 8:
                print("Posición inválida. Intenta nuevamente.")
                continue
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entre 0 y 8.")
            continue

        result = handle_move(board, position, turn)
        print_board(result["board"])

        if result["status"] == "WIN":
            print(f"¡El jugador {result['winner']} ha ganado!")
            game_over = True
        elif result["status"] == "DRAW":
            print("¡Es un empate!")
            game_over = True
        elif result["status"] == "INVALID":
            print("Movimiento inválido. Intenta de nuevo.")
        else:
            turn = "O" if turn == "X" else "X"


if __name__ == "__main__":
    main()
