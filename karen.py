from lib import *

#############################################
# FIRING RANGE
#############################################
#sendRandomGIF('momo avatar')

baseMessaage = lastMessage()

while True:
    
    currentMessage = lastMessage()

    if baseMessaage != currentMessage:

        print '[+] new message: %s' % currentMessage

        if keywordMonitor('karen') == True: 
            # search
            if keywordMonitor('karen, search for ') == True:
                query = currentMessage['msg'][18:]
                msg = 'Searching for query: %s...' % query
                sendMessage(msg)
                print '[+] sending message: %s' % msg
            elif keywordMonitor('karen search for ') == True:
                query = currentMessage['msg'][17:] 
                msg = 'Searching for query: %s...' % query
                sendMessage(msg)
                print '[+] sending message: %s' % msg

            # no direction
            else:
                msg = 'Yes, %s?' % lastMessage()['user']
                sendMessage(msg)
        
        baseMessaage = currentMessage
    else:
        print '[+] current message unchanged: %s' % currentMessage