from gym_service import SocketGymServer
import argparse


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--host", type=str, default="localhost")
    argparser.add_argument("--port", type=int, default=2333)
    args = argparser.parse_args()
    server = SocketGymServer(host=args.host, port=args.port)
    print("[Example Server] Starting server...")
    server.start()
