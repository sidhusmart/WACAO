
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
	- Make sure to create this group with some close contact so there aren't awkward questions later :)
	- Name this group as WACAO

- And now, we can start the chat assistant to start listening for instructions 

` driver.monitorWACAO() `

## Translation:

- Instruction format - "Translate to <language> - <your_message> and send to <contact_name>"
	- Example- "Translate to Spanish - Can we meet for coffee today? and send to Samuel"
	- Example- "Translate to Japanese - Do you like Sushi? and send to Nina"
- Currently following languages are supported - Spanish, German, English, French, Greek, Italian and Japanese. (But this is just a configuration change that can be added)
- The message in the language will be sent to the specific person in that chat and his/her replies will also be available there in the translated language
- However, in the WACAO chat you will also get back the translated message in English (default can be changed) so you can continue chatting from within the chat assistant
	- Example- "Samuel replied - Yeah sure, why not. At 5 today?"
	- Example- "Nina replied - No, I'm not a big fan"

## Chat Summarization:

- Instruction format - "Summarize <group_name>"
	- Example- "Summarize Analytics"
	- It's not necessary to provide the full group name, some part of the group name should be present
- You will receive a message that says - "Analytics summarized as: " followed by the summary of the messages in the group
	- There are several ways in which this summarization can be done and it currently uses an LSA Summarizer from the SUMY package
	- You can evaluate other summarizers to see which works best
	- I plan to research better techniques of achieving this summarization

## Happy Birthday Templates:

- Instruction format - "HBD <contact_name>"
	- Example- "HBD Samuel"
	- This will send the default configured Happy Birthday message to your contact. Message can be changed


` Limitation:- Phone has to be ON and connected to the internet `
