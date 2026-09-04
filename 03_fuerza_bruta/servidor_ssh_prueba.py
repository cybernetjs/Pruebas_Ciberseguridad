import argparse
import socket
import threading

import paramiko

CLAVE_SERVIDOR = paramiko.RSAKey.generate(2048)
USUARIO_VALIDO = "sistemas"
CONTRASENA_VALIDA = "ciberseguridad"


class ServidorPrueba(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        if username == USUARIO_VALIDO and password == CONTRASENA_VALIDA:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED


def atender_conexion(conexion_cliente):
    try:
        transporte = paramiko.Transport(conexion_cliente)
        transporte.add_server_key(CLAVE_SERVIDOR)
        servidor = ServidorPrueba()
        transporte.start_server(server=servidor)
        canal = transporte.accept(2)
        if canal is not None:
            canal.close()
    except Exception:
        pass
    finally:
        try:
            conexion_cliente.close()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--puerto", type=int, default=22)
    args = parser.parse_args()

    zocalo_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    zocalo_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    zocalo_servidor.bind(("0.0.0.0", args.puerto))
    zocalo_servidor.listen(50)
    print(f"Servidor SSH de prueba escuchando en el puerto {args.puerto}")
    print(f"Credencial valida configurada: {USUARIO_VALIDO}:{CONTRASENA_VALIDA}")

    while True:
        conexion_cliente, direccion_origen = zocalo_servidor.accept()
        print(f"Conexion entrante desde {direccion_origen[0]}:{direccion_origen[1]}")
        hilo = threading.Thread(target=atender_conexion, args=(conexion_cliente,), daemon=True)
        hilo.start()


if __name__ == "__main__":
    main()