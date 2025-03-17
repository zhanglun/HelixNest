from . import socketio

# 定义客户端连接事件处理函数
@socketio.on('connect')
def handle_connect():
  print('Client connected')

# 定义客户端发送消息事件处理函数
@socketio.on('message')
def handle_message(message):
  print('Received message: ' + message)
  # 向客户端发送消息
  socketio.send('Server received: ' + message)