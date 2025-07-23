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
playername_1 = ""
playername_2 = ""
playername_3 = ""
playername_4 = ""
playername_5 = ""
playername_6 = ""
is_server_up = True

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
    global clients_ready, playername_1, playername_2, playername_3, playername_4, playername_5, playername_6
    clients_ready += 1

    if clients_ready == 1:
        playername_1 = str(request).split("'")[1]
        return 0, bytes("1", "utf-8")
    elif clients_ready == 2:
        playername_2 = str(request).split("'")[1]
        return 0, bytes("1", "utf-8")
    elif clients_ready == 3:
        playername_3 = str(request).split("'")[1]
        return 0, bytes("2", "utf-8")
    elif clients_ready == 4:
        playername_4 = str(request).split("'")[1]
        return 0, bytes("2", "utf-8")
    elif clients_ready == 5:
        playername_5 = str(request).split("'")[1]
        return 0, bytes("3", "utf-8")
    elif clients_ready == 6:
        playername_6 = str(request).split("'")[1]
        return 0, bytes("3", "utf-8")
    elif clients_ready > 6:
        print("Alle Spiele sind voll.")
        return 0, bytes("all_games_full", "utf-8")

def disconnect_info_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    clients_ready -= 1
    return 0, bytes("-", "utf-8")

def playing_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    # create publisher
    while clients_ready % 2 != 0 and clients_ready != 0:
        print(f"clients_ready: {clients_ready}")
        idle()

    if clients_ready == 2:
        config = ecal_core.get_publisher_configuration()
        datatype_info = ecal_core.DataTypeInformation()
        topic_name = str(request).split("'")[1]
        pub_1 = ecal_core.Publisher(topic_name, datatype_info, config, event_callback = subscriber_event_callback)

        while ecal_core.ok():
            pub_1.send(bytes("Spiel 1 im Gange...", "utf-8"))
            time.sleep(2)

    if clients_ready == 4:
        config = ecal_core.get_publisher_configuration()
        datatype_info = ecal_core.DataTypeInformation()
        topic_name = str(request).split("'")[1]
        pub_2 = ecal_core.Publisher(topic_name, datatype_info, config, event_callback = subscriber_event_callback)

        while ecal_core.ok():
            pub_2.send(bytes("Spiel 2 im Gange...", "utf-8"))
            time.sleep(2)

    if clients_ready == 6:
        config = ecal_core.get_publisher_configuration()
        datatype_info = ecal_core.DataTypeInformation()
        topic_name = str(request).split("'")[1]
        pub_3 = ecal_core.Publisher(topic_name, datatype_info, config, event_callback = subscriber_event_callback)

        while ecal_core.ok():
            pub_3.send(bytes("Spiel 3 im Gange...", "utf-8"))
            time.sleep(2)

def idle():
    time.sleep(1)

if __name__ == "__main__":
    # initialize server
    ecal_core.initialize("Pong Server")

    # create server
    server = ecal_core.ServiceServer("Pong")

    # add methods to server
    connection_method_info = ecal_core.ServiceMethodInformation(method_name="connection_request")
    server.set_method_callback(connection_method_info, connection_request_callback)
    disconnect_info_method_info = ecal_core.ServiceMethodInformation(method_name="disconnect_info")
    server.set_method_callback(disconnect_info_method_info, disconnect_info_callback)
    playing_method_info = ecal_core.ServiceMethodInformation(method_name="playing_method")
    server.set_method_callback(playing_method_info, playing_callback)

    while ecal_core.ok():
        time.sleep(0.1)