import DATA
import kivy
import re
import socket
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.progressbar import ProgressBar
from kivy.base import runTouchApp
from smtplib import SMTP

if socket.gethostname()=='josley' or socket.gethostname()=='lamettrie3':
	from importlib import reload

DIAVAR=time.strftime('H%d_%m_%y')
D='DATA.py'
L=['BRT1', 'BRT1_DZ', 'BRT1_VLR', 'BRT2', 'BRT2_DZ', 'BRT2_VLR', 'BRT3', 'BRT3_DZ', 'BRT3_VLR',\
		'VRT1', 'VRT1_DZ', 'VRT1_VLR', 'BRDZ', 'BRDZ_DZ', 'BRDZ_VLR', 'VRDZ', 'VRDZ_DZ', 'VRDZ_VLR',\
		'BRMD', 'BRMD_DZ', 'BRMD_VLR', 'VRMD', 'VRMD_DZ', 'VRMD_VLR','TOTAL']
NOME=None

BRT1=''
VRT1=''
BRT2=''
BRT3=''
BRDZ=''
VRDZ=''
BRMD=''
VRMD=''
BRT1_VALOR=DATA._CV['V1']
VRT1_VALOR=DATA._CV['V2']
BRT2_VALOR=DATA._CV['V3']
BRT3_VALOR=DATA._CV['V4']
BRDZ_VALOR=DATA._CV['V5']
VRDZ_VALOR=DATA._CV['V6']
BRMD_VALOR=DATA._CV['V7']
VRMD_VALOR=DATA._CV['V8']

class Menu(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)

	def CHECKER(self):
		if DATA._C:
			self.manager.current='entry'
		else:
			self.manager.current='rota'

class Rota(Screen):

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

		H=getattr(DATA, '_H')
		H.insert(0, DIAVAR)
		P=open(D)
		PR=P.read()
		PS=re.sub('_H=\[.*\]', '_H={}'.format(H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		self.manager.current='carga'

	def RS_T(self):
		self.SB(DATA._TERCA)

	def RS_QUA(self):
		self.SB(DATA._QUARTA)

	def RS_QUI(self):
		self.SB(DATA._QUINTA)

class Carga(Screen):

	TEXTFOCUS=None
	INSERT=None

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

		C=dict()
		C['CLIENTE']='CARGA'
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if 0.0!=OVO.E[x]:
				SOMA+=OVO.E_VLR[x+'_VLR']
				C[x]=OVO.E[x]
				C[x+'_DZ']=OVO.E_DZ[x+'_DZ']
				C[x+'_VLR']=OVO.E_VLR[x+'_VLR']
		C['TOTAL']=SOMA

		W=open(D, 'a')
		W.write('\n{}=[{}]'.format(DIAVAR, C))
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

	INSERT=None
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
		B=self.ids.inpt0.text[:len(self.ids.inpt0.text)-1]
		self.ids.inpt0.text = B

class Catcher(Screen):

	TEXTFOCUS=None
	INSERT=None

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

		O=dict()
		O['CLIENTE']=NOME
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
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

		CARGA=getattr(DATA, '_CARGA')

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if x in O:
				A=CARGA[x]-O[x]
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
		try:
			for x in DATA._C['ROTA']:
				if DATA._C.get(x)==0:
					S_LIST.append(x)
			S.values=S_LIST
		except:
			pass

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
			BRMD(BMD)
		if VMD!='':
			VRMD(VMD)

		O=dict()
		O['CLIENTE']=NOME
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if 0.0!=OVO.E[x]:
				SOMA+=OVO.E_VLR[x+'_VLR']
				O[x]=OVO.E[x]
				O[x+'_DZ']=OVO.E_DZ[x+'_DZ']
				O[x+'_VLR']=OVO.E_VLR[x+'_VLR']
		O['TOTAL']=SOMA

		H=getattr(DATA, DATA._H[0])

		CARGA=getattr(DATA, '_CARGA')

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if x in H[Output.I]:
				A=CARGA[x]+H[Output.I][x]
				CARGA[x]=A

		H.pop(Output.I)
		H.insert(Output.I, O)
		P=open(D)
		PR=P.read()
		PS=re.sub('{}=\[.*\]'.format(DATA._H[0]), '{}={}'.format(DATA._H[0], H), PR)
		P1=open(D, 'w')
		P1.write(PS)
		P.close()
		P1.close()

		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			if x in O:
				A=CARGA[x]-O[x]
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

class HistSel(Screen):

	D=None

	def on_pre_enter(self, *args):
		reload(DATA)
		H=list()
		if DATA._H:
			for x in DATA._H:
				X=str.strip(x, 'H')
				S=str.replace(X, '_', '/')
				H.append(S)
			self.ids.hspin.text=H[0]
			self.ids.hspin.values=H

	def HSEL(self):
		if self.ids.hspin.text!='':
			HistSel.D=self.ids.hspin.text
			self.manager.current='history'

	def HCARGA(self):
		if self.ids.hspin.text!='':
			HistSel.D=self.ids.hspin.text
			self.manager.current='hcarga'

	def EXTRATO(self):
		if self.ids.hspin.text!='':
			G='H'+str.replace(self.ids.hspin.text, '/', '_')

			try:
				H=getattr(DATA, G)
				MSG=MIMEMultipart()
				MSG['From']='ratatoskr.sedex@yandex.com'
				MSG['To']='ggmoraes07@gmail.com'
				MSG['Subject']='Extrato {}.'.format(time.strftime('%d/%m/%y'))
				BODY='{}'.format(H)
				MSG.attach(MIMEText(BODY, 'plain'))
				YANDEX=SMTP(host='smtp.yandex.com', port=587)
				YANDEX.starttls()
				YANDEX.login('ratatoskr.sedex@yandex.com', 'lzcxthcehbgvcblq')
				TEXT=MSG.as_string()
				YANDEX.sendmail('ratatoskr.sedex@yandex.com', 'ggmoraes07@gmail.com', TEXT)
				YANDEX.quit()
				self.manager.current='menu'
			except:
				pass

			#if G==DATA._H[0]:
			#	P=open(D)
			#	PR=P.read()
			#	PS=re.sub('_C={.*}', '_C={}', PR)
			#	P1=open(D, 'w')
			#	P1.write(PS)
			#	P1.close()
			#	P.close()

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
		for x in History.H:
			if x['CLIENTE']=='CARGA':
				continue
			History.L.append(x['CLIENTE'])
		self.ids.hhspin.values=History.L

	def SEL(self):

		I=History.L.index(self.ids.hhspin.text)
		for x in L:
			try:
				self.ids[x].text=str(History.H[I][x])
			except:
				self.ids[x].text='-'

class HCarga(Screen):

	def on_pre_enter(self, *args):
		self.ids.DIA.text=HistSel.D
		H=getattr(DATA, 'H'+str.replace(HistSel.D, '/', '_'))
		for x in L:
			try:
				self.ids[x].text=str(H[0][x])
			except:
				self.ids[x].text='-'

class Settings(Screen):

	def CLEAN(self):
		pass

class Crg(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)
		SOMA=0.0
		self.ids.DIA.text=time.strftime('%d/%m/%y')
		for x in ['BRT1','BRT2','BRT3','VRT1','BRDZ','VRDZ','BRMD','VRMD']:
			self.ids[x].text=str(DATA._CARGA[x])
			self.ids[x+'_C'].text=str(DATA._CARGA[x]/30)[0:4]
			SOMA+=DATA._CARGA[x]/30
		self.ids.CT.text=str(SOMA)[0:5]

class Setc(Screen):

	INSERT=None
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
					self.ids[x].text=str(float(self.ids[x].text)/30)[0:4]
				else:
					self.ids[x].text=str(round(float(self.ids[x].text)*30))
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
		B=self.ids.cli.text[:len(self.ids.cli.text)-1]
		self.ids.cli.text = B

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
			V[x]=str(float(self.ids[x].text))
		P=open('DATA.py')
		PR=P.read()
		PS=re.sub('_V={.*}', '_V={}'.format(V), PR)
		P1=open('DATA.py', 'w')
		P1.write(PS)
		P1.close()
		P.close()
		self.manager.current='menu'

class Setcv(Screen):

	TEXTFOCUS=None
	INSERT=None

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
		self.sm.add_widget(HCarga(name='hcarga'))
		self.sm.add_widget(Settings(name='set'))
		self.sm.add_widget(Crg(name='crg'))
		self.sm.add_widget(Setc(name='setc'))
		self.sm.add_widget(PreSetr(name='presetr'))
		self.sm.add_widget(Setr(name='setr'))
		self.sm.add_widget(Setv(name='valor'))
		self.sm.add_widget(Setcv(name='setcv'))
		self.sm.current='menu'
		return self.sm

## MAIN.PY

class OVO:

	E={'BRT1':0.0,'BRT2':0.0,'BRT3':0.0,'VRT1':0.0,'BRDZ':0.0,'VRDZ':0.0,'BRMD':0.0,'VRMD':0.0}

	E_DZ={'BRT1_DZ':0.0,'BRT2_DZ':0.0,'BRT3_DZ':0.0,'VRT1_DZ':0.0,'BRDZ_DZ':0.0,'VRDZ_DZ':0.0,'BRMD_DZ':0.0,'VRMD_DZ':0.0}

	E_VLR={'BRT1_VLR':0.0,'BRT2_VLR':0.0,'BRT3_VLR':0.0,'VRT1_VLR':0.0,'BRDZ_VLR':0.0,'VRDZ_VLR':0.0,'BRMD_VLR':0.0,'VRMD_VLR':0.0}

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

class BRMD(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(BRMD_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['BRMD']=self.dz
		OVO.E_DZ['BRMD_DZ']=self.valor
		OVO.E_VLR['BRMD_VLR']=self.soma

class VRMD(OVO):
	def __init__(self, dz):
		OVO.__init__(self, dz)
		self.valor=float(VRMD_VALOR)
		self.soma=self.valor*self.dz
		OVO.E['VRMD']=self.dz
		OVO.E_DZ['VRMD_DZ']=self.valor
		OVO.E_VLR['VRMD_VLR']=self.soma


if __name__ == '__main__':
	MapaApp().run()
