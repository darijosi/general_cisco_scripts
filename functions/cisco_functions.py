#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
################################################################################
        CLASSES wtth functons for managing CISCO devices
################################################################################
"""
__author__  = 'Dario Josipović'
__version__ = '0.0.1'
__license__ = 'free'

# modules to import
import pexpect # for handling connections
import sys # for exit from script

"""
################################################################################
                            CLASSES AND FUNCTIONS
################################################################################
"""
#parent class
class CISCO:
    "parent class for managing login data "

    def __init__(self, device, login_username, login_password):
        """Init login data """
        self.device = device
        self.login_username = login_username
        self.login_password = login_password


    def chooseEnable(self, user_enable_filter, login_data, login_variables):
        """
        if there is configured different enable passwords in network, choose
        correct one based on user input description
        """

        try:
            # choose correct enable for login to choosen device
            for i in range(0,len(login_data.keys())):
                login_data_variable = list(login_data.keys())[i]
                login_data_value = list(login_data.values())[i]
                if user_enable_filter in login_data_value[1]:
                    # call correct enable from login variables
                    enable_line = getattr(login_variables, login_data_variable)
                    enable = enable_line[0]

            return enable

        except TypeError:
            print ('TypeError occured. Please use option -h for help.')
            #raise

        except:
            print ('Unexpected error occured.')
            raise


#child class
class CONNECTION(CISCO):
    "class for managing connection to CISCO devices"

    def getConnect(self,enable):
        """
        Connect to device
        """

        host = self.device
        user = self.login_username
        password = self.login_password
        enable_pass = enable
        query =  \
        'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no %s@%s'\
        % (user,host)
        child = pexpect.spawn(query)
        try:
            i = child.expect(['assword:'], timeout=5)
        except pexpect.EOF:
            print ('EOF error. Device not responding to SSH.')
            child.close()
            sys.exit()
        except pexpect.TIMEOUT:
            print ('Timeout. Device not responding to SSH.')
            child.close()
            sys.exit()
        except:
            print ('Unexpected error:', sys.exc_info()[0])
            child.close()
            sys.exit()
        if i==0:
            try:
                child.sendline(password)
                i=child.expect (['>','#','User'], timeout=5)
            except:
                print ('User not exist/password is not correct.')
                child.close()
                sys.exit()
        if i==0 or i==1 or i==2:
            try:
                """Enter in enable mode."""
                print ('Connected to %s! Entering enable mode!' % (host))
                child.sendline('ena')
                child.expect(['assword:'], timeout=5)
                child.sendline(enable_pass)
                child.expect(['#'], timeout=5)

                """Check if in enable."""
                cli_output = child.before.decode("utf-8") # byte to string
                if 'Access denied' in cli_output:
                    msg = '\tUnsuccessfull. Not in enable mode.'
                    print (msg)
                else:# 'x' in cli_output:
                    print ('\tSuccessfull.')
                return child
            except:
                print ('Problem with enable password.')
                raise
                child.close()
                sys.exit()

    def getDisconnect(self,child):
        """
        Disconnect from Cisco device
        """

        try:
            child.sendline('\n')
            child.expect (['#'], timeout=1)
            child.close()
        except:
            print ('Problem with disconnecting from device.')
            child.close()
            sys.exit()

    def getInteractive(self, child):
        """
        Get into interactive mode with Cisco device
        """

        try:
            child.sendline('\n')
            child.expect(['#'], timeout=1)
            child.interact()
        except:
            print ('Problem with getting into interactive mode')
            child.close()
            sys.exit()
