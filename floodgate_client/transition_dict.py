transition_dict = {

    "[Init]----InvalidOperation---->": "[Init]",  # ごまかし
    "[Init]----Login---->": "[Entrance]",

    "[Entrance]----InvalidOperation---->": "[Init]",  # ごまかし
    "[Entrance]----Ok---->": "[Lobby]",

    "[Lobby]----Loopback---->": "[Lobby]",
    "[Lobby]----BeginGameSummary---->": "[Listen]",

    "[Listen]----Loopback---->": "[Listen]",
    "[Listen]----EndGameSummary---->": "[Reply]",

    "[Reply]----StartMe---->": "[Play]",
    "[Reply]----StartOpponent---->": "[Judge]",

    "[Play]----DoneMove---->": "[Judge]",

    "[Judge]----Loopback---->": "[Judge]",
    "[Judge]----PlayMe---->": "[Play]",
    "[Judge]----EchoSelf---->": "[Judge]",
    "[Judge]----Move---->": "[Judge]",
    "[Judge]----Win---->": "[Init]",
    "[Judge]----Lose---->": "[Init]",
}
