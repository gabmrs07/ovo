O=open('EXTRATO_{}.txt'.format(DIAVAR), 'a')
H=getattr(DATA, DATA._H[0])
O.write('EXTRATO DIA {}\n\n'.format(time.strftime('%d/%m/%y')))
for x in range(len(H)):
    O.write('-----------------------------------------------------------')
        if H[x]['CLIENTE']=='CARGA':
            O.write('\nCARGA\n')
            for y in ['BRT1','VRT1','BRT2','BRT3','BRDZ','VRDZ','BRMD','VRMD']:
                if y in H[x]:
                    O.write('{0}: {1}	PREÇO CAIXA: R$ {2}	TOTAL {0}: R$ {3}\n'.format(y,H[x][y],H[x][y+'_DZ'],H[x][y+'_VLR']))
            O.write('					SOMA GERAL: R$ {}\n'.format(H[x]['TOTAL']))
        else:
            O.write('\n{}\n'.format(H[x]['CLIENTE']))
                for y in ['BRT1','VRT1','BRT2','BRT3','BRDZ','VRDZ','BRMD','VRMD']:
                    if y in H[x]:
                        O.write('{0}: {1}	PREÇO DÚZIA: R$ {2}	TOTAL {0}: R$ {3}\n'.format(y,H[x][y],H[x][y+'_DZ'],H[x][y+'_VLR']))
                O.write('					SOMA GERAL: R$ {}\n'.format(H[x]['TOTAL']))
O.close()
