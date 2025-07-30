import time
import sys
import pygame

import proto_messages.pong_game_data_pb2 as pong_game_data_pb2
import ecal.nanobind_core as ecal_core

# gamestate parameters
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
all_players_connected = False

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# screen
WIDTH = 800
HEIGHT = 600

# paddles
paddle_width = 10
paddle_height = 100
paddle_speed = 6

# callbacks
def data_callback(publisher_id : ecal_core.TopicId, datatype_info : ecal_core.DataTypeInformation, data : ecal_core.ReceiveCallbackData):
    global ball_position_x, ball_position_y, left_score, right_score, player, left_paddle_pos, right_paddle_pos, all_players_connected

    protobuf_message = pong_game_data_pb2.PongGameData()
    protobuf_message.ParseFromString(data.buffer)

    if protobuf_message.game_state.state == "waiting":
        print("Waiting for players...")

    elif protobuf_message.game_state.state == "playing":
        ball_position_x = protobuf_message.ball.position_x
        ball_position_y = protobuf_message.ball.position_y
        left_paddle_pos = protobuf_message.paddle_left.position
        right_paddle_pos = protobuf_message.paddle_right.position
        left_score = protobuf_message.score.left
        right_score = protobuf_message.score.right
        if all_players_connected == False:
            all_players_connected = True

def publisher_event_callback(publisher_id : ecal_core.TopicId, callback_data : ecal_core.SubEventCallbackData):
    print("Event callback invoked")
    entity = publisher_id.topic_id
    print("A publisher with id {} from host {} with PID {} has been {}".format(entity.entity_id, entity.host_name, entity.process_id, callback_data.event_type))

def playing():
    global game_id

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if player == 1:  
        if keys[pygame.K_UP] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
            if left_paddle.y < 1:
                left_paddle.y = 1
        if keys[pygame.K_DOWN] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed

        right_paddle.y = right_paddle_pos
        client.call_with_response("paddle_input_left", bytes(str(left_paddle.y) + "," + game_id, "utf-8"), timeout_ms=1000)

    else:
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
            if right_paddle.y < 1:
                right_paddle.y = 1
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        left_paddle.y = left_paddle_pos
        client.call_with_response("paddle_input_right", bytes(str(right_paddle.y) + "," + game_id, "utf-8"), timeout_ms=1000)

    ball.x = ball_position_x
    ball.y = ball_position_y

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, ball)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    left_text_score = font.render(str(left_score), True, WHITE)
    left_text_name = font.render(playername_1, True, WHITE)
    screen.blit(left_text_score, (WIDTH // 4, 20))
    screen.blit(left_text_name, (WIDTH // 4, 65))
    right_text_score = font.render(str(right_score), True, WHITE)
    right_text_name = font.render(playername_2, True, WHITE)
    screen.blit(right_text_score, (WIDTH * 3 // 4, 20))
    screen.blit(right_text_name, (WIDTH * 3 // 4, 65))

    pygame.display.flip()
    clock.tick(60)

if __name__ == "__main__":
    # initialize client
    ecal_core.initialize("Pong Client")

    # create client
    client = ecal_core.ServiceClient("Pong")

    # connect to server / get game_id
    time.sleep(1)
    response = client.call_with_response("connection_request", bytes(sys.argv[1], "utf-8"), timeout_ms=1000)
    time.sleep(1)
    game_id = str(response[0].response).split("'")[1]
    config = ecal_core.get_subscriber_configuration()
    datatype_info = ecal_core.DataTypeInformation()
    sub = ecal_core.Subscriber(game_id, datatype_info, config, event_callback = publisher_event_callback)
    sub.set_receive_callback(data_callback)

    # player assignment
    player_number = client.call_with_response("player_assignment", bytes("-", "utf-8"), timeout_ms=1000)
    player = int(str(player_number[0].response).split("'")[1])

    # waiting for players
    while not all_players_connected:
        time.sleep(1)

    # naming
    name_left = client.call_with_response("request_left_name", bytes(game_id, "utf-8"), timeout_ms=1000)
    name_right = client.call_with_response("request_right_name", bytes(game_id, "utf-8"), timeout_ms=1000)
    playername_1 = str(name_left[0].response).split("'")[1]
    playername_2 = str(name_right[0].response).split("'")[1]

    time.sleep(1)

    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong')

    ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 15, 15)
    left_paddle = pygame.Rect(10, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

    font = pygame.font.Font(None, 74)
    clock = pygame.time.Clock()

    while ecal_core.ok():
        playing()