from Util import properites_replies
properties_path = "D:\\Users\jixusheng\PycharmProjects\shanda\\replies.properties"
dictProperties = properites_replies.Properties(properties_path).getProperties()

slot = {}
sys_intent = [None]
usr_intent = [None, None]
ending_greeting = False
new_slot_flag=[]

for i in range(len(dictProperties["slots"].split(","))):
    new_slot_flag.append(True)

new_slot=dict(zip(dictProperties["slots"].split(","),new_slot_flag))


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