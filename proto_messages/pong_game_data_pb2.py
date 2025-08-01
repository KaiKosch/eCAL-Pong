# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pong_game_data.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pong_game_data.proto',
  package='proto_messages',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x14pong_game_data.proto\x12\x0eproto_messages\".\n\x04\x42\x61ll\x12\x12\n\nposition_x\x18\x01 \x01(\r\x12\x12\n\nposition_y\x18\x02 \x01(\r\"1\n\tGameState\x12\r\n\x05state\x18\x01 \x01(\t\x12\x15\n\rclients_ready\x18\x02 \x01(\r\"\x1a\n\x06Paddle\x12\x10\n\x08position\x18\x01 \x01(\r\"$\n\x05Score\x12\x0c\n\x04left\x18\x01 \x01(\r\x12\r\n\x05right\x18\x02 \x01(\r\"\xe2\x01\n\x0cPongGameData\x12\"\n\x04\x62\x61ll\x18\x01 \x01(\x0b\x32\x14.proto_messages.Ball\x12-\n\ngame_state\x18\x02 \x01(\x0b\x32\x19.proto_messages.GameState\x12+\n\x0bpaddle_left\x18\x03 \x01(\x0b\x32\x16.proto_messages.Paddle\x12,\n\x0cpaddle_right\x18\x04 \x01(\x0b\x32\x16.proto_messages.Paddle\x12$\n\x05score\x18\x05 \x01(\x0b\x32\x15.proto_messages.Scoreb\x06proto3'
)




_BALL = _descriptor.Descriptor(
  name='Ball',
  full_name='proto_messages.Ball',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='position_x', full_name='proto_messages.Ball.position_x', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='position_y', full_name='proto_messages.Ball.position_y', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=40,
  serialized_end=86,
)


_GAMESTATE = _descriptor.Descriptor(
  name='GameState',
  full_name='proto_messages.GameState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='proto_messages.GameState.state', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='clients_ready', full_name='proto_messages.GameState.clients_ready', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=88,
  serialized_end=137,
)


_PADDLE = _descriptor.Descriptor(
  name='Paddle',
  full_name='proto_messages.Paddle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='proto_messages.Paddle.position', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=139,
  serialized_end=165,
)


_SCORE = _descriptor.Descriptor(
  name='Score',
  full_name='proto_messages.Score',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='left', full_name='proto_messages.Score.left', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='right', full_name='proto_messages.Score.right', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=167,
  serialized_end=203,
)


_PONGGAMEDATA = _descriptor.Descriptor(
  name='PongGameData',
  full_name='proto_messages.PongGameData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ball', full_name='proto_messages.PongGameData.ball', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='game_state', full_name='proto_messages.PongGameData.game_state', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='paddle_left', full_name='proto_messages.PongGameData.paddle_left', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='paddle_right', full_name='proto_messages.PongGameData.paddle_right', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score', full_name='proto_messages.PongGameData.score', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=206,
  serialized_end=432,
)

_PONGGAMEDATA.fields_by_name['ball'].message_type = _BALL
_PONGGAMEDATA.fields_by_name['game_state'].message_type = _GAMESTATE
_PONGGAMEDATA.fields_by_name['paddle_left'].message_type = _PADDLE
_PONGGAMEDATA.fields_by_name['paddle_right'].message_type = _PADDLE
_PONGGAMEDATA.fields_by_name['score'].message_type = _SCORE
DESCRIPTOR.message_types_by_name['Ball'] = _BALL
DESCRIPTOR.message_types_by_name['GameState'] = _GAMESTATE
DESCRIPTOR.message_types_by_name['Paddle'] = _PADDLE
DESCRIPTOR.message_types_by_name['Score'] = _SCORE
DESCRIPTOR.message_types_by_name['PongGameData'] = _PONGGAMEDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Ball = _reflection.GeneratedProtocolMessageType('Ball', (_message.Message,), {
  'DESCRIPTOR' : _BALL,
  '__module__' : 'pong_game_data_pb2'
  # @@protoc_insertion_point(class_scope:proto_messages.Ball)
  })
_sym_db.RegisterMessage(Ball)

GameState = _reflection.GeneratedProtocolMessageType('GameState', (_message.Message,), {
  'DESCRIPTOR' : _GAMESTATE,
  '__module__' : 'pong_game_data_pb2'
  # @@protoc_insertion_point(class_scope:proto_messages.GameState)
  })
_sym_db.RegisterMessage(GameState)

Paddle = _reflection.GeneratedProtocolMessageType('Paddle', (_message.Message,), {
  'DESCRIPTOR' : _PADDLE,
  '__module__' : 'pong_game_data_pb2'
  # @@protoc_insertion_point(class_scope:proto_messages.Paddle)
  })
_sym_db.RegisterMessage(Paddle)

Score = _reflection.GeneratedProtocolMessageType('Score', (_message.Message,), {
  'DESCRIPTOR' : _SCORE,
  '__module__' : 'pong_game_data_pb2'
  # @@protoc_insertion_point(class_scope:proto_messages.Score)
  })
_sym_db.RegisterMessage(Score)

PongGameData = _reflection.GeneratedProtocolMessageType('PongGameData', (_message.Message,), {
  'DESCRIPTOR' : _PONGGAMEDATA,
  '__module__' : 'pong_game_data_pb2'
  # @@protoc_insertion_point(class_scope:proto_messages.PongGameData)
  })
_sym_db.RegisterMessage(PongGameData)


# @@protoc_insertion_point(module_scope)
