transition_dict = {
    "[Init]----Ok---->": "[Lobby]",
    "[Lobby]----Loopback---->": "[Lobby]",
    "[Lobby]----EndGameSummary---->": "[Reply]",
    "[Reply]----Start---->": "[Play]",
    "[Play]----Loopback---->": "[Play]",
    "[Play]----Move---->": "[Play]",
    "[Play]----Win---->": "[Init]",
    "[Play]----Lose---->": "[Init]",
}
