import pygame
pygame.font.init()


class GUI:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self.window = None

    def _create_window(self, caption: str) -> None:
        self.window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(caption)

    def draw(self) -> None:
        pass

    @staticmethod
    def check_events_exit() -> bool:
        """
        Checks to see if a `pygame` `QUIT` event has triggered.
        :return: If there is a `pygame.QUIT` event
        :rtype: bool
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

