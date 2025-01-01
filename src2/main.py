
# 0. Get userid
# curl -X GET 'https://api.twitch.tv/helix/users?login=spacebarplay' \
# -H 'Authorization: Bearer r4cd5s8mfhzbci9gfb5n5bw0wthsqq' \
# -H 'Client-Id: sy1kxf9t94bmdwo8n4eha8kjfa04pg'



# 1. Go to
#https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=sy1kxf9t94bmdwo8n4eha8kjfa04pg&redirect_uri=http://localhost:3000&scope=chat:edit+chat:read+user:write:chat+user:bot

# 2. Copy the code from the URL and paste it here
#curl -X POST 'https://id.twitch.tv/oauth2/token' \
#-H 'Content-Type: application/x-www-form-urlencoded' \
#-d "client_id=sy1kxf9t94bmdwo8n4eha8kjfa04pg&client_secret=6u6gta5luyb9yndv312551mfoa1r6c&code=[REPLACE_CODE]&grant_type=authorization_code&redirect_uri=http://localhost:3000"



#curl -X POST 'https://id.twitch.tv/oauth2/token' \
#-H 'Content-Type: application/x-www-form-urlencoded' \
#-d "client_id=sy1kxf9t94bmdwo8n4eha8kjfa04pg&client_secret=6u6gta5luyb9yndv312551mfoa1r6c&code=[code here]&grant_type=authorization_code&redirect_uri=http://localhost:3000"




# %%
import requests


def send_chat_message(broadcaster_id, sender_id, message, access_token, client_id, reply_parent_message_id=None):
    """
    Sends a chat message to a Twitch channel.

    :param broadcaster_id: The user ID of the broadcaster whose channel you're sending a message to.
    :param sender_id: The user ID of your bot.
    :param message: The chat message to send.
    :param access_token: OAuth2 bearer token.
    :param client_id: Twitch application client ID.
    :param reply_parent_message_id: (Optional) Message ID to reply to.
    :return: Response from the Twitch API.
    """
    url = 'https://api.twitch.tv/helix/chat/messages'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
        'Content-Type': 'application/json'
    }
    data = {
        "broadcaster_id": broadcaster_id,
        "sender_id": sender_id,
        "message": message
    }
    if reply_parent_message_id:
        data["reply_parent_message_id"] = reply_parent_message_id

    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Values
ACCESS_TOKEN = "3h992et9zwzjq8gqv413zoibqyly7h"
CLIENT_ID = "sy1kxf9t94bmdwo8n4eha8kjfa04pg"
BROADCASTER_ID = "708264432" #spacebarplay

SENDER_ID = "1224177800"


# Send a chat message
message = "catJAM"
response = send_chat_message(
    broadcaster_id=BROADCASTER_ID,
    sender_id=SENDER_ID,
    message=message,
    access_token=ACCESS_TOKEN,
    client_id=CLIENT_ID
)

print(response)
# %%
