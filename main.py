#TESTE2

import DATA
import kivy
import os
import os.path
import re
import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import FocusBehavior
from kivy.base import runTouchApp

from importlib import reload

## ADICIONAR RESET DE VALORES EM WRITER()

DIA=time.strftime('%d/%m/%y')
CWD=os.getcwd()
PLAN='PLANILHA.py'
_PL_LIST=['BRT1', 'BRT1_DZ', 'BRT1_VLR', 'BRT2', 'BRT2_DZ', 'BRT2_VLR', 'BRT3', 'BRT3_DZ', 'BRT3_VLR',\
		'VRT1', 'VRT1_DZ', 'VRT1_VLR', 'BRDZ', 'BRDZ_DZ', 'BRDZ_VLR', 'VRDZ', 'VRDZ_DZ', 'VRDZ_VLR',\
		'BRMDZ', 'BRMDZ_DZ', 'BRMDZ_VLR', 'VRMDZ', 'VRMDZ_DZ', 'VRMDZ_VLR','TOTAL']

FocusBehavior.keyboard_mode='managed'

class Menu(Screen):

	def on_pre_enter(self, *args):
		if os.path.isfile(CWD+'/'+PLAN):
			global PLANILHA
			import PLANILHA
			reload(PLANILHA)
			reload(DATA)

	def CHECKER(self):
		if os.path.isfile(CWD+'/'+PLAN):
			self.manager.current='entry'
		else:
			self.manager.current='rota'

class Rota(Screen):

	LAUDARE=None

	def SB(self, ROTA):
		K='_DIA=\'{}\'\n\n_R=0\n\n_C=[\n'.format(DIA)
		LEN_DATA=len(ROTA)
		for x in range(LEN_DATA):
			K+='\'{}'.format(ROTA[x])
			K+='=1\',\n'
		K+='\'_END\'\n]\n\n'
		P=open(PLAN, 'w')
		P.write(K)
		P.close()

	def RS_T(self):
		Rota.LAUDARE=0
		self.SB(DATA._TERCA)
		self.manager.current='entry'
	def RS_QUA(self):
		Rota.LAUDARE=1
		self.SB(DATA._QUARTA)
		self.manager.current='entry'
	def RS_QUI(self):
		Rota.LAUDARE=2
		self.SB(DATA._QUINTA)
		self.manager.current='entry'

class Entry(Screen):

	NOME=None
	INSERT=None
	OUTRO=None

	def on_pre_enter(self, *args):
		if os.path.isfile(CWD+'/'+PLAN):
			global PLANILHA
			import PLANILHA
			reload(PLANILHA)
			reload(DATA)
		global SP
		self.ids.inpt0.text=''
		SP=self.ids.spinner
		SP.text='OUTRO'
		LEN_C=len(PLANILHA._C)
		for x in range(LEN_C-1):
			S=PLANILHA._C[x]
			if '1' in S:
				SP.text=str.rstrip(S, '=1')
				break
		if Rota.LAUDARE==0:
			G=getattr(DATA, '_TERCA')
			if os.path.isfile(CWD+'/'+PLAN):
				R=list()
				for x in G:
					if x+'=1' in PLANILHA._C:
						R.append(x)
				R.insert(0, 'OUTRO')
				SP.values=R
			else:
				G.insert(0, 'OUTRO')
				SP.values=G
		elif Rota.LAUDARE==1:
			G=getattr(DATA, '_QUARTA')
			if os.path.isfile(CWD+'/'+PLAN):
				R=list()
				for x in G:
					if x+'=1' in PLANILHA._C:
						R.append(x)
				R.insert(0, 'OUTRO')
				SP.values=R
			else:
				G.insert(0, 'OUTRO')
				SP.values=G
		elif Rota.LAUDARE==2:
			G=getattr(DATA, '_QUINTA')
			if os.path.isfile(CWD+'/'+PLAN):
				R=list()
				for x in G:
					if x+'=1' in PLANILHA._C:
						R.append(x)
				R.insert(0, 'OUTRO')
				SP.values=R
			else:
				G.insert(0, 'OUTRO')
				SP.values=G
		elif os.path.isfile(CWD+'/'+PLAN):
			if PLANILHA._R==0:
				G=getattr(DATA, '_TERCA')
				R=list()
				for x in G:
					if x+'=1' in PLANILHA._C:
						R.append(x)
				R.insert(0, 'OUTRO')
				SP.values=R
			elif PLANILHA._R==1:
				G=getattr(DATA, '_QUARTA')
				R=list()
				for x in G:
					if x+'=1' in PLANILHA._C:
						R.append(x)
				R.insert(0, 'OUTRO')
				SP.values=R
			elif PLANILHA._R==2:
				G=getattr(DATA, '_QUINTA')
				R=list()
				for x in G:
					if x+'=1' in PLANILHA._C:
						R.append(x)
				R.insert(0, 'OUTRO')
				SP.values=R

	def NOME_TEXT(self):
		if SP.text=='OUTRO':
			Entry.NOME=self.ids.inpt0.text
			Entry.OUTRO=0
			if Entry.NOME=='':
				self.popup=Popup(title='ERRO: NOME EM BRANCO!', content=Label(text='Insira o nome do cliente.'),\
							size_hint=(0.7, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5})
				self.popup.open()
				return 0
			elif Entry.NOME+'=0' in PLANILHA._C:
				self.popup=Popup(title='ERRO: NOME EXISTENTE!', content=Label(text='Escolha outro nome.'),\
							size_hint=(0.7, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5})
				self.popup.open()
				return 0
		else:
			Entry.NOME=SP.text

		self.manager.current='catcher'

	def KEY(self, INSERT):
		self.ids['inpt0'].text += INSERT

	def BACKSPACE(self):
		self.ids.inpt0.text = ''

class Catcher(Screen):

	TEXTFOCUS=None
	INSERT=None
	BRT1=None
	BRT2=None
	BRT3=None
	VRT1=None
	BRDZ=None
	VRDZ=None
	BRMDZ=None
	VRMDZ=None
	BRT1_VALOR=DATA._V['V1']
	BRT2_VALOR=DATA._V['V2']
	BRT3_VALOR=DATA._V['V3']
	VRT1_VALOR=DATA._V['V4']
	BRDZ_VALOR=DATA._V['V5']
	VRDZ_VALOR=DATA._V['V6']
	BRMDZ_VALOR=DATA._V['V7']
	VRMDZ_VALOR=DATA._V['V8']

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
		self.ids['inp2'].text=DATA._V['V4']
		self.ids['inp3'].text=DATA._V['V2']
		self.ids['inp4'].text=DATA._V['V3']
		self.ids['inp5'].text=DATA._V['V5']
		self.ids['inp6'].text=DATA._V['V6']
		self.ids['inp7'].text=DATA._V['V7']
		self.ids['inp8'].text=DATA._V['V8']
		self.ids['NC'].text='CLIENTE: {}'.format(Entry.NOME)

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
		Catcher.BRT1=self.ids.inpt1.text
		Catcher.VRT1=self.ids.inpt2.text
		Catcher.BRT2=self.ids.inpt3.text
		Catcher.BRT3=self.ids.inpt4.text
		Catcher.BRT1_VALOR=self.ids.inp1.text
		Catcher.VRT1_VALOR=self.ids.inp2.text
		Catcher.BRT2_VALOR=self.ids.inp3.text
		Catcher.BRT3_VALOR=self.ids.inp4.text
		Catcher.BRDZ=self.ids.inpt5.text
		Catcher.VRDZ=self.ids.inpt6.text
		Catcher.BRMDZ=self.ids.inpt7.text
		Catcher.VRMDZ=self.ids.inpt8.text
		Catcher.BRDZ_VALOR=self.ids.inp5.text
		Catcher.VRDZ_VALOR=self.ids.inp6.text
		Catcher.BRMDZ_VALOR=self.ids.inp7.text
		Catcher.VRMDZ_VALOR=self.ids.inp8.text
		START()
		self.manager.current='menu'

class Output(Screen):

	def on_pre_enter(self, *args):
		if os.path.isfile(CWD+'/'+PLAN):
			global SO
			global SO_LIST
			SO=self.ids.outspin
			SO_LIST=list()
			LEN_C=len(PLANILHA._C)
			if SO.text!='':
				SO.text=''
				self.ids.DIA.text=''
				BTN0.text=''
				BTN0.background_color=(0, 0, 0, 1)
				for x in _PL_LIST:
					self.ids[x].text=''
			for x in range(LEN_C):
				if str.endswith(PLANILHA._C[x], '0'):
					SO_LIST.append(str.rstrip(PLANILHA._C[x], '=0'))
			SO.values=SO_LIST
		else:
			self.manager.current='menu'

	def SELECT(self):
		global BTN0
		S=getattr(PLANILHA, SO.text)
		BTN0=self.ids.EDIT
		self.ids.DIA.text=PLANILHA._DIA
		BTN0.text='EDITAR'
		BTN0.background_color=(0.8, 0, 0, 1)
		for x in _PL_LIST:
			if x in S:
				self.ids[x].text=str(S[x])
			else:
				self.ids[x].text='-'

	def EDITING(self):
		if self.ids.outspin.text=='':
			pass
		else:
			Entry.NOME=SO.text
			self.manager.current='editar'

class Editar(Screen):

	MODO=None
	TEXTFOCUS=None
	INSERT=None

	def on_pre_enter(self, *args):
		self.ids['t1'].text=''
		self.ids['t2'].text=''
		self.ids['t3'].text=''
		self.ids['t4'].text=''
		self.ids['t5'].text=''
		self.ids['t6'].text=''
		self.ids['t7'].text=''
		self.ids['t8'].text=''
		self.ids['p1'].text='4.0'
		self.ids['p2'].text='4.4'
		self.ids['p3'].text='3.6'
		self.ids['p4'].text='3.2'
		self.ids['p5'].text='4.0'
		self.ids['p6'].text='4.4'
		self.ids['p7'].text='2.0'
		self.ids['p8'].text='2.2'
		self.ids['NCL'].text='CLIENTE: {}'.format(SO.text)
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
		Editar.MODO=0
		Catcher.BRT1=self.ids.t1.text
		Catcher.VRT1=self.ids.t2.text
		Catcher.BRT2=self.ids.t3.text
		Catcher.BRT3=self.ids.t4.text
		Catcher.BRT1_VALOR=self.ids.p1.text
		Catcher.VRT1_VALOR=self.ids.p2.text
		Catcher.BRT2_VALOR=self.ids.p3.text
		Catcher.BRT3_VALOR=self.ids.p4.text
		Catcher.BRDZ=self.ids.t5.text
		Catcher.VRDZ=self.ids.t6.text
		Catcher.BRMDZ=self.ids.t7.text
		Catcher.VRMDZ=self.ids.t8.text
		Catcher.BRDZ_VALOR=self.ids.p5.text
		Catcher.VRDZ_VALOR=self.ids.p6.text
		Catcher.BRMDZ_VALOR=self.ids.p7.text
		Catcher.VRMDZ_VALOR=self.ids.p8.text
		START()
		self.manager.current='menu'

class Settings(Screen):
	pass

class Setv(Screen):

	TEXTFOCUS=None
	INSERT=None

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
		VDICT=dict()
		for x in ['V1','V2','V3','V4','V5','V6','V7','V8']:
			VDICT[x]=self.ids[x].text
		P0=open('DATA.py')
		PR=P0.read()
		PSUB=re.sub('_V={.*}', '_V={}'.format(VDICT), PR)
		P1=open('DATA.py', 'w')
		P1.write(PSUB)
		P1.close()
		P0.close()
		self.manager.current='menu'

class MapaApp(App):
	sm=None
	def build(self):
		self.sm=ScreenManager()
		self.sm.add_widget(Menu(name='menu'))
		self.sm.add_widget(Rota(name='rota'))
		self.sm.add_widget(Entry(name='entry'))
		self.sm.add_widget(Catcher(name='catcher'))
		self.sm.add_widget(Output(name='output'))
		self.sm.add_widget(Editar(name='editar'))
		self.sm.add_widget(Settings(name='set'))
		self.sm.add_widget(Setv(name='valor'))
		self.sm.current='menu'
		return self.sm

## MAIN.PY

class OVO:

	E={
'BRT1':0.0,
'BRT2':0.0,
'BRT3':0.0,
'VRT1':0.0,
'BRDZ':0.0,
'VRDZ':0.0,
'BRMDZ':0.0,
'VRMDZ':0.0
}

	E_DZ={
'BRT1_DZ':0.0,
'BRT2_DZ':0.0,
'BRT3_DZ':0.0,
'VRT1_DZ':0.0,
'BRDZ_DZ':0.0,
'VRDZ_DZ':0.0,
'BRMDZ_DZ':0.0,
'VRMDZ_DZ':0.0
}

	E_VLR={
'BRT1_VLR':0.0,
'BRT2_VLR':0.0,
'BRT3_VLR':0.0,
'VRT1_VLR':0.0,
'BRDZ_VLR':0.0,
'VRDZ_VLR':0.0,
'BRMDZ_VLR':0.0,
'VRMDZ_VLR':0.0
}

	def __init__(self, dz):
		self.dz=float(dz)

class BRT1(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.BRT1_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRT1']=self.dz
		OVO.E_DZ['BRT1_DZ']=self.valor
		OVO.E_VLR['BRT1_VLR']=self.soma

class BRT2(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.BRT2_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRT2']=self.dz
		OVO.E_DZ['BRT2_DZ']=self.valor
		OVO.E_VLR['BRT2_VLR']=self.soma

class BRT3(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.BRT3_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRT3']=self.dz
		OVO.E_DZ['BRT3_DZ']=self.valor
		OVO.E_VLR['BRT3_VLR']=self.soma

class VRT1(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.VRT1_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['VRT1']=self.dz
		OVO.E_DZ['VRT1_DZ']=self.valor
		OVO.E_VLR['VRT1_VLR']=self.soma

class BRDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.BRDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRDZ']=self.dz
		OVO.E_DZ['BRDZ_DZ']=self.valor
		OVO.E_VLR['BRDZ_VLR']=self.soma

class VRDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.VRDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['VRDZ']=self.dz
		OVO.E_DZ['VRDZ_DZ']=self.valor
		OVO.E_VLR['VRDZ_VLR']=self.soma

class BRMDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.BRMDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRMDZ']=self.dz
		OVO.E_DZ['BRMDZ_DZ']=self.valor
		OVO.E_VLR['BRMDZ_VLR']=self.soma

class VRMDZ(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(Catcher.VRMDZ_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['VRMDZ']=self.dz
		OVO.E_DZ['VRMDZ_DZ']=self.valor
		OVO.E_VLR['VRMDZ_VLR']=self.soma

def START():
	if Catcher.BRT1!='':
		BRT1(Catcher.BRT1)
	if Catcher.BRT2!='':
		BRT2(Catcher.BRT2)
	if Catcher.BRT3!='':
		BRT3(Catcher.BRT3)
	if Catcher.VRT1!='':
		VRT1(Catcher.VRT1)
	if Catcher.BRDZ!='':
		BRDZ(Catcher.BRDZ)
	if Catcher.VRDZ!='':
		VRDZ(Catcher.VRDZ)
	if Catcher.BRMDZ!='':
		BRMDZ(Catcher.BRMDZ)
	if Catcher.VRMDZ!='':
		VRMDZ(Catcher.VRMDZ)

	WRITER()

def WRITER(SOMA=0.0):

	DICT=dict()
	for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
		if 0.0!=OVO.E[x]:
			SOMA+=OVO.E_VLR[x+'_VLR']
			DICT[x]=OVO.E[x]
			DICT[x+'_DZ']=OVO.E_DZ[x+'_DZ']
			DICT[x+'_VLR']=OVO.E_VLR[x+'_VLR']
	DICT['TOTAL']=(SOMA)

	if Editar.MODO==0:
		P0=open(PLAN)
		PR=P0.read()
		PSUB=re.sub('{}={}'.format(Entry.NOME, '{.*}'), '{}={}'.format(Entry.NOME, DICT), PR)
		P1=open(PLAN, 'w')
		P1.write(PSUB)
		P1.close()
		P0.close()
	else:
		W=open(PLAN, 'a')
		W.write('{}={}\n\n'.format(Entry.NOME, DICT))
		W.close()
		WRITEVALUE()

	for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMDZ','VRMDZ']:
		OVO.E[x]=0.0

def WRITEVALUE ():

	if Entry.OUTRO==0:
		P0=open(PLAN)
		PR=P0.read()
		PSUB=re.sub('\'_END\'', '\'{}=0\',\n\'_END\'\n'.format(Entry.NOME), PR)
		P1=open(PLAN, 'w')
		P1.write(PSUB)
		P1.close()
		P0.close()
	else:
		P0=open(PLAN)
		PR=P0.read()
		PSUB=re.sub('{}=1'.format(Entry.NOME), '{}=0'.format(Entry.NOME), PR)
		P1=open(PLAN, 'w')
		P1.write(PSUB)
		P1.close()
		P0.close()

if __name__ == '__main__':
	MapaApp().run()
