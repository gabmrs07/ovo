import DATA
import kivy
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string('''
<Main>
	BoxLayout:
		pos_hint: {'top':1}
		orientation: 'vertical'
		Label:
			text: 'GERADOR DE EXTRATO'
		BoxLayout:
			Label:
				size_hint: 0.3, 1
				text: 'ESCOLHA O DIA:'
				canvas.before:
					Color:
						rgba: 0.3, 0.3, 0.3, 1
					Rectangle:
						pos: self.pos
						size: self.size
			Spinner:
				id: SPIN
		Label:
			id: STATUS
		Button:
			text: 'Gerar'
			background_color: 0, 0.8, 0, 1
			on_press: root.GEN()
''')

class Main(BoxLayout):
	def __init__(self, **kwargs):
		super(Main, self).__init__(**kwargs)
		H=list()
		for x in DATA._H:
			X=str.strip(x, 'H')
			S=str.replace(X, '_', '/')
			H.append(S)
		self.ids.SPIN.values=H
		self.ids.SPIN.text=H[0]

	def GEN(self):
		SOMA=0.0
		G='H'+str.replace(self.ids.SPIN.text, '/', '_')
		H=getattr(DATA, G)
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
		P=open('EXTRATO_{}.txt'.format(str.replace(self.ids.SPIN.text, '/', '_')), 'w')
		P.write(O)
		P.close()
		self.ids.STATUS.text='Extrato gerado com sucesso!'

class GenApp(App):
	def build(self):
		return Main()

if __name__ == '__main__':
	GenApp().run()
