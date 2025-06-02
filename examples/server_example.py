from gym_service import SocketGymServer

if __name__ == "__main__":
    server = SocketGymServer(host="localhost", port=2333)
    print("[Example Server] Starting server...")
    server.start()
