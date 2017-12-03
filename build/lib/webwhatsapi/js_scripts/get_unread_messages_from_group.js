var Chats = Store.Chat.models;
var Output = [];
var contact = arguments[0];

function isChatMessage(message) {
    if (message.__x_isSentByMe) {
        return false;
    }
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
    console.log("K3: ",Chats)
    temp.contact = Chats[chat].__x_formattedTitle;
    temp.id = Chats[chat].__x_id;
    temp.messages = [];
    if(typeof temp.contact != 'undefined' && temp.contact.toLowerCase().search(contact)!=-1){
        console.log("Into:")
        var messages = Chats[chat].msgs.models;
        for (var i = messages.length - 1; i >= 0; i--) {
            if (!isChatMessage(messages[i])) {
                continue
            }
            messages[i].__x_isNewMsg = false;
            temp.messages.push({
                message: messages[i].__x_body,
                timestamp: messages[i].__x_t
            });
        }
    }
    if(temp.messages.length > 0) {
        Output.push(temp);
    }
}
console.log("Unread messages: ", Output);
return Output;