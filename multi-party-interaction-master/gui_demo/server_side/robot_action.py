import sys

sys.path.append("../..")

from debug_scripts.master_control import call_command, test, inprogress, exec_keyframe, P_1, P_3, P_5, muted
from debug_scripts.master_control import say, look, intro_seq, exit_seq, default_sit, split_sent, exec_keyframe, intro_ques, exit_ques
import debug_scripts.master_control
# from my_thread import StoppableThread as Thread
from threading import Thread

SUPPORTED_ACTIONS = {
    "acknowledgement": "Acknowledgement",
    "advice": "Practical",
    "agreement": "Agreement",
    "clarification": "Clarification",
    "disagreement": "Disagreement",
    "followUp": "Follow-Up",
    "qLow": "Question Low",
    "qMed": "Question Medium",
    "qHigh": "Question High",
}

PARTICIPANT_MAP = {
    # "left": P_1,
    "left": P_5,
    "center": P_3,
    # "right": P_5,
    "right": P_1,
    "group": "group",
    "self": P_3,
}

UNIQ_SAY_MAP = {
    "low": "Question Low",
    "med": "Question Medium",
    "high": "Question High",
    "discL": "Disclosure Low",
    "discM": "Disclosure Medium",
    "discH": "Disclosure High",
    "warn": "Warning"
}

first = 1


def uniq_say(action_str, content, participant):
    print(split_sent(action_str)[1], content)
    command = UNIQ_SAY_MAP.get(split_sent(action_str)[1])
    time = (len(content) / 15.0) + 1.5
    time = 3.0
    exec_keyframe(participant, time, command, content, )
    default_sit()


def perform_action(target, action_str, content=None):
    # global inprogress
    # global interrupt
    global first
    thread = None
    #    return
    action = SUPPORTED_ACTIONS.get(action_str, None)
    print("START")
    if first:
        first = 0
    else:
        print("NOT FIRST TIME!")
        # not first time to run interrupt
        if debug_scripts.master_control.inprogress and not action_str == "look":
            print("send out interrupt")
            debug_scripts.master_control.interrupt = 1
            while debug_scripts.master_control.interrupt == 1:
                pass
    debug_scripts.master_control.inprogress = 1
    if action_str == "say":
        if muted:
            print("SPEECH MUTED")
            print("say ", str(content))
        else:
            say(str(content))
            debug_scripts.master_control.inprogress = 0

    elif action_str == "introq":
            thread = Thread(target=intro_ques)
    elif action_str == "exitq":
            thread = Thread(target=exit_ques)
    elif "speech" in action_str:
        if action_str == "speech in":
            thread = Thread(target=intro_seq)
        else:
            thread = Thread(target=exit_seq)
    elif action_str == "look":
        print(PARTICIPANT_MAP.get(target))
        part = PARTICIPANT_MAP.get(target, P_3)
        print(part)
        look(part)
        debug_scripts.master_control.inprogress = 0
    elif action is not None:
        thread = Thread(target=call_command, args=(action, PARTICIPANT_MAP.get(target, P_3)))
    elif "say" in action_str:
        # denotes special say case
        thread = Thread(target=uniq_say, args=(action_str, str(content), PARTICIPANT_MAP.get(target)))
    else:
        print("Unknown commad:", action_str)
    if thread:
        thread.start()
    return True


if __name__ == "__main__":
    pass
