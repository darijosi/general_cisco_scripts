#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
##                      Login data for Cisco devices
##
## *********   you need to create file with login data for yourself    *********
##
## *********         make sure your sensitive data is protected        *********
##
## Script expects login data in this format
## {
##    'username': 'your_username',
##    'password': 'your_password',
##    'enable1' : ['your_first_enable_password', 'enable1 description'],
##    'enable2' : ['your_second_enable_password', 'enable2 description'],
##    'enable3' : ['your_third_enable_password', 'enable3 description'],
##                                    .
##                                    .
##                                    .
##    'enableN' : ['your_nth_enable_password', 'enableN description']
## }
"""
# path to login data
file = '../sensitive_data/login_data' # change to your path

# write login data from file to variable
with open(file) as f:
    data =f.read()
    f.close()

# convert data to dictionary
logins = eval(data)
