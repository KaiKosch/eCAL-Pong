import time
import sys
import random
import pygame
from typing import Tuple

import proto_messages.pong_game_data_pb2 as pong_game_data_pb2
import ecal.nanobind_core as ecal_core

def subscriber_event_callback(subscriber_id : ecal_core.TopicId, callback_data : ecal_core.PubEventCallbackData):
    print("Event callback invoked")
    entity = subscriber_id.topic_id
    print("A subscriber with id {} from host {} with PID {} has been {}".format(entity.entity_id, entity.host_name, entity.process_id, callback_data.event_type))

class Game:

    def __init__(self, id):
        # gamestate parameters
        self.game_id = id
        self.left_paddle_pos = 250
        self.right_paddle_pos = 250
        self.ball_position_x = 400
        self.ball_position_y = 300
        self.ball_speed = [3, 3]
        self.ball_speeds = [[3, 3], [3, -3], [-3, 3], [-3, -3]]
        self.left_score = 0
        self.right_score = 0
        self.player_name_1 = "Player_1"
        self.player_name_2 = "Player_2"

        # create subscriber
        config = ecal_core.get_publisher_configuration()
        datatype_info = ecal_core.DataTypeInformation()
        self.pub = ecal_core.Publisher(str(id), datatype_info, config, event_callback = subscriber_event_callback)

        # screen 
        self.HEIGHT = 600
        self.WIDTH = 800

        # paddles
        self.paddle_width = 10
        self.paddle_height = 100

        # initialize pygame
        pygame.init()
        self.ball = pygame.Rect(self.WIDTH // 2 - 15, self.HEIGHT // 2 - 15, 15, 15)
        self.left_paddle = pygame.Rect(10, self.HEIGHT // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height)
        self.right_paddle = pygame.Rect(self.WIDTH - 20, self.HEIGHT // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height)

    def set_player_name(self, player_name):
        if self.player_name_1 == "Player_1":
            self.player_name_1 = player_name
        else:
            self.player_name_2 = player_name

    def set_paddle_left(self, paddle_y):
        self.left_paddle.y = paddle_y

    def set_paddle_right(self, paddle_y):
        self.right_paddle.y = paddle_y

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]
        if self.ball.left <= 0:
            self.right_score += 1
            self.ball = pygame.Rect(self.WIDTH // 2 - 15, self.HEIGHT // 2 - 15, 15, 15)
            self.ball_speed = self.ball_speeds[random.randint(2, 3)]
        if self.ball.right >= self.WIDTH:
            self.left_score += 1
            self.ball = pygame.Rect(self.WIDTH // 2 - 15, self.HEIGHT // 2 - 15, 15, 15)
            self.ball_speed = self.ball_speeds[random.randint(0, 1)]

        if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle):
            self.ball_speed[0] = -self.ball_speed[0]

        protobuf_message = pong_game_data_pb2.PongGameData()
        protobuf_message.ball.position_x = self.ball.x
        protobuf_message.ball.position_y = self.ball.y
        protobuf_message.paddle_left.position = self.left_paddle.y
        protobuf_message.paddle_right.position = self.right_paddle.y
        protobuf_message.score.left = self.left_score
        protobuf_message.score.right = self.right_score
        protobuf_message.game_state.state = "playing"

        serialized = protobuf_message.SerializeToString()
        self.pub.send(serialized)

    def idle(self):
        protobuf_message = pong_game_data_pb2.PongGameData()
        protobuf_message.game_state.state = "waiting"

        serialized = protobuf_message.SerializeToString()
        self.pub.send(serialized)

        print("Warte auf Spieler...")
        time.sleep(2.0)

    def print(self):
        print(f"Game Id: {self.game_id}")
        print(f"Spieler 1: {self.player_name_1}")
        print(f"Spieler 2: {self.player_name_2}")