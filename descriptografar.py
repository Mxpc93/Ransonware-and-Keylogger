from cryptography.fernet import Fernet
import os

def carregar_chave():
    return open("chave.key", "rb").read()

def descriptografar_arquivos(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados = file.read()
        dados_descriptografados = f.decrypt(dados)
    with open(arquivo, "wb") as file:
        file.write(dados_descriptografados)

def encontrar_arquivos(diretorio):
    listas = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            if nome != os.path.basename(__file__) and not nome.endswith(".key"):
                caminho_completo = os.path.join(raiz, nome)
                listas.append(caminho_completo)
    return listas

def main():
    chave = carregar_chave()
    arquivos = encontrar_arquivos("test_files")
    for arquivo in arquivos:
        descriptografar_arquivos(arquivo, chave)
    print("Descriptografia concluída! Arquivos restaurados.")

if __name__ == "__main__":
    main()