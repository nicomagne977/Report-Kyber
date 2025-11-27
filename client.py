#!/usr/bin/env python3
"""
client.py
Cliente TCP simples que:
- conecta ao servidor
- recebe a chave pública (pk)
- faz encapsulate(pk) para obter (ciphertext, ss_cliente)
- envia ciphertext ao servidor
- imprime/mostra evidências localmente

Uso:
    python3 client.py --host 127.0.0.1 --port 5000
"""
import socket
import struct
import base64
import argparse
import sys
from oqs import KeyEncapsulation

def send_bytes(conn: socket.socket, b: bytes) -> None:
    conn.sendall(struct.pack("!I", len(b)) + b)

def recv_bytes(conn: socket.socket) -> bytes:
    header = conn.recv(4)
    if len(header) < 4:
        raise ConnectionError("Conexão fechada ou cabeçalho incompleto")
    length = struct.unpack("!I", header)[0]
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Conexão fechada durante recebimento de dados")
        data += chunk
    return data

def main(host: str, port: int, algorithm: str):
    print(f"[CLIENT] Conectando a {host}:{port} usando KEM = {algorithm}")

    try:
        kem = KeyEncapsulation(algorithm)
    except Exception as e:
        print(f"[ERRO] não foi possível inicializar KeyEncapsulation: {e}")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("[CLIENT] Conectado ao servidor.")

        # recebe pk do servidor
        try:
            pk = recv_bytes(s)
        except ConnectionError as e:
            print(f"[ERRO] ao receber chave pública: {e}")
            return

        print(f"[CLIENT] Recebida chave pública ({len(pk)} bytes).")

        # encapsulate -> (ciphertext, shared_secret)
        try:
            ciphertext, ss_cliente = kem.encapsulate(pk)
        except Exception as e:
            print(f"[ERRO] encapsulate falhou: {e}")
            return

        print(f"[CLIENT] Encapsulate concluído. ciphertext tamanho = {len(ciphertext)} bytes.")

        # envia ciphertext ao servidor
        send_bytes(s, ciphertext)
        print("[CLIENT] ciphertext enviado ao servidor.")

        # mostra evidências locais
        print("=== EVIDÊNCIAS (CLIENT) ===")
        print(f"shared_secret (hex): {ss_cliente.hex()}")
        print(f"shared_secret (base64): {base64.b64encode(ss_cliente).decode()}")
        print("===========================")

    try:
        kem.close()
    except Exception:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente KEM (Kyber) - exemplo")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Endereço do servidor")
    parser.add_argument("--port", type=int, default=5000, help="Porta do servidor")
    parser.add_argument("--alg", type=str, default="Kyber768",
                        help="Nome do algoritmo KEM (ex: Kyber512, Kyber768, Kyber1024)")
    args = parser.parse_args()
    main(args.host, args.port, args.alg)
