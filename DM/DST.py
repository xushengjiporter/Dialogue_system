from NLU import IntentClassification,slot_recognizer
import static_variables,datetime
from DM import PL
from Util import data_cleaning
nlu_modular=IntentClassification.NLUModular()
slot_recognizers=slot_recognizer.SlotRecognizer()
policy_learning=PL.PolicyLearning()


class DST_manager:
    def __init__(self):
        pass

    def manager(self,text):
        ###get the result from intent+cf+slot
        ### and filling the slot value
        ### and update need-ask-slot,sys-intent,new-slot,sys-replies

        cf_results = nlu_modular.communicative_function(text)
        slot_results = slot_recognizers.slot_recognizer(text,cf_results)
        intent_results = nlu_modular.intent_classify(text,slot_results)
        if (intent_results is False)&(slot_results is False)&((cf_results=="inform")|(cf_results=="request")):
            ##在以inform的格式说话,但是搜不到意图以及slot,则认为是无法识别的话
            return False
        elif (intent_results is False)&(slot_results is False)&((cf_results=="confirm")|(cf_results=="deny")):
            ########回答为是或者否
            cf_and_slot_list = []
            if (static_variables.SYS_INTENT[-1]=="time")&(cf_results=="confirm"):
                #########回答为是,确认时间,进行填槽,并且维护sys_intent,new_slot,need_ask_slot
                cf_and_slot=self.filling_status_variables(text=text,cf_results=cf_results,slot_keys="time")
                cf_and_slot_list.append(cf_and_slot)
                return cf_and_slot_list
            elif (static_variables.SYS_INTENT[-1]=="time")&(cf_results=="deny"):
                #########回答为否,不能进行填槽和维护三元素,需要进一步沟通
                cf_and_slot=policy_learning.ambiguous_process(text,cf_results)
                cf_and_slot_list.append(cf_and_slot)
                return cf_and_slot_list
            else:
                return False

        elif (slot_results is not False)&(cf_results=="inform")&(intent_results=='booking'):
            cf_and_slot_list = []
            for slot in slot_results:
                cf_and_slot=policy_learning.ambiguous_process(text,cf_results=cf_results)
                if cf_and_slot is not False:
                    cf_and_slot_list.append(cf_and_slot)
                    return cf_and_slot_list
                else:
                    cf_and_slot=self.filling_status_variables(text=text,cf_results=cf_results,slot_keys=slot)
                cf_and_slot_list.append(cf_and_slot)
            return cf_and_slot_list
        elif(slot_results is not False)&(cf_results=="request"):
            cf_and_slot_list = []
            for slot in slot_results:
                cf_and_slot=policy_learning.ask_slot(slot_keys=slot)
                cf_and_slot_list.append(cf_and_slot)
            return cf_and_slot_list
        else:return False



    def slotFilling(self,text,slot_keys,cf=""):


        if (slot_keys == "location"):
            location=slot_recognizers.recognize_location(text)
            static_variables.SLOT["location"]=location
        elif (slot_keys == "failure"):
            failure = slot_recognizers.recognize_location(text)
            static_variables.SLOT["failure"] = failure
        elif (slot_keys == "brand"):
            brand = slot_recognizers.recognize_location(text)
            static_variables.SLOT["brand"] = brand
        elif (slot_keys == "version"):
            version = slot_recognizers.recognize_location(text)
            static_variables.SLOT["version"] = version
        elif (slot_keys == "tele"):
            tele = slot_recognizers.recognize_location(text)
            static_variables.SLOT["tele"] = tele
        elif (slot_keys == "time"):
            if cf == "confirm":
                static_variables.SLOT["time"]=(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H") + "点"
            elif cf=="inform":
                text=data_cleaning.clean_time_text(text)
                static_variables.SLOT["time"] = text

        else:return False

    def filling_status_variables(self,text,cf_results,slot_keys):
        self.slotFilling(text, slot_keys, cf_results)
        static_variables.SYS_INTENT.append(slot_keys)
        static_variables.REPLIES_DICT["need_ask_slot"].remove(slot_keys)
        static_variables.SYS_INTENT.append(static_variables.REPLIES_DICT["need_ask_slot"][0])
        cf_and_slot = policy_learning.confirm_booking_maintenance_slot(slot_keys)
        static_variables.NEW_SLOT[slot_keys] = False
        return cf_and_slot






