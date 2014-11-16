#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xchat
import re
import string


__module_name__ = 'xchat_smiley_reversal'
__module_version__ = '1.0'
__module_description__ = 'For correcting other people\'s annoying reverse smileys.'

###################################### SETTINGS ######################################
# Specify channel names (preceded by #, in lower-case) where plugin will take effect
# Example: channel = ('#hackerz', '#general')
channels = ('#omoi')
######################################################################################

# smiley match regex
smiley = re.compile(r'''(([/\\()\[\]0OoSsVvdIiXxiwW$#<*>])\2*[']{0,5}[-]?[:;=x8]+)''')

# In Python 2.6, instead of using maptrans(), we define a dict with unicode ordinals
tabin = u'()[]\\/><d'
tabout = u')(][/\\<>p'
tabin = [ord(char) for char in tabin]
trans_map = dict(zip(tabin, tabout))


def reverse(word, word_eol, userdata):
    """
        X-Chat callback that checks Channel Messages for reverse-smileys,
        reverses the string, maps non-symmetric chars to their mirror counterparts.
        Echoes reversed reverse-smileys to channel in context.
        
        Example: 'd:' turns into ':p'
    """
    channel = xchat.get_info('channel').lower()
    if channel in channels:
        words = word[1].split(' ')
        end_smiley = None
        for w in words:
            wordd = w.decode('utf-8')
            m = re.match(smiley, wordd)
            if m and len(m.group()) == len(wordd):
                end_smiley = wordd[::-1].translate(trans_map).encode('utf-8')
        if end_smiley:
            xchat.command('msg {0} {1}'.format(channel, end_smiley))
    return xchat.EAT_NONE

xchat.hook_print('Channel Message', reverse)
