import time
from app import app
from my_dynamodb.e_gov_delete_bestmove_table import delete_bestmove_table
from my_dynamodb.e_gov_create_bestmove_table import create_bestmove_table
from floodgate_client.transition_map_d.game_summary import GameSummaryState


def create_game_summary_state():
    """ステート生成"""
    state = GameSummaryState()

    def on_game_id(context):
        """Game ID を取得した"""
        pass

    state.on_game_id = on_game_id

    def on_end_game_summary(context):
        """初期局面情報取得した"""
        pass

    state.on_end_game_summary = on_end_game_summary

    def on_start(context):
        """対局成立した"""
        # テーブルを削除します
        try:
            delete_bestmove_table()

            # 時間間隔を開けてみる
            time.sleep(5)
        except Exception as e:
            app.log.write_by_internal(
                f"(Err.158) テーブル削除できなかった [{e}]")

        # テーブルを作成します
        try:
            create_bestmove_table()

            # 時間間隔を開けてみる
            time.sleep(5)
        except Exception as e:
            app.log.write_by_internal(
                f"(Err.163) テーブル作成できなかった [{e}]")

        # 次のステートへ引継ぎ
        # self._state = self._behavior_creator_dict["[Game]"]()

    state.on_start = on_start

    return state
