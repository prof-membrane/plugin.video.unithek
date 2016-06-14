import urllib,urllib2,re,random,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime,xbmc,xbmcaddon,xbmcvfs,time,string,sys,hashlib
#import urllib,urllib2,re,       xbmcplugin,xbmcgui,xbmcaddon,string,random,cookielib

__settings__ = xbmcaddon.Addon(id='plugin.video.unithek')
addon = xbmcaddon.Addon()
COOKIEFILE = xbmc.validatePath(xbmc.translatePath(__settings__.getAddonInfo('profile')+"cookies.lwp"))
USERDATAPATH = xbmc.validatePath(xbmc.translatePath(__settings__.getAddonInfo('profile')))
COOKIEFILE = COOKIEFILE.replace('\\\\','\\')
pluginhandle = int(sys.argv[1])

def hash(s):
	return hashlib.md5(s).hexdigest()
def f_basepath():
	return __settings__.getAddonInfo('profile')
def f_translate_path(path):
	return xbmc.validatePath(xbmc.translatePath(path))
def f_check_existance(path):
	return xbmcvfs.exists(path)
def f_rmdir(path):
	return xbmcvfs.rmdir(path)
def f_mkdir(path):
	return xbmcvfs.mkdir(path)
	
def f_open(path):
	f = xbmcvfs.File(path)
	result = f.read()
	f.close()
	return result

def f_write(path,data):
	print 'writing to '+path
	f = xbmcvfs.File(path, 'w')
	result = f.write(data)
	f.close()
	return True
	

def request(url,method='get',data=''):
	if method == 'get':
		GET(url)
	elif method == 'post':
		POST(url,data)
		
def GET(url):
	print url
	cj = cookielib.LWPCookieJar()
	cj.load(COOKIEFILE, ignore_discard=True)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
	usock=opener.open(url)
	response=usock.read()
	usock.close()
	cj.save(COOKIEFILE, ignore_discard=True)
	#print response
	return response
	
def POST(url,data):
	cj = cookielib.LWPCookieJar()
	cj.load(COOKIEFILE, ignore_discard=True)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
	usock=opener.open(url,data=urllib.urlencode(data))
	response=usock.read()
	usock.close()
	cj.save(COOKIEFILE, ignore_discard=True)
	return response
	
def DEL_COOKIES():
	xbmcvfs.delete(COOKIEFILE)
	
def epoch(ms=False):
	if ms:
		return int(time.time() * 1000)
	else:
		return int(time.time())
	
def log(s):
	if __settings__.getSetting('debug') == "true":
		print '### AIP log: '+s

def char_gen(size=1, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))

def num_gen(size=1, chars=string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	try:
		quality=iconimage.split('.')[-2]
		iconimage = iconimage.replace(quality,'_UY500_')
	except:
		iconimage = iconimage.replace('._UY200_.jpg','._UY500_.jpg')
	print iconimage
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	
def addLink(name,url,mode,iconimage,plot='',runtime='0'):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	try:
		quality=iconimage.split('.')[-2]
		iconimage = iconimage.replace(quality,'_UY500_')
	except:
		iconimage = iconimage.replace('._UY200_.jpg','._UY500_.jpg')

	print iconimage
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "plotoutline": plot  } )
	liz.setProperty('IsPlayable', 'true')
	#if __settings__.getSetting('hq_thumbnail') == '2':
	#	liz.setProperty('fanart_image',iconimage)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok
	

if not xbmcvfs.exists(COOKIEFILE):
	f_mkdir(USERDATAPATH)
	cj = cookielib.LWPCookieJar()
	cj.save(COOKIEFILE, ignore_discard=True)
	#f = xbmcvfs.File(COOKIEFILE, 'w')
	#result = f.write('')
	#f.close()