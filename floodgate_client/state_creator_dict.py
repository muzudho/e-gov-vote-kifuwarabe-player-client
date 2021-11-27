from floodgate_client.game_over_state_impl import GameOverStateImpl
from floodgate_client.none_state_impl import create_none_state
from floodgate_client.game_summary_state_impl import GameSummaryStateImpl
from floodgate_client.agreement_state_impl import AgreementStateImpl
from floodgate_client.game_state_impl import GameStateImpl

state_creator_dict = {
    "": create_none_state,  # 初期値
    "[GameSummary]": GameSummaryStateImpl().create_game_summary_state,
    "[Agreement]": AgreementStateImpl().create_agreement_state,
    "[Game]": GameStateImpl().create_game_state,
    "[GameOver]": GameOverStateImpl().create_game_over_state
}
