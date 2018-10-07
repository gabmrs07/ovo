# -*- coding: utf-8 -*-
#!/usr/bin/python2

import DATA
import kivy
import re
import sys
import time
from datetime import date
from kivy.app import App
from kivy.base import runTouchApp, ExceptionHandler, ExceptionManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

if sys.version_info[0] == 3:
	from importlib import reload

D='DATA.py'
L=['BRT1', 'BRT1_DZ', 'BRT1_VLR', 'BRT2', 'BRT2_DZ', 'BRT2_VLR', 'BRT3', 'BRT3_DZ', 'BRT3_VLR',\
		'VRT1', 'VRT1_DZ', 'VRT1_VLR', 'BRDZ', 'BRDZ_DZ', 'BRDZ_VLR', 'VRDZ', 'VRDZ_DZ', 'VRDZ_VLR',\
		'BRMD', 'BRMD_DZ', 'BRMD_VLR', 'VRMD', 'VRMD_DZ', 'VRMD_VLR','TOTAL']
L1=['BRT1','VRT1','BRT2','BRT3','BRDZ','VRDZ','BRMD','VRMD']
NOME=None

BRT1=None
VRT1=None
BRT2=None
BRT3=None
BRDZ=None
VRDZ=None
BRMD=None
VRMD=None
BRT1_VALOR=None
VRT1_VALOR=None
BRT2_VALOR=None
BRT3_VALOR=None
BRDZ_VALOR=None
VRDZ_VALOR=None
BRMD_VALOR=None
VRMD_VALOR=None

class E(ExceptionHandler):
	def handle_exception(self, inst):
		return ExceptionManager.PASS

ExceptionManager.add_handler(E())

class Menu(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)

	def CHECKER(self):
		if DATA._C:
			self.manager.current='entry'
		else:
			self.manager.current='rota'

class Rota(Screen):

	WEEK=None
	DA=int(time.strftime('%d'))
	M=int(time.strftime('%m'))
	Y=int(time.strftime('%y'))

	def on_pre_enter(self, *args):
		Rota.WEEK=None

	def SB(self, ROTA):
		C=dict()
		C['ROTA']=ROTA
		for x in ROTA:
			C[x]=1
		P=open(D)
		PR=P.read()
		PS=re.sub('_C={}', '_C={}'.format(C), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		P=open(D)
		PR=P.read()
		if not Dia.S:
			PS=re.sub('_W=None', '_W=\'H{}_{}_{}\''.format(Rota.DA, Rota.M, Rota.Y), PR)
		else:
			PS=re.sub('_W=None', '_W=\'H{}_{}_{}\''.format(int(Dia.S[0]), int(Dia.S[1]), int(Dia.S[2])), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()
		reload(DATA)

		H=getattr(DATA, '_H')
		if not Dia.S:
			H.insert(0, 'H{}_{}_{}'.format(Rota.DA, Rota.M, Rota.Y))
		else:
			H.insert(0, 'H{}_{}_{}'.format(int(Dia.S[0]), int(Dia.S[1]), int(Dia.S[2])))
		P=open(D)
		PR=P.read()
		PS=re.sub('_H=\[.*\]', '_H={}'.format(H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		try:
			self.manager.current='carga'
		except:
			pass

	def RS_T(self):
		if date.weekday(date(self.Y, self.M, self.DA))==1:
			self.SB(DATA._TERCA)
		else:
			self.manager.current='dia'
		Rota.WEEK=1

	def RS_QUA(self):
		if date.weekday(date(self.Y, self.M, self.DA))==2:
			self.SB(DATA._QUARTA)
		else:
			self.manager.current='dia'
		Rota.WEEK=2

	def RS_QUI(self):
		if date.weekday(date(self.Y, self.M, self.DA))==3:
			self.SB(DATA._QUINTA)
		else:
			self.manager.current='dia'
		Rota.WEEK=3

class Dia(Screen):

	S=None

	def on_pre_enter(self, *args):
		self.ids.DMY.text='{}/{}/{}'.format(Rota.DA, Rota.M, Rota.Y)

	def KEY(self, INSERT):
		self.ids['DMY'].text += INSERT

	def BACKSPACE(self):
		self.ids.DMY.text = self.ids.DMY.text[:len(self.ids.DMY.text)-1]

	def FCLEAR(self):
		self.ids.DMY.text = ''

	def OK(self):

		if re.search('[0-3][0-9]/[0-1][0-9]/[0-9][0-9]', self.ids.DMY.text):
			Dia.S=str.split(self.ids.DMY.text, '/')
			DA=int(Dia.S[0])
			M=int(Dia.S[1])
			Y=int(Dia.S[2])
			if DA not in range(1, 32):
				return 0
			elif M not in range(1, 13):
				return 0
			elif Y not in range(1, 100):
				return 0
			INSTANCE=Rota()
			if Rota.WEEK==1:
				if date.weekday(date(Y, M, DA)) != 1:
					return 0
				else:
					INSTANCE.SB(DATA._TERCA)
			elif Rota.WEEK==2:
				if date.weekday(date(Y, M, DA)) != 2:
					return 0
				else:
					INSTANCE.SB(DATA._QUARTA)
			elif Rota.WEEK==3:
				if date.weekday(date(Y, M, DA)) != 3:
					return 0
				else:
					INSTANCE.SB(DATA._QUINTA)
			reload(DATA)
			self.manager.current='carga'

class Carga(Screen):

	TEXTFOCUS=None

	def on_pre_enter(self, *args):
		reload(DATA)
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

		global BRT1_VALOR
		global VRT1_VALOR
		global BRT2_VALOR
		global BRT3_VALOR
		global BRDZ_VALOR
		global VRDZ_VALOR
		global BRMD_VALOR
		global VRMD_VALOR

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
		BRMD_VALOR=self.ids.inp7.text
		VRMD_VALOR=self.ids.inp8.text

		SOMA=0.0

		C=dict()
		C['WEEK']=Rota.WEEK
		C['CLIENTE']='CARGA'

		if B1!='':
			BRT1(B1)
		else:
			C['BRT1_DZ']=float(BRT1_VALOR)
		if B2!='':
			BRT2(B2)
		else:
			C['BRT2_DZ']=float(BRT2_VALOR)
		if B3!='':
			BRT3(B3)
		else:
			C['BRT3_DZ']=float(BRT3_VALOR)
		if V1!='':
			VRT1(V1)
		else:
			C['VRT1_DZ']=float(VRT1_VALOR)
		if BDZ!='':
			BRDZ(BDZ)
		else:
			C['BRDZ_DZ']=float(BRDZ_VALOR)
		if VDZ!='':
			VRDZ(VDZ)
		else:
			C['VRDZ_DZ']=float(VRDZ_VALOR)
		if BMD!='':
			BRMD(BMD)
		else:
			C['BRMD_DZ']=float(BRMD_VALOR)
		if VMD!='':
			VRMD(VMD)
		else:
			C['VRMD_DZ']=float(VRMD_VALOR)

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if 0.0!=OVO.E[x]:
				SOMA+=OVO.E_VLR[x+'_VLR']
				C[x]=OVO.E[x]
				C[x+'_DZ']=OVO.E_DZ[x+'_DZ']
				C[x+'_VLR']=OVO.E_VLR[x+'_VLR']
		C['TOTAL']=SOMA

		W=open(D, 'a')
		W.write('\n{}=[{}]'.format(DATA._W, C))
		W.close()

		CARGA=getattr(DATA, '_CARGA')

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if x in C:
				A=CARGA[x]+C[x]*30.0
				CARGA[x]=A

		P=open(D)
		PR=P.read()
		PS=re.sub('_CARGA={.*}', '_CARGA={}'.format(CARGA), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P1.close()
		P.close()

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				OVO.E[x]=0.0

		self.manager.current='entry'

class Entry(Screen):

	OUTRO=None

	def on_pre_enter(self, *args):
		reload(DATA)
		self.ids.inpt0.text=''
		Entry.OUTRO=None
		S=self.ids.spinner
		S.text='OUTRO'
		for x in DATA._C['ROTA']:
			if DATA._C.get(x)==1:
				S.text=x
				break
		R=list()
		for x in DATA._C['ROTA']:
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
				POPUP=Popup()
				BX=BoxLayout(orientation='vertical')
				BT=Button(text='OK', background_color=(0, 0.8, 0, 1), size_hint=(1, 0.3))
				BT.bind(on_press=POPUP.dismiss)
				BX.add_widget(Label(text='Insira o nome do cliente.', size_hint=(1, 0.7), pos_hint={'top':1}))
				BX.add_widget(BT)
				POPUP.title='ERRO: NOME EM BRANCO!'
				POPUP.content=BX
				POPUP.size_hint=(0.8, 0.5)
				POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
				POPUP.auto_dismiss=False
				POPUP.open()
				return 0
			elif NOME in DATA._C:
				POPUP=Popup()
				BX=BoxLayout(orientation='vertical')
				BT=Button(text='OK', background_color=(0, 0.8, 0, 1), size_hint=(1, 0.3))
				BT.bind(on_press=POPUP.dismiss)
				BX.add_widget(Label(text='Insira outro nome para o cliente.', size_hint=(1, 0.7), pos_hint={'top':1}))
				BX.add_widget(BT)
				POPUP.title='ERRO: NOME JÁ UTILIZADO!'
				POPUP.content=BX
				POPUP.size_hint=(0.8, 0.5)
				POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
				POPUP.auto_dismiss=False
				POPUP.open()
				return 0
		else:
			NOME=S.text
		self.manager.current='catcher'

	def KEY(self, INSERT):
		self.ids['inpt0'].text += INSERT

	def BACKSPACE(self):
		self.ids.inpt0.text = self.ids.inpt0.text[:len(self.ids.inpt0.text)-1]

class Catcher(Screen):

	CHECKER=1
	TEXTFOCUS=None
	O=None
	SOMA=0.0
	LABEL=Label(size_hint=(1, 0.45), pos_hint={'top':0.95}, font_size=60)
	POPUP=Popup()

	def on_pre_enter(self, *args):

		def FILL(W, X, Y):
			for x in DATA._H:
				H=getattr(DATA, x)
				if H[0].get('WEEK') == W:
					for y in H:
						if y['CLIENTE'] == NOME:
							if X in y:
								self.ids[Y].text=str(y[X+'_DZ'])
								return 0

		reload(DATA)
		self.CHECKER=1

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

		S=str.split(str.strip(DATA._W, 'H'), '_')
		if date.weekday(date(int(S[2]), int(S[1]), int(S[0]))) == 1:
			FILL(1, 'BRT1', 'inp1')
			FILL(1, 'VRT1', 'inp2')
			FILL(1, 'BRT2', 'inp3')
			FILL(1, 'BRT3', 'inp4')
			FILL(1, 'BRDZ', 'inp5')
			FILL(1, 'VRDZ', 'inp6')
			FILL(1, 'BRMD', 'inp7')
			FILL(1, 'VRMD', 'inp8')
		elif date.weekday(date(int(S[2]), int(S[1]), int(S[0]))) == 2:
			FILL(2, 'BRT1', 'inp1')
			FILL(2, 'VRT1', 'inp2')
			FILL(2, 'BRT2', 'inp3')
			FILL(2, 'BRT3', 'inp4')
			FILL(2, 'BRDZ', 'inp5')
			FILL(2, 'VRDZ', 'inp6')
			FILL(2, 'BRMD', 'inp7')
			FILL(2, 'VRMD', 'inp8')
		elif date.weekday(date(int(S[2]), int(S[1]), int(S[0]))) == 3:
			FILL(3, 'BRT1', 'inp1')
			FILL(3, 'VRT1', 'inp2')
			FILL(3, 'BRT2', 'inp3')
			FILL(3, 'BRT3', 'inp4')
			FILL(3, 'BRDZ', 'inp5')
			FILL(3, 'VRDZ', 'inp6')
			FILL(3, 'BRMD', 'inp7')
			FILL(3, 'VRMD', 'inp8')

		self.ids['NC'].text='CLIENTE: {}'.format(NOME)

		Catcher.TEXTFOCUS='inpt1'
		self.SOMA=0.0

	def FOCUS(self, IDS='inpt1'):
		Catcher.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		if self.CHECKER == 1:
			self.ids[Catcher.TEXTFOCUS].text += INSERT
		else:
			self.LABEL.text += INSERT

	def BACKSPACE(self):
		if self.CHECKER == 1:
			self.ids[Catcher.TEXTFOCUS].text = ''
		else:
			self.LABEL.text = self.LABEL.text[:len(self.LABEL.text)-1]

	def MEIA(self):
		TEXT=self.ids[Catcher.TEXTFOCUS].text
		if TEXT!='':
			FLT=float(self.ids[Catcher.TEXTFOCUS].text)
			self.ids[Catcher.TEXTFOCUS].text = str(FLT+2.5)
		else:
			self.ids[Catcher.TEXTFOCUS].text += '2.5'

	def OK(self):

		if self.CHECKER == 1:

			global BRT1_VALOR
			global VRT1_VALOR
			global BRT2_VALOR
			global BRT3_VALOR
			global BRDZ_VALOR
			global VRDZ_VALOR
			global BRMD_VALOR
			global VRMD_VALOR

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
			BRMD_VALOR=self.ids.inp7.text
			VRMD_VALOR=self.ids.inp8.text

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
				BRMD(BMD)
			if VMD!='':
				VRMD(VMD)

			self.O=dict()
			self.O['CLIENTE']=NOME
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if 0.0!=OVO.E[x]:
					self.SOMA+=OVO.E_VLR[x+'_VLR']
					self.O[x]=OVO.E[x]
					self.O[x+'_DZ']=OVO.E_DZ[x+'_DZ']
					self.O[x+'_VLR']=OVO.E_VLR[x+'_VLR']
			self.O['TOTAL']=self.SOMA

		else:
			self.SOMA=str(float(self.LABEL.text))
			self.O['TOTAL']=float(self.LABEL.text)

		BX=BoxLayout(orientation='vertical')
		BXT=BoxLayout(size_hint=(1, 0.3))
		BT1=Button(text='Sim', background_color=(0, 0.8, 0, 1))
		BT2=Button(text='Trocar', background_color=(0, 0, 1, 1))
		BT3=Button(text='Não', background_color=(0.8, 0, 0, 1))
		BT1.bind(on_press=self.WRITER)
		BT2.bind(on_press=self.DESC)
		BT3.bind(on_press=self.DISMISS)
		BXT.add_widget(BT1)
		BXT.add_widget(BT2)
		BXT.add_widget(BT3)
		BX.add_widget(Label(text='R$ {}'.format(self.SOMA), size_hint=(1, 0.7), pos_hint={'top':1}, font_size=40))
		BX.add_widget(BXT)
		self.POPUP.title='CONFIRMAÇÃO DO VALOR'
		self.POPUP.content=BX
		self.POPUP.size_hint=(0.8, 0.6)
		self.POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
		self.POPUP.auto_dismiss=False
		self.POPUP.open()

	def DESC(self, instance):
		if self.CHECKER == 1:
			self.remove_widget(self.ids.GL)
			self.add_widget(self.LABEL)
			self.POPUP.dismiss()
			self.LABEL.text = str(self.SOMA)
			self.CHECKER=0
		else:
			self.POPUP.dismiss()

	def DISMISS(self, instance):
		if self.CHECKER == 1:
			self.POPUP.dismiss()
			self.SOMA=0.0
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				OVO.E[x]=0.0
		else:
			self.POPUP.dismiss()

	def WRITER(self, instance):
		if self.CHECKER == 1:
			self.POPUP.dismiss()
		else:
			self.LABEL.text = ''
			self.POPUP.dismiss()
			self.remove_widget(self.LABEL)
			self.add_widget(self.ids.GL)

		DATA._C[NOME]=0
		P=open(D)
		PR=P.read()
		PS=re.sub('_C={.*}', '_C={}'.format(DATA._C), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P1.close()
		P.close()

		H=getattr(DATA, DATA._W)
		H.append(self.O)
		P=open(D)
		PR=P.read()
		PS=re.sub('{}=\[.*\]'.format(DATA._W), '{}={}'.format(DATA._W, H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		CARGA=getattr(DATA, '_CARGA')

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if x in self.O:
				A=CARGA[x]-self.O[x]
				CARGA[x]=A

		P=open(D)
		PR=P.read()
		PS=re.sub('_CARGA={.*}', '_CARGA={}'.format(CARGA), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P1.close()
		P.close()

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				OVO.E[x]=0.0

		self.manager.current='menu'

class Output(Screen):

	E=None
	I=None
	S=None

	def on_pre_enter(self, *args):
		if DATA._W:
			Output.S=getattr(DATA, DATA._W)
		B=self.ids.EDIT
		O=self.ids.outspin
		S_LIST=list()
		if O.text!='':
			O.text=''
			self.ids.UN.text='Unidade'
			self.ids.DIA.text=''
			B.text=''
			B.background_color=(0, 0, 0, 1)
			for x in L:
				self.ids[x].text=''
		try:
			if DATA._C:
				S_LIST.append('CARGA')
				self.ids.DIA.text=str.replace(str.strip(DATA._W, 'H'), '_', '/')
				for x in Output.S:
					if DATA._C.get(x['CLIENTE'])==0:
						S_LIST.append(x['CLIENTE'])
			O.values=S_LIST
		except:
			pass

	def SELECT(self):
		ST=self.ids.outspin.text
		if ST=='':
			return 0
		elif ST=='CARGA':
			self.ids.UN.text='Caixa'
		else:
			self.ids.UN.text='Dúzia'
		B=self.ids.EDIT
		for x in range(len(Output.S)):
			if Output.S[x]['CLIENTE']==ST:
				I=x
		Output.E=Output.S[I]
		Output.I=I
		B.text='EDITAR'
		B.background_color=(0.8, 0, 0, 1)
		for x in L:
			if x in Output.S[I]:
				self.ids[x].text=str(Output.S[I][x])
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

	CHECKER=1
	LABEL=Label(size_hint=(1, 0.45), pos_hint={'top':0.95}, font_size=60)
	TEXTFOCUS=None
	POPUP=Popup()
	O=None
	SOMA=0.0

	def on_pre_enter(self, *args):
		self.CHECKER=1
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
		FILL('t7', 'BRMD')
		FILL('t8', 'VRMD')
		FILLPILAS('p1', 'BRT1_DZ', 'V1')
		FILLPILAS('p2', 'VRT1_DZ', 'V2')
		FILLPILAS('p3', 'BRT2_DZ', 'V3')
		FILLPILAS('p4', 'BRT3_DZ', 'V4')
		FILLPILAS('p5', 'BRDZ_DZ', 'V5')
		FILLPILAS('p6', 'VRDZ_DZ', 'V6')
		FILLPILAS('p7', 'BRMD_DZ', 'V7')
		FILLPILAS('p8', 'VRMD_DZ', 'V8')
		self.ids['NCL'].text='CLIENTE: {}'.format(NOME)

		Editar.TEXTFOCUS='t1'

		for x in range(1,9):
			if NOME=='CARGA':
				self.ids['UN'+str(x)].text='CX'
			else:
				self.ids['UN'+str(x)].text='DZ'

	def FOCUS(self, IDS='t1'):
		Editar.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		if self.CHECKER == 1:
			self.ids[Editar.TEXTFOCUS].text += INSERT
		else:
			self.LABEL.text += INSERT

	def BACKSPACE(self):
		if self.CHECKER == 1:
			self.ids[Editar.TEXTFOCUS].text = ''
		else:
			self.LABEL.text = self.LABEL.text[:len(self.LABEL.text)-1]

	def MEIA(self):
		TEXT=self.ids[Editar.TEXTFOCUS].text
		if TEXT!='':
			FLT=float(self.ids[Editar.TEXTFOCUS].text)
			self.ids[Editar.TEXTFOCUS].text = str(FLT+2.5)
		else:
			self.ids[Editar.TEXTFOCUS].text += '2.5'

	def OK(self):

		global BRT1_VALOR
		global VRT1_VALOR
		global BRT2_VALOR
		global BRT3_VALOR
		global BRDZ_VALOR
		global VRDZ_VALOR
		global BRMD_VALOR
		global VRMD_VALOR

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
		BRMD_VALOR=self.ids.p7.text
		VRMD_VALOR=self.ids.p8.text

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
			BRMD(BMD)
		if VMD!='':
			VRMD(VMD)

		if self.CHECKER == 1:
			self.SOMA=0.0
			self.O=dict()
			self.O['CLIENTE']=NOME
			if NOME == 'CARGA':
				H=getattr(DATA, DATA._W)
				self.O['WEEK']=H[0]['WEEK']
				for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
					if x == 'BRT1':
						self.O[x+'_DZ']=float(BRT1_VALOR)
					if x == 'VRT1':
						self.O[x+'_DZ']=float(VRT1_VALOR)
					if x == 'BRT2':
						self.O[x+'_DZ']=float(BRT2_VALOR)
					if x == 'BRT3':
						self.O[x+'_DZ']=float(BRT3_VALOR)
					if x == 'BRDZ':
						self.O[x+'_DZ']=float(BRDZ_VALOR)
					if x == 'VRDZ':
						self.O[x+'_DZ']=float(VRDZ_VALOR)
					if x == 'BRMD':
						self.O[x+'_DZ']=float(BRMD_VALOR)
					if x == 'VRMD':
						self.O[x+'_DZ']=float(VRMD_VALOR)
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if 0.0!=OVO.E[x]:
					self.SOMA+=OVO.E_VLR[x+'_VLR']
					self.O[x]=OVO.E[x]
					self.O[x+'_DZ']=OVO.E_DZ[x+'_DZ']
					self.O[x+'_VLR']=OVO.E_VLR[x+'_VLR']
			self.O['TOTAL']=self.SOMA
		else:
			self.O=dict()
			self.O['CLIENTE']=NOME
			if NOME == 'CARGA':
				H=getattr(DATA, DATA._W)
				self.O['WEEK']=H[0]['WEEK']
				for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
					if x == 'BRT1':
						self.O[x+'_DZ']=float(BRT1_VALOR)
					if x == 'VRT1':
						self.O[x+'_DZ']=float(VRT1_VALOR)
					if x == 'BRT2':
						self.O[x+'_DZ']=float(BRT2_VALOR)
					if x == 'BRT3':
						self.O[x+'_DZ']=float(BRT3_VALOR)
					if x == 'BRDZ':
						self.O[x+'_DZ']=float(BRDZ_VALOR)
					if x == 'VRDZ':
						self.O[x+'_DZ']=float(VRDZ_VALOR)
					if x == 'BRMD':
						self.O[x+'_DZ']=float(BRMD_VALOR)
					if x == 'VRMD':
						self.O[x+'_DZ']=float(VRMD_VALOR)
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if 0.0!=OVO.E[x]:
					self.O[x]=OVO.E[x]
					self.O[x+'_DZ']=OVO.E_DZ[x+'_DZ']
					self.O[x+'_VLR']=OVO.E_VLR[x+'_VLR']
			self.SOMA=str(float(self.LABEL.text))
			self.O['TOTAL']=float(self.LABEL.text)

		BX=BoxLayout(orientation='vertical')
		BXT=BoxLayout(size_hint=(1, 0.3))
		BT1=Button(text='Sim', background_color=(0, 0.8, 0, 1))
		BT2=Button(text='Trocar', background_color=(0, 0, 1, 1))
		BT3=Button(text='Não', background_color=(0.8, 0, 0, 1))
		BT1.bind(on_press=self.WRITER)
		BT2.bind(on_press=self.DESC)
		BT3.bind(on_press=self.DISMISS)
		BXT.add_widget(BT1)
		BXT.add_widget(BT2)
		BXT.add_widget(BT3)
		BX.add_widget(Label(text='R$ {}'.format(self.SOMA), size_hint=(1, 0.7), pos_hint={'top':1}, font_size=40))
		BX.add_widget(BXT)
		self.POPUP.title='CONFIRMAÇÃO DO VALOR'
		self.POPUP.content=BX
		self.POPUP.size_hint=(0.8, 0.6)
		self.POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
		self.POPUP.auto_dismiss=False
		self.POPUP.open()

	def DESC(self, instance):
		if self.CHECKER == 1:
			self.remove_widget(self.ids.GL)
			self.add_widget(self.LABEL)
			self.POPUP.dismiss()
			self.LABEL.text += str(self.SOMA)
			self.CHECKER=0
		else:
			self.POPUP.dismiss()

	def DISMISS(self, instance):
		if self.CHECKER == 1:
			self.POPUP.dismiss()
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				OVO.E[x]=0.0
		else:
			self.POPUP.dismiss()

	def WRITER(self, instance):
		if self.CHECKER == 1:
			self.POPUP.dismiss()
		else:
			self.LABEL.text = ''
			self.POPUP.dismiss()
			self.remove_widget(self.LABEL)
			self.add_widget(self.ids.GL)

		H=getattr(DATA, DATA._W)

		CARGA=getattr(DATA, '_CARGA')

		if NOME == 'CARGA':
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if x in self.O:
					A=CARGA[x]+(self.O[x]*30)
					if x in H[Output.I]:
						CARGA[x]=A-(H[Output.I][x]*30)
					else:
						CARGA[x]=A
		else:
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if x in self.O:
					if x in H[Output.I]:
						A=CARGA[x]+H[Output.I][x]
						CARGA[x]=A-self.O[x]
					else:
						CARGA[x]=CARGA[x]-self.O[x]
				elif x in H[Output.I]:
					CARGA[x]=CARGA[x]+H[Output.I][x]

		H.pop(Output.I)
		H.insert(Output.I, self.O)
		P=open(D)
		PR=P.read()
		PS=re.sub('{}=\[.*\]'.format(DATA._W), '{}={}'.format(DATA._W, H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		P=open(D)
		PR=P.read()
		PS=re.sub('_CARGA={.*}', '_CARGA={}'.format(CARGA), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P1.close()
		P.close()

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				OVO.E[x]=0.0

		self.manager.current='menu'

class HistSel(Screen):

	D=None
	POPUP=Popup()

	def on_pre_enter(self, *args):
		reload(DATA)
		H=list()
		if DATA._H:
			for x in DATA._H:
				X=str.strip(x, 'H')
				S=str.replace(X, '_', '/')
				X=str.split(S, '/')
				DA=int(X[0])
				M=int(X[1])
				Y=int(X[2])
				if date.weekday(date(Y, M, DA))==1:
					X='TER - {}'.format(S)
				elif date.weekday(date(Y, M, DA))==2:
					X='QUA - {}'.format(S)
				else:
					X='QUI - {}'.format(S)
				H.append(X)
			self.ids.hspin.text=H[0]
			self.ids.hspin.values=H

	def HSEL(self):
		if self.ids.hspin.text!='':
			if re.search('TER', self.ids.hspin.text):
				X=self.ids.hspin.text.strip('TER - ')
			elif re.search('QUA', self.ids.hspin.text):
				X=self.ids.hspin.text.strip('QUA - ')
			elif re.search('QUI', self.ids.hspin.text):
				X=self.ids.hspin.text.strip('QUI - ')
			HistSel.D=X
			self.manager.current='history'

	def CLEAR(self):
		BX=BoxLayout(orientation='vertical')
		BXT=BoxLayout(size_hint=(1, 0.3))
		BT1=Button(text='Sim', background_color=(0, 0.8, 0, 1))
		BT2=Button(text='Não', background_color=(0.8, 0, 0, 1))
		BT1.bind(on_press=self.KILL)
		BT2.bind(on_press=self.POPUP.dismiss)
		BXT.add_widget(BT1)
		BXT.add_widget(BT2)
		BX.add_widget(Label(text='Deseja excluir \'{}\'?'.format(self.ids.hspin.text), size_hint=(1, 0.7), pos_hint={'top':1}))
		BX.add_widget(BXT)
		self.POPUP.title='LIMPEZA DO HISTÓRICO'
		self.POPUP.content=BX
		self.POPUP.size_hint=(0.8, 0.5)
		self.POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
		self.POPUP.auto_dismiss=False
		self.POPUP.open()

	def KILL(self, instance):
		self.POPUP.dismiss()
		G='H'+str.replace(self.ids.hspin.text, '/', '_')
		R=getattr(DATA, G)
		DATA._H.remove(G)
		P=open(D)
		PR=P.read()
		PS=re.sub('_H=\[.*\]', '_H={}'.format(DATA._H), PR)
		PS1=re.sub('{}=\[.*\]'.format(G), '', PS)
		P1=open(D, 'w')
		P1.write(PS1)
		P1.close()
		P.close()
		reload(DATA)
		self.ids.hspin.text=''
		self.ids.hspin.values=''
		H=list()
		if DATA._H:
			for x in DATA._H:
				X=str.strip(x, 'H')
				S=str.replace(X, '_', '/')
				H.append(S)
			self.ids.hspin.text=H[0]
			self.ids.hspin.values=H

class History(Screen):

	L=None
	H=None

	def on_pre_enter(self, *args):
		self.ids.hhspin.text=''
		for x in L:
			self.ids[x].text=''
		self.ids.UN.text='Unidade'
		self.ids.DIA.text=HistSel.D
		History.H=getattr(DATA, 'H'+str.replace(HistSel.D, '/', '_'))
		History.L=list()
		for x in History.H:
			History.L.append(x['CLIENTE'])
		self.ids.hhspin.values=History.L

	def SEL(self):

		HT=self.ids.hhspin.text
		I=History.L.index(HT)
		if HT=='CARGA':
			self.ids.UN.text='Caixa'
		else:
			self.ids.UN.text='Dúzia'
		for x in L:
			try:
				self.ids[x].text=str(History.H[I][x])
			except:
				self.ids[x].text='-'

class Extrato(Screen):

	POPUP=Popup()
	L=None
	SL=0.0

	def on_pre_enter(self, *args):
		self.L=None
		self.SL=0.0
		reload(DATA)
		H=list()
		if DATA._H:
			for x in DATA._H:
				X=str.strip(x, 'H')
				S=str.replace(X, '_', '/')
				H.append(S)
			self.ids.ESPIN.text=H[0]
			self.ids.ESPIN.values=H

	def EXT(self):

		SOMA=0.0
		D1=0.0
		D2=0.0
		D3=0.0
		D4=0.0
		D5=0.0
		D6=0.0
		D7=0.0
		D8=0.0
		T1=0.0
		T2=0.0
		T3=0.0
		T4=0.0
		T5=0.0
		T6=0.0
		T7=0.0
		T8=0.0

		try:
			H=getattr(DATA, 'H'+str.replace(self.ids.ESPIN.text, '/', '_'))
			O='EXTRATO DIA {}\n'.format(self.ids.ESPIN.text)
			for x in H:
				O+='--------------------------------------------------------------------------'
				if x['CLIENTE']=='CARGA':
					O+='\n--------------------------------------------------------------------------\nCARGA\n'
					for y in L1:
						if y in x:
							O+='{}: {}\t\tPREÇO: R$ {}\t\tSUBTOTAL: R$ {}\n'.format(y,x[y],x[y+'_DZ'],x[y+'_VLR'])
					O+='TOTAL: R$ {}\n'.format(x['TOTAL'])
					SOMACARGA=x['TOTAL']
					O+='--------------------------------------------------------------------------\n'
				else:
					O+='\n{}\n'.format(x['CLIENTE'])
					for y in L1:
						if y in x:
							O+='{}: {}\t\tPREÇO: R$ {}\t\tSUBTOTAL: R$ {}\n'.format(y,x[y],x[y+'_DZ'],x[y+'_VLR'])
							if y=='BRT1':
								D1+=x[y]
								T1+=x[y+'_VLR']
							elif y=='VRT1':
								D2+=x[y]
								T2+=x[y+'_VLR']
							elif y=='BRT2':
								D3+=x[y]
								T3+=x[y+'_VLR']
							elif y=='BRT3':
								D4+=x[y]
								T4+=x[y+'_VLR']
							elif y=='BRDZ':
								D5+=x[y]
								T5+=x[y+'_VLR']
							elif y=='VRDZ':
								D6+=x[y]
								T6+=x[y+'_VLR']
							elif y=='BRMD':
								D7+=x[y]
								T7+=x[y+'_VLR']
							elif y=='VRMD':
								D8+=x[y]
								T8+=x[y+'_VLR']
					O+='TOTAL: R$ {}\n'.format(x['TOTAL'])
					SOMA+=x['TOTAL']
			O+='--------------------------------------------------------------------------\n'
			O+='--------------------------------------------------------------------------\nBALANÇO BRUTO\n'

			def LP(X, Y, Z):
				CX=round(Y/30, 2)
				CP=round(CX*float(H[0][X+'_DZ']), 2)
				self.L='{}: {} cx\t\t\tCOMPRADO: R$ {}\nLUCRO: R$ {}\t\t\tVENDIDO: R$ {}\n'.format(X, CX, CP, round(Z-CP, 2), Z)
				self.SL+=round(Z-CP, 2)
				self.L+='--------------------------------------------------------------------------\n'

			if T1 != 0.0:
				LP('BRT1', D1, T1)
				O+=self.L
			if T2 != 0.0:
				LP('VRT1', D2, T2)
				O+=self.L
			if T3 != 0.0:
				LP('BRT2', D3, T3)
				O+=self.L
			if T4 != 0.0:
				LP('BRT3', D4, T4)
				O+=self.L
			if T5 != 0.0:
				LP('BRDZ', D5, T5)
				O+=self.L
			if T6 != 0.0:
				LP('VRDZ', D6, T6)
				O+=self.L
			if T7 != 0.0:
				LP('BRMD', D7, T7)
				O+=self.L
			if T8 != 0.0:
				LP('VRMD', D8, T8)
				O+=self.L

			O+='LUCRO BRUTO: R$ {}\n'.format(self.SL)
			O+='--------------------------------------------------------------------------\n'
			O+='--------------------------------------------------------------------------\nBALANÇO LÍQUIDO\n'
			O+='TOTAL COMPRADO: R$ {}\nTOTAL VENDIDO: R$ {}\n--------------------------------------------------------------------------\nLUCRO LÍQUIDO: R$ {}'.format(SOMACARGA, SOMA, round(SOMA-SOMACARGA, 2))
			O+='\n--------------------------------------------------------------------------'

			P=open('EXTRATO{}.txt'.format(str.replace(self.ids.ESPIN.text, '/', '')), 'w')
			P.write(O)
			P.close()

			if DATA._W and 'H'+str.replace(self.ids.ESPIN.text, '/', '_') == DATA._W:
				BX=BoxLayout(orientation='vertical')
				BXT=BoxLayout(size_hint=(1, 0.3))
				BT1=Button(text='Sim', background_color=(0, 0.8, 0, 1))
				BT2=Button(text='Não', background_color=(0.8, 0, 0, 1))
				BT1.bind(on_press=self.CLEAN)
				BT2.bind(on_press=self.POPUP.dismiss)
				BXT.add_widget(BT1)
				BXT.add_widget(BT2)
				BX.add_widget(Label(text='Deseja encerrar a praça?', size_hint=(1, 0.7), pos_hint={'top':1}))
				BX.add_widget(BXT)
				self.POPUP.title='ENCERRAMENTO DE PRAÇA'
				self.POPUP.content=BX
				self.POPUP.size_hint=(0.8, 0.5)
				self.POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
				self.POPUP.auto_dismiss=False
				self.POPUP.open()

			self.manager.current='menu'
		except:
			pass

	def CLEAN(self, instance):
		self.POPUP.dismiss()
		P=open(D)
		PR=P.read()
		PS1=re.sub('_C={.*}', '_C={}', PR)
		PS=re.sub('_W=.*', '_W=None', PS1)
		P1=open(D, 'w')
		P1.write(PS)
		P1.close()
		P.close()
		reload(DATA)

	def EMAIL(self):
		pass

class Settings(Screen):

	POPUP=Popup()

	def PUP(self):
		if DATA._C:
			BX=BoxLayout(orientation='vertical')
			BXT=BoxLayout(size_hint=(1, 0.3))
			BT1=Button(text='Sim', background_color=(0, 0.8, 0, 1))
			BT2=Button(text='Não', background_color=(0.8, 0, 0, 1))
			BT1.bind(on_press=self.CLEAN)
			BT2.bind(on_press=self.POPUP.dismiss)
			BXT.add_widget(BT1)
			BXT.add_widget(BT2)
			BX.add_widget(Label(text='Deseja encerrar a praça?', size_hint=(1, 0.7), pos_hint={'top':1}))
			BX.add_widget(BXT)
			self.POPUP.title='ENCERRAMENTO DE PRAÇA'
			self.POPUP.content=BX
			self.POPUP.size_hint=(0.8, 0.5)
			self.POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
			self.POPUP.auto_dismiss=False
			self.POPUP.open()

	def CLEAN(self, instance):
		self.POPUP.dismiss()
		P=open(D)
		PR=P.read()
		PS1=re.sub('_C={.*}', '_C={}', PR)
		PS=re.sub('_W=.*', '_W=None', PS1)
		P1=open(D, 'w')
		P1.write(PS)
		P1.close()
		P.close()
		reload(DATA)

class Crg(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)
		SOMA=0.0
		self.ids.DIA.text=time.strftime('%d/%m/%y')
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			self.ids[x].text=str(DATA._CARGA[x])
			self.ids[x+'_C'].text=str(round(DATA._CARGA[x]/30, 2))
			SOMA+=DATA._CARGA[x]/30
		self.ids.CT.text=str(round(SOMA, 2))

class Setc(Screen):

	TEXTFOCUS=None

	def on_pre_enter(self, *args):
		self.ids.CH.state='normal'
		Setc.TEXTFOCUS='BRT1'
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			self.ids[x].text=str(DATA._CARGA[x])

	def FOCUS(self, IDS):
		Setc.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		self.ids[Setc.TEXTFOCUS].text += INSERT

	def BACKSPACE(self):
		self.ids[Setc.TEXTFOCUS].text = ''

	def CHANGER(self):
		try:
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if self.ids[x].text=='':
					if self.ids.CH.state=='down':
						self.ids.CH.state='normal'
					else:
						self.ids.CH.state='down'
					return 0
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if self.ids.CH.state=='down':
					self.ids[x].text=str(round(float(self.ids[x].text)/30, 2))
				else:
					self.ids[x].text=str(round(float(self.ids[x].text)*30, 2))
		except:
			pass


	def OK(self):
		try:
			C=dict()
			for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
				if self.ids.CH.state=='down':
					C[x]=round(float(self.ids[x].text)*30.0)
				else:
					C[x]=float(self.ids[x].text)

			P=open(D)
			PR=P.read()
			PS=re.sub('_CARGA={.*}', '_CARGA={}'.format(C), PR)
			P1=open(D, 'w')
			P1.write(PS)
			P1.close()
			P.close()

			self.manager.current='menu'
		except:
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
		self.ids.cli.text = self.ids.cli.text[:len(self.ids.cli.text)-1]

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
		PR=P.read()
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
		try:
			V=dict()
			for x in ['V1','V2','V3','V4','V5','V6','V7','V8']:
				V[x]=str(float(self.ids[x].text))
			P=open('DATA.py')
			PR=P.read()
			PS=re.sub('_V={.*}', '_V={}'.format(V), PR)
			P1=open('DATA.py', 'w')
			P1.write(PS)
			P1.close()
			P.close()
			self.manager.current='menu'
		except:
			pass

class Setcv(Screen):

	TEXTFOCUS=None

	def on_pre_enter(self, *args):
		def FILL(X):
			self.ids[X].text=DATA._CV[X]
		for x in range(1,9):
			FILL('V'+str(x))

	def FOCUS(self, IDS='t1'):
		Setcv.TEXTFOCUS=IDS

	def KEY(self, INSERT):
		self.ids[Setcv.TEXTFOCUS].text += INSERT

	def BACKSPACE(self):
		self.ids[Setcv.TEXTFOCUS].text = ''

	def MEIA(self):
		TEXT=self.ids[Setcv.TEXTFOCUS].text
		if TEXT!='':
			FLT=float(self.ids[Setcv.TEXTFOCUS].text)
			self.ids[Setcv.TEXTFOCUS].text = str(FLT+2.5)
		else:
			self.ids[Setcv.TEXTFOCUS].text += '2.5'

	def OK(self):
		try:
			V=dict()
			for x in ['V1','V2','V3','V4','V5','V6','V7','V8']:
				V[x]=str(float(self.ids[x].text))
			P=open('DATA.py')
			PR=P.read()
			PS=re.sub('_CV={.*}', '_CV={}'.format(V), PR)
			P1=open('DATA.py', 'w')
			P1.write(PS)
			P1.close()
			P.close()

			self.manager.current='menu'
		except:
			pass

class MapaApp(App):
	sm=None
	def build(self):
		self.sm=ScreenManager()
		self.sm.add_widget(Menu(name='menu'))
		self.sm.add_widget(Rota(name='rota'))
		self.sm.add_widget(Dia(name='dia'))
		self.sm.add_widget(Carga(name='carga'))
		self.sm.add_widget(Entry(name='entry'))
		self.sm.add_widget(Catcher(name='catcher'))
		self.sm.add_widget(Output(name='output'))
		self.sm.add_widget(Editar(name='editar'))
		self.sm.add_widget(HistSel(name='histsel'))
		self.sm.add_widget(History(name='history'))
		self.sm.add_widget(Extrato(name='extrato'))
		self.sm.add_widget(Settings(name='set'))
		self.sm.add_widget(Crg(name='crg'))
		self.sm.add_widget(Setc(name='setc'))
		self.sm.add_widget(PreSetr(name='presetr'))
		self.sm.add_widget(Setr(name='setr'))
		self.sm.add_widget(Setv(name='valor'))
		self.sm.add_widget(Setcv(name='setcv'))
		self.sm.current='menu'
		return self.sm

	def on_pause(self):
		return True

	def on_resume(self):
		pass

class OVO:

	E={'BRT1':0.0,'BRT2':0.0,'BRT3':0.0,'VRT1':0.0,'BRDZ':0.0,'VRDZ':0.0,'BRMD':0.0,'VRMD':0.0}

	E_DZ={'BRT1_DZ':0.0,'BRT2_DZ':0.0,'BRT3_DZ':0.0,'VRT1_DZ':0.0,'BRDZ_DZ':0.0,'VRDZ_DZ':0.0,'BRMD_DZ':0.0,'VRMD_DZ':0.0}

	E_VLR={'BRT1_VLR':0.0,'BRT2_VLR':0.0,'BRT3_VLR':0.0,'VRT1_VLR':0.0,'BRDZ_VLR':0.0,'VRDZ_VLR':0.0,'BRMD_VLR':0.0,'VRMD_VLR':0.0}

	def __init__(self, dz):
		self.dz=float(dz)

class BRT1(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(BRT1_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['BRT1']=self.dz
		OVO.E_DZ['BRT1_DZ']=self.valor
		OVO.E_VLR['BRT1_VLR']=self.soma

class BRT2(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(BRT2_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['BRT2']=self.dz
		OVO.E_DZ['BRT2_DZ']=self.valor
		OVO.E_VLR['BRT2_VLR']=self.soma

class BRT3(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(BRT3_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['BRT3']=self.dz
		OVO.E_DZ['BRT3_DZ']=self.valor
		OVO.E_VLR['BRT3_VLR']=self.soma

class VRT1(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(VRT1_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['VRT1']=self.dz
		OVO.E_DZ['VRT1_DZ']=self.valor
		OVO.E_VLR['VRT1_VLR']=self.soma

class BRDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(BRDZ_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['BRDZ']=self.dz
		OVO.E_DZ['BRDZ_DZ']=self.valor
		OVO.E_VLR['BRDZ_VLR']=self.soma

class VRDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(VRDZ_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['VRDZ']=self.dz
		OVO.E_DZ['VRDZ_DZ']=self.valor
		OVO.E_VLR['VRDZ_VLR']=self.soma

class BRMD(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(BRMD_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['BRMD']=self.dz
		OVO.E_DZ['BRMD_DZ']=self.valor
		OVO.E_VLR['BRMD_VLR']=self.soma

class VRMD(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=round(float(VRMD_VALOR), 1)
		self.soma=round(self.valor*self.dz,2)
		OVO.E['VRMD']=self.dz
		OVO.E_DZ['VRMD_DZ']=self.valor
		OVO.E_VLR['VRMD_VLR']=self.soma

if __name__ == '__main__':
	MapaApp().run()
