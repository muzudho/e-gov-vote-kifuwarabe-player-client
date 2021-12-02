from floodgate_client.layer2_decoration_event.init import create as create_init
from floodgate_client.layer2_decoration_event.entrance import create as create_entrance
from floodgate_client.layer2_decoration_event.lobby import create as create_lobby
from floodgate_client.layer2_decoration_event.listen import create as create_listen
from floodgate_client.layer2_decoration_event.reply import create as create_reply
from floodgate_client.layer2_decoration_event.play import create as create_play
from floodgate_client.layer2_decoration_event.judge import create as create_judge

state_creator_dict = {
    "[Init]": create_init,  # 初期値
    "[Entrance]": create_entrance,  # 初期値
    "[Lobby]": create_lobby,
    "[Listen]": create_listen,
    "[Reply]": create_reply,
    "[Play]": create_play,
    "[Judge]": create_judge,
}
