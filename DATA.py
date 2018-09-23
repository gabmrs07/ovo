# -*- coding: utf-8 -*-

## VALORES FIXOS

_CV={'V1': '84.0', 'V2': '90.0', 'V3': '80.0', 'V4': '70.0', 'V5': '93.0', 'V6': '100.0', 'V7': '93.0', 'V8': '100.0'}

_V={'V1': '4.0', 'V2': '4.4', 'V3': '3.6', 'V4': '3.2', 'V5': '4.0', 'V6': '4.4', 'V7': '4.0', 'V8': '4.4'}

## ROTAS

_TERCA=["GIBA'S", 'LOCATELLI', 'SARA', 'LORI', 'TRENZINHO', 'VERDES CAMPOS', 'ACADEMIA', 'ADEMIR', 'NOVO PAN', 'PASSARINHO', 'JÚLIO', 'ALICE', 'POSTAÇO', 'ESCOLINHA', 'SAPIRANGA', 'MARLI', 'PAULO PILATTI', 'VÓ MIRIAM', 'MIRIAM', 'BAUM', 'FEEVALE', 'TAILOR', 'FÁBIO', 'CERRO LARGO', 'DEISE', 'REMI', 'COSTANEIRA', 'GILMAR', 'IMPERIAL', 'WANDA', 'LILI', 'SCHUTZ', 'SUPER BEM', 'EVANDRO', 'REGINA', 'VÓ', 'NONOAI', 'CLÁUDIO']
_QUARTA=['ELIAS', 'DÉLCIO', 'SIMONE', 'SAMUEL', 'MARLI', 'CÉZAR', 'BOLACHA', 'JUVENTINO', 'ZENOILDE', 'MÔNICA', 'IRACI', 'LAMB', 'LOURDES', 'SERRINHA', 'GIBA', 'PEDRO', 'MARIA', 'DANIEL', 'CLÁUDIO', 'ANDRÉ', 'CARLOS', 'AURÉLIO', 'OBA OBA', 'JÚNIOR', 'PENNA', 'DOG\'S', 'TIA', 'APARECIDA', 'ANTÔNIO/BETTE', 'ANTÔNIO TORRE', 'PRIMUS', 'FREEWAY', 'PAULO', 'TIA GETNET', 'VÔ GETNET', 'BOKAS', 'PAULO ROSA']
_QUINTA=['RICCI', 'JOEL', 'DAIANE', 'PARANÁ', 'JULIANO', 'MARLI', 'ANTÔNIO', 'ZÉ', 'ALEXANDRE', 'FLORES', 'JÔ', 'ALCEMAR', 'ALEMÃO', 'JÚLIO']

## ENTRADA

_C={}
_W=None

## CARGA

_CARGA={'VRDZ': 47.0, 'BRMD': 5.0, 'BRDZ': 37.0, 'VRMD': 6.0, 'VRT1': 45.0, 'BRT1': 155.0, 'BRT2': 62.5, 'BRT3': 0.0}

## HISTORICO

_H=['H20_09_18', 'H19_09_18', 'H18_09_18']

H18_09_18=[{'WEEK':1,'BRT3_VLR': 280.0, 'BRT2_VLR': 80.0, 'BRT1_DZ': 84.0, 'BRMD': 0.5, 'BRT3_DZ': 70.0, 'BRT2_DZ': 80.0, 'VRT1_DZ': 90.0, 'BRT1': 14.0, 'BRT2': 1.0, 'BRT3': 4.0, 'VRT1_VLR': 270.0, 'BRMD_DZ': 93.0, 'BRMD_VLR': 46.5, 'VRMD': 0.5, 'VRT1': 3.0, 'VRMD_VLR': 50.0, 'TOTAL': 1902.5, 'BRT1_VLR': 1176.0, 'CLIENTE': 'CARGA', 'VRMD_DZ': 100.0}, {'BRT3_DZ': 3.6, 'BRT3_VLR': 360.0, 'TOTAL': 360.0, 'CLIENTE': "GIBA'S", 'BRT3': 100.0}, {'BRT3_VLR': 34.0, 'BRT1_DZ': 3.6, 'BRT3_DZ': 3.4, 'TOTAL': 178.0, 'BRT1_VLR': 144.0, 'BRT1': 40.0, 'CLIENTE': 'LOCATTELI', 'BRT3': 10.0}, {'BRDZ_DZ': 4.0, 'VRDZ': 12.0, 'BRT1_DZ': 4.0, 'VRDZ_VLR': 50.4, 'BRT1': 120.0, 'BRDZ_VLR': 12.0, 'BRT1_VLR': 408.0, 'CLIENTE': 'SARA', 'VRDZ_DZ': 4.2, 'BRDZ': 3.0, 'TOTAL': 470.4}, {'BRMD_VLR': 40.0, 'BRMD_DZ': 4.0, 'TOTAL': 40.0, 'CLIENTE': 'TRENZINHO', 'BRMD': 10.0}, {'TOTAL': 27.0, 'BRT1_VLR': 27.0, 'BRT1_DZ': 3.6, 'CLIENTE': 'VERDES CAMPOS', 'BRT1': 7.5}, {'BRT1_DZ': 4.0, 'VRT1': 7.5, 'VRT1_VLR': 33.0, 'VRT1_DZ': 4.4, 'TOTAL': 43.0, 'BRT1_VLR': 10.0, 'BRT1': 2.5, 'CLIENTE': 'ACADEMIA'}, {'BRT1_DZ': 4.0, 'VRT1_DZ': 4.0, 'VRT1_VLR': 10.0, 'VRT1': 2.5, 'TOTAL': 20.0, 'BRT1_VLR': 10.0, 'BRT1': 2.5, 'CLIENTE': 'ADEMIR'}, {'TOTAL': 105.0, 'BRT1_VLR': 105.0, 'BRT1_DZ': 3.5, 'CLIENTE': 'NOVO PAN', 'BRT1': 30.0}, {'VRT1_VLR': 30.0, 'VRT1': 7.5, 'TOTAL': 30.0, 'CLIENTE': 'LORI', 'VRT1_DZ': 4.0}, {'BRT1_DZ': 4.0, 'VRT1_DZ': 4.4, 'VRT1_VLR': 11.0, 'VRT1': 2.5, 'TOTAL': 21.0, 'BRT1_VLR': 10.0, 'BRT1': 2.5, 'CLIENTE': 'PASSARINHO'}, {'BRT1': 5.0, 'TOTAL': 20.0, 'BRT1_VLR': 20.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'JÚLIO'}, {'TOTAL': 40.0, 'BRT1_VLR': 40.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'ALICE', 'BRT1': 10.0}, {'BRT1_DZ': 3.6, 'TOTAL': 36.0, 'BRT1_VLR': 36.0, 'BRT1': 10.0, 'CLIENTE': 'POSTAÇO'}, {'TOTAL': 50.0, 'BRT1_VLR': 50.0, 'BRT1': 12.5, 'CLIENTE': 'ESCOLINHA', 'BRT1_DZ': 4.0}, {'VRT1_VLR': 33.0, 'VRT1': 7.5, 'TOTAL': 33.0, 'CLIENTE': 'SAPIRANGA', 'VRT1_DZ': 4.4}, {'TOTAL': 0.0, 'CLIENTE': 'MARLI'}, {'BRT1_DZ': 4.0, 'TOTAL': 60.0, 'BRT1_VLR': 60.0, 'BRT1': 15.0, 'CLIENTE': 'PAULO PILATTI'}, {'VRT1_VLR': 12.0, 'VRT1': 2.5, 'TOTAL': 12.0, 'CLIENTE': 'MIRIAM', 'VRT1_DZ': 4.8}, {'VRT1_VLR': 11.0, 'VRT1': 2.5, 'TOTAL': 11.0, 'CLIENTE': 'VÓ MIRIAM', 'VRT1_DZ': 4.4}, {'VRDZ': 5.0, 'TOTAL': 20.0, 'VRDZ_DZ': 4.0, 'CLIENTE': 'BAUM', 'VRDZ_VLR': 20.0}, {'BRT2_DZ': 3.6, 'BRT2': 15.0, 'TOTAL': 54.0, 'CLIENTE': 'FEEVALE', 'BRT2_VLR': 54.0}, {'BRT1_DZ': 4.0, 'VRT1_DZ': 4.0, 'VRT1_VLR': 20.0, 'VRT1': 5.0, 'TOTAL': 40.0, 'BRT1_VLR': 20.0, 'BRT1': 5.0, 'CLIENTE': 'TAILOR'}, {'TOTAL': 0.0, 'CLIENTE': 'FÁBIO'}, {'BRDZ_DZ': 4.0, 'VRDZ': 10.0, 'BRMD_DZ': 4.2, 'VRDZ_VLR': 42.0, 'BRMD': 6.0, 'BRMD_VLR': 25.2, 'VRMD_VLR': 37.8, 'BRDZ_VLR': 40.0, 'CLIENTE': 'CERRO LARGO', 'VRMD_DZ': 4.20, 'VRDZ_DZ': 4.2, 'BRDZ': 10.0, 'VRMD': 9.0, 'TOTAL': 145.0}, {'TOTAL': 50.0, 'BRT1_VLR': 50.0, 'BRT1': 12.5, 'CLIENTE': 'DEISE', 'BRT1_DZ': 4.0}, {'TOTAL': 0.0, 'CLIENTE': 'REMI'}, {'TOTAL': 34.0, 'BRT1_VLR': 34.0, 'BRT1_DZ': 3.4, 'CLIENTE': 'COSTANEIRA', 'BRT1': 10.0}, {'TOTAL': 0.0, 'CLIENTE': 'GILMAR'}, {'BRT1_DZ': 3.6, 'VRT1_DZ': 4.0, 'VRT1_VLR': 20.0, 'VRT1': 5.0, 'TOTAL': 38.0, 'BRT1_VLR': 18.0, 'BRT1': 5.0, 'CLIENTE': 'ASSIS'}, {'BRT1': 2.5, 'TOTAL': 9.0, 'BRT1_VLR': 9.0, 'BRT1_DZ': 3.6, 'CLIENTE': 'WANDA'}, {'TOTAL': 20.0, 'BRT1_VLR': 20.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'TIA', 'BRT1': 5.0}, {'VRT1_VLR': 12.0, 'VRT1': 2.5, 'TOTAL': 12.0, 'CLIENTE': 'LILI', 'VRT1_DZ': 4.8}, {'TOTAL': 0.0, 'CLIENTE': 'SCHUTZ'}, {'BRT1': 60.0, 'TOTAL': 204.0, 'BRT1_VLR': 204.0, 'BRT1_DZ': 3.4, 'CLIENTE': 'SUPER BEM'}, {'VRT1_VLR': 11.0, 'VRT1': 2.5, 'TOTAL': 11.0, 'CLIENTE': 'EVANDRO', 'VRT1_DZ': 4.4}, {'BRT1_DZ': 4.0, 'TOTAL': 20.0, 'BRT1_VLR': 20.0, 'BRT1': 5.0, 'CLIENTE': 'REGINA'}, {'VRT1_VLR': 11.0, 'VRT1': 2.5, 'TOTAL': 11.0, 'CLIENTE': 'VÓ', 'VRT1_DZ': 4.4}, {'BRDZ_DZ': 4.0, 'VRDZ': 5.0, 'BRT1_DZ': 4.0, 'VRDZ_VLR': 21.0, 'BRT1': 5.0, 'BRDZ_VLR': 20.0, 'BRT1_VLR': 20.0, 'CLIENTE': 'NONOAI', 'VRDZ_DZ': 4.2, 'BRDZ': 5.0, 'TOTAL': 61.0}, {'VRT1_VLR': 11.0, 'VRT1': 2.5, 'TOTAL': 11.0, 'CLIENTE': 'CLÁUDIO', 'VRT1_DZ': 4.4}]
H19_09_18=[{'WEEK':2,'BRDZ_DZ': 93.0, 'BRT1_DZ': 84.0, 'BRT1': 6.0, 'BRT2': 5.0, 'BRT3': 12.0, 'BRMD_DZ': 93.0, 'BRT1_VLR': 504.0, 'BRT3_DZ': 70.0, 'VRT1_VLR': 90.0, 'BRDZ': 2.0, 'TOTAL': 2366.5, 'BRT3_VLR': 840.0, 'VRDZ': 3.0, 'BRT2_VLR': 400.0, 'VRDZ_VLR': 300.0, 'BRT2_DZ': 80.0, 'VRT1_DZ': 90.0, 'BRMD': 0.5, 'BRMD_VLR': 46.5, 'VRT1': 1.0, 'BRDZ_VLR': 186.0, 'CLIENTE': 'CARGA', 'VRDZ_DZ': 100.0}, {'BRT1_DZ': 4.0, 'TOTAL': 10.0, 'BRT1_VLR': 10.0, 'BRT1': 2.5, 'CLIENTE': 'ELIAS'}, {'BRT1_DZ': 4.0, 'VRT1_DZ': 4.0, 'VRT1_VLR': 20.0, 'VRT1': 5.0, 'TOTAL': 40.0, 'BRT1_VLR': 20.0, 'BRT1': 5.0, 'CLIENTE': 'DÉLCIO'}, {'BRT1': 7.5, 'TOTAL': 30.0, 'BRT1_VLR': 30.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'SIMONE'}, {'BRT1_DZ': 3.8, 'VRT1_DZ': 3.8, 'VRT1_VLR': 47.5, 'VRT1': 12.5, 'TOTAL': 180.5, 'BRT1_VLR': 133.0, 'BRT1': 35.0, 'CLIENTE': 'SAMUEL'}, {'TOTAL': 0.0, 'CLIENTE': 'MARLI'}, {'TOTAL': 0.0, 'CLIENTE': 'CÉZAR'}, {'BRT1': 7.5, 'TOTAL': 30.0, 'BRT1_VLR': 30.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'BOLACHA'}, {'BRT2_DZ': 4.0, 'TOTAL': 10.0, 'BRT2_VLR': 10.0, 'CLIENTE': 'JUVENTINO', 'BRT2': 2.5}, {'BRT3': 12.5, 'BRT3_VLR': 45.0, 'TOTAL': 45.0, 'CLIENTE': 'ZENOILDE', 'BRT3_DZ': 3.6}, {'VRDZ': 5.0, 'VRDZ_DZ': 4.8, 'VRT1_DZ': 4.4, 'VRDZ_VLR': 24.0, 'VRT1_VLR': 22.0, 'VRT1': 5.0, 'TOTAL': 46.0, 'CLIENTE': 'MÔNICA'}, {'BRT1_DZ': 4.0, 'TOTAL': 10.0, 'BRT1_VLR': 10.0, 'BRT1': 2.5, 'CLIENTE': 'IRACI'}, {'TOTAL': 0.0, 'CLIENTE': 'LAMB'}, {'BRT1': 2.5, 'TOTAL': 10.0, 'BRT1_VLR': 10.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'LOURDES'}, {'VRDZ': 5.0, 'TOTAL': 24.0, 'VRDZ_DZ': 4.8, 'CLIENTE': 'SERRINHA', 'VRDZ_VLR': 24.0}, {'VRDZ': 5.0, 'BRMD_DZ': 4.4, 'VRDZ_VLR': 22.0, 'BRMD': 5.0, 'BRMD_VLR': 22.0, 'VRMD_VLR': 22.0, 'CLIENTE': 'GIBA', 'VRMD_DZ': 4.4, 'VRDZ_DZ': 4.4, 'VRMD': 5.0, 'TOTAL': 66.0}, {'VRT1_VLR': 19.0, 'VRT1': 5.0, 'TOTAL': 19.0, 'CLIENTE': 'PEDRO', 'VRT1_DZ': 3.8}, {'BRT1': 12.5, 'TOTAL': 50.0, 'BRT1_VLR': 50.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'MARIA'}, {'TOTAL': 20.0, 'BRT1_VLR': 20.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'DANIEL', 'BRT1': 5.0}, {'BRDZ_DZ': 4.0, 'BRMD_DZ': 4.2, 'VRT1_DZ': 3.8, 'BRMD': 5.0, 'BRMD_VLR': 21.0, 'VRT1': 5.0, 'BRDZ_VLR': 20.0, 'CLIENTE': 'CLÁUDIO', 'VRT1_VLR': 19.0, 'BRDZ': 5.0, 'TOTAL': 60.0}, {'TOTAL': 0.0, 'CLIENTE': 'ANDRÉ'}, {'VRT1_VLR': 11.0, 'VRT1': 2.5, 'TOTAL': 11.0, 'CLIENTE': 'CARLOS', 'VRT1_DZ': 4.4}, {'TOTAL': 170.0, 'BRT1_VLR': 170.0, 'BRT1_DZ': 3.4, 'CLIENTE': 'AURÉLIO', 'BRT1': 50.0}, {'BRT3': 12.5, 'BRT3_VLR': 47.5, 'TOTAL': 47.5, 'CLIENTE': 'OBA OBA', 'BRT3_DZ': 3.8}, {'BRT2_DZ': 4.0, 'TOTAL': 40.0, 'BRT2_VLR': 40.0, 'CLIENTE': 'JÚNIOR', 'BRT2': 10.0}, {'TOTAL': 0.0, 'CLIENTE': 'PENNA'}, {'BRT2_VLR': 18.0, 'BRT1_DZ': 3.8, 'BRT2_DZ': 3.6, 'TOTAL': 27.5, 'BRT1_VLR': 9.5, 'BRT1': 2.5, 'BRT2': 5.0, 'CLIENTE': "DOG'S"}, {'TOTAL': 0.0, 'CLIENTE': 'TIA'}, {'BRDZ_DZ': 4.0, 'VRDZ': 10.0, 'BRT2_VLR': 119.0, 'VRDZ_VLR': 41.0, 'BRT2_DZ': 3.4, 'BRT2': 35.0, 'BRDZ_VLR': 80.0, 'CLIENTE': 'APARECIDA', 'VRDZ_DZ': 4.1, 'BRDZ': 20.0, 'TOTAL': 240.0}, {'BRT1': 12.5, 'TOTAL': 50.0, 'BRT1_VLR': 50.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'ANTÔNIO/BETTE'}, {'BRDZ_DZ': 4.2, 'VRDZ': 2.0, 'BRT1_DZ': 4.0, 'VRDZ_VLR': 8.8, 'VRT1_DZ': 4.0, 'BRT1': 15.0, 'VRT1': 2.5, 'BRDZ_VLR': 8.4, 'BRT1_VLR': 60.0, 'CLIENTE': 'ANTÔNIO TORRE', 'VRT1_VLR': 10.0, 'VRDZ_DZ': 4.4, 'BRDZ': 2.0, 'TOTAL': 87.2}, {'TOTAL': 38.0, 'BRT1_VLR': 38.0, 'BRT1_DZ': 3.8, 'CLIENTE': 'PRIMUS', 'BRT1': 10.0}, {'TOTAL': 0.0, 'CLIENTE': 'JAIR'}, {'BRT3': 195.0, 'BRT3_VLR': 585.0, 'TOTAL': 585.0, 'CLIENTE': 'FREEWAY', 'BRT3_DZ': 3.0}, {'BRT2_DZ': 3.4, 'BRT2': 17.5, 'TOTAL': 59.5, 'CLIENTE': 'PAULO', 'BRT2_VLR': 59.5}, {'BRT3': 12.5, 'BRT3_VLR': 45.0, 'TOTAL': 45.0, 'CLIENTE': 'TIA GETNET', 'BRT3_DZ': 3.6}, {'BRT3_DZ': 3.6, 'BRT3_VLR': 36.0, 'TOTAL': 36.0, 'CLIENTE': 'VÔ GETNET', 'BRT3': 10.0}, {'BRT3': 112.5, 'BRT3_VLR': 337.5, 'TOTAL': 337.5, 'CLIENTE': 'BOKAS', 'BRT3_DZ': 3.0}, {'VRDZ': 20.0, 'BRT1_DZ': 4.0, 'VRDZ_VLR': 80.0, 'BRT1': 10.0, 'VRDZ_DZ': 4.0, 'TOTAL': 120.0, 'BRT1_VLR': 40.0, 'CLIENTE': 'PAULO ROSA'}]
H20_09_18=[{'WEEK':3,'VRT1_VLR': 90.0, 'VRT1': 1.0, 'TOTAL': 90.0, 'CLIENTE': 'CARGA', 'VRT1_DZ': 90.0}, {'TOTAL': 0.0, 'CLIENTE': 'RICCI'}, {'TOTAL': 0.0, 'CLIENTE': 'JOEL'}, {'BRT1_DZ': 3.6, 'TOTAL': 135.0, 'BRT1_VLR': 135.0, 'BRT1': 37.5, 'CLIENTE': 'DAIANE'}, {'BRT2_VLR': 48.0, 'BRT1_DZ': 4.0, 'BRT2_DZ': 3.2, 'TOTAL': 58.0, 'BRT1_VLR': 10.0, 'BRT1': 2.5, 'BRT2': 15.0, 'CLIENTE': 'PARANÁ'}, {'BRT1': 15.0, 'TOTAL': 51.0, 'BRT1_VLR': 51.0, 'BRT1_DZ': 3.4, 'CLIENTE': 'JULIANO'}, {'VRT1_VLR': 44.0, 'VRT1': 10.0, 'TOTAL': 44.0, 'CLIENTE': 'MARLI', 'VRT1_DZ': 4.4}, {'BRT1_DZ': 4.0, 'TOTAL': 20.0, 'BRT1_VLR': 20.0, 'BRT1': 5.0, 'CLIENTE': 'ANTÔNIO'}, {'BRT1_DZ': 4.0, 'VRT1_DZ': 4.0, 'VRT1_VLR': 30.0, 'VRT1': 7.5, 'TOTAL': 80.0, 'BRT1_VLR': 50.0, 'BRT1': 12.5, 'CLIENTE': 'ZÉ'}, {'TOTAL': 0.0, 'CLIENTE': 'ALEXANDRE'}, {'VRT1_VLR': 44.0, 'VRT1': 10.0, 'TOTAL': 44.0, 'CLIENTE': 'FLORES', 'VRT1_DZ': 4.4}, {'VRT1_VLR': 20.0, 'VRT1': 5.0, 'TOTAL': 20.0, 'CLIENTE': 'JÔ', 'VRT1_DZ': 4.0}, {'BRT2_DZ': 4.0, 'BRT2_VLR': 60.0, 'TOTAL': 60.0, 'CLIENTE': 'ALCEMAR', 'BRT2': 15.0}, {'BRT1': 10.0, 'TOTAL': 40.0, 'BRT1_VLR': 40.0, 'BRT1_DZ': 4.0, 'CLIENTE': 'ALEMÃO'}, {'BRT3_VLR': 63.0, 'BRT2_VLR': 9.0, 'BRT1_DZ': 4.0, 'BRT3_DZ': 3.6, 'BRT2_DZ': 3.6, 'BRT1': 7.5, 'BRT2': 2.5, 'BRT3': 17.5, 'TOTAL': 102.0, 'BRT1_VLR': 30.0, 'CLIENTE': 'JÚLIO'}]
