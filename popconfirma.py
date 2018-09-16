def PUP(self):
	BX=BoxLayout(orientation='vertical')
	GL=GridLayout(cols=4, rows=8, size_hint=(1, 0.9))
	GL.add_widget(Label(text='BRT1'))
	GL.add_widget(Label(text='R$'))
	GL.add_widget(Label(text='VRT1'))
	GL.add_widget(Label(text='R$'))
	for x in range(1,9):
		if x==3:
			GL.add_widget(Label(text='BRT2'))
			GL.add_widget(Label(text='R$'))
			GL.add_widget(Label(text='BRT3'))
			GL.add_widget(Label(text='R$'))
		elif x==5:
			GL.add_widget(Label(text='BRDZ'))
			GL.add_widget(Label(text='R$'))
			GL.add_widget(Label(text='VRDZ'))
			GL.add_widget(Label(text='R$'))
		elif x==7:
			GL.add_widget(Label(text='BRMD'))
			GL.add_widget(Label(text='R$'))
			GL.add_widget(Label(text='VRMD'))
			GL.add_widget(Label(text='R$'))
		if self.ids['inpt'+str(x)].text=='':
			GL.add_widget(Label(text='0.0'))
			GL.add_widget(Label(text=self.ids['inp'+str(x)].text))
		else:
			GL.add_widget(Label(text=self.ids['inpt'+str(x)].text))
			GL.add_widget(Label(text=self.ids['inp'+str(x)].text))
	BXT=BoxLayout(size_hint=(1, 0.1))
	BT1=Button(text='Sim', background_color=(0, 0.8, 0, 1))
	BT2=Button(text='Não', background_color=(0.8, 0, 0, 1))
	BXT.add_widget(BT1)
	BXT.add_widget(BT2)
	BX.add_widget(GL)
	BX.add_widget(BXT)
	Catcher.POPUP.title='CONFIRMAÇÃO DE LANÇAMENTO.'
	Catcher.POPUP.content=BX
	Catcher.POPUP.auto_dismiss=False
	Catcher.POPUP.size_hint=(0.9, 0.9)
	Catcher.POPUP.pos_hint={'center_x': 0.5, 'center_y': 0.5}
	Catcher.POPUP.open()
	BT1.bind(on_press=self.OK)
	BT2.bind(on_press=Catcher.POPUP.dismiss)
