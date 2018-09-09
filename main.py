import DATA
import kivy
import os
import os.path
import re
import socket
import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.base import runTouchApp

if socket.gethostname()=='josley' or socket.gethostname()=='lamettrie3':
	from importlib import reload

DIAVAR=time.strftime('H%d_%m_%y')
CWD=os.getcwd()
D='DATA.py'
L=['BRT1', 'BRT1_DZ', 'BRT1_VLR', 'BRT2', 'BRT2_DZ', 'BRT2_VLR', 'BRT3', 'BRT3_DZ', 'BRT3_VLR',\
		'VRT1', 'VRT1_DZ', 'VRT1_VLR', 'BRDZ', 'BRDZ_DZ', 'BRDZ_VLR', 'VRDZ', 'VRDZ_DZ', 'VRDZ_VLR',\
		'BRMDZ', 'BRMDZ_DZ', 'BRMDZ_VLR', 'VRMDZ', 'VRMDZ_DZ', 'VRMDZ_VLR','TOTAL']
NOME=None

BRT1=''
VRT1=''
BRT2=''
BRT3=''
BRDZ=''
VRDZ=''
BRMDZ=''
VRMDZ=''
BRT1_VALOR=DATA._CV['V1']
VRT1_VALOR=DATA._CV['V2']
BRT2_VALOR=DATA._CV['V3']
BRT3_VALOR=DATA._CV['V4']
BRDZ_VALOR=DATA._CV['V5']
VRDZ_VALOR=DATA._CV['V6']
BRMDZ_VALOR=DATA._CV['V7']
VRMDZ_VALOR=DATA._CV['V8']

class Menu(Screen):

	BT=Button(text='Gerar extrato')
	TRIGGER=None

	def on_pre_enter(self, *args):
		reload(DATA)
		for x in DATA._C:
			if DATA._C.get(x)==1:
				Menu.TRIGGER=1
				break
			elif Menu.TRIGGER==2:
				break
			else:
				Menu.TRIGGER=0
		if Menu.TRIGGER==0:
			Menu.BT=Button(text='Gerar extrato')
			Menu.BT.bind(on_press=self.EXTRATO)
			self.ids.MENU.add_widget(Menu.BT, index=2)
			Menu.TRIGGER=2

	def EXTRATO(self, instance):
		pass
#		E=list()
#		E.append(PLANILHA.CARGA)
#		for x in PLANILHA._C:
#			if x=='_END':
#				break
#			X=str.rstrip(x, '=0')
#			Y=getattr(PLANILHA, X)
#			E.append(Y)
#		E_DIA='H'+str.replace(PLANILHA._DIA, '/', '_')
#		W=open('DATA.py', 'a')
#		W.write('\n{}={}'.format(E_DIA, E))
#		W.close()
#		P0=open('DATA.py')
#		PR=P0.read()
#		PSUB=re.sub('\'_END\'', '\'{}\', \'_END\''.format(E_DIA), PR)
#		P1=open('DATA.py', 'w')
#		P1.write(PSUB)
#		P1.close()
#		P0.close()
#		os.remove(PLAN)
#		self.ids.MENU.remove_widget(Menu.BT)

	def CHECKER(self):
		if DATA._C:
			self.manager.current='entry'
		else:
			self.manager.current='rota'

class Rota(Screen):

	def SB(self, ROTA):
		C=dict()
		for x in ROTA:
			C[x]=1
		P=open(D)
		PR=P.read()
		PS=re.sub('_C={}', '_C={}'.format(C), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		H=getattr(DATA, '_H')
		H.insert(0, DIAVAR)
		P=open(D)
		PR=P.read()
		PS=re.sub('_H=\[.*\]', '_H={}'.format(H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		W=open(D, 'a')
		W.write('\n{}=[]'.format(DIAVAR))
		self.manager.current='entry'

	def RS_T(self):
		self.SB(DATA._TERCA)

	def RS_QUA(self):
		self.SB(DATA._QUARTA)

	def RS_QUI(self):
		self.SB(DATA._QUINTA)

class Carga(Screen):

	TEXTFOCUS=None
	INSERT=None
	BRT1=''
	BRT2=''
	BRT3=''
	VRT1=''
	BRDZ=''
	VRDZ=''
	BRMDZ=''
	VRMDZ=''


	def on_pre_enter(self, *args):
		self.ids['inpt1'].text=''
		self.ids['inpt2'].text=''
		self.ids['inpt3'].text=''
		self.ids['inpt4'].text=''
		self.ids['inpt5'].text=''
		self.ids['inpt6'].text=''
		self.ids['inpt7'].text=''
		self.ids['inpt8'].text=''
		self.ids['inp1'].text=DATA._CV['V1']
		self.ids['inp2'].text=DATA._CV['V2']
		self.ids['inp3'].text=DATA._CV['V3']
		self.ids['inp4'].text=DATA._CV['V4']
		self.ids['inp5'].text=DATA._CV['V5']
		self.ids['inp6'].text=DATA._CV['V6']
		self.ids['inp7'].text=DATA._CV['V7']
		self.ids['inp8'].text=DATA._CV['V8']

		Rota.TEXTFOCUS='inpt1'

	def FOCUS(self, IDS='inpt1'):
		Rota.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		self.ids[Rota.TEXTFOCUS].text += INSERT

	def BACKSPACE(self):
		self.ids[Rota.TEXTFOCUS].text = ''

	def MEIA(self):
		TEXT=self.ids[Rota.TEXTFOCUS].text
		if TEXT!='':
			FLT=float(self.ids[Rota.TEXTFOCUS].text)
			self.ids[Rota.TEXTFOCUS].text = str(FLT+0.5)
		else:
			self.ids[Rota.TEXTFOCUS].text += '0.5'

	def OK(self):

		BRT1=self.ids.inpt1.text
		VRT1=self.ids.inpt2.text
		BRT2=self.ids.inpt3.text
		BRT3=self.ids.inpt4.text
		BRDZ=self.ids.inpt5.text
		VRDZ=self.ids.inpt6.text
		BRMDZ=self.ids.inpt7.text
		VRMDZ=self.ids.inpt8.text
		BRT1_VALOR=self.ids.inp1.text
		VRT1_VALOR=self.ids.inp2.text
		BRT2_VALOR=self.ids.inp3.text
		BRT3_VALOR=self.ids.inp4.text
		BRDZ_VALOR=self.ids.inp5.text
		VRDZ_VALOR=self.ids.inp6.text
		BRMDZ_VALOR=self.ids.inp7.text
		VRMDZ_VALOR=self.ids.inp8.text

		SOMA=0.0

		if BRT1!='':
			BRT1(BRT1)
		if BRT2!='':
			BRT2(BRT2)
		if BRT3!='':
			BRT3(BRT3)
		if VRT1!='':
			VRT1(VRT1)
		if BRDZ!='':
			BRDZ(BRDZ)
		if VRDZ!='':
			VRDZ(VRDZ)
		if BRMDZ!='':
			BRMDZ(BRMDZ)
		if VRMDZ!='':
			VRMDZ(VRMDZ)

		DICT=dict()
		DICT['CLIENTE']='CARGA'
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
			if 0.0!=OVO.E[x]:
				SOMA+=OVO.E_VLR[x+'_VLR']
				DICT[x]=OVO.E[x]
				DICT[x+'_DZ']=OVO.E_DZ[x+'_DZ']
				DICT[x+'_VLR']=OVO.E_VLR[x+'_VLR']
		DICT['TOTAL']=(SOMA)

		W=open(PLAN, 'a')
		W.write('CARGA={}\n\n'.format(DICT))
		W.close()

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
				OVO.E[x]=0.0

		self.manager.current='entry'

class Entry(Screen):

	INSERT=None
	OUTRO=None

	def on_pre_enter(self, *args):
		reload(DATA)
		self.ids.inpt0.text=''
		Entry.OUTRO=None
		S=self.ids.spinner
		S.text='OUTRO'
		for x in DATA._C:
			if DATA._C.get(x)==1:
				S.text=x
				break
		R=list()
		for x in DATA._C:
			if DATA._C.get(x)==1:
				R.append(x)
		R.insert(0, 'OUTRO')
		S.values=R

	def NOME_TEXT(self):
		global NOME
		S=self.ids.spinner
		if S.text=='OUTRO':
			NOME=self.ids.inpt0.text
			Entry.OUTRO=0
			if NOME=='':
				POPUP0=Popup(title='ERRO: NOME EM BRANCO!', content=Label(text='Insira o nome do cliente.'),\
							size_hint=(0.7, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5})
				POPUP0.open()
				return 0
			elif NOME in DATA._C:
				POPUP1=Popup(title='ERRO: NOME EXISTENTE!', content=Label(text='Escolha outro nome.'),\
							size_hint=(0.7, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5})
				POPUP1.open()
				return 0
		else:
			NOME=S.text
		self.manager.current='catcher'

	def KEY(self, INSERT):
		self.ids['inpt0'].text += INSERT

	def BACKSPACE(self):
		self.ids.inpt0.text = ''

class Catcher(Screen):

	TEXTFOCUS=None
	INSERT=None

	def on_pre_enter(self, *args):
		self.ids['inpt1'].text=''
		self.ids['inpt2'].text=''
		self.ids['inpt3'].text=''
		self.ids['inpt4'].text=''
		self.ids['inpt5'].text=''
		self.ids['inpt6'].text=''
		self.ids['inpt7'].text=''
		self.ids['inpt8'].text=''
		self.ids['inp1'].text=DATA._V['V1']
		self.ids['inp2'].text=DATA._V['V2']
		self.ids['inp3'].text=DATA._V['V3']
		self.ids['inp4'].text=DATA._V['V4']
		self.ids['inp5'].text=DATA._V['V5']
		self.ids['inp6'].text=DATA._V['V6']
		self.ids['inp7'].text=DATA._V['V7']
		self.ids['inp8'].text=DATA._V['V8']
		self.ids['NC'].text='CLIENTE: {}'.format(NOME)

		Catcher.TEXTFOCUS='inpt1'

	def FOCUS(self, IDS='inpt1'):
		Catcher.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		self.ids[Catcher.TEXTFOCUS].text += INSERT

	def BACKSPACE(self):
		self.ids[Catcher.TEXTFOCUS].text = ''

	def MEIA(self):
		TEXT=self.ids[Catcher.TEXTFOCUS].text
		if TEXT!='':
			FLT=float(self.ids[Catcher.TEXTFOCUS].text)
			self.ids[Catcher.TEXTFOCUS].text = str(FLT+2.5)
		else:
			self.ids[Catcher.TEXTFOCUS].text += '2.5'

	def OK(self):

		global BRT1
		global BRT2
		global BRT3
		global VRT1
		global BRDZ
		global VRDZ
		global BRMDZ
		global VRMDZ
		global BRT1_VALOR
		global VRT1_VALOR
		global BRT2_VALOR
		global BRT3_VALOR
		global BRDZ_VALOR
		global VRDZ_VALOR
		global BRMDZ_VALOR
		global VRMDZ_VALOR

		B1=self.ids.inpt1.text
		V1=self.ids.inpt2.text
		B2=self.ids.inpt3.text
		B3=self.ids.inpt4.text
		BDZ=self.ids.inpt5.text
		VDZ=self.ids.inpt6.text
		BMD=self.ids.inpt7.text
		VMD=self.ids.inpt8.text
		BRT1_VALOR=self.ids.inp1.text
		VRT1_VALOR=self.ids.inp2.text
		BRT2_VALOR=self.ids.inp3.text
		BRT3_VALOR=self.ids.inp4.text
		BRDZ_VALOR=self.ids.inp5.text
		VRDZ_VALOR=self.ids.inp6.text
		BRMDZ_VALOR=self.ids.inp7.text
		VRMDZ_VALOR=self.ids.inp8.text

		SOMA=0.0

		if B1!='':
			BRT1(B1)
		if B2!='':
			BRT2(B2)
		if B3!='':
			BRT3(B3)
		if V1!='':
			VRT1(V1)
		if BDZ!='':
			BRDZ(BDZ)
		if VDZ!='':
			VRDZ(VDZ)
		if BMD!='':
			BRMDZ(BMD)
		if VMD!='':
			VRMDZ(VMD)

		O=dict()
		O['CLIENTE']=NOME
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
			if 0.0!=OVO.E[x]:
				SOMA+=OVO.E_VLR[x+'_VLR']
				O[x]=OVO.E[x]
				O[x+'_DZ']=OVO.E_DZ[x+'_DZ']
				O[x+'_VLR']=OVO.E_VLR[x+'_VLR']
		O['TOTAL']=SOMA

		DATA._C[NOME]=0
		P=open(D)
		PR=P.read()
		PS=re.sub('_C={.*}', '_C={}'.format(DATA._C), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P1.close()
		P.close()

		H=getattr(DATA, DATA._H[0])
		H.append(O)
		P=open(D)
		PR=P.read()
		PS=re.sub('{}=\[.*\]'.format(DATA._H[0]), '{}={}'.format(DATA._H[0], H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
				OVO.E[x]=0.0

		self.manager.current='menu'

class Output(Screen):

	E=None
	I=None

	def on_pre_enter(self, *args):
		B=self.ids.EDIT
		S=self.ids.outspin
		S_LIST=list()
		if S.text!='':
			S.text=''
			self.ids.DIA.text=''
			B.text=''
			B.background_color=(0, 0, 0, 1)
			for x in L:
				self.ids[x].text=''
		for x in DATA._C:
			if DATA._C.get(x)==0:
				S_LIST.append(x)
		S.values=S_LIST

	def SELECT(self):
		ST=self.ids.outspin.text
		if ST=='':
			return 0
		B=self.ids.EDIT
		S=getattr(DATA, DATA._H[0])
		for x in range(len(S)):
			if S[x]['CLIENTE']==ST:
				I=x
		Output.E=S[I]
		Output.I=I
		self.ids.DIA.text=str.replace(str.strip(DATA._H[0], 'H'), '_', '/')
		B.text='EDITAR'
		B.background_color=(0.8, 0, 0, 1)
		for x in L:
			if x in S[I]:
				self.ids[x].text=str(S[I][x])
			else:
				self.ids[x].text='-'

	def EDITING(self):
		global NOME
		if self.ids.outspin.text=='':
			pass
		else:
			NOME=self.ids.outspin.text
			self.manager.current='editar'

class Editar(Screen):

	TEXTFOCUS=None
	INSERT=None

	def on_pre_enter(self, *args):
		def FILL(X, Y):
			if Y in Output.E:
				self.ids[X].text=str(Output.E[Y])
			else:
				self.ids[X].text=''
		def FILLPILAS(X, Y, Z):
			if Y in Output.E:
				self.ids[X].text=str(Output.E[Y])
			else:
				self.ids[X].text=DATA._V[Z]
		FILL('t1', 'BRT1')
		FILL('t2', 'VRT1')
		FILL('t3', 'BRT2')
		FILL('t4', 'BRT3')
		FILL('t5', 'BRDZ')
		FILL('t6', 'VRDZ')
		FILL('t7', 'VRMDZ')
		FILL('t8', 'BRMDZ')
		FILLPILAS('p1', 'BRT1_DZ', 'V1')
		FILLPILAS('p2', 'VRT1_DZ', 'V2')
		FILLPILAS('p3', 'BRT2_DZ', 'V3')
		FILLPILAS('p4', 'BRT3_DZ', 'V4')
		FILLPILAS('p5', 'BRDZ_DZ', 'V5')
		FILLPILAS('p6', 'VRDZ_DZ', 'V6')
		FILLPILAS('p7', 'VRMDZ_DZ', 'V7')
		FILLPILAS('p8', 'BRMDZ_DZ', 'V8')
		self.ids['NCL'].text='CLIENTE: {}'.format(NOME)

		Editar.TEXTFOCUS='t1'

	def FOCUS(self, IDS='t1'):
		Editar.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		self.ids[Editar.TEXTFOCUS].text += INSERT

	def BACKSPACE(self):
		self.ids[Editar.TEXTFOCUS].text = ''

	def MEIA(self):
		TEXT=self.ids[Editar.TEXTFOCUS].text
		if TEXT!='':
			FLT=float(self.ids[Editar.TEXTFOCUS].text)
			self.ids[Editar.TEXTFOCUS].text = str(FLT+2.5)
		else:
			self.ids[Editar.TEXTFOCUS].text += '2.5'

	def OK(self):

		global B1
		global B2
		global B3
		global V1
		global BDZ
		global VDZ
		global BMD
		global VMD
		global BRT1_VALOR
		global VRT1_VALOR
		global BRT2_VALOR
		global BRT3_VALOR
		global BRDZ_VALOR
		global VRDZ_VALOR
		global BRMDZ_VALOR
		global VRMDZ_VALOR

		B1=self.ids.t1.text
		V1=self.ids.t2.text
		B2=self.ids.t3.text
		B3=self.ids.t4.text
		BDZ=self.ids.t5.text
		VDZ=self.ids.t6.text
		BMD=self.ids.t7.text
		VMD=self.ids.t8.text
		BRT1_VALOR=self.ids.p1.text
		VRT1_VALOR=self.ids.p2.text
		BRT2_VALOR=self.ids.p3.text
		BRT3_VALOR=self.ids.p4.text
		BRDZ_VALOR=self.ids.p5.text
		VRDZ_VALOR=self.ids.p6.text
		BRMDZ_VALOR=self.ids.p7.text
		VRMDZ_VALOR=self.ids.p8.text

		SOMA=0.0

		if B1!='':
			BRT1(B1)
		if B2!='':
			BRT2(B2)
		if B3!='':
			BRT3(B3)
		if V1!='':
			VRT1(V1)
		if BDZ!='':
			BRDZ(BDZ)
		if VDZ!='':
			VRDZ(VDZ)
		if BMD!='':
			BRMDZ(BMD)
		if VMD!='':
			VRMDZ(VMD)

		O=dict()
		O['CLIENTE']=NOME
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
			if 0.0!=OVO.E[x]:
				SOMA+=OVO.E_VLR[x+'_VLR']
				O[x]=OVO.E[x]
				O[x+'_DZ']=OVO.E_DZ[x+'_DZ']
				O[x+'_VLR']=OVO.E_VLR[x+'_VLR']
		O['TOTAL']=SOMA

		H=getattr(DATA, DATA._H[0])
		H.pop(Output.I)
		H.insert(Output.I, O)
		P=open(D)
		PR=P.read()
		PS=re.sub('{}=\[.*\]'.format(DATA._H[0]), '{}={}'.format(DATA._H[0], H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
				OVO.E[x]=0.0

		self.manager.current='menu'

class HistSel(Screen):

	D=None

	def on_pre_enter(self, *args):
		reload(DATA)
		H=list()
		for x in DATA._H:
			X=str.strip(x, 'H')
			S=str.replace(X, '_', '/')
			H.append(S)
		self.ids.hspin.values=H

	def HSEL(self):
		if self.ids.hspin.text!='':
			HistSel.D=self.ids.hspin.text
			self.manager.current='history'
		else:
			pass

class History(Screen):

	L=None
	H=None

	def on_pre_enter(self, *args):
		self.ids.hhspin.text=''
		for x in L:
			self.ids[x].text=''
		self.ids.DIA.text=HistSel.D
		H='H'+str.replace(HistSel.D, '/', '_')
		History.H=getattr(DATA, H)
		History.L=list()
		for x in range(len(History.H)):
			History.L.append(History.H[x]['CLIENTE'])
		self.ids.hhspin.values=History.L

	def SEL(self):

		I=History.L.index(self.ids.hhspin.text)
		for x in L:
			try:
				self.ids[x].text=str(History.H[I][x])
			except:
				self.ids[x].text='-'

class Settings(Screen):
	pass

class PreSetr(Screen):

	MODO=None

	def T(self):
		PreSetr.MODO=1
		self.manager.current='setr'

	def Q(self):
		PreSetr.MODO=2
		self.manager.current='setr'

	def QI(self):
		PreSetr.MODO=3
		self.manager.current='setr'

class Setr(Screen):

	def on_pre_enter(self, *args):
		self.ids.adsubspin.text=''
		if PreSetr.MODO==1:
			self.ids.adsubspin.values=DATA._TERCA
		elif PreSetr.MODO==2:
			self.ids.adsubspin.values=DATA._QUARTA
		elif PreSetr.MODO==3:
			self.ids.adsubspin.values=DATA._QUINTA

	def KEY(self, INSERT):
		self.ids['cli'].text += INSERT

	def BACKSPACE(self):
		self.ids.cli.text = ''

	def REMOVE(self):
		if self.ids.adsubspin.text!='':
			if PreSetr.MODO==1:
				self.REMOVER('_TERCA')
			elif PreSetr.MODO==2:
				self.REMOVER('_QUARTA')
			elif PreSetr.MODO==3:
				self.REMOVER('_QUARTA')

	def REMOVER(self, DIA):
		R=getattr(DATA, DIA)
		R.remove(self.ids.adsubspin.text)
		P=open('DATA.py')
		PR=P.read()
		PS=re.sub('{}=\[.*\]'.format(DIA), '{}={}'.format(DIA, R), PR)
		P1=open('DATA.py', 'w')
		P1.write(PS)
		P1.close()
		P.close()
		self.ids.adsubspin.text=''
		reload(DATA)
		if PreSetr.MODO==1:
			self.ids.adsubspin.values=DATA._TERCA
		elif PreSetr.MODO==2:
			self.ids.adsubspin.values=DATA._QUARTA
		elif PreSetr.MODO==3:
			self.ids.adsubspin.values=DATA._QUINTA

	def ADD(self):
		if self.ids.cli.text!='':
			if PreSetr.MODO==1:
				self.ADDER('_TERCA')
			elif PreSetr.MODO==2:
				self.ADDER('_QUARTA')
			elif PreSetr.MODO==3:
				self.ADDER('_QUARTA')

	def ADDER(self, DIA):
		R=getattr(DATA, DIA)
		if self.ids.adsubspin.text!='':
			I=R.index(self.ids.adsubspin.text)
			R.insert(I, self.ids.cli.text)
		else:
			R.append(self.ids.cli.text)
		P=open('DATA.py')
		PR=P0.read()
		PS=re.sub('{}=\[.*\]'.format(DIA), '{}={}'.format(DIA, R), PR)
		P1=open('DATA.py', 'w')
		P1.write(PS)
		P1.close()
		P.close()
		self.ids.adsubspin.text=''
		self.ids.cli.text=''
		reload(DATA)
		if PreSetr.MODO==1:
			self.ids.adsubspin.values=DATA._TERCA
		elif PreSetr.MODO==2:
			self.ids.adsubspin.values=DATA._QUARTA
		elif PreSetr.MODO==3:
			self.ids.adsubspin.values=DATA._QUINTA

class Setv(Screen):

	TEXTFOCUS=None
	INSERT=None

	def on_pre_enter(self, *args):
		def FILL(X):
			self.ids[X].text=DATA._V[X]
		for x in range(1,9):
			FILL('V'+str(x))

	def FOCUS(self, IDS='t1'):
		Setv.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		self.ids[Setv.TEXTFOCUS].text += INSERT

	def BACKSPACE(self):
		self.ids[Setv.TEXTFOCUS].text = ''

	def MEIA(self):
		TEXT=self.ids[Setv.TEXTFOCUS].text
		if TEXT!='':
			FLT=float(self.ids[Setv.TEXTFOCUS].text)
			self.ids[Setv.TEXTFOCUS].text = str(FLT+2.5)
		else:
			self.ids[Setv.TEXTFOCUS].text += '2.5'

	def OK(self):
		V=dict()
		for x in ['V1','V2','V3','V4','V5','V6','V7','V8']:
			V[x]=self.ids[x].text
		P=open('DATA.py')
		PR=P.read()
		PS=re.sub('_V={.*}', '_V={}'.format(V), PR)
		P1=open('DATA.py', 'w')
		P1.write(PS)
		P1.close()
		P.close()
		self.manager.current='menu'

class MapaApp(App):
	sm=None
	def build(self):
		self.sm=ScreenManager()
		self.sm.add_widget(Menu(name='menu'))
		self.sm.add_widget(Rota(name='rota'))
		self.sm.add_widget(Carga(name='carga'))
		self.sm.add_widget(Entry(name='entry'))
		self.sm.add_widget(Catcher(name='catcher'))
		self.sm.add_widget(Output(name='output'))
		self.sm.add_widget(Editar(name='editar'))
		self.sm.add_widget(HistSel(name='histsel'))
		self.sm.add_widget(History(name='history'))
		self.sm.add_widget(Settings(name='set'))
		self.sm.add_widget(PreSetr(name='presetr'))
		self.sm.add_widget(Setr(name='setr'))
		self.sm.add_widget(Setv(name='valor'))
		self.sm.current='menu'
		return self.sm

## MAIN.PY

class OVO:

	E={'BRT1':0.0,'BRT2':0.0,'BRT3':0.0,'VRT1':0.0,'BRDZ':0.0,'VRDZ':0.0,'BRMDZ':0.0,'VRMDZ':0.0}

	E_DZ={'BRT1_DZ':0.0,'BRT2_DZ':0.0,'BRT3_DZ':0.0,'VRT1_DZ':0.0,'BRDZ_DZ':0.0,'VRDZ_DZ':0.0,'BRMDZ_DZ':0.0,'VRMDZ_DZ':0.0}

	E_VLR={'BRT1_VLR':0.0,'BRT2_VLR':0.0,'BRT3_VLR':0.0,'VRT1_VLR':0.0,'BRDZ_VLR':0.0,'VRDZ_VLR':0.0,'BRMDZ_VLR':0.0,'VRMDZ_VLR':0.0}

	def __init__(self, dz):
		self.dz=float(dz)

class BRT1(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(BRT1_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRT1']=self.dz
		OVO.E_DZ['BRT1_DZ']=self.valor
		OVO.E_VLR['BRT1_VLR']=self.soma

class BRT2(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(BRT2_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRT2']=self.dz
		OVO.E_DZ['BRT2_DZ']=self.valor
		OVO.E_VLR['BRT2_VLR']=self.soma

class BRT3(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(BRT3_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRT3']=self.dz
		OVO.E_DZ['BRT3_DZ']=self.valor
		OVO.E_VLR['BRT3_VLR']=self.soma

class VRT1(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(VRT1_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['VRT1']=self.dz
		OVO.E_DZ['VRT1_DZ']=self.valor
		OVO.E_VLR['VRT1_VLR']=self.soma

class BRDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(BRDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRDZ']=self.dz
		OVO.E_DZ['BRDZ_DZ']=self.valor
		OVO.E_VLR['BRDZ_VLR']=self.soma

class VRDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(VRDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['VRDZ']=self.dz
		OVO.E_DZ['VRDZ_DZ']=self.valor
		OVO.E_VLR['VRDZ_VLR']=self.soma

class BRMDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(BRMDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRMDZ']=self.dz
		OVO.E_DZ['BRMDZ_DZ']=self.valor
		OVO.E_VLR['BRMDZ_VLR']=self.soma

class VRMDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(VRMDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['VRMDZ']=self.dz
		OVO.E_DZ['VRMDZ_DZ']=self.valor
		OVO.E_VLR['VRMDZ_VLR']=self.soma


if __name__ == '__main__':
	MapaApp().run()
