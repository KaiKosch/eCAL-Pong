import time
import sys
import random
import pygame
from typing import Tuple

import proto_messages.pong_game_data_pb2 as pong_game_data_pb2
import ecal.nanobind_core as ecal_core

class Game:

    def __init__(self, id):

        # Gamestate parameters
        self.game_id = id
        self.clients_ready = 0
        self.left_paddle_pos = 250
        self.right_paddle_pos = 250
        self.ball_position_x = 400
        self.ball_position_y = 300
        self.left_score = 0
        self.right_score = 0
        self.player = 1
        self.playername_1 = "Player_1"
        self.playername_2 = "Player_2"
        self.player2IsConnected = False
        self.closed = False

    def set_playername(self, playername, playernumber):
        if playernumber == 1:
            self.playername_1 = playername
        elif playernumber == 2:
            self.playername_2 = playername

    def print(self):
        print(f"Game Id: {self.game_id}")
        print(f"Spieler 1: {self.playername_1}")
        print(f"Spieler 2: {self.playername_2}")