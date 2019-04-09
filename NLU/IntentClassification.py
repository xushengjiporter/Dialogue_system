from data import initial_data
from Util import data_cleaning
import static_variables
class NLUModular:
    def __init__(self):
        pass

    def intent_classify(self,text,slot_results):
        intent_list = []
        if slot_results is not False:
            d = [False for item in slot_results if item not in static_variables.REPLIES_DICT['askings_dict'].keys()]
            if (len(slot_results) > 0) & (len(d) == 0):
                intent_list.append("booking")
            else:
                for intent in static_variables.REPLIES_DICT["trigger_intent_dict"].keys():
                    for trigger_words in static_variables.REPLIES_DICT["trigger_intent_dict"][intent].split(","):
                        if trigger_words in text:
                            intent_list.append(intent)
                        else:
                            continue
        elif slot_results is False:
            return False

        ###only if booking exist then the intent should be booking
        if (len(intent_list)>0)&("booking" in intent_list):
            intent_result="booking"
            return intent_result
        elif(len(intent_list)>0)&("booking" not in intent_list):
            return intent_list[0]
        else:
            return False

    def communicative_function(self,text):
        #communicative_function_list=[]
        communicative_function_list =""

        if ("查询" in text) | ("告诉" in text):
            #communicative_function_list.append("request")
            communicative_function_list="request"
            return communicative_function_list
        elif ("不好" in text) | ("不行" in text) | ("不可以" in text) | ("不方便" in text):
            #communicative_function_list.append("deny")
            communicative_function_list = "deny"
            return communicative_function_list
        elif (("好的" in text) | ("行" in text) | ("可以" in text) | ("方便" in text)) & ("不" not in text)&("吗" not in text):
            #communicative_function_list.append("confirm")
            communicative_function_list = "confirm"
            return communicative_function_list
        else:
            #communicative_function_list.append("inform")
            communicative_function_list = "inform"
            return communicative_function_list


