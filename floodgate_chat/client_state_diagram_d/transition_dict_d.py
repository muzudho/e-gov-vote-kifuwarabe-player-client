transition_dict = {
    "[None]----Ok---->": "[GameSummary]",
    "[GameSummary]----Loopback---->": "[GameSummary]",
    "[GameSummary]----EndGameSummary---->": "[Agreement]",
    "[Agreement]----Start---->": "[Game]",
    "[Game]----Loopback---->": "[Game]",
    "[Game]----Move---->": "[Game]",
    "[Game]----Win---->": "[GameOver]",
    "[Game]----Lose---->": "[GameOver]",
}
