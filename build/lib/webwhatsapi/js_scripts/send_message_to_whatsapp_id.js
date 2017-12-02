var Chats = Store.Chat.models;
var id = arguments[0];
var message = arguments[1];
for (chat in Chats) {
    if (isNaN(chat)) {
        continue;
    };
    var temp = {};
    temp.contact = Chats[chat].__x_formattedTitle;
    temp.id = Chats[chat].__x_id;
    console.log("Key: ",temp.contact)
    if(typeof temp.contact != 'undefined' && temp.contact.toLowerCase().search(id)!=-1){
        console.log("Into")
        Chats[chat].sendMessage(message);
        return true;
    }
}
return false;