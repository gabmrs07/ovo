import DATA
import kivy
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string('''
<Main>
	Label:
		pos_hint: {'top':1}
		size_hint: 1, 0.1
		text: 'Gerador de Extrato'
	FileChooserListView:
		size_hint: 1, 0.3
		pos_hint: {'top': 0.9}
''')

class Main(BoxLayout):
	pass

class GenApp(App):
	def build(self):
		return Main()

if __name__ == '__main__':
	GenApp().run()


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
		O+='					   TOTAL: R$ {}\n'.format(x['TOTAL'])
		SOMACARGA=x['TOTAL']
	else:
		O+='\n{}\n'.format(x['CLIENTE'])
		for y in ['BRT1','VRT1','BRT2','BRT3','BRDZ','VRDZ','BRMD','VRMD']:
			if y in x:
				O+='{}: {}	PREÇO DÚZIA: R$ {}	SUBTOTAL: R$ {}\n'.format(y,x[y],x[y+'_DZ'],x[y+'_VLR'])
		O+='					   TOTAL: R$ {}\n'.format(x['TOTAL'])
		SOMA+=x['TOTAL']
O+='-----------------------------------------------------------\n'
O+='TOTAL COMPRADO: R$ {}\nTOTAL VENDIDO: R$ {}\n'.format(SOMACARGA, SOMA)
O+='LUCRO: R$ {}'.format(SOMA-SOMACARGA)
P=open('EXTRATO.txt', 'w')
P.write(O)
P.close()
