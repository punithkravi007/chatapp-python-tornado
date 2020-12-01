var modal = document.getElementById('id01');
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

$("#user_exist").hide()
$("#conversation").hide()
$("#no_conversation_history").hide()

user_info = {
    "user_id" : "user_01",
    "user_name":"User_Name_01"
}

target_user_info = {
    "user_id" : "",
    "user_name" :""
}

CHAT_APP = {
    wsURL : 'ws://'+window.location.host+"/chat/ws",
    isConnected : false,

    initialise : function(){

        CHAT_APP.socket = new WebSocket(CHAT_APP.wsURL);

        CHAT_APP.socket.onopen = function(event){
            CHAT_APP.isConnected = true
            CHAT_APP.socket.registerUser(user_info)
        },
        CHAT_APP.socket.onmessage = function(event){
            payload = JSON.parse(event.data)
            console.log(payload)
            switch (payload.action){
                case "registered-users" :
                    $(".chat-register").hide();
                    $(".app").show();
                    $(".sideBar").empty()
                    online_users = payload["content"]
                    for(user= 0; user<online_users.length;user++){
                        if (user_info["user_id"] == online_users[user]["user_id"]) continue
                        create_user_online_list(online_users[user]["user_id"], online_users[user]["username"])
                    }
                    break;
                case "user_already_exist":
                    $("#user_exist").show()
                    break;
                case "message_received":
                    console.log(payload)
                    console.log(target_user_info["user_id"])
                    if (target_user_info["user_id"] == payload["content"]["source_user_id"]){
                        conversations = payload["content"]["target_messages"]
                        for(conversation=0;conversation<conversations.length;conversation++){
                            console.log(conversations[conversation])
                            if(conversations[conversation]["msg_from"] == user_info["user_id"]){
                                console.log(conversations[conversation]["msg_from"],user_info["user_id"])
                                display_message(conversations[conversation]["message"],"SENT")
                            }else{
                                display_message(conversations[conversation]["message"],"RECEIVED")
                            }
                        }
                    }else{
                        $(".msg-badge-"+["source_user_id"]).css("{display:block}")
                    }
                    break;
                case "chat_connected_to_user":
                    $(".heading-name-meta").html(payload["content"]["target_user_name"])
                    target_user_info["user_id"] = payload["content"]["target_user_id"]
                    target_user_info["user_name"] = payload["content"]["target_user_name"]
                    $("#conversation").show()
                    $("div.message-body").remove()
                    if(payload["content"]["target_messages"].length ==0){
                        $("#no_conversation_history").show()
                        $("#no_conversation_history").html("No conversation yet")
                    }
                    else{
                        $("#no_conversation_history").hide()
                        conversations = payload["content"]["target_messages"]
                        for(conversation=0;conversation<conversations.length;conversation++){
                            console.log(conversations[conversation])
                            if(conversations[conversation]["msg_from"] == user_info["user_id"]){
                                console.log(conversations[conversation]["msg_from"],user_info["user_id"])
                                display_message(conversations[conversation]["message"],"SENT")
                            }else{
                                display_message(conversations[conversation]["message"],"RECEIVED")
                            }
                        }
                    }


            }
        },
        CHAT_APP.socket.registerUser = function(data){
            message = {
                action : "register-user",
                data : data
            }
            CHAT_APP.socket.send(JSON.stringify(message))
        },
        CHAT_APP.socket.start_conversation = function(data){
            message = {
                action:"start_conversation",
                data:data
            }
            CHAT_APP.socket.send(JSON.stringify(message))
        },
        CHAT_APP.socket.send_user_message = function(data){
            message = {
                action:"sent_message",
                data:data
            }
            CHAT_APP.socket.send(JSON.stringify(message))
        }
    }
}


$("#register-chat").click(function(){
    username = $("#username").val()
    fullName = $("#full-name").val()
    if (username!='undefined'){
        user_info["user_id"] = username
        user_info["user_name"] = fullName
        $("#user_name").html(fullName)
        CHAT_APP.initialise()
    }
});

$("#quit-chat").click(function(){
    location.reload();
})

$(".reply-send").click(function(){
    message = {
        "msg_from":user_info["user_id"],
        "msg_to":target_user_info["user_id"],
        "message": $("#message").val()
    }
    $("#message").val('')
    CHAT_APP.socket.send_user_message(message)
})

const create_user_online_list = (user_id, user_name) => {
    let innerHTML = '<div class="row sideBar-body" onclick="open_conversation(\''+user_id+'\')">'+
       '<div class="col-sm-1 col-xs-1 sideBar-avatar">'+
          '<div class="avatar-icon" style="">'+
             '<span class="badge" style="height:12px; width:2px;background-color:green;color:green;margin-top:12px margin-left:6px;padding-top:11px">o</span>'+
          '</div>'+
       '</div>'+
       '<div class="col-sm-11 col-xs-11 sideBar-main">'+
          '<div class="row">'+
             '<div class="col-sm-10 col-xs-10 sideBar-name">'+
                '<span class="name-meta">'+user_name+
                '</span>'+
             '</div>'+
             '<div class="col-sm-2 col-xs-2 pull-right sideBar-time">'+
                '<div class="avatar-icon" style="">'+
                   '<span class="badge msg-badge-'+user_id+'" style="display:none;height:12px; width:2px;background-color:red;color:red;margin-top:12px margin-left:6px;padding-top:11px">'+
                   'o</span></div>'+
             '</div>'+
          '</div>'+
       '</div>'+
    '</div>'
    $(".sideBar").append(innerHTML)
}

function display_message(message, target){
    console.log(message, target)

    temp_1 = (target == 'SENT') ? 'message-main-sender' : 'message-main-receiver';
    temp_2 = (target == 'SENT') ? 'sender': 'receiver'

    var innerHTML = '<div class="row message-body">'+
                    '<div class="col-sm-12 '+temp_1+'">'+
                        '<div class="'+temp_2+'">'+
                            '<div class="message-text">'+message+' </div> <span class="message-time pull-right">'+
                                '</span>'+
                        '</div>'+
                    '</div>'+
                '</div>';
    $(".message").append(innerHTML)
}

function open_conversation(user_id){
    data = {
        "source_user":user_info["user_id"],
        "target_user":user_id
    }
    CHAT_APP.socket.start_conversation(data)
}
