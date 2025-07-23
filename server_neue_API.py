import time
import sys
import random
import pygame
from typing import Tuple

import proto_messages.pong_game_data_pb2 as pong_game_data_pb2
import ecal.nanobind_core as ecal_core

# Gamestate parameters
clients_ready = 0
left_paddle_pos = 250
right_paddle_pos = 250
ball_pos = [400, 300]
ball_speeds = [[3, 3], [3, -3], [-3, 3], [-3, -3]]
ball_speed = [3, 3]
left_score = 0
right_score = 0
playername_1 = ""
playername_2 = ""
name_left_called = False
paused = False

# Screen
WIDTH, HEIGHT = 800, 600

# Paddles
paddle_width, paddle_height = 10, 100

# callback will be called when a subscriber is connected / disconnected to the publisher
def subscriber_event_callback(subscriber_id : ecal_core.TopicId, callback_data : ecal_core.PubEventCallbackData):
    print("Event callback invoked")
    entity = subscriber_id.topic_id
    print("A subscriber with id {} from host {} with PID {} has been {}".format(entity.entity_id, entity.host_name, entity.process_id, callback_data.event_type))

def connection_request_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    global clients_ready, playername_1, playername_2
    clients_ready += 1
    print("Hallo "+ str(request).split("'")[1])

    if clients_ready == 1:
        playername_1 = str(request).split("'")[1]
        return 0, bytes("player1_ready", "utf-8")
    elif clients_ready == 2:
        playername_2 = str(request).split("'")[1]
        return 0, bytes("player2_ready", "utf-8")
    elif clients_ready > 2:
        print("Das Spiel ist voll.")
        return 0, bytes("game_full", "utf-8")

def idle():
    protobuf_message = pong_game_data_pb2.PongGameData()
    protobuf_message.game_state.state = "waiting"
    protobuf_message.game_state.clients_ready = clients_ready

    serialized = protobuf_message.SerializeToString()
    pub.send(serialized)

    print("Waiting for players...")
    print(f"Players ready: {clients_ready}")
    time.sleep(2.0)

def playing():
    global right_score, left_score, ball, ball_speed, left_paddle_pos, right_paddle_pos, paused

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    while paused:
        time.sleep(0.1)

    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]
    if ball.left <= 0:
        right_score += 1
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 15, 15)
        ball_speed = ball_speeds[random.randint(2, 3)]
    if ball.right >= WIDTH:
        left_score += 1
        ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 15, 15)
        ball_speed = ball_speeds[random.randint(0, 1)]

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed[0] = -ball_speed[0]

    protobuf_message = pong_game_data_pb2.PongGameData()
    protobuf_message.ball.position_x = ball.x
    protobuf_message.ball.position_y = ball.y
    protobuf_message.paddle_left.position = left_paddle.y
    protobuf_message.paddle_right.position = right_paddle.y
    protobuf_message.score.left = left_score
    protobuf_message.score.right = right_score
    protobuf_message.game_state.state = "playing"

    serialized = protobuf_message.SerializeToString()
    pub.send(serialized)

    time.sleep(0.01)

def paddle_input_left_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    left_paddle.y = int(str(request).split("'")[1])
    return 0, bytes("-", "utf-8")

def paddle_input_right_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    right_paddle.y = int(str(request).split("'")[1])
    return 0, bytes("-", "utf-8")

def name_transmission_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    global name_left_called
    if not name_left_called:
        name_left_called = True
        return 0, bytes(playername_1, "utf-8")
    else:
        return 0, bytes(playername_2, "utf-8")

def call_pause_callback(method_information : ecal_core.ServiceMethodInformation, request : bytes) -> Tuple[int, bytes]:
    global paused
    if paused:
        paused = False
        return 0, bytes("-", "utf-8")
    elif not paused:
        paused = True
        print("Spiel pausiert.")
        return 0, bytes("-", "utf-8")

if __name__ == "__main__":
    # initialize server and pygame
    ecal_core.initialize("Pong Server")
    pygame.init()

    ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 15, 15)
    left_paddle = pygame.Rect(10, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

    # create server and publisher
    server = ecal_core.ServiceServer("Pong")
    config = ecal_core.get_publisher_configuration()
    datatype_info = ecal_core.DataTypeInformation()
    pub = ecal_core.Publisher("Pong_Topic", datatype_info, config, event_callback = subscriber_event_callback)

    # add methods to server
    connection_method_info = ecal_core.ServiceMethodInformation(method_name="connection_request")
    server.set_method_callback(connection_method_info, connection_request_callback)
    paddle_left_method_info = ecal_core.ServiceMethodInformation(method_name="paddle_input_left")
    server.set_method_callback(paddle_left_method_info, paddle_input_left_callback)
    paddle_right_method_info = ecal_core.ServiceMethodInformation(method_name="paddle_input_right")
    server.set_method_callback(paddle_right_method_info, paddle_input_right_callback)
    name_method_info = ecal_core.ServiceMethodInformation(method_name="name_transmission")
    server.set_method_callback(name_method_info, name_transmission_callback)
    pause_method_info = ecal_core.ServiceMethodInformation(method_name="call_pause")
    server.set_method_callback(pause_method_info, call_pause_callback)

    # idle loop
    while clients_ready < 2:
        idle()

    # playing loop
    while ecal_core.ok():
        playing()
  
    # finalize eCAL API
    ecal_core.finalize()