import time
import threading
from typing import Tuple
from Game import Game

import proto_messages.pong_game_data_pb2 as pong_game_data_pb2
import ecal.nanobind_core as ecal_core

# globals
clients_ready = 0
player_names  = []
games = []

# screen
WIDTH  = 800
HEIGHT = 800

# paddles
paddle_width  =  10
paddle_height = 100

# loop for threads
def run_game(game : Game):
    game.idle()

    while ecal_core.ok():
        game.play()
        time.sleep(0.01)

# callbacks
def subscriber_event_callback(subscriber_id : ecal_core.TopicId, callback_data : ecal_core.PubEventCallbackData):
    print("Event callback invoked")
    entity = subscriber_id.topic_id
    print("A subscriber with id {} from host {} with PID {} has been {}".format(entity.entity_id, entity.host_name, entity.process_id, callback_data.event_type))

def connection_request_callback(method_information: ecal_core.ServiceMethodInformation, request: bytes) -> Tuple[int, bytes]:
    global clients_ready, player_names, games

    player_name = request.decode()
    player_names.append(player_name)
    clients_ready += 1

    # calculate game id
    game_id = (clients_ready - 1) // 2

    # create game on demand
    if clients_ready % 2 == 0:
        new_game = Game(game_id)
        new_game.set_player_name(player_names[game_id * 2])
        new_game.set_player_name(player_names[game_id * 2 + 1])
        games.append(new_game)

        # start new thread
        game_thread = threading.Thread(target=run_game, args=(new_game,), daemon=True)
        game_thread.start()

    print(f"{player_name} wurde Spiel {game_id} zugewiesen.")
    return 0, bytes(str(game_id), "utf-8")

def left_name_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    game_id = int(request.decode())
    return 0, bytes(player_names[game_id * 2], "utf-8")

def right_name_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    game_id = int(request.decode())
    return 0, bytes(player_names[game_id * 2 + 1], "utf-8")

def player_assignment_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    if clients_ready % 2 == 0:
        return 0, bytes("2", "utf-8")
    else:
        return 0, bytes("1", "utf-8")

def paddle_input_left_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    game_id  = int(request.decode().split(",")[1])
    paddle_y = int(request.decode().split(",")[0])

    games[game_id].set_paddle_left(paddle_y)
    return 0, bytes("-", "utf-8")

def paddle_input_right_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    game_id  = int(request.decode().split(",")[1])
    paddle_y = int(request.decode().split(",")[0])

    games[game_id].set_paddle_right(paddle_y)
    return 0, bytes("-", "utf-8")

if __name__ == "__main__":
    # initialize server
    ecal_core.initialize("Pong Server")

    # create server
    server = ecal_core.ServiceServer("Pong")

    # add methods to server
    connection_method_info = ecal_core.ServiceMethodInformation(method_name="connection_request")
    name_left_method_info  = ecal_core.ServiceMethodInformation(method_name="request_left_name")
    name_right_method_info = ecal_core.ServiceMethodInformation(method_name="request_right_name")
    player_assignment_method_info = ecal_core.ServiceMethodInformation(method_name="player_assignment")
    paddle_left_method_info  = ecal_core.ServiceMethodInformation(method_name="paddle_input_left")
    paddle_right_method_info = ecal_core.ServiceMethodInformation(method_name="paddle_input_right")
    server.set_method_callback(connection_method_info, connection_request_callback)
    server.set_method_callback(name_left_method_info, left_name_callback)
    server.set_method_callback(name_right_method_info, right_name_callback)
    server.set_method_callback(player_assignment_method_info, player_assignment_callback)
    server.set_method_callback(paddle_left_method_info, paddle_input_left_callback)
    server.set_method_callback(paddle_right_method_info, paddle_input_right_callback)

    # waiting for at least 2 players
    while clients_ready < 2:
        print("Warte auf mindestens 2 Spieler...")
        time.sleep(3)

    # main loop
    while ecal_core.ok():
        print("Spiele im Gange...")
        time.sleep(15)

    # finalize eCAL API
    ecal_core.finalize()
