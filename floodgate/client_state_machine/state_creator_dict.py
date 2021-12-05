from floodgate.client_state_machine.layer2_decoration_event.init import create as create_init
from floodgate.client_state_machine.layer2_decoration_event.lobby import create as create_lobby
from floodgate.client_state_machine.layer2_decoration_event.reply import create as create_reply
from floodgate.client_state_machine.layer2_decoration_event.game import create as create_game
from floodgate.keywords import GAME, INIT, LOBBY, REPLY

state_creator_dict = {
    INIT: create_init,
    LOBBY: create_lobby,
    REPLY: create_reply,
    GAME: create_game,
}
