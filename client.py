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
    - Send and receive messages in chat
    - Show one user info
    - Delete account
    - Add contact
    - Log out
    -Define Presence
Pending Functions:
    - Register account (?) 
    - Notifications (typing)
    - Create group
Uncompleted functions:
    - how to make while logging stays online
    - Files
    - Group chat
'''

import logging
import sys
from getpass import getpass
from argparse import ArgumentParser

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import asyncio
'''
class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.Message)
        self.add_event_handler("changed_status", self.wait_for_presences)

        self.received = set()
        self.presences_received = asyncio.Event()

        #plugins
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0030') # Service Disc
        self.register_plugin('xep_0077') # In-band Register
        self.register_plugin('xep_0066') # Ping
        self.register_plugin('xep_0045') # MUC

    def start(self, event):
        try:
            self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:

            print('Error: Request timed out')
        self.send_presence(pshow='chat',pstatus='Estoy disponible')
        self.disconnect()
        
    
    def Login(self):
        self.connect()
        self.process(forever=False)
        self.disconnect()
    
    async def ShowUsers(self):
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

    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    
    def ChangePresence(self,option,message):
        self.send_presence(pshow=option,pstatus=message)

    def AddUser(self,jiduser):
        self.send_presence_subscription(pto=jiduser)
        print("User added! " + str(jiduser))
    
    def DeleteAccount(self):
        request=self.Iq()
        request['type'] = 'set'
        request['from'] = self.boundjid.user
        request['password'] = self.password
        request['register']['remove'] = 'remove'
        try:
            request.send()
            print("Success! Acount Deleted"+str(self.boundjid))
        except IqError as e:
            print("IQ Error:Account Not Deleted")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect()
    
    def Logout(self):
        self.disconnect()
        print('Bye! See you soon :) ')
    
    def Message(self, recipient, msg):
        self.send_message(mto=recipient,
                          mbody=msg,
                          mtype='chat')
        if msg['type'] in ('chat'):
            recipient = msg['from']
            body = msg['body']
            print(str(recipient) +  ": " + str(body))
            message = input("You: ")
            self.send_message(mto=recipient,
                              mbody=message, mtype='chat')
    
    def ShowUserInfo(self):
        jid_user=input('User jid: ')
        print('Waiting for presence updates...\n')
        #await asyncio.sleep(10)

        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name'] and jid==jid_user:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                    connections = self.client_roster.presence(jid_user)
                    for res, pres in connections.items():
                        show = 'available'
                        if pres['show']:
                            show = pres['show']
                        print('   - %s (%s)' % (res, show))
                        if pres['status']:
                            print('       %s' % pres['status'])
                elif self.client_roster[jid]['name']==False and jid==jid_user:
                    print(' %s [%s]' % (jid, sub))
                    connections = self.client_roster.presence(jid_user)
                    for res, pres in connections.items():
                        show = 'available'
                        if pres['show']:
                            show = pres['show']
                        print('   - %s (%s)' % (res, show))
                        if pres['status']:
                            print('       %s' % pres['status'])
    
    def ChatGroup(self, room, nick,msg):
        self.send_message(mto=room,mbody=msg,mtype='groupchat',mnick=nick)

'''
###################################################################################################################

###################################################################################################################

if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class RegisterBot(slixmpp.ClientXMPP):
    def _init_(self, jid, password):
        slixmpp.ClientXMPP._init_(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        try:
            iq.send()
            print("Nueva Cuenta Creada", self.boundjid,"\n")
        except IqError as e:
            print("Error en Registro ", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("Timeout en el servidor")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()


class DeleteAccountBot(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.user=jid
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        self.send_presence()
        await self.get_roster()

        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['password'] = self.password
        resp['register']['remove'] = 'remove'

        try:
            resp.send()
            print("Success! Acount Deleted"+str(self.boundjid))
        except IqError as e:
            print("IQ Error:Account Not Deleted")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect() 

class Logout(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()

class Login(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        self.send_presence()
        await self.get_roster()
        print('Hello! You are in')
        self.disconnect()

class ChangePresence(slixmpp.ClientXMPP):
    def __init__(self, jid,password,option,message):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.option=option
        self.message=message
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        self.send_presence(pshow=self.option,pstatus=self.message)
        await asyncio.sleep(10)
        self.get_roster()
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
            recipient = msg['from']
            body = msg['body']
            print(str(recipient) +  ": " + str(body))
            message = input("You: ")
            self.send_message(mto=self.recipient,
                              mbody=message, mtype='chat')


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
                    connections = self.client_roster.presence(jid_user)
                    for res, pres in connections.items():
                        show = 'available'
                        if pres['show']:
                            show = pres['show']
                        print('   - %s (%s)' % (res, show))
                        if pres['status']:
                            print('       %s' % pres['status'])
                elif self.client_roster[jid]['name']==False and jid==jid_user:
                    print(' %s [%s]' % (jid, sub))
                    connections = self.client_roster.presence(jid_user)
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

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room, self.nick,)

    async def muc_message(self, msg):
        message=input('You: ')
        self.send_message(mto=self.room,
                          mbody=message,
                          mtype='groupchat')
        if msg['type'] in ('groupchat'):
            recipient = msg['from']
            body = msg['body']
            print(str(recipient) +  ": " + str(body))
            message = input("You: ")
            self.send_message(mto=self.room,mbody=message, mtype='chat')
    
class Sendfile(slixmpp.ClientXMPP):
    def __init__(self, jid, password, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.receiver = receiver
        self.file = open(filename, 'rb')
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        try:
            # Open the S5B stream in which to write to.
            proxy = await self['xep_0065'].handshake(self.receiver)

            # Send the entire file.
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)

            # And finally close the stream.
            proxy.transport.write_eof()
        except (IqError, IqTimeout):
            print('File transfer errored')
        else:
            print('File transfer finished')
        finally:
            self.file.close()
            self.disconnect()


class AddUser(slixmpp.ClientXMPP):
    def __init__(self, jid,password,jiduser):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.presences_received = asyncio.Event()
        self.recieved=set()        
        self.jiduser=jiduser
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status",self.wait_for_presences)

    async def start(self,event): 
        try:
            await self.get_roster()
            self.send_presence_subscription(pto=self.jiduser)
            print("User added! " + str(self.jiduser))
            self.disconnect()
        except IqError as e:
            print("IQ Error")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
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
            xmpp=Login(args.jid,args.password)
            xmpp.connect()
            xmpp.process(forever=False)
            connected=False
        elif(opt==2):
            if args.jid is None: 
                args.jid = input("Enter a new username (yourname@alumchat.xyz): ")
            if args.password is None:
                args.password = getpass("Password: ") 
            xmpp = RegisterBot(args.jid, args.password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0004') # Data forms
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0066') # Out-of-band Data
            xmpp.register_plugin('xep_0077') # In-band Registration
            xmpp['xep_0077'].force_registration = True
            xmpp.connect()
            xmpp.process(forever=True)
            connected=True

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
            xmpp = ShowUsersBot(args.jid,args.password)
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==2):
            user=input('Enter the username you want to add: ')
            xmpp=AddUser(args.jid,args.password,user)
            xmpp.connect()
            xmpp.process()
        elif(option==3):
            xmpp = UserInfoBot(args.jid, args.password)
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==4):
            user=input('Enter the username ')
            message=input('msg: ')
            xmpp = MsgBot(args.jid, args.password, user, message)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0004') ### Data Forms
            xmpp.register_plugin('xep_0066') ### Band Data
            xmpp.register_plugin('xep_0077') ### Band Registration
            xmpp.connect()
            xmpp.process()
        elif(option==5):
            room=input('Enter the name of the group ')
            room=room+'@conference.alumchat.xyz'
            nick=input('Enter your nick ')
            message=input('msg: ')
            xmpp = MultiChatBot(args.jid,args.password,room,nick)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0004') ### Data Forms
            xmpp.register_plugin('xep_0066') ### Band Data
            xmpp.register_plugin('xep_0077') ### Band Registration
            xmpp.register_plugin('xep_0045') # MUC
            xmpp.connect()
            xmpp.process()
        elif(option==6):
            presence=input('Select presence status (chat,away,xa,dnd): ')
            message=input('Select message presence: ')
            xmpp=ChangePresence(args.jid,args.password,presence,message)
            xmpp.connect()
            xmpp.process()
        elif(option==7):
            pass
        elif(option==8):
            user=input('Enter the username ')
            file=input('Insert file name: ')
            xmpp=Sendfile(args.jid,args.password,user,file)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0004') ### Data Forms
            xmpp.register_plugin('xep_0066') ### Band Data
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0065') # SOCKS5 Bytestreams
            xmpp.register_plugin('xep_0077') ### Band Registration
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==9):
            xmpp=Logout(args.jid,args.password)
            xmpp.connect()
            xmpp.process(forever=False)
            loop=False
        elif(option==10):
            xmpp=DeleteAccountBot(args.jid,args.password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0004') # Data forms
            xmpp.register_plugin('xep_0066') # Out-of-band Data
            xmpp.register_plugin('xep_0077') # In-band Registration
            xmpp.connect()
            xmpp.process(forever=False)
            loop=False
        else:
            print('Opcion incorrecta')
    
    
        