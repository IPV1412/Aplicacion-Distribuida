import socket
import json
import threading

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 65432

# Tablero inicial y estado del juego
board = [" " for _ in range(9)]
players = {}  # {'X': conn1, 'O': conn2}
current_turn = "X"
lock = threading.Lock()

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

def handle_client(player, conn):
    """Maneja la comunicación con un cliente."""
    global board, current_turn
    conn.send(json.dumps({"player_type": player, "board": board}).encode())

    # Enviar mensaje de confirmación al cliente
    conn.send(json.dumps({"status": "CONNECTED", "message": f"Conexión exitosa. Eres el jugador '{player}'."}).encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                print(f"Jugador {player} desconectado.")
                break

            message = json.loads(data)
            if message["type"] == "MOVE":
                with lock:
                    if message["player"] != current_turn:
                        conn.send(json.dumps({"status": "NOT_YOUR_TURN"}).encode())
                        continue

                    position = message["position"]
                    if 0 <= position < 9 and board[position] == " ":
                        board[position] = current_turn
                        winner = check_winner()
                        if winner:
                            broadcast({"status": "WIN", "winner": winner, "board": board})
                            break
                        elif is_draw():
                            broadcast({"status": "DRAW", "board": board})
                            break
                        else:
                            current_turn = "O" if current_turn == "X" else "X"
                            broadcast({"status": "CONTINUE", "board": board, "turn": current_turn})
                    else:
                        conn.send(json.dumps({"status": "INVALID"}).encode())
        except Exception as e:
            print(f"Error con el jugador {player}: {e}")
            break

    conn.close()
    with lock:
        del players[player]

def broadcast(message):
    """Envía mensajes a los jugadores."""
    for player, conn in players.items():
        conn.send(json.dumps(message).encode())

# Configuración del socket del servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print(f"Servidor iniciado en {HOST}:{PORT}")

    while len(players) < 2:
        conn, addr = server_socket.accept()
        player = "X" if "X" not in players else "O"
        players[player] = conn
        print(f"Jugador {player} conectado desde {addr}.")
        threading.Thread(target=handle_client, args=(player, conn)).start()
