from game.casting.actor import Actor

class FallingObject(Actor):
    """A visible thing falling from the top of the screen that participates in the game. 
    
    The responsibility of Actor is to keep track of its appearance, position,velocity in 2d space, and points awarded after a collision.

    Attributes:
        _text (string): The text to display
        _font_size (int): The font size to use.
        _color (Color): The color of the text.
        _position (Point): The screen coordinates.
        _velocity (Point): The speed and direction.
    """
    def __init__(self):
        super().__init__()

    def calculate_points(self):
        points = 0

        if self.get_text() == '*':
            points = 1
        else:
            points = -1

        return points