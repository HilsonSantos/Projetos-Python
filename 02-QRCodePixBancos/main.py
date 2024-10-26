from bbrasil import ApiPixCobrancaImediata



if __name__ == '__main__':
    brasil = ApiPixCobrancaImediata()
    brasil.consultar_cobranca_imediata()
    #processo_bancobrasil(3)
    #GerarQrCodePix(nome=getnome, chavepix=getchavepix, valor=getvalor, cidade=getcidade, txtid=gettxtid).gerar_cr16()