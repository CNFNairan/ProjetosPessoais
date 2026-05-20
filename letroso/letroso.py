from random import choice as c
import unicodedata
import os


def normalizar(texto):
    texto = texto.strip().upper()
    texto = unicodedata.normalize("NFD", texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

def palpite():
    while True:
        entrada = input("Digite uma palavra: ").strip()
        if not entrada:
            print("\033[1;31mVocê não digitou nada. Por favor, digite uma palavra.\033[m")
            print('.'*60)
            continue

        palavra_logica = normalizar(entrada)

        if not palavra_logica.replace(" ", "").isalpha():
            print("\033[1;31mEntrada inválida. Digite somente palavras.\033[m")
            print('.'*60)
            continue
        if len(palavra_logica) > 11:
            print("\033[1;31mEntrada inválida. Digite palavras de no máximo 11 caracteres.\033[m")
            print('.'*60)
            continue
        if palavra_logica in tentativas:
            print("\033[0;33mVocê já tentou essa palavra. Tente outra.\033[m")
            print('.'*60)
            continue
        break
    return entrada.upper(), palavra_logica

pasta_do_jogo = os.path.dirname(os.path.abspath(__file__))
caminho_txt = os.path.join(pasta_do_jogo, "palavras.txt")

try:
    with open(caminho_txt, "r", encoding="utf-8") as arquivo:
        palavras_forca = [linha.strip().upper() for linha in arquivo if linha.strip()]
except FileNotFoundError:
    print("\033[1;31mERRO: O arquivo 'palavras.txt' não foi encontrado na mesma pasta do jogo!\033[m")
    exit()

tentativas = []
contador = 0

secreta_display = c(palavras_forca).upper()
secreta_logica = normalizar(secreta_display)


print("-=-"*20)
print(f"{'BEM VINDO AO LETROSO!':^60}")
print("-=-"*20)
print(f"{'Digite uma palavra e tente acertar a palavra secreta.\n':^60}")
print('\033[42m  \033[m = letra correta na posição correta')
print('\033[43m  \033[m = letra correta na posição incorreta\n')
print("-=-"*20)

while True:
    chute_display, chute_logica = palpite()
    print('.'*60)
    tentativas.append(chute_logica)

    index_chute = []
    index_secreta = []
    verde = []
    amarelo = []

    if chute_logica == secreta_logica:
        vitoria = [f"\033[7;32m {letra} \033[m" for letra in chute_display]
        vitoria[0] = f"\033[7;32m( {chute_display[0]} \033[m"
        vitoria[-1] = f"\033[7;32m {chute_display[-1]} )\033[m"
        print("".join(vitoria))
        break

    for i, letra in enumerate(chute_logica):
        if letra in secreta_logica:
            contador = chute_logica[:i+1].count(letra)
            if contador <= secreta_logica.count(letra): 
                index_chute.append(i)                       
    for i, letra in enumerate(secreta_logica):
        if letra in chute_logica:
            contador = secreta_logica[:i+1].count(letra)
            if contador <= chute_logica.count(letra): 
                index_secreta.append(i)

    letras_chute = [chute_logica[i] for i in index_chute]
    letras_secreta = [secreta_logica[i] for i in index_secreta]

    verde_indices = {}
    for i, j in enumerate(letras_chute):
        if j == letras_secreta[i]:
            verde.append(letras_chute[i])
            verde_indices[index_chute[i]] = index_secreta[i]
        else:
            amarelo.append(letras_chute[i])

    lista_escrita = [a for a in chute_display]

    for l, letra_display in enumerate(lista_escrita):
        letra_logica = chute_logica[l]
        if letra_logica in verde:
            lista_escrita[l] = f"\033[7;32m {letra_display} \033[m"
            verde.pop(0)
        elif letra_logica in amarelo:
            lista_escrita[l] = f"\033[7;33m {letra_display} \033[m"
            amarelo.pop(0)
        else:
            lista_escrita[l] = f" {letra_display} "
    
    if secreta_logica[0].strip() == chute_logica[0]:
        lista_escrita[0] = f"\033[7;32m( {chute_display[0]} \033[m"
    if secreta_logica[-1].strip() == chute_logica[-1]:
        lista_escrita[-1] = f"\033[7;32m {chute_display[-1]} )\033[m"

    print_final = lista_escrita[0]
    for i in range(len(chute_logica) - 1):
        if i in verde_indices and (i + 1) in verde_indices:
            sao_vizinhas_na_secreta = verde_indices[i+1] == verde_indices[i] + 1
        else:
            sao_vizinhas_na_secreta = False
        if sao_vizinhas_na_secreta:
            print_final += lista_escrita[i+1]
        else:
            print_final += " " + lista_escrita[i+1]
    print(print_final)
    print('.'*60)

print("-=-"*20)
print(f"{f"Você acertou a palavra em {len(tentativas)} tentativas! Parabéns!":^60}")
print("-=-"*20)
