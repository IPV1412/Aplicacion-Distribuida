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

# Iniciar comunicación con el servidor
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
            print("\nEsperando tu turno...")
            response = json.loads(client_socket.recv(1024).decode())
            
            if response["status"] == "NOT_YOUR_TURN":
                continue
            elif response["status"] == "GAME_OVER":
                print("El juego ya terminó.")
                break
            elif response["status"] == "WIN":
                print(f"¡El jugador {response['winner']} ha ganado!")
                break
            elif response["status"] == "DRAW":
                print("¡Es un empate!")
                break
            
            print_board(response["board"])

            position = int(input("Ingresa una posición (0-8): "))
            message = {"type": "MOVE", "position": position, "player": player_type}
            client_socket.send(json.dumps(message).encode())
    except KeyboardInterrupt:
        print("\nDesconexión del cliente.")
    except Exception as e:
        print(f"Error en el cliente: {e}")