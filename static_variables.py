from data import initial_data
HISTORY_PATH = "D:\\Users\jixusheng\PycharmProjects\Dialogue_system\\history\\"
REPLIES_DICT = initial_data.loading_replies()
SLOT, SYS_INTENT, USR_INTENT, ENDING_GREETING, NEW_SLOT, NEW_DATE, DENY_COUNT = initial_data.initial_variable()
HISTORY_WITH_TIME=initial_data.loading_history()
NEWEST_HISTORY=initial_data.get_newest_history()



