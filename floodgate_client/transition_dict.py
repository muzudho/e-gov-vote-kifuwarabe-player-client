transition_dict = {
    "[Init]----Ok---->": "[GameSummary]",
    "[GameSummary]----Loopback---->": "[GameSummary]",
    "[GameSummary]----EndGameSummary---->": "[Agreement]",
    "[Agreement]----Start---->": "[Game]",
    "[Game]----Loopback---->": "[Game]",
    "[Game]----Move---->": "[Game]",
    "[Game]----Win---->": "[Init]",
    "[Game]----Lose---->": "[Init]",
}
