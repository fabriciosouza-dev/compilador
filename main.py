import os
import os.path
import re

token_value = []


def abre_arquivo(nme_arquivo):
    try:
        return open('arquivo_substituicao\\' + nme_arquivo, "r", encoding="utf8")
    except:
        print("Arquivo não existe!!")
        return False


def cria_arquivo(nme_arquivo):
    array = nme_arquivo.split(".")
    # ['arquivo','txt']
    index = 1
    while True:
        if index != 1:
            # array[0] = arquivo1, arquivo2, arquivo3, ..., arquivoN
            array[0] = array[0][:-1]
        array[0] += str(index)
        nme_arquivo = '.'.join(array)
        if not os.path.exists('arquivo_substituicao\\' + nme_arquivo):
            return open('arquivo_substituicao\\' + nme_arquivo, 'w+', encoding="utf8")
        index += 1


# def remove_comentario(texto):
#     # [10,15,30,35,40]
#     comentario = [m.start() for m in re.finditer('//', texto)][:2]
#     # [10,15]
#     while len(comentario) > 0 and len(comentario) % 2 == 0:
#         if texto[comentario[0]:comentario[1] + 3][-1] in ['\n', ' ']:
#             texto = texto.replace(texto[comentario[0]:comentario[1] + 3], "")
#         else:
#             texto = texto.replace(texto[comentario[0]:comentario[1] + 2], "")
#         comentario = [m.start() for m in re.finditer('//', texto)][:2]
#         # [20, 20]
#     return texto

def remove_comentario(texto):
    start = None
    end = None
    index = 0
    while index < len(texto):
        if not ((len(texto) - index) == 1):
            coment = texto[index] + texto[index + 1]
        if coment == '/*':
            start = index
        elif coment == '*/':
            end = index + 2
        if isinstance(start, int) and isinstance(end, int):
            if texto[start:end + 1][-1] in ['\n', ' ']:
                texto = texto.replace(texto[start:end + 1], "")
            else:
                texto = texto.replace(texto[start:end], "")
            index = start - 1
            start = None
            end = None
        index += 1
    return texto


def substituir_texto(arquivo):
    texto = ""
    for linha in arquivo.readlines():
        string = ""
        string += linha
        if string == '\n':
            string = string.replace("\n", "")
        elif "\n" in string:
            string = " ".join(add_colchets(split_texto(string))) + "\n"
        else:
            string = " ".join(add_colchets(split_texto(string)))
        if '//' in string:
            try:
                comentario = string.index('//')
            except:
                comentario = None
            end = len(string)
            if isinstance(comentario, int):
                string = string.replace(string[comentario:end], "")
        texto += string
    return texto


def split_texto(string):
    array = []
    posicao_texto = [m.start() for m in re.finditer("'", string)]
    if len(posicao_texto) > 1:
        texto = string[posicao_texto[0]:posicao_texto[1] + 1]
        string = string.replace(texto, '#$%¨&*()')
    for palavra in string.split():
        if palavra == "#$%¨&*()":
            array.append(texto)
        else:
            array.append(palavra)
    return array


def add_colchets(array):
    out_array = []
    for palavra in array:
        if '//' in palavra or '/*' in palavra or '*/' in palavra:
            out_array.append(palavra)
        else:
            if palavras_reservadas(palavra):
                out_array.append(palavra.replace(palavra, '[' + palavra + ',]'))
            else:
                out_array.append(palavra.replace(palavra, tokens(palavra)))
    return out_array


def palavras_reservadas(string):
    palavras = ["inicio", "fim", "var", "leia", "escreva",
                "'", "se", "senao", "(", ")", ":", ";"]

    for palavra in palavras:
        if string == palavra:
            return True
    return False


def tokens(string):
    id = len(token_value) + 1
    if len([m.start() for m in re.finditer("'", string)]) > 1:
        string = string.replace(string, '[FR,' + string.replace("'", "") + ']')
    elif len(re.findall("^[a-z]+$", string)) > 0:
        const = False
        for token in token_value:
            if token['const'] == string:
                id = token['id']
                const = True
        if not const:
            token_value.append({'const': string, 'id': id})
        string = string.replace(string, '[ID,' + str(id) + ']')
    elif len(re.findall("[0-9]+", string)) > 0:
        string = string.replace(string, '[NU,' + string + ']')
    elif len(re.findall("[+|*|/|-|%]", string)) > 0:
        string = string.replace(string, '[OM,' + string + ']')
    elif len(re.findall("[<|>|=|!]", string)) > 0:
        string = string.replace(string, '[OL,' + string + ']')
    elif len(re.findall("[||&]", string)) > 0:
        string = string.replace(string, '[CL,' + string + ']')
    else:
        erro = cria_arquivo('erro')
        erro.write(string + ' inválido\n')

    return string


if __name__ == '__main__':
    arquivo = False
    nme_arquivo = ''
    while not arquivo:
        nme_arquivo = input("Digite o nome do arquivo para ser copiado:\n")
        arquivo = abre_arquivo(nme_arquivo)
    arquivo_secundario = cria_arquivo(nme_arquivo)
    texto = substituir_texto(arquivo)
    texto = remove_comentario(texto)
    arquivo_secundario.write(texto)
    arquivo_secundario.close()
    arquivo.close()
