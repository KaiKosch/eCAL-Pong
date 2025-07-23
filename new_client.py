import time
import sys
import pygame

import proto_messages.pong_game_data_pb2 as pong_game_data_pb2
import ecal.nanobind_core as ecal_core

# Gamestate parameters
clients_ready = 0
left_paddle_pos = 250
right_paddle_pos = 250
ball_position_x = 400
ball_position_y = 300
left_score = 0
right_score = 0
player = 1
playername_1 = "Player_1"
playername_2 = "Player_2"
player2IsConnected = False
closed = False

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen
WIDTH, HEIGHT = 800, 600

# Paddles
paddle_width, paddle_height = 10, 100
paddle_speed = 6

# callbacks
def data_callback(publisher_id : ecal_core.TopicId, datatype_info : ecal_core.DataTypeInformation, data : ecal_core.ReceiveCallbackData):
    print(f"{data.buffer}")

def publisher_event_callback(publisher_id : ecal_core.TopicId, callback_data : ecal_core.SubEventCallbackData):
    print("Event callback invoked")
    entity = publisher_id.topic_id
    print("A publisher with id {} from host {} with PID {} has been {}".format(entity.entity_id, entity.host_name, entity.process_id, callback_data.event_type))

if __name__ == "__main__":
    # initialize client
    ecal_core.initialize("Pong Client")

    # create client
    client = ecal_core.ServiceClient("Pong")

    time.sleep(1)

    # connect to server / get game_id
    response = client.call_with_response("connection_request", bytes(sys.argv[1], "utf-8"), timeout_ms=1000)
    game_id = str(response[0].response).split("'")[1]
    config = ecal_core.get_subscriber_configuration()
    datatype_info = ecal_core.DataTypeInformation()
    sub = ecal_core.Subscriber(game_id, datatype_info, config, event_callback = publisher_event_callback)
    sub.set_receive_callback(data_callback)

    time.sleep(1)

    client.call_with_response("playing_method", bytes("-", "utf-8"), timeout_ms=1000)

    while ecal_core.ok():
        time.sleep(0.1)