from NLU.slot_recognizer import slot_recognizer
from NLU.intent_classification import IntentClassification
import static_variables,datetime
from DM.PL import PL
from Util import data_cleaning
nlu_modular= IntentClassification.NLUModular()
slot_recognizers=slot_recognizer.SlotRecognizer()
policy_learning=PL.PolicyLearning()


class DST_manager:
    def __init__(self):
        pass
    def manager(self,text):
        cf_results = nlu_modular.communicative_function(text)
        slot_results = slot_recognizers.slot_recognizer(text,cf_results)
        intent_results = nlu_modular.intent_classify(text,slot_results)
        if (intent_results is False)&(slot_results is False)&((cf_results=="inform")|(cf_results=="request")):
            ##在以inform的格式说话,但是搜不到意图以及slot,则认为是无法识别的话
            return False
        elif (intent_results is False)&(slot_results is False)&((cf_results=="confirm")|(cf_results=="deny")):
            ########回答为是或者否
            sys_cf_and_slot_list = []
            if (static_variables.SYS_INTENT[-1]=="time")&(cf_results=="confirm"):
                #########回答为是,确认时间,进行填槽,并且维护sys_intent,new_slot,need_ask_slot
                sys_cf_and_slot=self.update_dialog_status(text=text,cf_results=cf_results,slot_keys="time")
                sys_cf_and_slot_list.append(sys_cf_and_slot)
                return sys_cf_and_slot_list
            elif (static_variables.SYS_INTENT[-1]=="time")&(cf_results=="deny"):
                #########回答为否,不能进行填槽和维护三元素,需要进一步沟通
                cf_and_slot=policy_learning.ambiguous_process(text,cf_results)
                sys_cf_and_slot_list.append(cf_and_slot)
                return sys_cf_and_slot_list
            elif (static_variables.SYS_INTENT[-1]!="time")&(cf_results=="confirm"):
                sys_cf_and_slot = self.update_dialog_status(text=text, cf_results=cf_results, slot_keys=static_variables.SYS_INTENT[-1])
                sys_cf_and_slot_list.append(sys_cf_and_slot)
                return sys_cf_and_slot_list
            elif (static_variables.SYS_INTENT[-1]!="time")&(cf_results=="deny"):
                #########回答为否,不能进行填槽和维护三元素,需要进一步沟通
                cf_and_slot=policy_learning.ambiguous_process(text,cf_results)
                sys_cf_and_slot_list.append(cf_and_slot)
                return sys_cf_and_slot_list
            else:
                return False
        elif (slot_results is not False)&(cf_results=="inform")&(intent_results=='booking'):
            sys_cf_and_slot_list = []
            for slot in slot_results:
                sys_cf_and_slot=policy_learning.ambiguous_process(text,cf_results=cf_results)
                if sys_cf_and_slot is not False:
                    sys_cf_and_slot_list.append(sys_cf_and_slot)
                    return sys_cf_and_slot_list
                else:
                    sys_cf_and_slot=self.update_dialog_status(text=text,cf_results=cf_results,slot_keys=slot)
                    sys_cf_and_slot_list.append(sys_cf_and_slot)
            sys_cf_and_slot_list=self.trunk_multiple_slot_request(cf_and_slot_list=sys_cf_and_slot_list,)
            return sys_cf_and_slot_list
        elif(slot_results is not False)&(cf_results=="request"):
            sys_cf_and_slot_list = []
            for slot in slot_results:
                sys_cf_and_slot=policy_learning.ask_slot(slot_keys=slot)
                sys_cf_and_slot_list.append(sys_cf_and_slot)
            return sys_cf_and_slot_list
        else:return False

    def slot_filling(self,text,slot_keys,cf=""):
        if slot_keys == "location":
            if cf == "confirm":
                static_variables.SLOT["location"] = static_variables.NEWEST_HISTORY["location"]
            elif cf=="inform":
                location=slot_recognizers.recognize_location(text)
                static_variables.SLOT["location"]=location
        elif slot_keys == "failure":
            failure = slot_recognizers.recognize_failure(text)
            static_variables.SLOT["failure"] = failure
        elif slot_keys == "brand":
            if cf=="confirm":
                static_variables.SLOT["brand"]=static_variables.NEWEST_HISTORY["brand"]
            elif cf=="inform":
                brand = slot_recognizers.recognize_brand(text)
                static_variables.SLOT["brand"] = brand
        elif slot_keys == "version":
            if cf=="confirm":
                static_variables.SLOT["version"] = static_variables.NEWEST_HISTORY["version"]
            elif cf=="inform":
                version = slot_recognizers.recognize_version(text)
                static_variables.SLOT["version"] = version
        elif slot_keys == "tele":
            if cf == "confirm":
                static_variables.SLOT["tele"] = static_variables.NEWEST_HISTORY["tele"]
            elif cf=="inform":
                tele = slot_recognizers.recognize_tele(text)
                static_variables.SLOT["tele"] = tele
        elif slot_keys == "time":
            if cf == "confirm":
                static_variables.SLOT["time"]=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H") + "点"
            elif cf=="inform":
                text=data_cleaning.clean_time_text(text)
                static_variables.SLOT["time"] = text
        else:return False

    def update_dialog_status(self,text,cf_results,slot_keys):
        ##check whether the slot has been filled, if yes,then no need to filling slots

        if static_variables.NEW_SLOT[slot_keys] is True:
            self.slot_filling(text, slot_keys, cf_results)
            static_variables.SYS_INTENT.append(slot_keys)
            static_variables.REPLIES_DICT["need_ask_slot"].remove(slot_keys)
            static_variables.SYS_INTENT.append(static_variables.REPLIES_DICT["need_ask_slot"][0])
            cf_and_slot = policy_learning.generate_sys_cf_and_slot(slot_keys)
            static_variables.NEW_SLOT[slot_keys] = False
            return cf_and_slot
        elif (static_variables.NEW_SLOT[slot_keys] is False)&(len(static_variables.REPLIES_DICT["need_ask_slot"])>1):
            self.slot_filling(text, slot_keys, cf_results)
            static_variables.SYS_INTENT.append(slot_keys)
            static_variables.SYS_INTENT.append(static_variables.REPLIES_DICT["need_ask_slot"][0])
            cf_and_slot = policy_learning.generate_sys_cf_and_slot(slot_keys)
            return cf_and_slot
        elif (static_variables.NEW_SLOT[slot_keys] is False) & (len(static_variables.REPLIES_DICT["need_ask_slot"]) == 1):
            self.slot_filling(text, slot_keys, cf_results)
            static_variables.SYS_INTENT.append(slot_keys)
            static_variables.SYS_INTENT.append("ending")
            cf_and_slot = policy_learning.generate_sys_cf_and_slot(slot_keys)
            return cf_and_slot

    def trunk_multiple_slot_request(self,cf_and_slot_list):
        request_list = []
        count=0
        if len(cf_and_slot_list)>=2:
            for cf_and_slot in cf_and_slot_list:
                [request_list.append(item) for item in list(cf_and_slot.keys()) if item=="request"]
            if len(request_list)>=2:
                for cf_and_slot in cf_and_slot_list:
                    if count<len(cf_and_slot_list)-1:
                        cf_and_slot.pop("request")
                        count+=1

        return cf_and_slot_list









