"""
Translation rules for Brazilian city Belo Horizonte, state of Minas Gerais

Copyright 2019

"""
import string

def sigla(tag):
	addrtypemap = {
        "ACS":"ACESSO",
        "ALA":"ALAMEDA",
        "AVE":"AVENIDA",
        "BEC":"BECO",
        "ELP":"ESPACO LIVRE DE USO PUBLICO",
        "EST":"ESTRADA",
        "LRG":"LARGO",
        "PCA":"PRACA",
        "RDP":"RUA DE PEDESTRE",
        "ROD":"RODOVIA",
        "RUA":"RUA",
        "TRE":"TREVO",
        "TRI":"TRINCHEIRA",
        "TRV":"TRAVESSA",
        "VDP":"VIA DE PEDESTRE",
        "VDT":"VIADUTO",
        "VIA":"VIA"
        #"":"PASSARELA"
        #"":"PISTA DE COOPER"
        #"":"QUARTEIRAO FECHADO"
        #"":"TUNEL"
    }
	return addrtypemap.get(tag.upper()) or tag

def filterFeature(ogrfeature, fieldNames, reproject):
	if ogrfeature is None:
		return
	if ogrfeature.GetFieldAsString("STATUS") == "Inexistente":
		return
	return ogrfeature

def filterTags(attrs):
	if not attrs: return

	tags = {}
	#Add the source
	#tags.update({'source':'Layer Enderecamento from http://bhmap.pbh.gov.br parsed with --translation=brazil_mg_bh --encoding=ISO8859-1'})
	#automagically convert names
	if attrs.get('NOME_LOGRA'):
		street = ""
		if attrs.get('SIGLA_TIPO']:
			street +=  string.capwords(sigla(attrs['SIGLA_TIPO'])) + ' '
		street += string.capwords(attrs['NOME_LOGRA'].strip(' '))
		tags.update({'addr:street':street})

	if attrs.get('NUMERO_IMO'):
		housenumber = "%d"%float(attrs['NUMERO_IMO'].strip(' '))
		if attrs.get('LETRA_IMOV'):
			housenumber += ' ' + attrs['LETRA_IMOV'].strip(' ')
		tags.update({'addr:housenumber':housenumber})

	if attrs.get('CEP'):
		cep = "%d"%float(attrs['CEP'].strip(' '))
		cep = cep[:5]+'-'+cep[5:]
		tags.update({'addr:postcode':cep})

	return tags

