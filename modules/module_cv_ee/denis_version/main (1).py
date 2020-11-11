
#___________________________________________________________
############################################################
#import sys
#import requests
#from urllib.parse import urljoin, urlparse
#from bs4 import BeautifulSoup

import os
import re
import _


global ERRORCNTR

ERRORCNTR = 0

#___________________________________________________________
############################################################

# generate test file(s) ?

#What this fucntion does
def	unescape(t):
	return t

def	getfield(src, rxp, grp):

	m = re.search(rxp, src)
	if m:
		return unesc( m[ grp ] )

# vacancy-item__info-main">
# secondary-text">Avaldatud 10 kuud tagasi

def	getvacancy( t ):

	a = re.sub( '><', '>\x0D\x0A<', t )
	_.wrfile( 'html.txt', a )
	vacancy_split_pattern	 = 'vacancy-item">'
	title_rxp = re.compile( 'vacancy-item__title">([^<]*)' )
	howold_rxp = re.compile( 'secondary-text">Avaldatud ([0-9]+)' )
	information_rxp = re.compile( 'vacancy-item__info-main">([^<>]*)' )
	link_rxp = re.compile( 'href="([^"]*)' )
	deadline_rxp = 'htaeg: ([0-9\.\-/]+)'
	V = t.split( vacancy_split_pattern )

	L = []

	f = 2

	for v in V:

		f -= 1

		if f == 1:

			continue

		if f == 0:

			a = re.sub('><', '>\x0D\x0A<', v )

			_.wrfile( "vacancy.txt", a )


		title = getfield( v, title_rxp, 1 )

		howold = getfield( v, howold_rxp, 1 )

		information = getfield( v, information_rxp, 1 )

		url = "https://cv.ee" + getfield( v, link_rxp, 1 )

		print( "title ", title, "'" )
		print( "howold ", howold, " months ago" )
		print( "host ", information, "'" )
		print( "url: ", url, "'" )

		t = _.rdurl( url )

		deadline = getfield( t, deadline_rxp, 1 )

		print( "deadline: ", deadline, "'" )

		t = re.sub('><', '>\x0D\x0A<', t )

		_.wrfile( 'vhtml.txt', t )




		print()

	#print( len( V ), " vacancies / errors: ", ERRORCNTR, "'" )

	return L



url = 'https://www.cv.ee/search?limit=10000&offset=0&isHourlySalary=false'

L = getvacancy( _.rdurl( url ) )

exit(0)


