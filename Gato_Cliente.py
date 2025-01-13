import socket
import json
import sys

# Verificar si el entorno es interactivo
if not sys.stdin.isatty() or not sys.stdout.isatty():
    print("Este script requiere una terminal interactiva para funcionar.")
    sys.exit(1)

HOST = 'Gato_Servidor'
PORT = 65432

def print_board(board):
    """Muestra el tablero en consola."""
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("--+---+--")

# Iniciar comunicación con el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))
        print("Conectado al servidor.")
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Asegúrate de que el servidor esté ejecutándose.")
        sys.exit(1)
    
    while True:
        try:
            print("\nTurno de jugar.")
            position = int(input("Ingresa una posición (0-8): "))
            player = input("¿Eres 'X' o 'O'? ").strip().upper()

            # Validar entrada
            if position < 0 or position > 8:
                print("La posición debe estar entre 0 y 8.")
                continue
            if player not in ["X", "O"]:
                print("El jugador debe ser 'X' o 'O'.")
                continue

            message = {
                "type": "MOVE",
                "position": position,
                "player": player
            }
            client_socket.send(json.dumps(message).encode())

            response = json.loads(client_socket.recv(1024).decode())
            print_board(response["board"])

            if response["status"] == "WIN":
                print(f"¡El jugador {response['winner']} ha ganado!")
                break
            elif response["status"] == "DRAW":
                print("¡Es un empate!")
                break
            elif response["status"] == "INVALID":
                print("Movimiento inválido. Inténtalo de nuevo.")
            elif response["status"] == "GAME_OVER":
                print("El juego ya terminó. Por favor, reinicia el cliente.")
                break
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número para la posición.")
        except KeyboardInterrupt:
            print("\nJuego terminado por el jugador.")
            break
        except ConnectionResetError:
            print("El servidor cerró la conexión. Terminando el juego.")
            break
