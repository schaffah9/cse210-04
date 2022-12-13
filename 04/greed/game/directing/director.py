class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            _keyboard_service (KeyboardService): An instance of KeyboardService.
            _video_service (VideoService): An instance of VideoService.
            _score (int): amount of points the player has scored.
            _is_playing (boolean): Whether or not to keep playing.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        self._is_playing = True
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with falling objects.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        falling_objects = cast.get_actors("falling objects")

        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        for object in falling_objects:
            if robot.get_position().equals(object.get_position()):
                self._score += object.calculate_points()
                cast.remove_actor("falling objects", object)
            object.move_next(max_x, max_y)

        banner.set_text(f'Score: {self._score}')

        if all(map(lambda actor: actor.get_text() == 'O', falling_objects)):
            self._is_playing = False

        if not self._is_playing:
            banner.set_text(f"GAME OVER. Final Score: {self._score}")
            banner.set_font_size(32)

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()