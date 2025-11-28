#!/usr/bin/env python3
"""
server.py
Servidor TCP simples que:
- inicializa um KEM (CRYSTALS-Kyber)
- gera (public_key, secret_key)
- envia a public_key ao cliente
- recebe o ciphertext do cliente
- faz decapsulate para obter o segredo compartilhado (ss_servidor)
- imprime/mostra evidências

Uso:
    python3 server.py
"""
import socket
import struct
import base64
import argparse
import sys
from oqs import KeyEncapsulation  # liboqs-python

HOST = "0.0.0.0"
PORT = 5000


def send_bytes(conn: socket.socket, b: bytes) -> None:
    """Envia um bloco de bytes com prefixo de 4 bytes (big-endian) com o tamanho."""
    conn.sendall(struct.pack("!I", len(b)) + b)


def recv_bytes(conn: socket.socket) -> bytes:
    """Recebe primeiro 4 bytes de tamanho e depois lê exatamente esse número de bytes."""
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


def main(algorithm: str):
    print(f"[SERVER] Iniciando servidor na porta {PORT} usando KEM = {algorithm}")

    # inicializa KEM e gera par de chaves
    try:
        kem = KeyEncapsulation(algorithm)
    except Exception as e:
        print(f"[ERRO] não foi possível inicializar KeyEncapsulation: {e}")
        sys.exit(1)

    try:
        # public_key, secret_key = kem.generate_keypair()
        public_key = kem.generate_keypair()  # Clé publique
        secret_key = kem.export_secret_key()  # Clé secrète

    except Exception as e:
        print(f"[ERRO] falha ao gerar par de chaves: {e}")
        sys.exit(1)

    print(f"[SERVER] Chave pública gerada ({len(public_key)} bytes).")

    # socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[SERVER] Aguardando conexão de cliente em {HOST}:{PORT} ...")
        conn, addr = s.accept()
        with conn:
            print(f"[SERVER] Conexão aceita de {addr}")

            # envia a chave pública ao cliente
            send_bytes(conn, public_key)
            print("[SERVER] Chave pública enviada ao cliente (raw bytes).")

            # recebe o ciphertext enviado pelo cliente
            try:
                ciphertext = recv_bytes(conn)
            except ConnectionError as e:
                print(f"[ERRO] durante recebimento do ciphertext: {e}")
                return

            print(f"[SERVER] Recebido ciphertext ({len(ciphertext)} bytes).")

            # decapsulate usando a secret_key
            try:
                ss_servidor = kem.decap_secret(ciphertext)
            except Exception as e:
                print(f"[ERRO] decapsulate falhou: {e}")
                return

            print("[SERVER] Decapsulate concluído.")
            print("=== EVIDÊNCIAS (SERVER) ===")
            print(f"shared_secret (hex): {ss_servidor.hex()}")
            print(f"shared_secret (base64): {base64.b64encode(ss_servidor).decode()}")
            print("===========================")

    # opcional: liberar recursos do kem (se necessário)
    try:
        kem.close()
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor KEM (Kyber) - exemplo")
    parser.add_argument(
        "--alg",
        type=str,
        default="Kyber768",
        help="Nome do algoritmo KEM (ex: Kyber512, Kyber768, Kyber1024)",
    )
    args = parser.parse_args()
    main(args.alg)
