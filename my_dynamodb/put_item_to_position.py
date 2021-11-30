"""
# Run
python.exe -m my_dynamodb.put_item_to_position
"""

from pprint import pprint
import boto3
from app import app

TABLE_NAME = 'Position'


def put_position(your_name, secret, position, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',
                                  region_name="us-east-2")
        # ↓ region_name に変えて、ローカルのDynamoDBも指せます
        # endpoint_url="http://localhost:8000"

    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(
        Item={
            'yourName': your_name,
            'secret': secret,
            'position': position,
        }
    )
    return response


if __name__ == '__main__':
    app.log.init()
    movie_resp = put_position("Kifuwarabe", "warawara", """P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
P2 * -HI *  *  *  *  * -KA * 
P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
P4 *  *  *  *  *  *  *  *  * 
P5 *  *  *  *  *  *  *  *  * 
P6 *  *  *  *  *  *  *  *  * 
P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
P8 * +KA *  *  *  *  * +HI * 
P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
""")
    app.log.write_by_internal("Put bestmove succeeded:")
    pprint(movie_resp, sort_dicts=False)
