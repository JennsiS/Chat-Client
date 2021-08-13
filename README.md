<br />
<p align="center">
  <h2 align="center">Chat client with XMPP protocol</h2>
</p>

### Author

Jennifer Daniela Sandoval Rivas

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Description">About The Project</a>
    </li>
    <li><a href="#Requirements">Requirements</a></li>
    <li>
      <a href="#Libraries-and-modules-required">Libraries and modules required</a>
    </li>
    <li><a href="#How-to-use">Usage</a></li>
    <li><a href="#Structure">Structure</a></li>
    <li><a href="#References">Refereces</a></li>
  </ol>
</details>


### Description

This project generates a client that allows communication with an XMPP server with the domain @alumchat.xyz, it is programmed in python language and the [slixmpp](https://slixmpp.readthedocs.io/en/latest/) library is used to implement the main functionalities of the XMPP protocol.

### Requirements

- Python 3.7 +
- Slixmpp
- Connecting to a XMPP server to use the client

### Libraries and modules required

- Logging
- sys
- base64
- getpass 
- argparse
- slixmpp
- asyncio

### How to use

Run from command line as follows: 
                            ```python
                            python client.py  
                            ```
The following parameters can be added (optional) when executing the program:  
                            `python client.py -d[debug] -q[quiet] -j[JID] -p[password]`  

                            - **debug:** argument that allows debugging to be shown when running the program  
                            - quiet: argument that allows you to silence any message outside the program  
                            - JID: Jid to login or register. It must be entered in the following way username@domain (in this case username@alumchat.xyz)  
                            - password: The password corresponding to the JID entered to log in or create an account
 
### Structure

This program is composed of different classes and each of these classes performs a client functionality.  
Below are the classes and a brief description of them:  


    - RegisterBot : Class that registers a user to the server.
    - DeleteAccountBot : Class that unregisters a user from the server.  
    - Logout : Class that allows a user to log out  
    - Login : Class that allows a user to log in  
    - ChangePresence : Class that allows a user to change their presence message  
    - ShowUsersBot : Class that shows all users in my roster, their status and presence message  
    - UserInfoBot: Class that shows the information of a specific user in my roster  
    - MultiChatBot: Class that allow group chat  
    - Sendfile: Class that allow to send files  
    - AddUser: Class that allow to add a new contact to your roster  
    - CreateGroup: Class that allow to create a group for chat  


### References

1. Slixmpp documentation. https://slixmpp.readthedocs.io/en/latest/
2. Fritz, N. https://github.com/poezio/slixmpp/tree/master/examples
3. XMPP. https://xmpp.org/extensions/

                     