import time
from app import app
from my_dynamodb.delete_table_bestmove import delete_bestmove_table
from my_dynamodb.create_table_bestmove import create_bestmove_table


def clean_up_vote(req):
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
