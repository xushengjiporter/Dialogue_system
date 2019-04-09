from DM import PL,DST
from Util import data_cleaning
import static_variables,datetime
dst_manager=DST.DST_manager()

class NLGManager:
    def __init__(self):
        pass

    def generation(self,text):
        cf_and_slot_list=dst_manager.manager(text)
        repiles = []
        return_sentence = ""
        if cf_and_slot_list is not False:
            for cf_and_slot in cf_and_slot_list:
                for sys_communicative_function,sys_slot in cf_and_slot.items():
                    if ("inform" in sys_communicative_function)&("".join(list(sys_slot.keys()))=="confirm"):
                        repiles.append(static_variables.REPLIES_DICT["confirms_dict"][static_variables.SYS_INTENT[-2]])
                    if ("inform" in sys_communicative_function)&("".join(list(sys_slot.keys()))=="update"):
                        repiles.append(static_variables.REPLIES_DICT["update_dict"][static_variables.SYS_INTENT[-2]])
                    if ("inform" in sys_communicative_function)&("".join(list(sys_slot.keys()))=="ending"):
                        repiles.append(static_variables.REPLIES_DICT["ending"])
                    if ("inform" in sys_communicative_function)&("".join(list(sys_slot.keys()))=="operator"):
                        repiles.append("已经为您转接客服")
                    if ("inform" in sys_communicative_function)&("".join(list(sys_slot.keys())) in static_variables.REPLIES_DICT['askings_dict'].keys()):
                        infor=static_variables.SLOT["".join(list(sys_slot.keys()))]
                        repiles.append(static_variables.REPLIES_DICT['confirm_request_dict']["".join(list(sys_slot.keys()))]+infor+'。')

                    if (sys_communicative_function=="request")&(list(sys_slot.values())[0] is None)&(static_variables.SYS_INTENT[-1]=='time'):
                        repiles.append(
                            ''.join(
                                static_variables.REPLIES_DICT["askings_dict"][static_variables.SYS_INTENT[-1]]).format(
                                (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                                    "%Y-%m-%d ") + "16点30分"))
                        # slot_value=list(sys_slot.values())[0]
                        # if (static_variables.SYS_INTENT[-1]=='time')&(slot_value == None):
                    if(sys_communicative_function=="request")&(list(sys_slot.values())[0]==["again"])&(static_variables.SYS_INTENT[-1]=='time'):
                        hours = int((datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H"))
                        if hours >= 13 & hours <= 24:
                            static_variables.NEW_DATE = (datetime.datetime.now() + datetime.timedelta(
                                        days=1)).strftime("%Y-%m-%d ") + "10点00分"
                        else:
                                static_variables.NEW_DATE = (datetime.datetime.now() + datetime.timedelta(
                                        hours=5)).strftime("%Y-%m-%d %H") + "点00分"
                        repiles.append("那您看{}行吗".format(static_variables.NEW_DATE))
                    if (sys_communicative_function == "request") & (list(sys_slot.values())[0] == ["format"]) & (
                                static_variables.SYS_INTENT[-1] == 'time'):
                        repiles.append("请您提供合适的时间段，格式为xx年xx月xx日xx点(xx年xx月xx日上午/下午),例如2019年3月25日10点或者2019年3月25日上午/下午")
                    if (sys_communicative_function == "request") & (list(sys_slot.values())[0] == ["ambiguous"]) & (
                                static_variables.SYS_INTENT[-1] == 'time'):
                        text = data_cleaning.clean_time_text(text)
                        repiles.append("请问{}可以吗".format(text))
                    if(sys_communicative_function == "request") & (list(sys_slot.values())[0] != ["ambiguous"])& (list(sys_slot.values())[0] != ["again"])& (list(sys_slot.values())[0] != ["format"]):
                        repiles.append(static_variables.REPLIES_DICT["askings_dict"][static_variables.SYS_INTENT[-1]])
            for reply in repiles:
                reply = "".join(reply)
                return_sentence = return_sentence + reply
            return return_sentence
        elif cf_and_slot_list is False:
            repiles.append(static_variables.REPLIES_DICT["error_reply"])
            repiles = "".join(repiles)
            return repiles




