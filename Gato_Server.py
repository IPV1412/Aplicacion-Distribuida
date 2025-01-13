import socket
import json

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 65432

# Tablero inicial y estado del juego
board = [" " for _ in range(9)]
turn = "X"
game_over = False

def check_winner():
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

def is_draw():
    """Comprueba si el tablero está lleno."""
    return " " not in board

def reset_game():
    """Reinicia el tablero y el estado del juego."""
    global board, turn, game_over
    board = [" " for _ in range(9)]
    turn = "X"
    game_over = False

def handle_move(position, player):
    """Procesa el movimiento del jugador."""
    global turn, game_over
    if game_over:
        return {"status": "GAME_OVER", "board": board}
    if board[position] == " ":
        board[position] = player
        winner = check_winner()
        if winner:
            game_over = True
            return {"status": "WIN", "winner": winner, "board": board}
        elif is_draw():
            game_over = True
            return {"status": "DRAW", "board": board}
        else:
            turn = "O" if player == "X" else "X"
            return {"status": "CONTINUE", "board": board, "turn": turn}
    return {"status": "INVALID", "board": board}

# Configuración del socket del servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor iniciado en {HOST}:{PORT}")
    
    while True:
        try:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Conexión recibida de {addr}")
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        print("El cliente cerró la conexión.")
                        break

                    message = json.loads(data)

                    if message["type"] == "MOVE":
                        position = message["position"]
                        player = message["player"]
                        response = handle_move(position, player)
                        conn.send(json.dumps(response).encode())

                        # Reinicia el juego después de un resultado final
                        if response["status"] in ["WIN", "DRAW"]:
                            reset_game()
        except Exception as e:
            print(f"Error en el servidor: {e}")

