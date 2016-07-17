import requests
from keys import keys

access_token = keys['token']
group_token = keys['group']
bot_id_token = keys['bot_id']
payload_url = 'https://api.groupme.com/v3/bots/post'

#############################################
# HELPER FUNCTIONS
#############################################

# monitoring functions
#############################################

# get last message
def lastMessage():
    monitoring_url_latest = 'https://api.groupme.com/v3/groups/%s/messages?token=%s&limit=1' % (group_token,access_token)
    r = requests.get(monitoring_url_latest)
    msg_id = r.json()['response']['messages'][0]['id']
    timestamp = r.json()['response']['messages'][0]['created_at']
    msg = r.json()['response']['messages'][0]['text']
    user = r.json()['response']['messages'][0]['name']
    return {'user':user,'msg':msg,'timestamp':timestamp,'msg_id':msg_id}

# get last messages
def allMessages():

    chat_history = []
    count = 0

    allMessageCount = requests.get('https://api.groupme.com/v3/groups/%s?token=%s' % (group_token,access_token)).json()['response']['messages']['count']
    latestMessage = lastMessage()
    baseMessage = {'count':count,'user':latestMessage['user'],'msg':latestMessage['msg'],'timestamp':latestMessage['timestamp'],'msg_id':latestMessage['msg_id']}
    chat_history.append(baseMessage)
    count += 1

    while count < allMessageCount:
        lastID = chat_history[-1]['msg_id']
        monitoring_url_max_with_id = 'https://api.groupme.com/v3/groups/%s/messages?token=%s&limit=100&before_id=' % (group_token,access_token)
        r = requests.get(monitoring_url_max_with_id+lastID)
        messageBucket = r.json()['response']['messages']
        for each in messageBucket:
            msg_id = each['id']
            timestamp = each['created_at']
            msg = each['text']
            user = each['name']
            message_history_row = {'count':count,'user':user,'msg':msg,'timestamp':timestamp,'msg_id':msg_id}
            chat_history.append(message_history_row)
            count += 1

    return chat_history

# monitor for keyword
def keywordMonitor(query, lastMsg):
    if query.lower() in lastMsg['msg'].lower():
        return True
    else: return False

# searching functions
#############################################
# Expects an array like this
# [
#   {
#       "user": "Sam Joseph",
#       "msg": "I like pandas"
#   },
#   {
#       "user": "Aaron DeVera",
#       "msg": "I like gummy bears"
#   },
# ]

def searchFor(query):
    messages = allMessages()
    #print "allMessages:", messages
    resultSet = []
    if type(messages) != list:
        #print '[+] Error! Query \'messages is not a list.\''
        return None

    for message in messages:
        if message['msg'] is not None:
            if query.lower() in message['msg'].lower():
                message['msg'] = message['msg'].replace('\n','\\n')
                resultSet.append(message)

    #No results found. Returning none.
    if resultSet == []:
        return None

    #print "resultSet: ", resultSet
    return resultSet

# messaging functions
#############################################

def compileMessage(bot_id, msg):
    return '{"bot_id": "%s", "text": "%s"}' % (bot_id,msg)

def compilePictureMessage(bot_id, msg, img_url):
    return '{"bot_id":"%s","text":"%s","attachments":[{"type":"image","url":"%s"}]}' % (bot_id,msg,img_url)

def stockGarbageDay(bot_id):
    msg = 'GARRRRBAGE DAAAAAAY'
    img_url = giphySearchRandom('garbage day silent night')
    return compilePictureMessage(bot_id, msg, img_url)

# imaging functions
#############################################

def giphySearchFirst(search_term):
    compiled_search_term = search_term.replace(' ','+')
    r = requests.get('http://api.giphy.com/v1/gifs/search?limit=1&q=%s&api_key=dc6zaTOxFJmzC' % compiled_search_term)
    return r.json()['data'][0]['images']['original']['url']

def giphySearchRandom(search_term):
    compiled_search_term = search_term.replace(' ','+')
    r = requests.get('http://api.giphy.com/v1/gifs/search?limit=50&q=%s&api_key=dc6zaTOxFJmzC' % compiled_search_term)
    import random
    limit = random.randint(0,49)
    return r.json()['data'][limit]['images']['original']['url']

# sending functions
#############################################

# send a text message
def sendMessage(msg):
    r = requests.post(payload_url, data = compileMessage(bot_id_token, msg))

# send the first gif given as a result
def sendFirstGIF(search_term):
    r = requests.post(payload_url, data = compilePictureMessage(bot_id_token, '', giphySearchFirst(search_term)))

# send a random gif 
def sendRandomGIF(search_term):
    r = requests.post(payload_url, data = compilePictureMessage(bot_id_token, '', giphySearchRandom(search_term)))

