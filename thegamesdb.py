#!/bin/env python
# -*- coding: utf-8 -*-
#
#
# Changelog
# 2013/11/08:
# * Changed to urllib2
# * Added User-Agent to workaround "Cloudfare ban" (http://forums.thegamesdb.net/showthread.php?tid=1577&pid=3157#pid3157)
#
import sys, os, re, time, urllib2
import xml.etree.ElementTree as ET

class theGamesDB():
    def __init__(self):
        self.debug = False
        self.useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'
        self.apiurl = 'http://thegamesdb.net/api/'
        self.debugurl = 'http://mameau:8315/thegamesdb/'
        return

    def readUrl(self, arg):
        ''' Format & read URL '''
        url = '%s%s' % (self.apiurl,arg)
        if self.debug:
            url = '%s%s.xml' % (self.debugurl,arg)
        if url:
            url = urllib2.Request(url)
            url.add_unredirected_header('User-Agent', self.useragent)
            resp = urllib2.urlopen(url)
            resp_code = resp.getcode()
            if resp_code == 200:
                return resp
            else:
                pass
        else:
            pass
        return None

    def getAPI(self, id, api, debugapi):
        ''' Process API Arguement based on debug condition'''
        if self.debug:
            return self.readUrl('%s_%d' % (debugapi,id))
        else:
            return self.readUrl('%s=%d' % (api,id))

    def getPlatformList(self, ):
        ''' Process the Platformlist'''
        return self.readUrl('GetPlatformsList.php')

    def readXML(self, xmlResp):
        tree = ET.parse(xmlResp)
        return tree.getroot()

    def menuXML(self, xmltree, tag):
        l = []
        for platform in xmltree[1].findall(tag):
            id = platform.find('id').text
            name = platform.find('name').text
            l.append([id, name])
            sorted(l, key=lambda name: name[1])
        return l

    def gameXML(self, xmltree, tag, p):
        ''' Temporary function imported from old data to process xml and download files '''
        if xmltree.tag == tag:
            for game in xmltree:
                for detail in game:
                    clean_name = None
                    if detail.tag == 'id':
                        game_id = detail.text
                    if detail.tag == 'GameTitle':
                        unicode_clean = detail.text.encode(sys.stdout.encoding, 'replace')
                        if unicode_clean:
                            # Identified Special Cases
                            if ":" in unicode_clean:
                                unicode_clean = unicode_clean.replace(':', ' -')
                            if "?" in unicode_clean:
                                unicode_clean = unicode_clean.replace('?', '-')
                            if "//" in unicode_clean:
                                unicode_clean = unicode_clean.replace('//', '- ')
                            unicode_clean = re.sub('[^A-Za-z0-9\s\'\,\(\)\[\]\-\&\.\!]+', ' ', unicode_clean)
                            clean_name = unicode_clean
                        else:
                            pass
                    if detail.tag == 'ReleaseDate':
                        pass
                    if game_id and clean_name:
                        outpath = os.path.join('xml',p)
                        if not os.path.exists(outpath):
                            os.mkdir(outpath)
                        outfile = os.path.join(outpath,clean_name+'.xml')
                        if not os.path.exists(outfile):
                            print "Now at: %s with ID: %s" % (clean_name, game_id)
                            g_ids = self.getAPI(int(game_id),'GetGame.php?id','game')
                            if g_ids:
                                    with open(outfile, 'w') as f:
                                        for line in g_ids:
                                            f.write(line)
                                        f.close()
                            else:
                                pass
                        else:
                           print "SKIPPING! file exists: %s" % clean_name
                time.sleep(0)


    def gameART(self):
        pass
