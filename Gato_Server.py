import socket
import json

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 65432

# Tablero inicial y estado del juego
board = [" " for _ in range(9)]
turn = "X"
game_over = False
players = {}  # Almacena las conexiones de los jugadores {"X": conn1, "O": conn2}

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
    global board, turn, game_over, players
    board = [" " for _ in range(9)]
    turn = "X"
    game_over = False
    players = {}

def handle_move(position, player):
    """Procesa el movimiento del jugador."""
    global turn, game_over
    if game_over:
        return {"status": "GAME_OVER", "board": board}
    if player != turn:
        return {"status": "NOT_YOUR_TURN", "board": board}
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
    server_socket.listen(2)  # Permite hasta 2 jugadores
    print(f"Servidor iniciado en {HOST}:{PORT}")

    try:
        while True:
            # Aceptar nuevas conexiones
            if len(players) < 2:
                conn, addr = server_socket.accept()
                player_type = "X" if "X" not in players else "O"
                players[player_type] = conn
                print(f"Jugador {player_type} conectado desde {addr}")
                conn.send(json.dumps({"player_type": player_type, "message": f"Eres el jugador {player_type}"}).encode())
            else:
                conn, addr = server_socket.accept()
                conn.send(json.dumps({"message": "El juego ya tiene dos jugadores conectados"}).encode())
                conn.close()
                continue

            # Manejo de comunicación con jugadores
            for player, conn in list(players.items()):
                try:
                    data = conn.recv(1024).decode()
                    if not data:
                        print(f"Jugador {player} desconectado.")
                        players.pop(player)
                        reset_game()
                        break

                    message = json.loads(data)
                    if message["type"] == "MOVE":
                        position = message["position"]
                        response = handle_move(position, player)
                        conn.send(json.dumps(response).encode())

                        # Notificar al otro jugador
                        other_player = "O" if player == "X" else "X"
                        if other_player in players:
                            players[other_player].send(json.dumps(response).encode())

                        # Reiniciar el juego si hay un resultado final
                        if response["status"] in ["WIN", "DRAW"]:
                            reset_game()
                            break
                except Exception as e:
                    print(f"Error con el jugador {player}: {e}")
                    players.pop(player, None)
                    reset_game()
                    break
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        # Cerrar todas las conexiones al finalizar
        for conn in players.values():
            conn.close()