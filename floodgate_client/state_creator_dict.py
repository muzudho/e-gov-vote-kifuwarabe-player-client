from floodgate_client.layer2_decoration_event.init import create as create_init
from floodgate_client.layer2_decoration_event.lobby import create as create_lobby
from floodgate_client.layer2_decoration_event.reply import create as create_reply
from floodgate_client.layer2_decoration_event.play import create as create_play

state_creator_dict = {
    "[Init]": create_init,  # 初期値
    "[Lobby]": create_lobby,
    "[Reply]": create_reply,
    "[Play]": create_play
}
