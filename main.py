# -*- coding: utf-8 -*-
#!/usr/bin/python2

start = 'menu'

import DATA
import kivy
import re
import sys
import time
from datetime import date
from kivy.app import App
from kivy.base import runTouchApp, EventLoop, ExceptionHandler, ExceptionManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
from threading import Thread
from time import sleep

if sys.version_info[0] == 3:
	from importlib import reload

d = 'DATA.py'

tipos = [
	'BRT1','VRT1','BRT2',
	'BRT3','BRDZ','VRDZ',
	'BRMD','VRMD'
	]

class E(ExceptionHandler):
	def handle_exception(self, inst):
		return ExceptionManager.PASS

ExceptionManager.add_handler(E())


class Menu(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)

	def checker(self):
		if DATA._current_day:
			self.manager.current = 'entry'
		else:
			self.manager.current = 'rota'


class Rota(Screen):

	week = None

	def on_pre_enter(self, *args):
		Rota.week = None

	def day_checker(self, day_int):
		self.d = int(time.strftime('%d'))
		self.m = int(time.strftime('%m'))
		self.y = int(time.strftime('%y'))
		if date.weekday(date(self.y, self.m, self.d)) == day_int:
			if 'H{}_{}_{}'.format(self.d, self.m, self.y) in DATA._reported_list:
				call_popup('ERRO: DATA EXISTENTE', 'Já existe um registro\ncomo "{}/{}/{}".'.format(self.d, self.m, self.y))
				return 1
			else:
				Rota.week = day_int
				self.day = 'H{}_{}_{}'.format(self.d, self.m, self.y)
				Writer().day_writer(self.day)
				self.manager.current = 'catcher'
		else:
			Rota.week = day_int
			self.manager.current = 'dia'


class Dia(Screen):

	def on_pre_enter(self, *args):
		self.ids.DMY.text = 'dd/mm/yy'

	def key(self, insert):
		self.ids.DMY.text += insert

	def backspace(self):
		self.ids.DMY.text = self.ids.DMY.text[:len(self.ids.DMY.text)-1]

	def full_clear(self):
		self.ids.DMY.text = ''

	def ok(self):
		if re.search('[0-9][0-9]/[0-9][0-9]/[0-9][0-9]', self.ids.DMY.text):
			self.data_split = str.split(self.ids.DMY.text, '/')
			self.d = int(self.data_split[0])
			self.m = int(self.data_split[1])
			self.y = int(self.data_split[2])

			if self.d not in range(1, 32):
				call_popup('ERRO: DIA INEXISTENTE', 'Os dias vão de 01 a 31!')
				return 1
			elif self.m not in range(1, 13):
				call_popup('ERRO: MÊS INEXISTENTE', 'Os meses vão de 01 a 12!')
				return 1
			elif self.y not in range(1, 100):
				call_popup('ERRO: ANO INEXISTENTE', 'Os anos vão de 01 a 99!')
				return 1
			elif 'H{}_{}_{}'.format(self.d, self.m, self.y) in DATA._reported_list:
				call_popup('ERRO: DATA EXISTENTE', 'Já existe um registro\ncomo "{}/{}/{}".'.format(self.d, self.m, self.y))
				return 1
			else:
				self.day = 'H{}_{}_{}'.format(self.d, self.m, self.y)
				self.morfologia()
		else:
			call_popup('ERRO: FORMATO EQUIVOCADO', 'Exemplo: "07/03/96".')
			return 1

	def morfologia(self):
		day_name = {
			0: 'segunda', 1: 'terça', 2: 'quarta',
			3: 'quinta', 4: 'sexta', 5: 'sábado',
			6: 'domingo'
			}

		if Rota.week == date.weekday(date(self.y, self.m, self.d)):
			Writer().day_writer(self.day)
			self.manager.current = 'catcher'
		else:
			day_int = date.weekday(date(self.y, self.m, self.d))
			self.popup_confirm(day_name[Rota.week], day_name[day_int])

	def popup_confirm(self, day_name1, day_name2):
		self.popup = Popup()
		bx = BoxLayout(orientation='vertical')
		bxt = BoxLayout(size_hint=(1, 0.3))
		bt1 = Button(text='Sim', background_color=(0, 0.8, 0, 1))
		bt2 = Button(text='Não', background_color=(0.8, 0, 0, 1))
		bt1.bind(on_press=self.day_writer)
		bt2.bind(on_press=self.popup.dismiss)
		bxt.add_widget(bt1)
		bxt.add_widget(bt2)
		msg = '"{}/{}/{}" não é {}, mas {}.\n\nDeseja continuar?'.format(self.d, self.m, self.y, day_name1, day_name2)
		bx.add_widget(Label(text=msg, size_hint=(1, 0.7), pos_hint={'top':1}))
		bx.add_widget(bxt)
		self.popup.title = 'ERRO: DIA DA PRAÇA EQUIVOCADO'
		self.popup.content = bx
		self.popup.size_hint = (0.8, 0.5)
		self.popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.popup.auto_dismiss = False
		self.popup.open()

	def day_writer(self, instance):
		self.popup.dismiss()
		Writer().day_writer(self.day)
		self.manager.current = 'catcher'


class Entry(Screen):

	nome = None

	def on_pre_enter(self, *args):
		reload(DATA)
		self.ids.LINE.text = ''
		Entry.nome = None
		self.spinner_values()

	def spinner_values(self):
		self.clientes = DATA._current_route
		self.clientes.insert(0, 'OUTRO')
		self.ids.BOOK.values = self.clientes
		self.nome = self.ids.BOOK
		self.line = self.ids.LINE
		self.values = self.ids.BOOK.values
		self.line.font_size = DATA._font_size

		if len(self.clientes) > 1:
			self.nome.text = self.values[1]
		else:
			self.nome.text = self.values[0]

	def definition(self):
		if self.nome.text == 'OUTRO':
			if self.line.text == '':
				call_popup('ERRO: AUSÊNCIA DE CLIENTE', 'Insira um nome.')
				return 0
			elif self.line.text in DATA._current_route:
				call_popup('ERRO: CLIENTE EXISTENTE', 'Insira outro nome.')
				return 0
			else:
				Entry.nome = self.line.text
		elif self.line.text != '':
			call_popup('ERRO: INDEFINIÇÃO DE OPERAÇÃO', 'Selecione "OUTRO" ou\napague o texto.')
			return 0
		else:
			Entry.nome = self.nome.text

		self.manager.current = 'catcher'

	def nothing(self):
		if self.line.text != '':
			call_popup('ERRO: INDEFINIÇÃO DE OPERAÇÃO', 'Apague o texto.')
			return 1
		attr = getattr(DATA, DATA._current_day)
		attr.append({'NOME': self.nome.text, 'TOTAL': 0.0})
		self.clientes.remove('OUTRO')
		if self.nome.text in self.clientes:
			self.clientes.remove(self.nome.text)
			Writer().replace('_current_route=\[.*\]', '_current_route={}'.format(self.clientes))
			Writer().replace('{}=\[.*\]'.format(DATA._current_day),
							'{}={}'.format(DATA._current_day, attr))
		self.on_pre_enter()

	def key(self, insert):
		self.ids.LINE.text += insert

	def backspace(self):
		self.ids.LINE.text = self.ids.LINE.text[:len(self.ids.LINE.text)-1]


class Catcher(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)
		self.text_focus = 'BRT1'
		self.ids.BRT1_BTN.state = 'down'

		if Entry.nome:
			self.modus = 'client'
		elif isinstance(History.data, int):		# isinstance serve para reconhecer
			self.index = History.data			# 0 como True, o que não acontece
			if self.index == 0:					# porque 0 e 1 são instâncias do
				self.modus = 'edit_load'		# built-in bool; cf. pep-0285
			else:
				self.modus = 'edit'
		else:
			self.modus = 'load'

		self.builder()

	def on_leave(self, *args):
		if self.modus == 'client':
			Entry.nome = None
		elif self.modus == 'edit' or self.modus == 'edit_load':
			History.data = None
		if self.text_focus == 'LINE':
			self.ids.LINE.text = ''
			self.add_widget(self.ids.PAINEL)
		else:
			self.ids[self.text_focus + '_BTN'].state = 'normal'

	def builder(self):
		if self.modus != 'load':
			attr = getattr(DATA, DATA._current_day)
		if self.modus == 'client' or self.modus == 'edit':
			self.ids.PLUS.text = '2.5'
			if self.modus == 'client':
				self.ids.CLIENTE.text = 'CLIENTE: {}'.format(Entry.nome)
			else:
				self.ids.CLIENTE.text = 'CLIENTE: {}'.format(attr[self.index]['NOME'])
		elif self.modus == 'load' or self.modus == 'edit_load':
			self.ids.CLIENTE.text = 'CARGA'
			self.ids.PLUS.text = '0.5'

		for item in tipos:
			if self.modus == 'client' or self.modus == 'edit':
				unidade = 'DZ'
			else:
				unidade = 'CX'

			self.ids[item + '_DZ_BTN'].text = unidade

			if self.modus == 'client' or self.modus == 'load':
				self.ids[item].text = ''
				if self.modus == 'client':
					datas = DATA._reported_list
					if self.last_price(datas, item, attr[0]['WEEK']) == 1:
						self.ids[item + '_DZ'].text = str(DATA._dozen_price[item])
				else:
					self.ids[item + '_DZ'].text = str(DATA._box_price[item])
			elif self.modus == 'edit':
				if item in attr[self.index]:
					self.ids[item].text = str(attr[self.index][item])
					self.ids[item + '_DZ'].text = str(attr[self.index][item + '_DZ'])
				else:
					self.ids[item].text = ''
					self.ids[item + '_DZ'].text = str(DATA._dozen_price[item])
			else:
				if item in attr[self.index]:
					self.ids[item].text = str(attr[self.index][item] / 30)
				else:
					self.ids[item].text = ''
				self.ids[item + '_DZ'].text = str(attr[self.index][item + '_DZ'])



	def last_price(self, list, tipo, week):
		for dia in list:
			if dia == DATA._current_day:
				continue
			else:
				attr = getattr(DATA, dia)
				if attr[0].get('WEEK') == week:
					for dict in attr:
						if 'NOME' in dict and dict['NOME'] == Entry.nome:
							if tipo in dict:
								self.ids[tipo + '_DZ'].text =  str(dict[tipo + '_DZ'])
								return 0
							else:
								return 1
						else:
							continue
				else:
					continue
		else:
			return 1

	def focus(self, ids):
		self.text_focus = ids

	def key(self, insert):
		self.ids[self.text_focus].text += insert

	def backspace(self):
		self.ids[self.text_focus].text = ''

	def plus(self):
		number = self.ids.PLUS
		if self.ids[self.text_focus].text != '':
			old = float(self.ids[self.text_focus].text)
			self.ids[self.text_focus].text = str(old + float(number.text))
		else:
			self.ids[self.text_focus].text += number.text

	def pre_ok(self):
		if self.text_focus == 'LINE' and self.ids.LINE.text != '':
			self.popup_confirm(float(self.ids.LINE.text))
		elif self.text_focus == 'LINE' and self.ids.LINE.text == '':
			call_popup('ERRO: AUSÊNCIA DE PREÇO', 'Insira o valor cobrado.')
			return 1
		else:
			self.ok()

	def ok(self):
		prime = {}
		for item in tipos:
			if not self.ids[item + '_DZ'].text:
				call_popup('ERRO: AUSÊNCIA DE PREÇO', 'Insira todos os preços.')
				return 1
			elif self.ids[item].text:
				prime[item] = self.ids[item].text
				prime[item + '_DZ'] = self.ids[item + '_DZ'].text
			else:
				if self.modus == 'load' or self.modus == 'edit_load':
					prime[item + '_DZ'] = self.ids[item + '_DZ'].text

		self.instance = Ovo(prime)
		if self.modus == 'client' or self.modus == 'edit':
			if self.instance.total == 0.0:
				self.instance.client_edit_write()
				self.manager.current = 'menu'
			else:
				self.popup_confirm(self.instance.total)
		elif self.modus == 'edit_load':
			self.instance.client_edit_write()
			self.manager.current = 'menu'
		else:
			self.instance.load_write()
			self.manager.current = 'entry'

	def popup_confirm(self, money):
		self.popup = Popup()
		bx = BoxLayout(orientation='vertical')
		bxt = BoxLayout(size_hint=(1, 0.3))
		bt1 = Button(text='Sim', background_color=(0, 0.8, 0, 1))
		bt2 = Button(text='Trocar', background_color=(0, 0, 1, 1))
		bt3 = Button(text='Não', background_color=(0.8, 0, 0, 1))
		bt1.bind(on_press=self.yes)
		bt2.bind(on_press=self.maybe)
		bt3.bind(on_press=self.no)
		bxt.add_widget(bt1)
		bxt.add_widget(bt2)
		bxt.add_widget(bt3)
		msg = 'R$ {}'.format(str(money))
		bx.add_widget(Label(text=msg, size_hint=(1, 0.7), pos_hint={'top':1}, font_size=DATA._font_size*3))
		bx.add_widget(bxt)
		self.popup.title = 'CONFIRMAÇÃO DO VALOR'
		self.popup.content = bx
		self.popup.size_hint = (0.8, 0.6)
		self.popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.popup.auto_dismiss = False
		self.popup.open()

	def yes(self, instance, variation = None):
		if self.text_focus == 'LINE':
			chasm = float(self.ids.LINE.text)
			if self.instance.total != chasm:
				if self.instance.total > chasm:
					variation = chasm - self.instance.total
					self.instance.dict['TOTAL'] = chasm
				elif self.instance.total < chasm:
					variation = chasm - self.instance.total
					self.instance.dict['TOTAL'] = chasm

		if variation:
			self.instance.client_edit_write(variation)
		else:
			self.instance.client_edit_write()

		self.popup.dismiss()
		self.manager.current='menu'

	def no(self, instance):
		if self.text_focus == 'LINE':
			self.ids.LINE.text = str(self.instance.total)
		self.popup.dismiss()

	def maybe(self, instance):
		if self.text_focus != 'LINE':
			self.remove_widget(self.ids.PAINEL)
			self.ids.LINE.font_size = 100
			self.ids[self.text_focus + '_BTN'].state = 'normal'
			self.text_focus = 'LINE'
		self.ids.LINE.text = str(self.instance.total)
		self.popup.dismiss()


class History(Screen):

	data = None

	def on_pre_enter(self, *args):
		day_builder = {
			1: 'TER - ',
			2: 'QUA - ',
			3: 'QUI - '
			}

		reload(DATA)
		self.raw_list = []
		History.data = None
		lista = DATA._reported_list
		self.book = self.ids.BOOK
		self.book.values = []

		for dia in lista:
			self.raw_list.append(dia)

		if lista:
			for dia in lista:
				data = str.replace(str.strip(dia, 'H'), '_', '/')
				attr = getattr(DATA, dia)
				day_int = attr[0]['WEEK']
				elemento = '{}{}'.format(day_builder[day_int], data)
				self.book.values.append(elemento)
				self.book.text = self.book.values[0]

	def popup_confirm(self, msg, title, func):
		self.popup = Popup()
		bx = BoxLayout(orientation='vertical')
		bxt = BoxLayout(size_hint=(1, 0.3))
		bt1 = Button(text='Sim', background_color=(0, 0.8, 0, 1))
		bt2 = Button(text='Não', background_color=(0.8, 0, 0, 1))
		bt1.bind(on_press=func)
		bt2.bind(on_press=self.popup.dismiss)
		bxt.add_widget(bt1)
		bxt.add_widget(bt2)
		bx.add_widget(Label(text=msg, size_hint=(1, 0.7), pos_hint={'top':1}))
		bx.add_widget(bxt)
		self.popup.title = title
		self.popup.content = bx
		self.popup.size_hint = (0.8, 0.5)
		self.popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.popup.auto_dismiss=False
		self.popup.open()

	def output(self, modo):
		if self.book.text:
			History.data = modo, self.raw_list[self.book.values.index(self.book.text)]
			self.manager.current = 'output'

	def extract_text(self):
		instance = Extract(self.raw_list[self.book.values.index(self.book.text)])
		instance.parser()

		if self.raw_list[self.book.values.index(self.book.text)] == DATA._current_day:
			self.popup_confirm(
					'Deseja encerrar a praça?', 'FINALIZAÇÃO DE PRAÇA', self.finisher)
		else:
			self.manager.current = 'menu'

	def finisher(self, *args):
		Writer().clean()
		self.popup.dismiss()
		self.manager.current = 'menu'

	def remove_data(self):
		msg = 'Deseja remover "{}"?'.format(
							str.replace(str.strip(self.book.text, 'H'), '_', '/')[5:])
		self.popup_confirm(msg, 'LIMPEZA DO HISTÓRICO', self.remover)

	def remover(self, *args):
		Writer().remove(self.raw_list[self.book.values.index(self.book.text)])
		self.popup.dismiss()
		self.on_pre_enter()

class Output(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)
		modo, raw_day = History.data
		data = str.replace(str.strip(raw_day, 'H'), '_', '/')
		self.ids.DIA.text = data
		self.attr = getattr(DATA, raw_day)
		if modo == 'launch':
			self.launch(raw_day)
		elif modo == 'number':
			self.instance = Extract(raw_day)
			self.numbers()

	def on_leave(self, *args):
		self.ids.BXL.clear_widgets()
		for key in ['TOTAL', 'TOTAL_1', 'TOTAL_2', 'TOTAL_3']:
			self.ids[key].text = ''

	def launch(self, day):
		book_elements = []
		for dict in self.attr:
			if 'NOME' in dict:
				book_elements.append(dict['NOME'])

		self.ids.TITLE.text = 'LANÇAMENTOS'
		self.ids.SUBTITLE_2.text = 'Preço'
		self.ids.SUBTITLE_3.text = 'Total'
		self.BOOK = Spinner(size_hint = (0.75, 1))
		self.BOOK.values = book_elements
		self.ids.BXL.add_widget(self.BOOK)

		if day == DATA._current_day:
			self.BOOK.text = self.BOOK.values[-1]
			self.EDIT_BTN = Button()
			self.EDIT_BTN.text = 'Editar'
			self.EDIT_BTN.size_hint = 0.25, 1
			self.EDIT_BTN.background_color = 0.8, 0, 0, 1
			self.EDIT_BTN.bind(on_press = self.edit)
			self.ids.BXL.add_widget(self.EDIT_BTN)
		else:
			self.BOOK.text = self.BOOK.values[0]
			self.EDIT_BTN = None

		self.selected()

	def edit(self, instance):
		History.data = self.index
		self.manager.current = 'catcher'

	def selected(self):
		key_chain = [
		'BRT1', 'BRT1_DZ', 'BRT1_VLR',
		'BRT2', 'BRT2_DZ', 'BRT2_VLR',
		'BRT3', 'BRT3_DZ', 'BRT3_VLR',
		'VRT1', 'VRT1_DZ', 'VRT1_VLR',
		'BRDZ', 'BRDZ_DZ', 'BRDZ_VLR',
		'VRDZ', 'VRDZ_DZ', 'VRDZ_VLR',
		'BRMD', 'BRMD_DZ', 'BRMD_VLR',
		'VRMD', 'VRMD_DZ', 'VRMD_VLR',
		'TOTAL'
		]

		self.diff = self.BOOK.text
		if self.diff == 'CARGA':
			self.index = self.BOOK.values.index(self.BOOK.text)
		else:
			self.index = self.BOOK.values.index(self.BOOK.text) + 1

		if self.BOOK.text == 'CARGA':
			self.ids.SUBTITLE_1.text = 'Caixa'
		else:
			self.ids.SUBTITLE_1.text = 'Dúzia'

		for key in key_chain:
			if key in self.attr[self.index]:
				if key == 'TOTAL':
					self.ids[key + '_3'].text = str(self.attr[self.index][key])
				elif self.BOOK.text == 'CARGA' and key in tipos:
					self.ids[key].text = str(self.attr[self.index][key] / 30)
				else:
					self.ids[key].text = str(self.attr[self.index][key])
			else:
				self.ids[key].text = '-'

		self.process = Thread(target = self.loop)
		self.process.setDaemon(True)	# Daemon encerra o loop assim
		self.process.start()			# que o app se fecha totalmente.

	def loop(self):
		while self.BOOK.text == self.diff:
			if self.manager.current != 'output':
				break
			else:
				sleep(0.05)
		else:
			self.selected()

	def numbers(self):
		self.ids.TITLE.text = 'ESTATÍSTICAS'
		self.BALANCE_BTN1 = ToggleButton(group='numbers', text='Bruto', state='down')
		self.BALANCE_BTN2 = ToggleButton(group='numbers', text='Líquido')
		self.BALANCE_BTN3 = ToggleButton(group='numbers', text='Números')
		self.BALANCE_BTN1.allow_no_selection = False
		self.BALANCE_BTN2.allow_no_selection = False
		self.BALANCE_BTN3.allow_no_selection = False
		self.BALANCE_BTN1.bind(on_press=self.balance_1)
		self.BALANCE_BTN2.bind(on_press=self.balance_2)
		self.BALANCE_BTN3.bind(on_press=self.balance_3)
		self.ids.BXL.add_widget(self.BALANCE_BTN1)
		self.ids.BXL.add_widget(self.BALANCE_BTN2)
		self.ids.BXL.add_widget(self.BALANCE_BTN3)
		self.balance_1()

	def filler_balance_1(self, dict, text_suffix = '', dict_suffix = ''):
		for item in tipos:
			if item in dict and dict[item] != 0.0:
				self.ids[item + text_suffix].text = str(dict[item + dict_suffix])
			else:
				self.ids[item + text_suffix].text = '-'

		if not text_suffix:
			total = 'TOTAL_1'
		elif text_suffix == '_DZ':
			total = 'TOTAL_2'
		else:
			total = 'TOTAL_3'

		if total == 'TOTAL_3':
			text = self.instance.worked_dict['TOTAL'] - self.instance.bought_dict['TOTAL']
		else:
			text = dict['TOTAL']

		self.ids[total].text = str(text)

	def filler_balance_2(self, dict, text_suffix = '', dict_suffix = ''):
		for item in tipos:
			if item in dict and dict[item] != 0.0:
				self.ids[item + text_suffix].text = str(dict[item + dict_suffix])
			else:
				self.ids[item + text_suffix].text = '-'

		if not text_suffix:
			total = 'TOTAL_1'
		elif text_suffix == '_DZ':
			total = 'TOTAL_2'
		else:
			total = 'TOTAL_3'

		self.ids[total].text = str(dict['TOTAL'])

	def filler_balance_3(self, dict, text_suffix = '', total = 'TOTAL_1'):
		total_value = 0.0
		for item in tipos:
			if item in dict and dict[item] != 0.0:
				self.ids[item + text_suffix].text = str(dict[item])
				total_value += dict[item]
			else:
				self.ids[item + text_suffix].text = '-'

			self.ids[total].text = str(total_value)

	def balance_1(self, *args):
		self.ids.SUBTITLE_1.text = 'Comprado'
		self.ids.SUBTITLE_2.text = 'Vendido'
		self.ids.SUBTITLE_3.text = 'Lucro'
		self.ids.TOTAL.text = 'Total'

		self.filler_balance_1(self.instance.bought_dict)
		self.filler_balance_1(self.instance.worked_dict, '_DZ', '_VLR')
		self.filler_balance_1(self.instance.profit_dict, '_VLR')

	def balance_2(self, *args):
		self.ids.SUBTITLE_1.text = 'Comprado'
		self.ids.SUBTITLE_2.text = 'Vendido'
		self.ids.SUBTITLE_3.text = 'Lucro'
		self.ids.TOTAL.text = 'Total'

		self.filler_balance_2(self.instance.load_dict, dict_suffix = '_VLR')
		self.filler_balance_2(self.instance.worked_dict, '_DZ', '_VLR')
		self.filler_balance_2(self.instance.net_dict, '_VLR')

	def balance_3(self, *args):
		self.ids.SUBTITLE_1.text = 'Dz. Comp.'
		self.ids.SUBTITLE_2.text = 'Dz. Vend.'
		self.ids.SUBTITLE_3.text = 'Restante'
		self.ids.TOTAL.text = 'Total'

		self.filler_balance_3(self.instance.load_dict)
		self.filler_balance_3(self.instance.worked_dict, '_DZ', 'TOTAL_2')
		self.filler_balance_3(self.instance.surplus_load, '_VLR', 'TOTAL_3')


class Settings(Screen):

	unidade = None

	def on_pre_enter(self):
		Settings.modo = None

	def price_modus(self, value):
		Settings.modo = value
		self.manager.current = 'price_setter'

	def remove_data(self):
		self.popup = Popup()
		bx = BoxLayout(orientation='vertical')
		bxt = BoxLayout(size_hint=(1, 0.3))
		bt1 = Button(text='Sim', background_color=(0, 0.8, 0, 1))
		bt2 = Button(text='Não', background_color=(0.8, 0, 0, 1))
		bt1.bind(on_press=self.finisher)
		bt2.bind(on_press=self.popup.dismiss)
		bxt.add_widget(bt1)
		bxt.add_widget(bt2)
		msg = 'Deseja encerrar a praça?'
		bx.add_widget(Label(text=msg, size_hint=(1, 0.7), pos_hint={'top':1}))
		bx.add_widget(bxt)
		self.popup.title = 'FINALIZAÇÃO DE PRAÇA'
		self.popup.content = bx
		self.popup.size_hint = (0.8, 0.5)
		self.popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.popup.auto_dismiss=False
		self.popup.open()

	def finisher(self, *args):
		Writer().clean()
		self.popup.dismiss()
		self.manager.current = 'menu'


class Carga(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)
		day = DATA._current_day
		load = DATA._load
		total = 0.0

		if DATA._current_day:
			self.ids.DIA.text = str.replace(str.strip(day, 'H'), '_', '/')
		else:
			self.ids.DIA.text = time.strftime('%d/%m/%y')

		for item in tipos:
			if load[item] != 0.0:
				box = load[item] / 30
				total += load[item]
				self.ids[item].text = str(load[item])
				self.ids[item + '_BOX'].text = str(round(box, 2))
			else:
				self.ids[item].text = '-'
				self.ids[item + '_BOX'].text = '-'

		box_total = total / 30
		self.ids.TOTAL_1.text = str(total)
		self.ids.TOTAL_2.text = str(round(box_total, 2))


class EditCarga(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)
		self.text_focus = 'BRT1'
		self.ids.BRT1_BTN.state = 'down'
		self.ids.PLUS.text = '15'
		self.load = DATA._load

		for item in tipos:
			if self.load[item] != 0.0:
				self.ids[item].text = str(self.load[item])

		self.process = Thread(target = self.loop)
		self.process.setDaemon(True)
		self.process.start()

	def on_leave(self, *args):
		self.ids[self.text_focus + '_BTN'].state = 'normal'

	def converter(self):
		for item in tipos:
			if self.ids[item].text:
				box = float(self.ids[item].text) / 30
				self.ids[item + '_BOX'].text = str(round(box, 2))
			else:
				self.ids[item + '_BOX'].text = ''

	def loop(self):
		while True:
			if self.manager.current != 'edit_carga':
				break
			else:
				self.converter()
				sleep(0.05)

	def focus(self, ids):
		self.text_focus = ids

	def key(self, insert):
		self.ids[self.text_focus].text += insert

	def backspace(self):
		self.ids[self.text_focus].text = ''

	def plus(self):
		number = self.ids.PLUS
		if self.ids[self.text_focus].text != '':
			old = float(self.ids[self.text_focus].text)
			self.ids[self.text_focus].text = str(old + float(number.text))
		else:
			self.ids[self.text_focus].text += number.text

	def ok(self):
		if DATA._current_day:
			attr = getattr(DATA, DATA._current_day)
			surplus = attr[1]
		else:
			surplus = None

		for item in tipos:
			if self.ids[item].text:
				self.load[item] = float(self.ids[item].text)
				if surplus:
					surplus[item] = float(self.ids[item].text)

		Writer().replace('_load={.*}', '_load={}'.format(self.load))
		if surplus:
			Writer().replace('{}=\[.*\]'.format(DATA._current_day), '{}={}'.format(
															DATA._current_day, attr))
		self.manager.current = 'carga'


class PriceSetter(Screen):

	def on_pre_enter(self, *args):
		self.text_focus = 'BRT1'
		self.ids.BRT1_BTN.state = 'down'
		if Settings.modo == 'box':
			self.box_price()
		elif Settings.modo == 'dozen':
			self.dozen_price()

	def on_leave(self, *args):
		self.ids[self.text_focus + '_BTN'].state = 'normal'
		Settings.modo = None

	def box_price(self):
		self.ids.TITLE.text = 'ALTERAÇÃO DE PREÇO DA CAIXA'
		self.ids.PLUS.text = '5'
		self.unit = DATA._box_price
		self.filler()

	def dozen_price(self):
		self.ids.TITLE.text = 'ALTERAÇÃO DE PREÇO DA DÚZIA'
		self.ids.PLUS.text = '0.2'
		self.unit = DATA._dozen_price
		self.filler()

	def filler(self):
		for item in tipos:
			if item != 0.0:
				self.ids[item].text = str(self.unit[item])

	def focus(self, ids):
		self.text_focus = ids

	def key(self, insert):
		self.ids[self.text_focus].text += insert

	def backspace(self):
		self.ids[self.text_focus].text = ''

	def plus(self):
		number = self.ids.PLUS
		if self.ids[self.text_focus].text != '':
			old = float(self.ids[self.text_focus].text)
			self.ids[self.text_focus].text = str(old + float(number.text))
		else:
			self.ids[self.text_focus].text += number.text

	def ok(self):
		for item in tipos:
			if self.ids[item].text:
				self.unit[item] = float(self.ids[item].text)
			else:
				call_popup('ERRO: AUSÊNCIA DE PREÇO', 'Insira todos os preços.')
				return 1

		if Settings.modo == 'box':
			unit = '_box_price'
		elif Settings.modo == 'dozen':
			unit = '_dozen_price'

		Writer().replace('{}={}'.format(unit, '{.*}'), '{}={}'.format(unit, self.unit))
		self.manager.current = 'settings'


class PreRouteSetter(Screen):

	def transition(self, value):
		Settings.modo = value
		self.manager.current = 'route_setter'

class RouteSetter(Screen):

	def on_pre_enter(self, *args):
		reload(DATA)
		self.day = Settings.modo
		self.route = getattr(DATA, self.day)
		self.route.insert(0, '')
		self.ids.BOOK_INDEX.values = self.route
		self.ids.BOOK_INDEX.text = ''
		self.ids.LINE.text = ''

	def on_leave(self, *args):
		Settings.modo = None

	def key(self, insert):
		self.ids.LINE.text += insert

	def backspace(self):
		self.ids.LINE.text = self.ids.LINE.text[:len(self.ids.LINE.text)-1]

	def pre_ok(self, operation):
		self.book_index = self.ids.BOOK_INDEX.text
		self.nome = self.ids.LINE.text

		if operation == 'sub':
			if self.book_index:
				if not self.nome:
					text = 'Deseja remover "{}"?'.format(self.book_index)
					self.popup_confirm(self.sub, text)
				else:
					text = 'Apague "{}"\nou o adicione à rota.'.format(self.nome)
					call_popup('ERRO: INDECISÃO DE OPERAÇÃO', text)
					return 1
			else:
				text = 'Selecione um cliente\npara remoção.'
				call_popup('ERRO: CLIENTE NÃO SELECIONADO', text)
		elif operation == 'add':
			if self.nome:
				if self.nome in self.ids.BOOK_INDEX.values:
					text = '"{}" já está\npresente na rota.'.format(self.nome)
					call_popup('ERRO: CLIENTE EXISTENTE', text)
					return 1
				elif not self.book_index:
					text = 'Adicionar "{}"\ncomo 1º da rota?'.format(self.nome)
					self.popup_confirm(self.add, text)
				else:
					text = 'Inserir "{}" após\n"{}" na rota?'.format(
															self.nome, self.book_index)
					self.popup_confirm(self.add, text)
			else:
				call_popup('ERRO: AUSÊNCIA DE CLIENTE', 'Digite um nome.')
				return 1

	def sub(self, *args):
		self.route.remove('')
		self.route.remove(self.book_index)
		self.writer()

	def add(self, *args):
		self.route.remove('')
		if self.book_index:
			index = self.route.index(self.book_index) + 1
		else:
			index = 0

		self.route.insert(index, self.nome)
		self.writer()

	def popup_confirm(self, func, msg):
		self.popup = Popup()
		bx = BoxLayout(orientation='vertical')
		bxt = BoxLayout(size_hint=(1, 0.3))
		bt1 = Button(text='Sim', background_color=(0, 0.8, 0, 1))
		bt2 = Button(text='Não', background_color=(0.8, 0, 0, 1))
		bt1.bind(on_press=func)
		bt2.bind(on_press=self.popup.dismiss)
		bxt.add_widget(bt1)
		bxt.add_widget(bt2)
		bx.add_widget(Label(text=msg, size_hint=(1, 0.7), pos_hint={'top':1}))
		bx.add_widget(bxt)
		self.popup.title = 'CONFIRMAR OPERAÇÃO NA ROTA'
		self.popup.content = bx
		self.popup.size_hint = (0.8, 0.5)
		self.popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.popup.auto_dismiss = False
		self.popup.open()

	def writer(self):
		Writer().replace('{}=\[.*\]'.format(self.day), '{}={}'.format(
																self.day, self.route))
		self.popup.dismiss()
		self.on_pre_enter()


class FontSetter(Screen):

	def on_pre_enter(self, *args):
		self.ids.TEST_1.state = 'down'
		self.ids.SIZE.text = str(DATA._font_size)
		self.font_size = self.ids.SIZE
		self.text('text 1')

	def on_leave(self, *args):
		self.ids[self.find_suffix()].state = 'normal'

	def find_suffix(self):
		for suffix in ['_1', '_2']:
			if self.ids['TEST' + suffix].state == 'down':
				return 'TEST' + suffix

	def test(self):
		if self.ids.TEST_2.state == 'down':
			size = int(self.font_size.text) * 3
		else:
			size = int(self.font_size.text)
		self.ids.LINE.font_size = size

	def text(self, modo):
		if modo == 'text 1':
			self.ids.LINE.text = 'Este é o tamanho da fonte.'
		elif modo == 'text 2':
			self.ids.LINE.text = 'R$ 520.0'
		self.test()

	def plus(self, number):
		self.font_size.text = str(int(self.font_size.text) + int(number))
		self.test()

	def ok(self):
		new_value = int(self.font_size.text)
		Writer().replace('_font_size=.*', '_font_size={}'.format(new_value))
		self.manager.current = 'menu'


class MapaApp(App):

	sm = None

	def build(self):
		self.sm = ScreenManager()
		self.sm.add_widget(Menu(name = 'menu'))
		self.sm.add_widget(Rota(name = 'rota'))
		self.sm.add_widget(Dia(name = 'dia'))
		self.sm.add_widget(Entry(name = 'entry'))
		self.sm.add_widget(Catcher(name = 'catcher'))
		self.sm.add_widget(History(name = 'history'))
		self.sm.add_widget(Output(name = 'output'))
		self.sm.add_widget(Settings(name = 'settings'))
		self.sm.add_widget(Carga(name = 'carga'))
		self.sm.add_widget(EditCarga(name = 'edit_carga'))
		self.sm.add_widget(PriceSetter(name = 'price_setter'))
		self.sm.add_widget(PreRouteSetter(name = 'pre_route_setter'))
		self.sm.add_widget(RouteSetter(name = 'route_setter'))
		self.sm.add_widget(FontSetter(name = 'font_setter'))
		self.sm.current = start
		return self.sm

	def on_start(self):
		EventLoop.window.bind(on_keyboard=self.hook_keyboard)

	def hook_keyboard(self, window, key, *args):
		if key == 27:
			self.sm.current = 'menu'
  			return True

	def on_pause(self):
		return True

	def on_resume(self):
		pass


class Ovo:

	def __init__(self, prime):
		self.carga = getattr(DATA, '_load')
		self.dict = {}
		self.file = Writer()
		self.total = 0.0
		if isinstance(History.data, int):
			self.index = History.data
			self.edit_attr = getattr(DATA, DATA._current_day)
			self.edit_dict = self.edit_attr[self.index]
		else:
			self.index = 'Ou não há History.data e Entry.nome. ou há apenas este.'

		self.builder(prime)

	def builder(self, prime):
		if Entry.nome:
			self.dict['NOME'] = Entry.nome
		elif History.data and self.index != 0:
			self.dict['NOME'] = self.edit_dict['NOME']
		elif not Entry.nome or self.index == 0:
			self.dict['NOME'] = 'CARGA'
			if self.index == 0:
				self.dict['WEEK'] = self.edit_dict['WEEK']
			else:
				self.dict['WEEK'] = Rota.week

		for item in tipos:
			if item in prime:
				duzia = float(prime[item])
				valor = float(prime[item + '_DZ'])
				produto = duzia * valor
				produto = round(produto, 2)
				if self.dict['NOME'] == 'CARGA':
					self.dict[item] = duzia * 30
				else:
					self.dict[item] = duzia
				self.dict[item + '_DZ'] = valor
				self.dict[item + '_VLR'] = produto
				self.total += produto
			elif self.dict['NOME'] == 'CARGA':
				self.dict[item + '_DZ'] = float(prime[item + '_DZ'])
		self.dict['TOTAL'] = self.total

	def load_plus(self):
		for item in tipos:
			if isinstance(History.data, int) and self.index != 0:
				if item in self.edit_dict:
					soma = self.carga[item] + self.edit_dict[item]
					self.carga[item] = soma
			else:
				if item in self.dict:
					soma = self.carga[item] + self.dict[item]
					self.carga[item] = soma
		self.file.replace('_load={.*}', '_load={}'.format(self.carga))

	def load_sub(self):
		for item in tipos:
			if (isinstance(History.data, int) and self.index != 0) or self.index != 0:
				if item in self.dict:
					sub = self.carga[item] - self.dict[item]
					self.carga[item] = sub
			elif isinstance(History.data, int) and self.index == 0:
				if item in self.edit_dict:
					sub = self.carga[item] - self.edit_dict[item]
					self.carga[item] = sub
		self.file.replace('_load={.*}', '_load={}'.format(self.carga))

	def load_write(self):
		self.load_plus()
		load_dict = {'NAME': 'SURPLUS LOAD'}
		for item in tipos:
			load_dict[item] = DATA._load[item]
		self.file.append('\n{}={}\n'.format(DATA._current_day, [self.dict, load_dict]))

	def client_edit_write(self, chasm = 0.0):
		self.load_sub()
		if chasm:
			self.dict['CHASM'] = chasm
		if Entry.nome:
			Writer().client_remove()
			attr = getattr(DATA, DATA._current_day)
			attr.append(self.dict)
			new = attr
		elif isinstance(History.data, int):
			self.load_plus()
			self.edit_attr.remove(self.edit_dict)
			self.edit_attr.insert(self.index, self.dict)
			new = self.edit_attr

		# atualização da carga no dict do dia da praça para gerar
		# a carga restante no extrato
		for item in tipos:
			new[1][item] = DATA._load[item]

		self.file.replace('{}=\[.*\]'.format(DATA._current_day), '{}={}'.format(DATA._current_day, new))


class Extract:
	"""Gerador de informações e de outputs"""

	def __init__(self, day):
		self.raw_day = str.strip(day, 'H')
		self.human_day = str.replace(self.raw_day, '_', '/')
		self.raw_dict = getattr(DATA, day)
		self.load_dict = self.raw_dict[0]
		self.surplus_load = self.raw_dict[1]
		self.bought_dict = {
				'BRT1': 0.0, 'VRT1': 0.0, 'BRT2': 0.0,
				'BRT3': 0.0, 'BRDZ': 0.0, 'VRDZ': 0.0,
				'BRMD': 0.0, 'VRMD': 0.0, 'TOTAL': 0.0
				}
		self.net_dict = {
				'BRT1': 0.0, 'VRT1': 0.0, 'BRT2': 0.0,
				'BRT3': 0.0, 'BRDZ': 0.0, 'VRDZ': 0.0,
				'BRMD': 0.0, 'VRMD': 0.0, 'TOTAL': 0.0
				}
		self.profit_dict = {
				'BRT1': 0.0, 'VRT1': 0.0, 'BRT2': 0.0,
				'BRT3': 0.0, 'BRDZ': 0.0, 'VRDZ': 0.0,
				'BRMD': 0.0, 'VRMD': 0.0, 'TOTAL': 0.0
				}
		self.worked_dict = {
				'BRT1': 0.0, 'BRT1_VLR': 0.0, 'VRT1': 0.0, 'VRT1_VLR': 0.0,
				'BRT2': 0.0, 'BRT2_VLR': 0.0, 'BRT3': 0.0, 'BRT3_VLR': 0.0,
				'BRDZ': 0.0, 'BRDZ_VLR': 0.0, 'VRDZ': 0.0, 'VRDZ_VLR': 0.0,
				'BRMD': 0.0, 'BRMD_VLR': 0.0, 'VRMD': 0.0, 'VRMD_VLR': 0.0,
				'CHASM': 0.0, 'TOTAL': 0.0
				}

		self.worker()

	def worker(self):
		"""Transforma os dados de self.raw_dict para para gerar output em texto
		e no app."""

		# Soma a quantidade e o total vendido de cada tipo de ovo
		for dict in self.raw_dict:
			if 'NOME' in dict and dict['NOME'] != 'CARGA':
				for key in self.worked_dict.keys():
					if key in dict:
						self.worked_dict[key] += dict[key]


		# Calcula o que foi comprado em relação ao que foi vendido para gerar
		# o balanço bruto
		for item in tipos:
			box_price = self.load_dict[item + '_DZ'] / 30
			value = self.worked_dict[item] * round(box_price, 2)
			self.bought_dict[item] = value
			self.bought_dict['TOTAL'] += value

		# Calcula o lucro bruto
		for item in tipos:
			value = self.worked_dict[item + '_VLR'] - self.bought_dict[item]
			self.profit_dict[item] = value
			self.profit_dict['TOTAL'] += value		# total lucrado sem os descontos

		# Calcula o lucro líquido
		for item in tipos:
			if item in self.load_dict:
				value = self.worked_dict[item + '_VLR'] - self.load_dict[item + '_VLR']
				self.net_dict[item] = value
				self.net_dict['TOTAL'] += value

		self.surplus_load['TOTAL'] = 0.0
		for item in tipos:
			if item in self.surplus_load:
				self.surplus_load['TOTAL'] += self.surplus_load[item]

	def parser(self):
		"""Gerador de lista com conteúdos para fornecer ao gerador de texto(self.builder)"""

		contents = []
		## DICT COM CARGA RESTANTE E RECONHECIMENTO DE FALSO PARA 0.0
		for dict in self.raw_dict:
			if 'NOME' in dict and dict['NOME'] == 'CARGA':
				load_1 = ['CARGA COMPRADA\n']
				load_2 = ['CARGA RESTANTE\n']
				total_load_2 = 0
				for item in tipos:
					if item in dict:
						current_box_rounded = round(self.surplus_load[item] / 30, 2)
						phrase_1 = '{}: {}\t\t\tPREÇO: R$ {}\t\tSUBTOTAL: R$ {}\n'.format(
														item, self.load_dict[item] / 30,
														self.load_dict[item + '_DZ'],
														self.load_dict[item + '_VLR'])
						phrase_2 = '{}: {} CAIXAS\t\t\t{} DÚZIAS\n'.format(
														item, current_box_rounded,
														self.surplus_load[item])
					else:
						phrase_1 = '{}: -\t\t\tPREÇO: R$ {}\n'.format(
														item,
														self.load_dict[item + '_DZ'])
						phrase_2 = '{}: -\n'.format(item)
					load_1.append(phrase_1)
					load_2.append(phrase_2)
				load_1.append('TOTAL: R$ {}'.format(self.load_dict['TOTAL']))
				load_2.append('TOTAL: {} CAIXAS\t\t\t{} DÚZIAS\n'.format(
											round(self.surplus_load['TOTAL'] / 30, 2),
											self.surplus_load['TOTAL']))
				contents.append(load_1)
				contents.append(load_2)
			elif 'NOME' in dict:
				client = ['{}\n'.format(dict['NOME'])]
				if dict['TOTAL']:
					for item in tipos:
						if item in dict:
							client.append(
								'{}: {}\t\t\tPREÇO: R$ {}\t\tSUBTOTAL: R$ {}\n'.format(
															item, dict[item],
															dict[item + '_DZ'],
															dict[item + '_VLR']))
					if 'CHASM' in dict:
						client.append(
								'\t\t\t\t\t\t\t\tDESCONTO: R$ {}\nTOTAL: RS {}'.format(
															dict['CHASM'], dict['TOTAL']))
					else:
						client.append('TOTAL: R$ {}'.format(dict['TOTAL']))
				else:
					client.append('-')

				contents.append(client)

		contents[-1].append('\n')

		balance_1 = ['BALANÇO BRUTO\n']
		balance_profit = 0
		for item in tipos:
			if self.worked_dict[item]:
				part_1 = '{}: {}\t   COMPRADO: R$ {}\t  VENDIDO: R$ {}\t  '.format(
													item, self.worked_dict[item],
													self.bought_dict[item],
													self.worked_dict[item + '_VLR'])
				part_2 = 'LUCRO: R$ {}\n'.format(self.profit_dict[item])
				balance_1.append(part_1 + part_2)
			else:
				phrase = '{}: -\n'.format(item)
				balance_1.append(phrase)

		if self.worked_dict['CHASM']:
			balance_1.append('DESCONTO TOTAL: R$ {}\n'.format(self.worked_dict['CHASM']))
		balance_1.append('LUCRO BRUTO: R$ {}, APROXIMADAMENTE.\n'.format(
													self.worked_dict['TOTAL']
													- self.bought_dict['TOTAL']))
		contents.append(balance_1)

		balance_2 = ['BALANÇO LÍQUIDO\n']
		for item in tipos:
			if item in self.load_dict:
				part_1 = '{}: {}\t  COMPRADO: R$ {}\t  VENDIDO: R$ {}\t  '.format(
													item, self.load_dict[item],
													self.load_dict[item + '_VLR'],
													self.worked_dict[item + '_VLR'])
				part_2 = 'LUCRO: R$ {}\n'.format(self.net_dict[item])
				balance_2.append(part_1 + part_2)
			else:
				phrase = '{}: -\n'.format(item)
				balance_2.append(phrase)
		balance_2.append('TOTAL COMPRADO: R$ {}\n'.format(self.load_dict['TOTAL']))
		balance_2.append('TOTAL VENDIDO: R$ {}\n'.format(self.worked_dict['TOTAL']))
		balance_2.append('LUCRO LÍQUIDO: R$ {}'.format(self.net_dict['TOTAL']))
		contents.append(balance_2)

		self.builder(contents)

	def builder(self, parsed_contents):
		"""Gerador de texto"""

		text = 'EGGBERTO: EXTRATO - DIA {}.\n'.format(self.human_day)

		for element in parsed_contents:
			if isinstance(element, list):
				text += '\n{}\n'.format('-' * 80)
				for item in element:
					text += item
			else:
				text += '\n{}\n'.format('-' * 80)
				text += element

		Writer().create_extract(text, self.raw_day)


class Writer:

	def open(self, option = 'r'):
		self.file = open(d, option)

	def append(self, content):
		self.open('a')
		self.file.write(content)
		self.file.close()

	def clean(self):
		Writer().replace('_current_day=.*', '_current_day=None')
		Writer().replace('_current_route=\[.*\]', '_current_route=[]')

	def client_remove(self):
		clientes = DATA._current_route
		if Entry.nome in clientes:
			clientes.remove(Entry.nome)
			self.replace('_current_route=\[.*\]', '_current_route={}'.format(clientes))

	def create_extract(self, content, day):
		numbers_list = day.split('_')
		for number in numbers_list:
			if len(number) == 1:
				numbers_list[numbers_list.index(number)] = '0' + number
		new_file = open('EXTRATO{}.txt'.format(''.join(numbers_list)), 'w')
		new_file.write(content)
		new_file.close()

	def day_writer(self, day):
		day_func = {
			1: DATA._tuesday,
			2: DATA._wednesday,
			3: DATA._thursday
			}
		attr = getattr(DATA, '_reported_list')
		attr.insert(0, day)
		self.replace('_current_route=\[\]', '_current_route={}'.format(day_func[Rota.week]))
		self.replace('_current_day=None', "_current_day='{}'".format(day))
		self.replace('_reported_list=\[.*\]', '_reported_list={}'.format(attr))

	def remove(self, day):
		reported_list = getattr(DATA, '_reported_list')
		reported_list.remove(day)
		self.replace('_reported_list=\[.*\]', '_reported_list={}'.format(reported_list))
		self.replace('{}=\[.*\]'.format(day), '')

	def replace(self, old, new):
		self.open()
		sub = re.sub(old, new, self.file.read())
		self.file.close()
		self.open('w')
		self.file.write(sub)
		self.file.close()


def call_popup(title, msg):
	popup = Popup()
	bx = BoxLayout(orientation='vertical')
	bt = Button(text='OK', background_color=(0, 0.8, 0, 1), size_hint=(1, 0.3))
	bt.bind(on_press=popup.dismiss)
	bx.add_widget(Label(text=msg, size_hint=(1, 0.7), pos_hint={'top':1}, font_size=DATA._font_size))
	bx.add_widget(bt)
	popup.title = title
	popup.content = bx
	popup.size_hint = (0.8, 0.5)
	popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
	popup.auto_dismiss = False
	popup.open()


if __name__ == '__main__':
	MapaApp().run()
