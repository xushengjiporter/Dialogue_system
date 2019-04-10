from Util import properites_replies
import os,datetime
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

def loading_history():
    import static_variables,collections
    historywithtime=collections.OrderedDict()
    filelists = os.listdir(static_variables.HISTORY_PATH)
    for file in filelists:
        if file=="__pycache__":
            continue
        else:
            with open(static_variables.HISTORY_PATH + file, "r", encoding="utf8") as f:
                history = {}
                lines = f.readlines()
                for line in lines:
                    listline = line.strip("\n").split(":")
                    history[listline[0]] = listline[1]
            file = file.strip(".txt")
            historywithtime[file] = history

    return historywithtime


def save_history():
    import static_variables
    log_name = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    path =static_variables.HISTORY_PATH +log_name + ".txt"
    with open(path,"a",encoding="utf-8") as f:
        for slot_key,slot_value in static_variables.SLOT.items():
            f.write(slot_key)
            f.write(":")
            f.write(slot_value+"\n")
    f.close()

def get_newest_history():
    import static_variables
    if len(static_variables.HISTORY_WITH_TIME)>0:
        newest_history_key = list(static_variables.HISTORY_WITH_TIME.keys())[-1]
        newest_history = static_variables.HISTORY_WITH_TIME[newest_history_key]
        return newest_history
    else:
        return {}