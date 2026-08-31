import argparse
import socket
import time


def enviar_beacon(destino, puerto):
    payload = b"GET /check HTTP/1.1\r\nHost: c2\r\n\r\n"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((destino, puerto))
        s.send(payload)
        s.recv(1024)
        s.close()
        return True
    except Exception as error:
        print(f"  fallo el beacon: {error}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", required=True)
    parser.add_argument("--puerto", type=int, required=True)
    parser.add_argument("--intervalo", type=float, default=15)
    parser.add_argument("--repeticiones", type=int, default=20)
    args = parser.parse_args()

    print(f"Simulando beacon C2 hacia {args.destino}:{args.puerto}")
    print(f"Intervalo: {args.intervalo}s | Repeticiones: {args.repeticiones}")

    for i in range(1, args.repeticiones + 1):
        exito = enviar_beacon(args.destino, args.puerto)
        print(f"[{i}/{args.repeticiones}] beacon enviado, exito={exito}")
        if i < args.repeticiones:
            time.sleep(args.intervalo)

    print("Simulacion finalizada.")


if __name__ == "__main__":
    main()
