transition_dict = {

    "[Init]----InvalidOperation---->": "[Init]",  # ごまかし
    "[Init]----Login---->": "[Entrance]",

    "[Entrance]----InvalidOperation---->": "[Init]",  # ごまかし
    "[Entrance]----Ok---->": "[Lobby]",

    "[Lobby]----Loopback---->": "[Lobby]",
    "[Lobby]----BeginGameSummary---->": "[Listen]",

    "[Listen]----Loopback---->": "[Listen]",
    "[Listen]----EndGameSummary---->": "[Reply]",

    "[Reply]----Start---->": "[Play]",

    "[Play]----Loopback---->": "[Play]",
    "[Play]----Move---->": "[Play]",
    "[Play]----Win---->": "[Init]",
    "[Play]----Lose---->": "[Init]",
}
