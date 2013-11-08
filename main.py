#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
###
# Application: ScraperAPI
# File:        main
# Description: starts the api
# Copyright (c) 2013 Wayne Moulden
###
#
#
#

import sys
from interface import Interface
from thegamesdb import theGamesDB


if __name__ == "__main__":
    running = True
    menu = True
    gui = Interface()
    scraper = theGamesDB()

    # Read the Platform List from the API
    p_list = scraper.readUrl('GetPlatformsList.php')
    proot = scraper.readXML(p_list)
    g_list = scraper.menuXML(proot, 'Platform')

    # Program loop (Unrestricted)
    while running:
        # Draw the table
        while menu:
            g_id = gui.draw_table(g_list)
            # check the user input
            if g_id:
                if g_id == 'Q' or g_id == 'q':
                    print 'Exiting...'
                    sys.exit()
                else:
                    menu = False
                    try:
                        g_id = int(g_id)
                    except ValueError:
                        menu = True
                        print "Not a number"
        # Games List
        if g_id:
            p_gids = scraper.getAPI(g_id,'GetPlatformGames.php?platform','platform')
            for id, p in g_list:
                if int(id) == g_id:
                    break
            g_id = None
            groot = scraper.readXML(p_gids)
            files = scraper.gameXML(groot, 'Data', p )



        # Redrawing the table
        menu = True
