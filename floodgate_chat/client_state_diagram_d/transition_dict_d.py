transition_dict = {
    "[None]----Ok---->": "[GameSummary]",
    "[GameSummary]----Loopback---->": "[GameSummary]",
    "[GameSummary]----EndGameSummary---->": "[Agreement]",
    "[Agreement]----Start---->": "[Game]",
    "[Game]----Move---->": "[Game]",
    "[Game]----Win---->": "[Game]",
    "[Game]----Lose---->": "[Game]",
}
