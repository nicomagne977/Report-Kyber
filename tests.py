import oqs
import time
import random


# -----------------------------------------------------------
#  UTILITAIRES — Version finale corrigée
# -----------------------------------------------------------


def create_server_kem(alg="Kyber768"):
    """
    Crée l’objet KEM du serveur et génère les clés.
    Retourne : (kem_server, public_key)
    """
    kem = oqs.KeyEncapsulation(alg)
    pk = kem.generate_keypair()
    return kem, pk


def client_encapsulate(pk, alg="Kyber768"):
    """
    Le client encapsule avec la clé publique du serveur.
    Retourne : (ciphertext, shared_secret_client)
    """
    kem = oqs.KeyEncapsulation(alg)
    ct, ss = kem.encap_secret(pk)
    return ct, ss


def server_decapsulate(kem_server, ct):
    """
    Le serveur décapsule avec son objet KEM (qui contient déjà la clé secrète).
    Retourne : shared_secret_server
    """
    return kem_server.decap_secret(ct)


# -----------------------------------------------------------
#  TESTS
# -----------------------------------------------------------


def test_1_key_generation():
    print("\n[TEST 1] Génération de clés pour le serveur")
    kem_server, pk = create_server_kem()
    print(" - OK : clés générées")
    print("   Taille PK :", len(pk), "octets")
    return kem_server, pk


def test_2_encapsulation(pk):
    print("\n[TEST 2] Encapsulation côté client")
    ct, ss_client = client_encapsulate(pk)
    print(" - OK : encapsulation validée")
    print("   Taille CT :", len(ct), "octets")
    print("   Secret partagé (client) :", ss_client.hex()[:32], "...")
    return ct, ss_client


def test_3_decapsulation(kem_server, ct):
    print("\n[TEST 3] Décapsulation côté serveur")
    ss_server = server_decapsulate(kem_server, ct)
    print(" - OK : décapsulation validée")
    print("   Secret partagé (serveur) :", ss_server.hex()[:32], "...")
    return ss_server


def test_4_match_shared_secrets(ss_client, ss_server):
    print("\n[TEST 4] Vérification du secret partagé")
    if ss_client == ss_server:
        print(" - SUCCÈS : les deux secrets sont IDENTIQUES")
    else:
        print(" - ÉCHEC : les secrets sont différents")


def test_5_tampered_ciphertext(kem_server, ct):
    print("\n[TEST 5] Test de résistance à une altération du ciphertext")
    ct_mod = bytearray(ct)
    ct_mod[0] ^= 0xFF  # on modifie un octet
    try:
        ss = server_decapsulate(kem_server, bytes(ct_mod))
        print(" - ATTENTION : le serveur a accepté un CT modifié !")
    except Exception as e:
        print(" - OK : le serveur REJETTE un ciphertext modifié")
        print("   Exception :", str(e))


def test_6_multiple_sessions():
    print("\n[TEST 6] Test sur 10 échanges consécutifs")
    kem_server, pk = create_server_kem()
    ok = 0
    for i in range(10):
        ct, ss_client = client_encapsulate(pk)
        ss_server = server_decapsulate(kem_server, ct)
        if ss_client == ss_server:
            ok += 1
    print(f" - {ok}/10 échanges réussis (secrets identiques)")


def test_7_performance():
    print("\n[TEST 7] Mesure simple de performance (100 encapsulations)")
    import time

    kem_server, pk = create_server_kem()

    t0 = time.time()
    for _ in range(100):
        ct, ss_client = client_encapsulate(pk)
        ss_server = server_decapsulate(kem_server, ct)
    t1 = time.time()

    print(" - Temps total :", round(t1 - t0, 4), "s")
    print(" - Temps moyen par échange :", round((t1 - t0) / 100, 6), "s")


# -----------------------------------------------------------
#  MAIN
# -----------------------------------------------------------

if __name__ == "__main__":
    print("\n=========== TESTS ALGORITHME PQC (Kyber768) ===========")

    kem_server, pk = test_1_key_generation()
    ct, ss_client = test_2_encapsulation(pk)
    ss_server = test_3_decapsulation(kem_server, ct)
    test_4_match_shared_secrets(ss_client, ss_server)
    test_5_tampered_ciphertext(kem_server, ct)
    test_6_multiple_sessions()
    test_7_performance()

    print("\n=========== FIN DES TESTS ===========\n")
