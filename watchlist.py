# -*- coding: utf-8 -*-
# 

import os
import xbmc,xbmcaddon,xbmcgui
import time, socket

try: import simplejson as json
except ImportError: import json

from utilities import *

try:
    # Python 3.0 +
    import http.client as httplib
except ImportError:
    # Python 2.7 and earlier
    import httplib

try:
  # Python 2.6 +
  from hashlib import sha as sha
except ImportError:
  # Python 2.5 and earlier
  import sha

__author__ = "Ralph-Gordon Paul, Adrian Cowan"
__credits__ = ["Ralph-Gordon Paul", "Adrian Cowan", "Justin Nemeth",  "Sean Rudford"]
__license__ = "GPL"
__maintainer__ = "Ralph-Gordon Paul"
__email__ = "ralph-gordon.paul@uni-duesseldorf.de"
__status__ = "Production"

# read settings
__settings__ = xbmcaddon.Addon( "script.traktutilities" )
__language__ = __settings__.getLocalizedString

apikey = '0a698a20b222d0b8637298f6920bf03a'
username = __settings__.getSetting("username")
pwd = sha.new(__settings__.getSetting("password")).hexdigest()
debug = __settings__.getSetting( "debug" )
https = __settings__.getSetting('https')

if (https == 'true'):
    conn = httplib.HTTPSConnection('api.trakt.tv')
else:
    conn = httplib.HTTPConnection('api.trakt.tv')

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

# list watchlist movies
def showWatchlistMovies():
    
    movies = getWatchlistMoviesFromTrakt()
    
    if movies == None: # movies = None => there was an error
        return # error already displayed in utilities.py
    
    if len(movies) == 0:
        xbmcgui.Dialog().ok(__language__(1201).encode( "utf-8", "ignore" ), __language__(1160).encode( "utf-8", "ignore" )) # Trakt Utilities, there are no movies in your watchlist
        return
        
    # display watchlist movie list
    import windows
    ui = windows.MoviesWindow("movies.xml", __settings__.getAddonInfo('path'), "Default")
    ui.initWindow(movies, 'watchlist')
    ui.doModal()
    del ui

# list watchlist tv shows
def showWatchlistTVShows():

    tvshows = getWatchlistTVShowsFromTrakt()
    
    if tvshows == None: # tvshows = None => there was an error
        return # error already displayed in utilities.py
    
    if len(tvshows) == 0:
        xbmcgui.Dialog().ok(__language__(1201).encode( "utf-8", "ignore" ), __language__(1161).encode( "utf-8", "ignore" )) # Trakt Utilities, there are no tv shows in your watchlist
        return
    
    # display watchlist tv shows
    import windows
    ui = windows.TVShowsWindow("tvshows.xml", __settings__.getAddonInfo('path'), "Default")
    ui.initWindow(tvshows, 'watchlist')
    ui.doModal()
    del ui
    
