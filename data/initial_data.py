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

    for i in range(len(dictProperties["slots"].split(","))):
        new_slot_flag.append(True)

    new_slot = dict(zip(dictProperties["slots"].split(","), new_slot_flag))
    return slot,sys_intent,usr_intent,ending_greeting,new_slot


def loading_replies():
    slot_keys = []
    askings = []
    confirms = []
    trigger_words = []
    updates = []

    slot_daily_talk = []
    confirm_daily_talk = []
    trigger_daily_talk = []
    print("loading slot replies...........")
    for item in dictProperties["slots"].split(","):
        slot_keys.append(item)
    for item in dictProperties["asking"].split(","):
        askings.append(dictProperties[item])
    for item in dictProperties["confirm"].split(","):
        confirms.append(dictProperties[item])
    for item in dictProperties["trigger"].split(","):
        trigger_words.append(dictProperties[item])
    for item in dictProperties["update"].split(","):
        updates.append(dictProperties[item])

    print("loading normal replies..........")
    for item in dictProperties["slot_daily_talk"].split(","):
        slot_daily_talk.append(item)
    for item in dictProperties["confirm_daily_talk"].split(","):
        confirm_daily_talk.append(dictProperties[item])
    for item in dictProperties["trigger_daily_talk"].split(","):
        trigger_daily_talk.append(dictProperties[item])

    ending = dictProperties["ending"]
    error_reply = dictProperties["error_reply"]
    need_ask_slot = slot_keys+["ending"]
    askings_dict = dict(zip(slot_keys, askings))
    confirms_dict = dict(zip(slot_keys, confirms))
    trigger_dict = dict(zip(slot_keys, trigger_words))
    update_dict = dict(zip(slot_keys, updates))
    confirm_daily_talk_dict = dict(zip(slot_daily_talk, confirm_daily_talk))
    trigger_daily_talk_dict = dict(zip(slot_daily_talk, trigger_daily_talk))
    keys = ["update_dict", "ending", "error_reply", "need_ask_slot", "askings_dict", "confirms_dict", "trigger_dict",
            "confirm_daily_talk_dict", "trigger_daily_talk_dict"]
    values = [update_dict, ending, error_reply, need_ask_slot, askings_dict, confirms_dict, trigger_dict,
              confirm_daily_talk_dict, trigger_daily_talk_dict]
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
