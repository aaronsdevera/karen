from lib import *

#############################################
# FIRING RANGE
#############################################
#sendRandomGIF('momo avatar')

baseMessage = lastMessage()

while True:
    
    currentMessage = lastMessage()

    if baseMessage != currentMessage:

        #print '[+] new message: %s' % currentMessage

        if keywordMonitor('karen',currentMessage) == True: 
            # Disregard comma after karen
            if len(currentMessage['msg']) > 5:
                currentMessage['msg'] = currentMessage['msg'].replace(',','',1)

            # Search methods
            if keywordMonitor('karen search for ',currentMessage) == True:
                # Query detection
                query = currentMessage['msg'][17:]
                msg = 'Searching for query: %s...' % query
                sendMessage(msg)
                #print '[+] sending message: %s' % msg

                results = searchFor(query)
                # No results found
                if results is None:
                    msg = 'No one has mentioned \"%s\" so far.' % query
                    sendMessage(msg)
                    #print '[+] sending message: %s' % msg
                #Send a message with the results
                else:
                    msg = '' #reset the message variable
                    for result in results: 
                        # double slash is needed to escape in JSON
                        msg += "{0}: {1} \\n".format(result['user'], result['msg'])
                    sendMessage(msg) 
                    #print '[+] sending message: %s' % msg

            # no direction
            else:
                msg = 'Yes, %s?' % currentMessage['user']
                sendMessage(msg)
        
        baseMessage = currentMessage
    else:
        #print '[+] current message unchanged: %s' % currentMessage