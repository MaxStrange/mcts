"""
This is UI API module. This should be shielded from any particular
game logic and needs to command a well-defined API from the
game_module.
"""

ai_module = None
game_module = None


def start_game():
    """
    Main entry into the actual game. This starts the game, but requires
    that the globals ai_module and game_module be imported already.
    """
    global ai_module
    global game_module
    print("Welcome to the MCTS prototyping framework!")
    print(game_module.welcome_string())

    def get_next_metadata():
        request_str = game_module.get_next_metadata_request_str()
        d = input(request_str)
        return d

    while game_module.needs_more_metadata():
        d = get_next_metadata()
        while game_module.metadata_not_valid(d):
            d = get_next_metadata()
        game_module.set_next_metadata(d)





