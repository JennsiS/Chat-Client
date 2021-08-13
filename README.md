# Chat client with xmpp protocol


#####                                                  author: Jennifer Sandoval

<hr> </hr>

### Description

This project generates a client that allows communication with an XMPP server with the domain @alumchat.xyz, it is programmed in python language and the [slixmpp](https://slixmpp.readthedocs.io/en/latest/) library is used to implement the main functionalities of the XMPP protocol.

### Libraries and modules

- Logging
- sys
- base64
- getpass 
- argparse
- slixmpp
- asyncio

### How to use

1. Run from command line as follows:
                            `python client.py`
2. A menu like the following will be shown:
                        ``` python
                            Welcome to alumchat.xyz
                            1. Log in`
                            2. Register a new user
                        ```
    - When the login function is chosen, the following menu is displayed:
        `MENU
        Select the option you want to use:
        1.Show all users
        2.Add contact
        3.Show user
        4.DM
        5.Group Chat
        6.Define status
        7.Create group
        8.Send/receive files
        9.Logout
        10.Delete account`
                    

