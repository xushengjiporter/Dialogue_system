from DM.DST import DST
from Util import data_cleaning
import static_variables,datetime
from data import initial_data
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
                        repiles.append(static_variables.REPLIES_DICT["confirms_dict"]["".join(sys_slot.values())])
                    if ("inform" in sys_communicative_function)&("".join(list(sys_slot.keys()))=="update"):
                        repiles.append(static_variables.REPLIES_DICT["update_dict"]["".join(sys_slot.values())])
                    if ("inform" in sys_communicative_function)&("".join(list(sys_slot.keys()))=="ending"):
                        repiles.append(static_variables.REPLIES_DICT["ending"])
                        initial_data.save_history()
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

                    if(sys_communicative_function == "request")&(list(sys_slot.keys())[0] != "time")&(list(sys_slot.keys())[0] != "failure")&(len(static_variables.NEWEST_HISTORY)>0):
                        if list(sys_slot.values())[0] != "again":
                            slot_after_translation=data_cleaning.transfer_slot_to_chinese(list(sys_slot.keys())[0])
                            repiles.append("请问您的{}是否为{}?".format(slot_after_translation,static_variables.NEWEST_HISTORY[list(sys_slot.keys())[0]]))
                            continue
                        elif(list(sys_slot.keys())[0] == list(sys_slot.keys())[0])&(list(sys_slot.values())[0] == "again"):
                            repiles.append(static_variables.REPLIES_DICT["askings_dict"][static_variables.SYS_INTENT[-1]])
                            continue
                    if (sys_communicative_function == "request") & (static_variables.SYS_INTENT[-1] != 'time') & (
                            list(sys_slot.values())[0] != "ambiguous") & (list(sys_slot.values())[0] != "again") & (
                            list(sys_slot.values())[0] != "format")&((len(static_variables.NEWEST_HISTORY)==0)):
                        repiles.append(static_variables.REPLIES_DICT["askings_dict"][static_variables.SYS_INTENT[-1]])

                    if(sys_communicative_function=="request")&(list(sys_slot.values())[0]=="again")&(static_variables.SYS_INTENT[-1]=='time'):
                        hours = int((datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H"))
                        if hours >= 13 & hours <= 24:
                            static_variables.NEW_DATE = (datetime.datetime.now() + datetime.timedelta(
                                        days=1)).strftime("%Y-%m-%d ") + "10点00分"
                        else:
                                static_variables.NEW_DATE = (datetime.datetime.now() + datetime.timedelta(
                                        hours=5)).strftime("%Y-%m-%d %H") + "点00分"
                        repiles.append("那您看{}行吗".format(static_variables.NEW_DATE))
                    if (sys_communicative_function == "request") & (list(sys_slot.values())[0] == "format") & (
                                static_variables.SYS_INTENT[-1] == 'time'):
                        repiles.append("请您提供合适的时间段，格式为xx年xx月xx日xx点(xx年xx月xx日上午/下午),例如2019年3月25日10点或者2019年3月25日上午/下午")

                    if (sys_communicative_function == "request") & (list(sys_slot.values())[0] == "ambiguous") & (
                                static_variables.SYS_INTENT[-1] == 'time'):
                        text=static_variables.SLOT["time"]
                        reply="请问{}可以吗".format(text)
                        repiles.append(reply)

            for reply in repiles:
                reply = "".join(reply)
                return_sentence = return_sentence + reply
            return return_sentence
        elif cf_and_slot_list is False:
            repiles.append(static_variables.REPLIES_DICT["error_reply"])
            repiles = "".join(repiles)
            return repiles









