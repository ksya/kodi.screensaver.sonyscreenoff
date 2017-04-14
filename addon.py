import xbmc
import xbmcaddon
# LIB_DIR = xbmc.translatePath(
#     os.path.join(xbmcaddon.Addon(id="plugin.video.dumpert").getAddonInfo('path'), 'resources', 'lib'))
# sys.path.append(LIB_DIR)

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))
# from kodipopcorntime import monkey_patches, plugin


from resources.lib.bravialib import Bravia
import sys
import json

ADDON = "screensaver.sonyscreenoff"
__addon__ = xbmcaddon.Addon(id=ADDON)
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

CLIENTID_PREFIX = 'KodiScreensaver'
NICKNAME = 'Kodi Screensaver'
pin = __addon__.getSetting('code')
ip = __addon__.getSetting('ipaddress')

notifytime = 3000 #in miliseconds

def Main():
    tv = Bravia(ip)
    tv.device_id = CLIENTID_PREFIX
    tv.nickname = NICKNAME

    checkTvIsOn(tv)
    success, note = checkConnection(tv)

    if not xbmc.Player().isPlayingAudio():
        if success:
            tv.do_remote_control("PicOff")
        else:
            notify(note)

def notify(note):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__, note, notifytime, __icon__))

def checkTvIsOn(tv):
    is_telly_on = tv.is_available()
    if is_telly_on is False:
        notify("Not able to connect to the TV.")
        sys.exit(1)

def checkConnection(tv):
    success = False
    note = ""

    response, state = tv.connect()
    if type(response) is not None:
        try:
            if response.status_code == 401:
                note = "Not paired yet!"
            elif response.status_code == 200:
                success = True
                note = "Succes! TV is already paired!"
            else:
                note = "Something went wrong here. Response code problem."
        except:
            note = "Something went wrong here. Exception."
    else:
        note = "Something went wrong here. Response type problem."

    return success, note

if __name__ == '__main__':
    Main()

