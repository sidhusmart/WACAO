var Chats = Store.Chat.models;
var Output = [];
var contact = arguments[0];
var numberOfMsg = arguments[1];

function isChatMessage(message) {
    if (message.__x_isNotification) {
        return false;
    }
    if (!message.__x_isUserCreatedType) {
        return false;
    }
    return true;
}

for (chat in Chats) {
    if (isNaN(chat)) {
        continue;
    };
    var temp = {};
    console.log("Key: ",Object.entries(Chats[chat]))
    temp.contact = Chats[chat].__x_name;
    temp.id = Chats[chat].__x_id;
    temp.messages = [];
    if(typeof temp.contact != 'undefined' && temp.contact.toLowerCase().search(contact)!=-1){
        var messages = Chats[chat].msgs.models;
        console.log("Count: ",messages.length)
        for (var i = messages.length - 1; i >= 0; i--) {
            if (!isChatMessage(messages[i])) {
                continue
            }
            temp.messages.push({
                message: messages[i].__x_body,
                timestamp: messages[i].__x_t
            });
        }
        if(temp.messages.length > 0) {
            Output.push(temp);
        }
    }
    
}
console.log("Unread messages: ", Output);
return Output;