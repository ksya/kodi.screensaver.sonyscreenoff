# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import sys
import xbmcaddon
from resources.lib.bravialib import Bravia


ADDON = "screensaver.sonyscreenoff"
__addon__ = xbmcaddon.Addon(id=ADDON)
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

CLIENTID_PREFIX = 'KodiScreensaver'
NICKNAME = 'Kodi Screensaver'

pin = __addon__.getSetting('code')
ip = __addon__.getSetting('ipaddress')



notifytime = 3000 #in miliseconds

def __getArguments():
    data = None

    if len(sys.argv) > 1:
        data = {}
        for item in sys.argv:
            values = item.split("=")
            if len(values) == 2:
                data[values[0].lower()] = values[1]
        #data['action'] = data['action'].lower()

    return data

def Main():
    tv = Bravia(ip)
    tv.device_id = CLIENTID_PREFIX
    tv.nickname = NICKNAME

    is_telly_on = tv.is_available()
    if is_telly_on is False:
        xbmc.log("Not able to connect to the TV.")
        sys.exit(1)


    args = __getArguments()
    data = {}
    note = ""

    if args['action'] == 'start_pair':
        xbmc.log("Started pairing")

        response, state = tv.connect()
        if state is True:
            notify("Already paired and connected to the TV.")
        else:
            tv.start_pair()

            notify("Now fill in the code visible on the TV.")

            d = xbmcgui.Dialog().input(__addonname__, type=xbmcgui.INPUT_NUMERIC) 
            __addon__.setSetting('code', d)

            r,status = tv.complete_pair(d)

            if status is True:
                #data = json.dumps(tv.system_info, sort_keys=True, indent=4)
                note = "Successfully paired!"
            else:
                note = "Something went wrong in the pairing process."

            notify(note)

    elif args['action'] == 'test':
        xbmc.log("Test")

        response, state = tv.connect()
        if type(response) is not None:
            try:
                if response.status_code == 401:
                    note = "Not paired yet!"
                elif response.status_code == 200:
                    note = "Paired!"
                else:
                    note = "Something went wrong here. Response code problem."
            except:
                note = "Something went wrong here. Exception."
        else:
            note = "Something went wrong here. Response type problem."

        notify(note)


def notify(note):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__, note, notifytime, __icon__))


if __name__ == '__main__':
    Main()

