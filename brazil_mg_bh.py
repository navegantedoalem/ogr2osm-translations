"""
Translation rules for Brazilian city Belo Horizonte, state of Minas Gerais

Example:
curl -o TEMP_BHMAP_ENDERECO_PBH.xml 'http://bhmap.pbh.gov.br/v2/api/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=germem:BHMAP_ENDERECO_PBH&SRSNAME=urn:ogc:def:crs:EPSG::31983&urn:ogc:def:crs:EPSG::31983&OUTPUTFORMAT=GML3&STARTINDEX=0&COUNT=100'
python3 ./ogr2osm/ogr2osm.py -fv --epsg=31983 --encoding=ISO8859-1 TEMP_BHMAP_ENDERECO_PBH.xml --translation=brazil_mg_bh

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
	tags.update({'source':'bhmap.pbh.gov.br'})
	#automagically convert names
	if attrs.get('NOME_LOGRADOURO'):
		street = ""
		if attrs.get('SIGLA_TIPO'):
			street +=  string.capwords(sigla(attrs['SIGLA_TIPO'])) + ' '
		street += string.capwords(attrs['NOME_LOGRADOURO'].strip(' '))
		tags.update({'addr:street':street})

	if attrs.get('NUMERO_IMOVEL'):
		housenumber = "%d"%float(attrs['NUMERO_IMOVEL'].strip(' '))
		if attrs.get('LETRA_IMOVEL'):
			housenumber += ' ' + attrs['LETRA_IMOVEL'].strip(' ')
		tags.update({'addr:housenumber':housenumber})

	if attrs.get('CEP'):
		cep = "%d"%float(attrs['CEP'].strip(' '))
		cep = cep[:5]+'-'+cep[5:]
		tags.update({'addr:postcode':cep})

	return tags

