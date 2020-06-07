from PIL import Image
from fpdf import FPDF
from os import listdir, getcwd

#-------------------------------------------------------------------------------------------------------------
def redimensiona(imagem, nova_largura): #função para redimensionar a imagem
    largura, altura = imagem.size
    proporcao = altura/largura
    nova_altura = int(proporcao*nova_largura)
    return imagem.resize((nova_largura, nova_altura))
#-------------------------------------------------------------------------------------------------------------
def pixels2ascii(imagem):
    razao = int( 255/(len(SIMBOLOS)-1) )
    largura = imagem.size[0]  
    pixels = list(imagem.getdata())
    arte   = ""
    for i, pixel in enumerate(pixels):
        if i%largura==0:
            arte = arte + 'break'
        simbolo = int(pixel/razao)
        arte = arte + SIMBOLOS[simbolo]*2    
    return arte
#-------------------------------------------------------------------------------------------------------------
def converteASCII(imagem, largura):
    imagem = redimensiona(imagem, largura)
    return pixels2ascii(imagem)
#-------------------------------------------------------------------------------------------------------------
def gera_pdf(SIMBOLOS, msg, arqentrada, arqsaida):
    imagem = Image.open(arqentrada).convert("L")
    largura, altura = imagem.size
    # define se a folha será apresentada como paisagem ou retrato, conforme a altura e largura da imagem original
    if largura > altura:
        folha = 'L'
        linha = 400
        coluna = 550
    else:
        folha = 'P'
        linha = 277
        coluna = 450
    imagem1 = converteASCII(imagem, coluna)
    imagem2 = list(imagem1.split('break'))
    pdf = FPDF(folha, 'mm', 'A3')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(linha, 10, msg, 0, 1, 'C')
    pdf.set_font('Courier', '', 1)
    for i in imagem2:
        pdf.cell(linha,0.44,i, 0, 1, 'C')
    pdf.output(arqsaida, 'F')
    return
#-------------------------------------------------------------------------------------------------------------
def escolhe_imagem():
    listarquivos = listdir()
    listaimagens = []
    for i in listarquivos:
        if (i[-4]+i[-3]+i[-2]+i[-1]) in ['.bmp', '.jpg', '.png', '.tif', 'tiff']:
            listaimagens.append(i)
    listaimagens.append('sair')
    print('\n' + '-' * 100)
    if len(listaimagens) == 1:
        print('Não existem imagens no formato .bmp, .jpg, .png, .tif ou .tiff.\nInsira a imagem que deseja converter na mesma pasta do script python')
        #escolha = 'sair'
        return 'sair'
    else:
        print('\n--# Imagens encontradas no diretório %s #--\n' % (getcwd()))
        for i in range(len(listaimagens)):
            print('%s -> %s' %((i+1), listaimagens[i]))
        while True:
            try:
                escolha = int(input(('\nDigite o número da imagem que deseja converter ou o número da opção SAIR para encerrar o programa: ')))
                escolha = listaimagens[escolha-1]
                return escolha
            except Exception:
                return 'sair'
#----------------------     PROGRAMA PRINCIPAL      ----------------------------------------------------------
arqentrada = escolhe_imagem()
while arqentrada != 'sair':
    print('\nGerar imagem regular(R) ou em negativo(N)?')
    escolha = input()
    while escolha not in 'RNrn':
        print('Opção Inválida -> Gerar imagem regular(R) ou em negativo(N)?')
        escolha = input()
    escolha = escolha.upper()
    arqsaida = list(arqentrada.split('.'))
    arqsaida = str(arqsaida[0]+'_'+escolha+'.pdf')
    if escolha == 'N':
        SIMBOLOS = " .,:;+!ox?*%#@" #símbolos que formarão a imagem negativa
        msg = 'Imagem Negativa' + arqentrada
    else:
        SIMBOLOS = "@#%*?xo!+;:,. " #símbolos que formarão a imagem regular
        msg = 'Imagem Regular - ' + arqentrada

    gera_pdf(SIMBOLOS, msg, arqentrada, arqsaida)
    arqentrada = escolhe_imagem()






