import pygame
pygame.font.init()


class GUI:
    """
    Class for creating a GUI object
    """
    def __init__(self, width: int, height: int) -> None:
        """
        :param width: The width of the window
        :param height: The height of the window
        """
        self._width = width
        self._height = height
        self.window = None

    def _create_window(self, caption: str) -> None:
        """
        Creates the window
        :param caption: The name of the window
        """
        self.window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(caption)

    def draw(self) -> None:
        """
        Redraws the window
        """
        pass

    @staticmethod
    def check_events_exit() -> bool:
        """
        Checks to see if a `pygame` `QUIT` event has triggered
        :return: If there is a `pygame.QUIT` event
        :rtype: bool
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    @staticmethod
    def close() -> None:
        """
        Closes the current Pygame window
        """
        pygame.quit()
        pygame.init()

