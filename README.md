# 🛡️ Échange de Clés Post-Quantiques avec CRYSTALS-Kyber (Kyber-768)

Ce projet implémente un **protocole d’échange de clés sécurisé post-quantique** basé sur le schéma KEM **CRYSTALS-Kyber (Kyber-768)**, utilisant la bibliothèque **Open Quantum Safe (liboqs)**.
Il montre comment un **client** et un **serveur** peuvent établir un secret partagé sécurisé même en présence d’un attaquant interceptant les communications.

---

## 📌 Objectifs du projet

- Implémenter un échange de clés **post-quantique** avec Kyber-768
- Créer une communication **client-serveur** en Python
- Générer et échanger un **ciphertext**
- Démontrer que les deux parties obtiennent le **même secret partagé**
- Fournir des **évidences** de fonctionnement (logs, captures d'écran)

---

## 🧩 Architecture du système

### Serveur

- Génère une paire de clés Kyber-768
- Envoie sa **clé publique** au client
- Reçoit le **ciphertext**
- Déchiffre pour récupérer le **secret partagé**

### Client

- Reçoit la clé publique du serveur
- Encapsule un secret → produit un **ciphertext**
- Envoie ce ciphertext au serveur
- Obtient localement son **secret partagé**

### Résultat attendu

Les deux valeurs doivent être **identiques** :
shared_secret_client == shared_secret_server

Le ciphertext doit mesurer environ **1088 bytes** (taille typique pour Kyber-768).

---

## 🚀 Exécution du projet

### 1️⃣ Installer les dépendances

Installe la version Python de liboqs :

```bash
pip install git+https://github.com/open-quantum-safe/liboqs-python.git

### 2️⃣ Lancer le serveur

Dans un premier terminal :
'''
python3 server.py
'''

### 3️⃣ Lancer le client

Dans un second terminal :
'''
python3 client.py
'''
```

## Authors

- Nicolas Magne
- Jessica Devulder
- Tania ..
