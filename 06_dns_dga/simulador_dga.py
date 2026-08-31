import argparse
import random
import socket
import string
import time


def generar_dominio():
    longitud = random.randint(8, 16)
    nombre = "".join(random.choices(string.ascii_lowercase, k=longitud))
    tld = random.choice(["com", "net", "org", "info", "biz"])
    return f"{nombre}.{tld}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cantidad", type=int, default=50)
    parser.add_argument("--retardo", type=float, default=0.5)
    args = parser.parse_args()

    print(f"Generando y resolviendo {args.cantidad} dominios tipo DGA")

    for i in range(1, args.cantidad + 1):
        dominio = generar_dominio()
        try:
            socket.gethostbyname(dominio)
            resultado = "resuelto"
        except socket.gaierror:
            resultado = "no existe (esperado, la mayoria de dominios DGA no estan registrados)"
        print(f"[{i}/{args.cantidad}] {dominio} -> {resultado}")
        time.sleep(args.retardo)

    print("Simulacion finalizada.")


if __name__ == "__main__":
    main()
