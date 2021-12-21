import json

def check_if_bot_exists(name):
    file = open('bot_data.json')
    data = json.load(file) 

    # bots list 
    bots_list = data["bots"]
    bots_list_names = []
    for bot in bots_list:
        bots_list_names.append(bot["bot_name"])

    #print(bots_list_names)

    if name in bots_list_names: 
        return True
    else: 
        return False