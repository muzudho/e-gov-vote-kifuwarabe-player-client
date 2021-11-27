from floodgate_client.impl_init import create_init_state
from floodgate_client.impl_game_summary import create_game_summary_state
from floodgate_client.impl_agreement import create_agreement_state
from floodgate_client.impl_game import create_game_state

state_creator_dict = {
    "[Init]": create_init_state,  # 初期値
    "[GameSummary]": create_game_summary_state,
    "[Agreement]": create_agreement_state,
    "[Game]": create_game_state
}
