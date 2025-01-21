import socket
import json
import sys

HOST = 'Gato_Servidor'
PORT = 65432

def print_board(board):
    """Muestra el tablero en consola."""
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("--+---+--")

# Inicia la comunicación con el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))
        print("Conectado al servidor.")
        
        # Recibir el tipo de jugador asignado por el servidor
        data = json.loads(client_socket.recv(1024).decode())
        player_type = data.get("player_type", None)
        if not player_type:
            print(data["message"])
            sys.exit(1)
        
        print(f"Has sido asignado como jugador '{player_type}'.")

        while True:
            print_board(data.get("board", [" " for _ in range(9)]))
            position = int(input(f"Jugador {player_type}, ingresa una posición (0-8): "))
            message = {"type": "MOVE", "position": position, "player": player_type}
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
            elif response["status"] == "NOT_YOUR_TURN":
                print("No es tu turno. Espera al otro jugador.")
    except KeyboardInterrupt:
        print("\nDesconexión del cliente.")
    except Exception as e:
        print(f"Error en el cliente: {e}")
