var Chats = Store.Chat.models;
var Output = [];
var Output1 = [];
var contact = arguments[0];
var message = arguments[1];
for (chat in Chats) {
    if (isNaN(chat)) {
        continue;
    };
    obj = Chats[chat]
    var temp = {};
    temp.contact = Chats[chat].__x_formattedTitle;
    temp.id = Chats[chat].__x_id;
    Output.push(temp.contact);
    Output.push(temp.id);
}
console.log("Contacts: ", Output);
return Output

