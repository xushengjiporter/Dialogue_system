import static_variables,collections
from Util import data_cleaning
class PolicyLearning:
    #####responsible for maintain the sys-replies

    def __init__(self):
        pass

    def ask_slot(self,slot_keys):
        if len(static_variables.REPLIES_DICT["need_ask_slot"])<2:
            sys_communicative_function, sys_slot_keys, sys_slot_values = [], [], []
            sys_communicative_function.append("inform")
            sys_slot_keys.append(slot_keys)
            sys_slot_values.append(static_variables.SLOT[slot_keys])
            cf_and_slot = collections.OrderedDict()
            for i in range(len(sys_communicative_function)):
                dict = {}
                dict[sys_slot_keys[i]] = sys_slot_values[i]
                cf_and_slot[sys_communicative_function[i]] = dict
        else:
            sys_communicative_function, sys_slot_keys, sys_slot_values = [], [], []
            sys_communicative_function.append("inform")
            sys_slot_keys.append(slot_keys)
            sys_slot_values.append(static_variables.SLOT[slot_keys])
            sys_communicative_function.append("request")
            sys_slot_keys.append(static_variables.REPLIES_DICT["need_ask_slot"][0])
            sys_slot_values.append(None)
            cf_and_slot = collections.OrderedDict()
            for i in range(len(sys_communicative_function)):
                dict = {}
                dict[sys_slot_keys[i]] = sys_slot_values[i]
                cf_and_slot[sys_communicative_function[i]] = dict

        return cf_and_slot

    def generate_sys_cf_and_slot(self,slot_keys):
        sys_communicative_function, sys_slot_keys, sys_slot_values = [], [], []

        if (static_variables.NEW_SLOT[slot_keys] is True)&(len(static_variables.REPLIES_DICT["need_ask_slot"])>=2):
            sys_communicative_function.append("inform")
            sys_slot_keys.append("confirm")
            sys_slot_values.append(slot_keys)
            sys_communicative_function.append("request")
            sys_slot_keys.append(static_variables.REPLIES_DICT["need_ask_slot"][0])
            sys_slot_values.append(None)
        elif (static_variables.NEW_SLOT[slot_keys] is True)&(len(static_variables.REPLIES_DICT["need_ask_slot"])==1):
            sys_communicative_function.append("inform")
            sys_slot_keys.append("confirm")
            sys_slot_values.append(slot_keys)
            sys_communicative_function.append("inform_inform")
            sys_slot_keys.append("ending")
            sys_slot_values.append(None)
        elif (static_variables.NEW_SLOT[slot_keys] is False)&(len(static_variables.REPLIES_DICT["need_ask_slot"])>=2):
            sys_communicative_function.append("inform")
            sys_slot_keys.append("update")
            sys_slot_values.append(slot_keys)
            sys_communicative_function.append("request")
            sys_slot_keys.append(static_variables.REPLIES_DICT["need_ask_slot"][0])
            sys_slot_values.append(None)
        elif len(static_variables.REPLIES_DICT["need_ask_slot"])==1:
            sys_communicative_function.append("inform")
            sys_slot_keys.append("update")
            sys_slot_values.append(slot_keys)
        else:return False

        cf_and_slot=collections.OrderedDict()
        for i in range(len(sys_communicative_function)):
            dict={}
            dict[sys_slot_keys[i]]=sys_slot_values[i]
            cf_and_slot[sys_communicative_function[i]]=dict
        return cf_and_slot

    def ambiguous_process(self,text,cf_results):
        d=[True for item in static_variables.REPLIES_DICT["trigger_ambiguous_time"] if item in text]
        if (len(d)>0)&(cf_results=="inform"):
            static_variables.SYS_INTENT.append("time")
            cf_and_slot = {"request": {"time": "ambiguous"}}
            text = data_cleaning.clean_time_text(text=text)
            static_variables.SLOT["time"] = text
            return cf_and_slot
        elif (cf_results=="deny")&(static_variables.SYS_INTENT[-1]=="time"):
            if static_variables.DENY_COUNT == 1:
                static_variables.DENY_COUNT += 1
                cf_and_slot = {"request": {"time": "format"}}
                return cf_and_slot
            elif static_variables.DENY_COUNT == 2:
                static_variables.DENY_COUNT += 1
                cf_and_slot = {"inform": {"operator": None}}
                return cf_and_slot
            elif static_variables.DENY_COUNT == 0:
                static_variables.DENY_COUNT += 1
                cf_and_slot = {"request": {"time": "again"}}
                return cf_and_slot
        elif(cf_results=="deny")&(static_variables.SYS_INTENT[-1]!="time"):
            cf_and_slot = {"request": {static_variables.SYS_INTENT[-1]: "again"}}
            return cf_and_slot
        else:
            return False












