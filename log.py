#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
################################################################################
                        SCRIPT to log on CISCO devices
################################################################################
"""
__author__  = 'darijosi'
__version__ = '0.0.1'
__license__ = 'free'

# modules to import
import argparse # for defining input variables
import sys # for error handling
from types import SimpleNamespace # for using dict keys as variables
from functions import cisco_functions # functions for maintaing connection

# import login data
from input.parse_login_data import logins # get login data
login = SimpleNamespace(**logins) # use login dict keys as variables

# defining input variables
parser = argparse.ArgumentParser(description="Script to log on Cisco devices!")
requiredNamed = parser.add_argument_group('Required input variables:')
requiredNamed.add_argument("-d", "--device", help="Device IP address to \
                            connect.", required=True)
requiredNamed.add_argument("-e", "--enable", help="Enable to use.",\
                            required=True)
args = parser.parse_args()

"""
################################################################################
                                    MAIN
################################################################################
"""
# get device IP from user input
device = args.device

# get filter for enable from user input
enable_filter = args.enable

# prepare data for connection
cisco_device = cisco_functions.CONNECTION(device, login.username, login.password)

# get correct enable
enable = cisco_device.chooseEnable(enable_filter, logins, login)

# connect to device
connect = cisco_device.getConnect(enable)

# start interactive mode
interact = cisco_device.getInteractive(connect)


"""
################################################################################
                                TESTING AREA
################################################################################
"""

"""
import sys # for defining path to login data
sys.path.append('../input') # path to login data
from parse_login_data import logins # import login data
"""
