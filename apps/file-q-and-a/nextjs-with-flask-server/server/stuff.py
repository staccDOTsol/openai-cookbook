import json 
with open ("/home/st/Downloads/result.json", 'r') as f: 
    data = json.loads(f.read() )
with open ('./stuff.txt', 'w+') as stuff:
    for chat in data['chats']['list']:
        for message in chat['messages']:
            if 'from' in message.keys():
                try:
                    
                    if 'Jarett Dunn' in message['from']:
                        for ent in message['text_entities']:
                            if 'text' in ent:
                                stuff.write(ent['text'] + '\n')
                except:
                    pass