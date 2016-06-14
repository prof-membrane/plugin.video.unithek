# -*- coding: utf-8 -*-
from time import *
from datetime import date, timedelta
import time
import xbmc
startTime = int(round(time.time() * 1000))
def log(message = False):
	xbmc.log('Unithek Log: '+str(message))
def logTime():
	xbmc.log('Unithek Log: Runtime '+str(int(round(time.time() * 1000)) - startTime)+'ms')

log('Starting')	
logTime()	
import urllib,urllib2,re,random,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime
#from time import *
#from datetime import date, timedelta
from operator import itemgetter
#import time
import resources.lib.utils as utils
import libArd
import libArte
import libZdf
__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString
addon = xbmcaddon.Addon()
translation = addon.getLocalizedString

dir = xbmc.validatePath(xbmc.translatePath(__settings__.getAddonInfo('profile')))
if not utils.f_check_existance(dir):
	utils.f_mkdir(dir)

ardLimit = int(addon.getSetting("ardLimit"))
zdfLimit = int(addon.getSetting("zdfLimit"))
showSubtitles = addon.getSetting("showSubtitles") == "true"
hideAudioDisa = addon.getSetting("hideAudioDisa") == "true"
helix = False

html_parser = HTMLParser.HTMLParser()

month = strftime("%m", gmtime())
year = strftime("%Y", gmtime())
startTime = int(round(time.time() * 1000))
viewMode = '515'
viewModeA = '515'
viewModeB = '515'
baseArd = 'http://ardmediathek.de'
pluginhandle = int(sys.argv[1])


cannelList = [['3sat',                  'ZDF',  '1209116'],
			  ['ARD-alpha',             'ARD',  '5868'   ],
			  ['Arte',                  'Arte', ''       ],
			  ['BR',                    'ARD',  '2224'   ],
			  #['Einsfestival',          'ARD',  '673348' ],
			  ['EinsPlus',              'ARD',  '4178842'],
			  ['Das Erste',             'ARD',  '208'    ],
			  ['HR',                    'ARD',  '5884'   ],
			  ['MDR Fernsehen',         'ARD',  '5882'   ],
			  ['MDR Thüringen',         'ARD',  '1386988'],
			  ['MDR Sachsen',           'ARD',  '1386804'],
			  ['NDR Fernsehen',         'ARD',  '5906'   ],
			  ['Phoenix',               'ZDF',  '2256088'],
			  ['RB',                    'ARD',  '5898'   ],
			  ['RBB',                   'ARD',  '5874'   ],
			  ['SR',                    'ARD',  '5870'   ],
			  ['SWR Fernsehen',         'ARD',  '5310'   ],
			  ['SWR Rheinland-Pfalz',   'ARD',  '5872'   ],
			  ['SWR Baden-Württemberg', 'ARD',  '5904'   ],
			  ['tagesschau24',          'ARD',  '5878'   ],
			  ['WDR',                   'ARD',  '5902'   ],
			  ['ZDF',                   'ZDF',  '1209114'],
			  ['ZDFinfo',               'ZDF',  '1209120'],
			  ['ZDF.kultur',            'ZDF',  '1317640'],
			  ['ZDFneo',                'ZDF',  '1209122']]

weekdayDict = { '0': translation(31013),#Sonntag
				'1': translation(31014),#Montag
				'2': translation(31015),#Dienstag
				'3': translation(31016),#Mittwoch
				'4': translation(31017),#Donnerstag
				'5': translation(31018),#Freitag
				'6': translation(31019)}#Samstag

arteDict = { 'Dokumentationen': 'http://www.arte.tv/guide/de/plus7/par_themes?value=DOC',
             'Kino':            'http://www.arte.tv/guide/de/plus7/par_themes?value=CIN',
             'Kultur':          'http://www.arte.tv/guide/de/plus7/par_themes?value=ART',
             'Sport':           False,
             'Technik':         False,
             'Wissen':          'http://www.arte.tv/guide/de/plus7/par_themes?value=ENV'}
zdfDict = {  'Dokumentationen': 'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=546',
             'Kino':            'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=548',
             'Kultur':          'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=554',
             'Sport':           'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=610',
             'Technik':         'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=558',
             'Wissen':          'http://www.zdf.de/ZDFmediathek/xmlservice/web/aktuellste?maxLength=50&id=570'}
ardDict = {  'Dokumentationen': '/tv/Reportage-Doku/mehr?documentId=21301806',
             'Kino':            '/tv/Film-Highlights/mehr?documentId=21301808',
             'Kultur':          '/tv/Kultur/mehr?documentId=21282546',
             'Sport':           '/tv/Sport-in-der-Mediathek/mehr?documentId=26439062',
             'Technik':         '/einslike/Netz-Tech/mehr?documentId=21301898',
             'Wissen':          '/tv/Wissen/mehr?documentId=21282530'}
log("Init time:")
logTime()

def MAIN():
	addDir({'name':translation(31030), 'mode':100})
	addDir({'name':translation(31031), 'mode':101})
	addDir({'name':translation(31032), 'mode':1  })
	addDir({'name':translation(31033), 'mode':110})
	addDir({'name':'Suche',            'mode':'search'})
		
def LISTNEW():#100
	items  = libArd.getNew()
	items += libZdf.getNew()
	addEntries(items)
	
def LISTMV():#101
	items  = libArd.getMostViewed()
	items += libZdf.getMostViewed()
	addEntries(items)
	
def listShowsAZMain():#1
	dict = {}
	dict['name'] = "0-9"
	dict['letter'] = "#"
	dict['mode'] = 'listShows'
	addDir(dict)
	letters = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
	for letter in letters:
		dict['name'] = letter.upper()
		dict['letter'] = letter.upper()
		addDir(dict)
	
def listShows():#2
	letter = params["letter"]
	list = []
	logTime()
	items = libArd.getAZ(letter)
	items += libZdf.getAZ(letter.replace('#','0%2D9'))
	for dict in items:
		dict['sortName'] = convSortName(dict['name'],letter.replace('#','0'))
		list.append(dict)
	logTime()
	sortedList = sorted(list, key=itemgetter('sortName'))
	for dict in sortedList:#adds ' - $channel' to name if there are multiple channels
		dict['showname'] = dict['name']
		i=0
		j=0
		while i < len(sortedList):
			if dict['name'] == sortedList[i]['name']:
				j += 1
			i += 1
		if j > 1:
			dict['name'] += ' - '+dict['channel']
		addDir(dict)
	
def listDates():#110
	dict = {}
	dict['mode'] = 111
	dict['name'] = translation(31020)
	dict['datum']  = '0'
	addDir(dict)
	dict['name'] = translation(31021)
	dict['datum']  = '1'
	addDir(dict)
	i = 2
	while i <= 6:
		day = date.today() - timedelta(i)
		dict['name'] = weekdayDict[day.strftime("%w")]
		dict['datum'] = str(i)
		addDir(dict)
		i += 1
	
def listChannels():#111
	datum = params['datum']
	day = date.today() - timedelta(int(datum))
	ddmmyy = day.strftime('%d%m%y')
	libArd.libArdListDateChannels(datum)
	libZdf.listDateChannels(datum)
	xbmcplugin.addSortMethod(pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE )
	
def search():
	addDir({'name':'Allgemeine Suche', 'mode':'generalSearch'})
	addDir({'name':'Detailsuche ARD', 'mode':'libArdSearch'})
	addDir({'name':'Detailsuche ZDF', 'mode':'libZdfSearch'})
	
def generalSearch():
	keyboard = xbmc.Keyboard('', "TODO")
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		search_string = keyboard.getText()
		items = libArd.getSearch(search_string)
		items += limitEntries(libZdf.getSearch(search_string), 20, True)
		addEntries(items)

def limitEntries(items, i = 50, videosOnly=False):
	result = []
	n = 1
	for dict in items:
		if dict["type"] == "video" or not videosOnly:
			result.append(dict)
			n += 1
			if n > i:
				break
	return result
	
def convSortName(name,firstletter):
	firstletter = firstletter.lower()
	#hardcoded
	if firstletter != '0':
		name = name.replace('7 Tage','Sieben Tage')
	#umlaute
	name = name.replace('ä','a')
	name = name.replace('ö','o')
	name = name.replace('ü','u')
	name = name.replace('"','')
	name = name.replace('-','')
	name = name.replace("'",'')
	name = name.replace(".",'')
	#artikel entfernen:
	if name.startswith('Der ') or name.startswith('der ') or name.startswith('Die ') or name.startswith('die ') or name.startswith('Das ') or name.startswith('das '):
		name = name[4:]
	if name.startswith('zdf') or name.startswith('ZDF') or name.startswith('Zdf'):
		name = name[3:]
	while name.startswith(' '):
		name = name[1:]
	name = name.lower()
	#find first ' s':
	if not name.startswith(firstletter):
		if ' '+firstletter in name:
			width = len(name.split(' '+firstletter)[0]) + 1
			name = name[width:]
		elif firstletter in name:
			width = len(name.split(firstletter)[0])
			name = name[width:]
	return name

def get_params():
	param={}
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

def addEntries(list):
	for dict in list:
		if dict["type"] == "video":
			addLink(dict)
		else:
			addDir(dict)
	xbmcplugin.addSortMethod(pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE )

def addLink(dict):	
	if hideAudioDisa:
		if 'Hörfassung' in dict['name'] or 'Audiodeskription' in dict['name'] or '(AD)' in dict['name']:
			return False
	#u=sys.argv[0]+"?url="+urllib.quote_plus(dict['url'])+"&mode="+str(dict['mode'])+"&name="+urllib.quote_plus(dict['name'])
	u = makeUrl(dict)
	ok=True
	liz=xbmcgui.ListItem(dict['name'], iconImage="DefaultVideo.png", thumbnailImage=dict['thumb'])
	liz.setInfo( type="Video", infoLabels={ "Title": dict['name'] , "Plot": dict.get("plot","") , "Plotoutline": dict.get("plot","") , "Duration": dict.get("duration","") } )
	liz.setProperty('IsPlayable', 'true')
	if 'fanart' in dict:
		liz.setProperty('fanart_image',dict["fanart"])
	else:
		liz.setProperty('fanart_image',dict['thumb'])
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(dict):
	u = makeUrl(dict)
	ok=True
	liz=xbmcgui.ListItem(dict.get('name',''), iconImage="DefaultFolder.png", thumbnailImage=dict.get('thumb',''))
	liz.setInfo( type="Video", infoLabels={ "Title": dict.get('name','') , "Plot": dict.get('plot','') , "Plotoutline": dict.get('plot','') } )
	liz.setProperty('fanart_image',dict.get('thumb',''))
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def makeUrl(dict):
	u = sys.argv[0]+'?'
	i = 0
	for key in dict.keys():
		if i > 0:
			u += '&'
		u += key + '=' + urllib.quote_plus(str(dict[key]))
		i += 1
	return u


params=get_params()

for key,val in params.items():
	try:
		params[key] = urllib.unquote_plus(val)
	except: 
		log('Cant unquote this: '+ str(val))

if not params.has_key('mode'):
	MAIN()
elif params["mode"].startswith('libArd'):
	libArd.list(params)
elif params["mode"].startswith('libZdf'):
	libZdf.list(params)

elif params['mode']=='search':
	search()
elif params['mode']=='generalSearch':
	generalSearch()
	
elif params['mode']=='1':
	listShowsAZMain()
elif params['mode']=='listShows':
	listShows()
elif params['mode']=='100':
	LISTNEW()
elif params['mode']=='101':
	LISTMV()
elif params['mode']=='110':
	listDates()
elif params['mode']=='111':
	listChannels()
else:
	MAIN()

xbmcplugin.endOfDirectory(pluginhandle)

logTime()	