# Universidad del Valle de Guatemala
# Redes 
# Chat client project
# Author: Jennifer Sandoval

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2010  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

'''
Implemented Functions:
    - Show all users
    - Log in
    - Send messages to one user
Pending Functions:
    - Delete account
    - Register account
    - Log out
    - Add Contact
    - Group chat
    - Prescense 
    - Notifications
    - Files
Uncompleted functions:
    - Show one user info (Select only user status)
    - Receive message from chat
'''

import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import asyncio




class RegisterBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()

    async def register(self, iq):
        resp = iq
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            print("Account created for %s!"+ str(self.boundjid))
        except IqError as e:
            print('Account not created')
            self.disconnect()
        except IqTimeout:
            print('No response from server')
            self.disconnect()

class DeleteAccountBot(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("unregister", self.unregister)

    async def start(self,event):
        self.send_presence()
        await self.get_roster()
        await self.unregister()
        self.disconnect()

    async def unregister(self,iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['password'] = self.password
        resp['register']['remove'] = 'remove'

        try:
            await resp.send()
            print("Success! Acount Deleted"+str(self.boundjid))
        except IqError as e:
            print("IQ Error:Account Not Deleted")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect() 



class MsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
        self.disconnect()

    def message(self, msg):
        if msg['type'] in ('chat'):
            recipient = msg['to']
            body = msg['body']
            print(str(recipient) +  ": " + str(body))
            message = input("Write the message: ")
            self.send_message(mto=self.recipient,
                              mbody=message)


        

class ShowUsersBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status", self.wait_for_presences)

        self.received = set()
        self.presences_received = asyncio.Event()

    async def start(self, event):
        try:
            await self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        self.send_presence()


        print('Waiting for presence updates...\n')
        await asyncio.sleep(10)

        print('Roster for %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])

        self.disconnect()

    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

class UserInfoBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status", self.wait_for_presences)

        self.received = set()
        self.presences_received = asyncio.Event()

    async def start(self, event):
        try:
            await self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        self.send_presence()

        jid_user=input('User jid: ')
        print('Waiting for presence updates...\n')
        await asyncio.sleep(10)

        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name'] and jid==jid_user:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                elif self.client_roster[jid]['name']==False and jid==jid_user:
                    print(' %s [%s]' % (jid, sub))

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])

        self.disconnect()

    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

class MultiChatBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.room = room
        self.nick = nick
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room,
                                        self.nick)
    
    def muc_message(self, msg):
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                            mbody="I heard that, %s." % msg['mucnick'],
                            mtype='groupchat')
    

class Client(slixmpp.ClientXMPP):
    slixmpp.ClientXMPP.__init__(self, jid, password)
    self.add_event_handler("session_start", self.start)


class AddUser(slixmpp.ClientXMPP):
        def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.presences_received = asyncio.Event()
        self.recieved=set()        
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status",self.wait_for_presences)

    async def start(self,event):
        
        try:
            await self.get_roster()
        except IqError as e:
            print("IQ Error")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect()
        self.send_presence()

        print('Roster  for %s'% self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s} [%s]'% (name,jid,sub))
                else:
                    print(' %s (%s} [%s]'% (jid,sub))
                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])
        self.disconnect()


    def wait_for_presences(self,pres):
        self.received.add(pres['from'].bare)
        if len(self.recieved)>=len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()
    
    def send_request(self,to):
        try:
            self.send_presence_subscription(to, self.local_jid, 'subscribe')
        except:
            print("Couldn't add Friend")




if __name__ == '__main__':
    parser = ArgumentParser(description=MsgBot.__doc__)
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    

    connected=True
    while connected:
        print('Welcome to alumchat.xyz') 
        print('1. Log in')
        print('2. Register a new user')
        opt=int(input('\n'))
        if(opt==1):
            if args.jid is None: 
                args.jid = input("Username: ")
            if args.password is None:
                args.password = getpass("Password: ")
        elif(opt==2):
            if args.jid is None: 
                args.jid = input("Enter a new username (yourname@alumchat.xyz): ")
            if args.password is None:
                args.password = getpass("Password: ") 
            xmpp = RegisterBot(args.jid, args.password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0004') # Data forms
            xmpp.register_plugin('xep_0066') # Out-of-band Data
            xmpp.register_plugin('xep_0077') # In-band Registration

            #xmpp['xep_0077'].force_registration = True
            xmpp.connect()
            xmpp.process()

        loop=True

        while loop:
            print('MENU')
            print('Select the option you want to use: ')
            print(' 1.Show all users')
            print(' 2.Add contact')
            print(' 3.Show user')
            print(' 4.DM')
            print(' 5.Group Chat')
            print(' 6.Define status')
            print(' 7.Send/recieve notifications')
            print(' 8.Send/receive files')
            print(' 9.Logout')
            print(' 10.Delete account')
            option=int(input("\n"))
            if(option==1):
                xmpp = ShowUsersBot(args.jid, args.password)
                xmpp.connect()
                xmpp.process(forever=False)
                loop=False
            elif(option==2):
                pass
            elif(option==3):
                xmpp = UserInfoBot(args.jid, args.password)
                xmpp.connect()
                xmpp.process(forever=False)
                loop=False
            elif(option==4):
                user=input('Enter the username ')
                message=input('msg: ')
                xmpp = MsgBot(args.jid, args.password, user, message)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0004') ### Data Forms
                xmpp.register_plugin('xep_0066') ### Band Data
                xmpp.register_plugin('xep_0077') ### Band Registration
                # Connect to the XMPP server and start processing XMPP stanzas.
                xmpp.connect()
                xmpp.process(forever=False)
                
            elif(option==5):
                room=input('Enter the room you want to create ')
                nick=input('Select your nickname: ')
                xmpp = MultiChatBot(args.jid,args.password,room,nick)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0045') # Multi-User Chat
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.connect()
                xmpp.process()
            elif(option==6):
                pass
            elif(option==7):
                pass
            elif(option==8):
                pass
            elif(option==9):
                pass
            elif(option==10):
                xmpp=DeleteAccountBot(args.jid,args.password)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0004') # Data forms
                xmpp.register_plugin('xep_0066') # Out-of-band Data
                xmpp.register_plugin('xep_0077') # In-band Registration
                loop=False
            else:
                print('Opcion incorrecta')