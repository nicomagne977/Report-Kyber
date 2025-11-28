# 🛡️ Post-Quantum Key Exchange with CRYSTALS-Kyber (Kyber-768)

This project implements a **secure post-quantum key exchange protocol** based on the **CRYSTALS-Kyber (Kyber-768)** KEM scheme, using the **Open Quantum Safe (liboqs)** library.
It shows how a **client** and a **server** can establish a secure shared secret even in the presence of an attacker intercepting communications.

---

## 📌 Project objectives

- Implement a **post-quantum** key exchange with Kyber-768
- Create **client-server** communication in Python
- Generate and exchange a **ciphertext**
- Demonstrate that both parties obtain the **same shared secret**
- Provide **evidence** of operation (logs, screenshots)

---

## 🧩 System architecture

### Server

- Generates a Kyber-768 key pair
- Sends its **public key** to the client
- Receives the **ciphertext**
- Decrypts to retrieve the **shared secret**

### Client

- Receives the server's public key
- Encapsulates a secret → produces a **ciphertext**
- Sends this ciphertext to the server
- Obtains its **shared secret** locally

### Expected result

The two values must be **identical**:
shared_secret_client == shared_secret_server

The ciphertext should be approximately **1088 bytes** (typical size for Kyber-768).

---

## 🚀 Project execution

### 1️⃣ Install dependencies

Install the Python version of liboqs:

```bash
pip install git+https://github.com/open-quantum-safe/liboqs-python.git
```

### 2️⃣ Launch the server

In a first terminal:
```
python3 server.py
```

### 3️⃣ Launch the client

In a second terminal:
```
python3 client.py
```


## Authors

- Nicolas Magne
- Jessica Devulder
- Tainá Da Cruz
