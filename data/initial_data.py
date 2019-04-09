from Util import properites_replies
import os
properties_path = "D:\\Users\jixusheng\PycharmProjects\Dialogue_system\\Ontology.properties"
dictProperties = properites_replies.Properties(properties_path).getProperties()


def initial_variable():
    slot = {}
    sys_intent = [None]
    usr_intent = [None, None]
    ending_greeting = False
    new_slot_flag = []
    new_date=False
    deny_count=0

    for i in range(len(dictProperties["slots"].split(","))):
        new_slot_flag.append(True)

    new_slot = dict(zip(dictProperties["slots"].split(","), new_slot_flag))
    return slot,sys_intent,usr_intent,ending_greeting,new_slot,new_date,deny_count


def loading_replies():
    slot = []
    askings = []
    confirms = []
    trigger = []
    updates = []
    trigger_request=[]
    intent = []
    confirm_intent = []
    trigger_intent = []
    confirm_request=[]
    print("loading slot replies...........")
    for item in dictProperties["slots"].split(","):
        slot.append(item)
    for item in dictProperties["asking"].split(","):
        askings.append(dictProperties[item])
    for item in dictProperties["confirm"].split(","):
        confirms.append(dictProperties[item])
    for item in dictProperties["trigger"].split(","):
        trigger.append(dictProperties[item])
    for item in dictProperties["update"].split(","):
        updates.append(dictProperties[item])
    for item in dictProperties["trigger_request"].split(","):
        trigger_request.append(dictProperties[item])
    for item in dictProperties["confirm_request"].split(","):
        confirm_request.append(dictProperties[item])

    print("loading normal replies..........")
    for item in dictProperties["intent"].split(","):
        intent.append(item)
    for item in dictProperties["confirm_intent"].split(","):
        confirm_intent.append(dictProperties[item])
    for item in dictProperties["trigger_intent"].split(","):
        trigger_intent.append(dictProperties[item])


    ending = dictProperties["ending"]
    error_reply = dictProperties["error_reply"]
    need_ask_slot = slot+["ending"]
    trigger_ambiguous_time=dictProperties["trigger_ambiguous_time"]
    askings_dict = dict(zip(slot, askings))
    confirms_dict = dict(zip(slot, confirms))
    trigger_dict = dict(zip(slot, trigger))
    trigger_request_dict = dict(zip(slot, trigger_request))
    update_dict = dict(zip(slot, updates))
    confirm_intent_dict = dict(zip(intent, confirm_intent))
    trigger_intent_dict = dict(zip(intent, trigger_intent))

    confirm_request_dict = dict(zip(slot, confirm_request))

    keys = ["update_dict", "ending", "error_reply", "need_ask_slot", "askings_dict", "confirms_dict", "trigger_dict","trigger_request_dict",
            "confirm_intent_dict", "trigger_intent_dict",'confirm_request_dict','trigger_ambiguous_time']
    values = [update_dict, ending, error_reply, need_ask_slot, askings_dict, confirms_dict, trigger_dict,trigger_request_dict,
              confirm_intent_dict, trigger_intent_dict,confirm_request_dict,trigger_ambiguous_time]
    replies_dict = dict(zip(keys, values))

    return replies_dict

def loading_history(path):
    historywithtime = {}
    filelists = os.listdir(path)
    for file in filelists:
        with open(path + file, "r", encoding="utf8") as f:
            history = {}
            lines = f.readlines()
            for line in lines:
                listline = line.strip("\n").split(":")
                history[listline[0]] = listline[1]
        file = file.strip(".txt")
        historywithtime[file] = history
    return historywithtime
