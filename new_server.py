import time
import sys
import random
import pygame
from typing import Tuple
from class_game import Game

import proto_messages.pong_game_data_pb2 as pong_game_data_pb2
import ecal.nanobind_core as ecal_core

# globals
clients_ready = 0
player_names = []
games = []

# Screen
WIDTH, HEIGHT = 800, 600

# Paddles
paddle_width, paddle_height = 10, 100

# callbacks
def subscriber_event_callback(subscriber_id : ecal_core.TopicId, callback_data : ecal_core.PubEventCallbackData):
    print("Event callback invoked")
    entity = subscriber_id.topic_id
    print("A subscriber with id {} from host {} with PID {} has been {}".format(entity.entity_id, entity.host_name, entity.process_id, callback_data.event_type))

def connection_request_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    global clients_ready, player_names
    clients_ready += 1

    if clients_ready <= 6:
        player_names.append(request.decode())
        if clients_ready == 1 or clients_ready == 2:
            game_id = 0
        elif clients_ready == 3 or clients_ready == 4:
            game_id = 1
        elif clients_ready == 5 or clients_ready == 6:
            game_id = 2
        return 0, bytes(str(game_id), "utf-8")
    else:
        print("Alle Spiele sind voll.")
        return 0, bytes("-", "utf-8")
    
def left_name_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    if int(request.decode()) == 0:
        return 0, bytes(player_names[0], "utf-8")
    elif int(request.decode()) == 1:
        return 0, bytes(player_names[2], "utf-8")
    elif int(request.decode()) == 2:
        return 0, bytes(player_names[4], "utf-8")
    
def right_name_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    if int(request.decode()) == 0:
        return 0, bytes(player_names[1], "utf-8")
    elif int(request.decode()) == 1:
        return 0, bytes(player_names[3], "utf-8")
    elif int(request.decode()) == 2:
        return 0, bytes(player_names[5], "utf-8")

def player_assignment_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    if clients_ready % 2 == 0:
        return 0, bytes("2", "utf-8")
    else:
        return 0, bytes("1", "utf-8")

def paddle_input_left_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    game_id = int(request.decode().split(",")[1])
    paddle_y = int(request.decode().split(",")[0])

    games[game_id].set_paddle_left(paddle_y)
    return 0, bytes("-", "utf-8")

def paddle_input_right_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    game_id = int(request.decode().split(",")[1])
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
    name_left_method_info = ecal_core.ServiceMethodInformation(method_name="request_left_name")
    name_right_method_info = ecal_core.ServiceMethodInformation(method_name="request_right_name")
    player_assignment_method_info = ecal_core.ServiceMethodInformation(method_name="player_assignment")
    paddle_left_method_info = ecal_core.ServiceMethodInformation(method_name="paddle_input_left")
    paddle_right_method_info = ecal_core.ServiceMethodInformation(method_name="paddle_input_right")
    server.set_method_callback(connection_method_info, connection_request_callback)
    server.set_method_callback(name_left_method_info, left_name_callback)
    server.set_method_callback(name_right_method_info, right_name_callback)
    server.set_method_callback(player_assignment_method_info, player_assignment_callback)
    server.set_method_callback(paddle_left_method_info, paddle_input_left_callback)
    server.set_method_callback(paddle_right_method_info, paddle_input_right_callback)

    game0 = Game(0)
    game1 = Game(1)
    game2 = Game(2)

    games.append(game0)
    games.append(game1)
    games.append(game2)

    while clients_ready < 6:
        for game in games:
            game.idle()

        print(f"Warte auf Spieler. Ready: {clients_ready}")
        time.sleep(2)

    for i, game in enumerate(games):
        game.set_player_name(player_names[i * 2])
        game.set_player_name(player_names[i * 2 + 1])

    for game in games:
        game.print()

    while ecal_core.ok():
        for game in games:
            game.play()
            time.sleep(0.004)