transition_dict = {

    "[Init]----InvalidOperation---->": "[Init]",  # ごまかし
    "[Init]----Login---->": "[Entrance]",

    "[Entrance]----InvalidOperation---->": "[Init]",  # ごまかし
    "[Entrance]----Ok---->": "[Lobby]",

    "[Lobby]----Loopback---->": "[Lobby]",
    "[Lobby]----BeginGameSummary---->": "[Listen]",

    "[Listen]----Loopback---->": "[Listen]",
    "[Listen]----Agree---->": "[Reply]",
    "[Listen]----Reject---->": "[Lobby]",

    "[Reply]----StartMe---->": "[Play]",
    "[Reply]----StartOpponent---->": "[Judge]",

    "[Play]----MyMove---->": "[Judge]",

    "[Judge]----Loopback---->": "[Judge]",
    "[Judge]----PlayMe---->": "[Play]",
    "[Judge]----EchoSelf---->": "[Judge]",

    # floodgateでは [Init] に戻る
    "[Judge]----Win---->": "[Init]",
    "[Judge]----Draw---->": "[Init]",
    "[Judge]----Lose---->": "[Init]",
    "[Judge]----Censored---->": "[Init]",
}
