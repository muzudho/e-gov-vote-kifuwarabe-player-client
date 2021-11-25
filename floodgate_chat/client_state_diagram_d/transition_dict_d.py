transition_dict = {
    "[None]----Ok---->": "[GameSummary]",
    "[GameSummary]----Loopback---->": "[GameSummary]",
    "[GameSummary]----EndGameSummary---->": "[Agreement]",
    "[Agreement]----Start---->": "[Game]",
}
