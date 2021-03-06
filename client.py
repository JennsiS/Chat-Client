# Universidad del Valle de Guatemala
# Redes 
# Chat client project
# name: client.py
# Description: this program is a client that allows communication with the xmpp server, specifically the domain @ alumchat.xyz
# Author: Jennifer Daniela Sandoval

# Note: Most of the implemented classes are based on the examples provided by the repository belonging to the slixmpp library.
# References: https://github.com/poezio/slixmpp/tree/master/examples

#Importing libraries
import logging
import sys
import base64
from getpass import getpass
from argparse import ArgumentParser
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
import asyncio

###################################################################################################################

#                               Chat client whit xmpp protocol                                              

###################################################################################################################

#Small fix that allows the program to run on windows operating systems due to an error with the asyncio library
if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

'''
Class that registers a user to the server. 
Parameters:
    - JID
    - Password
'''
class RegisterBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    async def start(self, event):
        #Connecting to the server
        self.send_presence()
        await self.get_roster()
        self.disconnect()

    async def register(self, iq):
        #Configuring the necessary parameters to perform the query with xmpp to register an account
        response = self.Iq()
        response['type'] = 'set'
        response['register']['username'] = self.boundjid.user
        response['register']['password'] = self.password

        #Trying to send the query to the server
        try:
            await response.send()
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

'''
Class that unregisters a user from the server. 
Parameters:
    - JID
    - Password
'''

class DeleteAccountBot(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.user=jid
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        self.send_presence()
        await self.get_roster()
        #Preparing the query to unregister the indicated jid
        response = self.Iq()
        response['type'] = 'get'
        response['from'] = self.boundjid.user
        response['password'] = self.password
        response['register']['remove'] = 'remove'

        #Trying to send the query to the server
        try:
            response.send()
            print("\nSuccess! Acount Deleted for: "+str(self.boundjid))
        except IqError as e:
            print("IQ Error: Account Not Deleted")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect() 

'''
Class that allows a user to log out
Parameters:
    - JID
    - Password
'''
class Logout(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        self.send_presence()
        await self.get_roster()
        print('\nBye! See you soon :) \n')
        #Log out session
        self.disconnect()

'''
Class that allows a user to log in
Parameters:
    - JID
    - Password
'''
class Login(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        try:
            self.send_presence()
            await self.get_roster()
            print('\nHello! You are in :)\n')
            self.disconnect()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            print('Error: Request timed out')
            self.send_presence()
            self.disconnect()

'''
Class that allows a user to change their presence message
Parameters:
    - JID
    - Password
    - Option: Status (away,chat,dnd,xa)
    - Message: Presence message
'''

class ChangePresence(slixmpp.ClientXMPP):
    def __init__(self, jid,password,option,message):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.option=option
        self.message=message
        self.add_event_handler("session_start", self.start)

    async def start(self,event):
        #Changing presence message setting the status and the presence message entered by the user
        self.send_presence(pshow=self.option,pstatus=self.message)
        await asyncio.sleep(40)
        self.get_roster()
        self.disconnect()


'''
Class that allows sending and receiving direct messages with a user
Parameters:
    - JID
    - Password
    - Recipient: jid of the user who receives the message
    - Message: body of the message you want to send
'''

class MsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = message
        #Handlers
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        #self.add_event_handler("message", self.Notification)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
        
    #Send notification inside the chat when someone is typing
    def Notification(self):
        itemStanza = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        body='Someone is writting you...'
        # Send a notification
        message=self.Message()
        message.append(itemStanza)
        message['to'] = self.recipient
        message['type'] = 'chat'
        message['body'] = body
        try:
            message.send()
        except IqError as e:
            raise Exception("Notification not sended", e)
        except IqTimeout:
            raise Exception("Server not responding")

    #asynchronous function that is listening messages from the recipient and allow to send message 
    async def message(self, msg):
        #self.Notification()
        message=input('You: ')
        if msg['type'] in ('chat'):
            recipient = msg['from']
            body = msg['body']
            print(str(recipient) +  ": " + str(body))
            message = input("You: ")
            self.send_message(mto=self.recipient,
                              mbody=message, mtype='chat')

'''
Class that shows all users in my roster, their status and presence message
Parameters:
    - JID
    - Password
'''
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

        #giving the server time to send the roster
        print('Waiting for presence updates...\n')
        await asyncio.sleep(10)

        print('Roster for %s' % self.boundjid.bare)
        #getting the existing groups in the roster
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                #Extracting the subscription status of one user
                sub = self.client_roster[jid]['subscription']
                #Extracting the name of one user
                name = self.client_roster[jid]['name']
                #Not all users have name, in this case only extract the jid
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))

                #Extracting the presence status of the user
                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])

        self.disconnect()

    #Receiving the users presences from the server
    def wait_for_presences(self, pres):
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

'''
Class that shows the information of a specific user in my roster
Parameters:
    - JID
    - Password
'''
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

        #Asking the user to enter the jid of the user he wants to display
        jid_user=input('User jid: ')
        #giving the server time to send the roster
        print('Waiting for presence updates...\n')
        await asyncio.sleep(10)

        #getting the existing groups in the roster
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                #Extracting the subscription status of one user
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                #Showing only the information of the required user when they have name
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
                #Showing only the information of the required user when they don't have name
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
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()


'''
Class that allow group chat
Parameters:
    - JID
    - Password
    - room: room name including @conference.alumchat.xyz
    - nick: the nickname assigned when entering the room
'''
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
        #loading the necessary plugin for group communication
        self.plugin['xep_0045'].join_muc(self.room, self.nick,)

    #Asynchronous function that is listening to the messages sent in the group
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

'''
Class that allow to send files
Parameters:
    - JID
    - Password
    - receiver: jid of the user you want to send a file
    - filename: complete path of the file
'''
class Sendfile(slixmpp.ClientXMPP):
    def __init__(self, jid, password, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.receiver = receiver
        self.file = filename
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        #Open the file with the path indicated and encoding to utf-8
        with open (self.file,'rb') as img:
            file_=base64.b64encode(img.read()).decode('utf-8')
            self.disconnect()
        try:
            self.send_message(mto=self.receiver, mbody=file_, mtype='chat')
            print('Sent file ')
            self.disconnect()
        except:
            print('Error sending file')
            self.disconnect()

'''
Class that allow to add a new user to your contacts
Parameters:
    - JID
    - Password
    - jiduser: jid of the user you want to addd to your roster
'''
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
            #Sending the subscription to the jid user you want to add
            self.send_presence_subscription(pto=self.jiduser)
            print("User added! " + str(self.jiduser))
            self.disconnect()
        except IqError as e:
            print("IQ Error")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect()

    #Receiving presences from the roster
    def wait_for_presences(self,pres):
        self.received.add(pres['from'].bare)
        if len(self.recieved)>=len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()
    
    def send_request(self,to):
        try:
            #Sending the request to the server to add the jid user to your contacts
            self.send_presence_subscription(to, self.local_jid, 'subscribe')
        except:
            print("Couldn't add Friend")

'''
Class that allow to create groups to chat
Parameters:
    - JID
    - Password
    - jiduser: jid of the user you want to addd to your roster
'''

class CreateGroup(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick
        self.add_event_handler("session_start", self.start)
    
    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        try:
            status = "Joining to: " + str(self.room)
            self.plugin['xep_0045'].join_muc(room,nick, pstatus=status, pfrom=self.boundjid.full)
            #Set the affilation
            await self.plugin['xep_0045'].set_affiliation(room,'owner')
            #Publicate chat room
            self.plugin['xep_0045'].set_room_config(room,None,ifrom=self.boundjid.full)
            print("You have succesfully created the room: " + room + "with NickName: "+nick)
            self.disconnect()

        except IqError as e:
            raise Exception("The room could not been created", e)
        except IqTimeout:
            raise Exception("No response from server")

#Simple function to check if the option is numeric
def is_num():
    num=False
    while num==False:
        option=input('Choose an option from the menu: ')
        num=option.isnumeric()
        if (num==False):
            print ('You must enter a number ')
        else:
            option=int(option)
    return option   


'''MAIN FUNCTION'''
if __name__ == '__main__':
    #Add arguments to use when running the program
    parser = ArgumentParser(description=MsgBot.__doc__)
    #Stop verbose
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    #Show debug
    parser.add_argument("-d", "--debug", help="set logging to DEBUG", action="store_const", dest="loglevel",const=logging.DEBUG, default=logging.INFO)

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
        jid=None
        password=None
        print('Welcome to alumchat.xyz') 
        print('1. Log in')
        print('2. Register a new user')
        opt=int(input('\n'))
        if(opt==1):
            if args.jid is None: 
                args.jid = input("Username: ")
            if args.password is None:
                args.password = getpass("Password: ")
            jid = args.jid
            password = args.password 
            connected=False
            #Login function
            try: 
                xmpp=Login(args.jid,args.password)
                xmpp.connect()
                xmpp.process(forever=False)
                jid=args.jid
                password=args.password
                connected=False
            except:
                print('\nAn error has occurred. Verify that the username and password are correct')
                connected=True  
        elif(opt==2):
            #Using RegisterBot Class
            jid = input("Enter a new username (yourname@alumchat.xyz): ")
            password = getpass("Password: ") 
            xmpp = RegisterBot(jid, password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0004') # Data forms
            xmpp.register_plugin('xep_0066') # Out-of-band Data
            xmpp.register_plugin('xep_0077') # In-band Registration
            xmpp['xep_0077'].force_registration = True
            xmpp.connect()
            xmpp.process(forever=False)
            connected=True
        else:
            print('Invalid option. Try again!')
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
        print(' 7.Create group')
        print(' 8.Send/receive files')
        print(' 9.Logout')
        print(' 10.Delete account')
        option=is_num()
        if(option==1):
            #Showing all users
            xmpp = ShowUsersBot(jid,password)
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==2):
            #Add a new contact
            user=input('Enter the username you want to add (example@alumchat.xyz): ')
            xmpp=AddUser(jid,password,user)
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==3):
            #Showing one user info
            xmpp = UserInfoBot(jid, password)
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==4):
            #Chat with some user
            try:
                user=input('Enter the username (user@alumchat.xyz): ')
                message=input('msg: ')
                xmpp = MsgBot(jid, password, user, message)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0004') # Data Forms
                xmpp.connect()
                xmpp.process(forever=False)
            except KeyboardInterrupt:
                xmpp.disconnect()
        elif(option==5):
            #Chat in group
            try:
                room=input('Enter the name of the group: (just the name without the domain) ')
                room=room+'@conference.alumchat.xyz'
                nick=input('Enter your nick in this room: ')
                message=input('msg: ')
                xmpp = MultiChatBot(jid,password,room,nick)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0004') # Data Forms
                xmpp.register_plugin('xep_0045') # MUC
                xmpp.connect()
                xmpp.process(forever=False)
            except KeyboardInterrupt:
                xmpp.disconnect()
        elif(option==6):
            #Change presence message
            presence=input('Select presence status (chat,away,xa,dnd): ')
            message=input('Select message presence: ')
            xmpp=ChangePresence(jid,password,presence,message)
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==7):
            #Create a new group to chat
            room=input('Enter the name of the group (just the name without the domain): ')
            room=room+'@conference.alumchat.xyz'
            nick=input('Enter your nick in this room: ')
            xmpp=CreateGroup(jid,password,room, nick)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0004') # Data Forms
            xmpp.register_plugin('xep_0045') # MUC
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==8):
            #Sending files
            user=input('Enter the username ')
            file=input('Insert file path: ')
            xmpp=Sendfile(jid,password,user,file)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0065') # SOCKS5 Bytestreams
            xmpp.connect()
            xmpp.process(forever=False)
        elif(option==9):
            #Log out
            xmpp=Logout(jid,password)
            xmpp.connect()
            xmpp.process(forever=False)
            loop=False
        elif(option==10):
            #Delete the present account
            xmpp=DeleteAccountBot(jid,password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0004') # Data forms
            xmpp.register_plugin('xep_0066') # Out-of-band Data
            xmpp.register_plugin('xep_0077') # In-band Registration
            xmpp.connect()
            xmpp.process(forever=False)
            loop=False
        else:
            print('Invalid option. Try again!')
            loop=True
    
    
        