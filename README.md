
# WACAO - the Whatsapp Chat Assistant created at TechCrunch Disrupt Berlin Hackathon 2017 and featured [here](https://techcrunch.com/2017/12/03/wacao-is-an-assistant-that-can-summarize-and-translate-your-whatsapp-chats/)

This project uses the Whatapp project by mukulhase available [here](https://github.com/mukulhase/WebWhatsAPI)

## What is it?
This package can be used to create a personal Whatsapp Chat Assistant that can

- be used to chat with a contact on Whatsapp in a foreign language without leaving Whatsapp
- be used to Summarize chats from a Whatsapp group, saves you reading many unread messages
- be used to send customized 'Happy Birthday' messages to your friends [WIP] 
- be used to send Away/Do Not Disturb messages when you're not near the phone [WIP]
- provide interesting statistics on your chats [WIP]

## Installation

#### From Source
- Clone the Repo
- Use `pip install -r requirements.txt' to install the required packages.

#### From PyPI
- Star the repo :)
- Install from pip

`pip install webwhatsapi`

You will need to install [Gecko Driver](https://github.com/mozilla/geckodriver) separately, if using firefox, which is the default.


## Usage:
- Import library

` from webwhatsapi import WhatsAPIDriver `

- Instantiate driver and set username

` driver = WhatsAPIDriver("mkhase") `

- If the module is to be used as part of a script, and you need an image of the QR code, run the firstrun method. This saves the QR as username.png in, stored in the same directory after running command.

` driver.firstrun() `

If not, you can skip the above step, and directly scan the QR with your phone from the opened Firefox Tab.

- And now, the fun part, sending messages.

` driver.send_to_phone_number(phonenumber, message) `

- Viewing unread messages

` driver.view_unread() `

- Callback on receiving messages

For scripting, to set a function to be called whenever a message is received, use the create_callback method, and pass as the only argument, a function. The function must accept an argument, which is the received messages as a list.

## TODO:
- Add 'get profile picture' accessor

## Use Cases:
- Auto Reply bot for whatsapp, “I am away from phone”
- Can use whatsapp on phone and this api at the same time, (unlike the other whatsapp APIs, since this uses web.whatsapp)
- No need for number registration
- Hackathons, very easy to setup a whatsapp messaging service.
- API for custom bot making
- Whatsapp cloud( A service):-
-- User can access and send messages from anywhere without scanning qr anymore, just simple user login and password

` Limitation:- Phone has to be ON and connected to the internet `


This is the README file for the project.
# WACAO
# WACAO
