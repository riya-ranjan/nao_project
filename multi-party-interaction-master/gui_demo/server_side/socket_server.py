from websocket_server import WebsocketServer
import json
import os.path as path
import subprocess
import argparse
import atexit
import sys


from robot_action import perform_action

sys.path.append("../..")

import config
from config import to_path_str, debugScriptPath, projectRootPath

HOST = config.SERVER_HOST
PORT = config.SERVER_PORT
FLAGS = None
SHELL = "bash"

clientIDMap = dict()
# values are boolean value, True means this client is recording
recordingStatusMap = dict()
isRecording = False


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    clientIDMap[client['id']] = client
    recordingStatusMap[client['id']] = False


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])
    clientIDMap.pop(client['id'], None)
    recordingStatusMap.pop(client['id'], None)


# Called when a client sends a message
def message_received(client, server, message):
    global BASE_OUTPUT_DIR
    global isRecording

    msg_obj = json.loads(message)
    print("Client(%d) said: %s" % (client['id'], message))
    msg_type = msg_obj.get("type", "").strip()

    if msg_type == "robotCommand":
        # if message type command, perform on robot
        target = str(msg_obj["target"].strip())
        action = str(msg_obj["action"].strip())
        content = str(msg_obj.get("content", "").strip())

        if action.lower() == "say":
            print("say \"{}\" to \"{}\"".format(content, target))
        else:
            print("perform \"{}\" to \"{}\"".format(action, target))
        perform_action(target, action, content)
    elif msg_type == "systemCommand":
        content = str(msg_obj.get("content", "").strip())

        if content == "startRecording":
            subprocess.Popen([SHELL, '{}/record_all_in_one.sh'.format(FLAGS.output)])
            isRecording = True

        if content == "stopRecording":
            subprocess.call(['tmux', 'ls'])
            subprocess.Popen(['tmux', 'kill-server'])
            isRecording = False
    elif msg_type == "systemQuery":
        content = str(msg_obj.get("content", "").strip())

        if content == "recordStatus":
            response_obj = json.dumps({
                "type": "systemResponse",
                "response": "recordStatus",
                "content": isRecording
            })

            server.send_message(client, response_obj)
    else:
        # if type unknown
        print("unknown type message:\n\t{}".format(msg_obj))


@atexit.register
def exit_hook():
    print("\nServer exiting...")
    subprocess.Popen(['tmux', 'kill-server'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    parser.add_argument("-o", "--output", dest="output", help="the path to output directory to store the recording",
                        default=to_path_str(projectRootPath, "record"))
    FLAGS = parser.parse_args()

    from debug_scripts.master_control import pop_source
    pop_source(to_path_str(debugScriptPath, "nao_mvt_data"))

    from debug_scripts import master_control
    master_control.muted = False

    server = WebsocketServer(PORT, HOST)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    print("server running...")
    server.run_forever()
