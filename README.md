
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

You will need to install [Gecko Driver](https://github.com/mozilla/geckodriver) separately, if using firefox, which is the default.

## Usage:
- Import library

` from webwhatsapi import WhatsAPIDriver `

- Instantiate driver and set username -

` driver = WhatsAPIDriver("sidhusmart") `

- This should bring up Whatsapp Web on Firefox browser which will show you the QR code
- Please scan this QR code by going to the 'Whatsapp Web' option on the Whatsapp app on your phone

- Next step is to create a group called WACAO with only yourself in it - 
	- The way to do this is to create a new group with another contact and once the group has been created, remove that contact
	- Make sure to create this person with some close contact so there aren't awkward questions later :)
	- Name this group as WACAO

- And now, we can start monitoring for messages on the WACAO group

` driver.monitorWACAO() `


` Limitation:- Phone has to be ON and connected to the internet `
