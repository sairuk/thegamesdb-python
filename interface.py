#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
###
# Application: ScraperAPI
# File:        interface
# Description: interface class
# Copyright (c) 2013 Wayne Moulden
###
#

class Interface():
    def __init__(self):
        pass

    def draw_table(self, slist, c1_width=40, c2_width=6):
        div = "+%s+%s+" % ("-"*(c1_width+1),("-"*(c2_width+1)))

        print ""
        print div
        print "| Platform%s| ID%s|" % ((' '*(c1_width-8)),(' '*(c2_width-2)))
        print div
        for id, name in slist:
            # Calculate padding for table cells
            c1_pad = ' '*(c1_width - len(name))
            c2_pad = ' '*(c2_width - len(id))
            # Write table row to screen
            print "| %s%s| %s%s|" % (name, c1_pad, id, c2_pad)
        print div
        return raw_input('Enter Platform ID (Q to Quit): ')
