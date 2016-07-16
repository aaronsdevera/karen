import requests
from keys import keys

access_token = keys['token']
group_token = keys['group']
bot_id_token = keys['bot_id']
monitoring_url = 'https://api.groupme.com/v3/groups/%s/messages?token=%s&limit=1' % (group_token,access_token)
payload_url = 'https://api.groupme.com/v3/bots/post'

#############################################
# HELPER FUNCTIONS
#############################################

# monitoring functions
#############################################

# get last message
def lastMessage():
    r = requests.get(monitoring_url)
    msg = r.json()['response']['messages'][0]['text']
    user = r.json()['response']['messages'][0]['name']
    return {'user':user,'msg':msg}

# monitor for keyword
def keywordMonitor(query):
    if query.lower() in lastMessage()['msg'].lower():
        return True
    else: return False


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

