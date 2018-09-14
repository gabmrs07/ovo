# -*- coding: utf-8 -*-

import DATA
import os
import time
import re

os.chdir('/storage/emulated/0/kivy/app/')
SOMA=0.0
H=getattr(DATA, DATA._H[0])
O='EXTRATO DIA {}\n\n'.format(time.strftime('%d/%m/%y'))
for x in H:
	O+='-----------------------------------------------------------'
	if x['CLIENTE']=='CARGA':
		O+='\nCARGA\n'
		for y in ['BRT1','VRT1','BRT2','BRT3','BRDZ','VRDZ','BRMD','VRMD']:
			if y in x:
				O+='{}: {}	PREÇO CAIXA: R$ {}	SUBTOTAL: R$ {}\n'.format(y,x[y],x[y+'_DZ'],x[y+'_VLR'])
		O+='\nTOTAL: R$ {}\n'.format(x['TOTAL'])
		SOMACARGA=x['TOTAL']
	else:
		O+='\n{}\n'.format(x['CLIENTE'])
		for y in ['BRT1','VRT1','BRT2','BRT3','BRDZ','VRDZ','BRMD','VRMD']:
			if y in x:
				O+='{}: {}	PREÇO DÚZIA: R$ {}	SUBTOTAL: R$ {}\n'.format(y,x[y],x[y+'_DZ'],x[y+'_VLR'])
		O+='\nTOTAL: R$ {}\n'.format(x['TOTAL'])
		SOMA+=x['TOTAL']
O+='-----------------------------------------------------------\n'
O+='TOTAL COMPRADO: R$ {}\nTOTAL VENDIDO: R$ {}\n'.format(SOMACARGA, SOMA)
O+='LUCRO: R$ {}'.format(SOMA-SOMACARGA)
P=open('EXTRATO.txt', 'w')
P.write(O)
P.close()

P=open('DATA.py')
PR=P.read()
PS=re.sub('_C={.*}', '_C={}', PR)
P1=open('DATA.py', 'w')
P1.write(PS)
P1.close()
P.close()
