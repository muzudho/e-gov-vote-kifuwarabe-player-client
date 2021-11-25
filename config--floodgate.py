MESSAGE_SIZE = 1024

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = 'wdoor.c.u-tokyo.ac.jp'
SERVER_PORT = 4081
# [0-9A-za-z_-]32文字まで
CLIENT_USER = 'e-gov-vote-kifuwarabe'
# [0-9A-za-z_-]32文字まで
CLIENT_PASS = 'floodgate-300-10F,egov-kif'

# 接続が破棄されたら再接続
# （フラッドゲートは対局終了時に接続を切るので）
IS_RECONNECT_WHEN_CONNECTION_ABORT = True
