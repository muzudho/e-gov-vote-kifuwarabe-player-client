from floodgate_client.layer2_decoration_event.init import create as create_init
from floodgate_client.layer2_decoration_event.game_summary import create as create_game_summary
from floodgate_client.layer2_decoration_event.agreement import create as create_agreement
from floodgate_client.layer2_decoration_event.game import create as create_game

state_creator_dict = {
    "[Init]": create_init,  # 初期値
    "[GameSummary]": create_game_summary,
    "[Agreement]": create_agreement,
    "[Game]": create_game
}
