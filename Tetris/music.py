import pygame


class BackgroundMusic:
    def __init__(self, music_file="tetris.ogg"):
        """
        Initialize the BackgroundMusic manager.

        :param music_file: Path to the background music file (default: 'tetris.wav').
        """
        pygame.mixer.init()
        self.music_file = music_file

    def play(self, loop=True):
        """
        Play the background music.

        :param loop: Boolean indicating if the music should loop indefinitely.
        """
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play(-1 if loop else 0)
        except pygame.error as e:
            print(f"Error loading or playing music: {e}")

    def stop(self):
        """Stop the background music."""
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        """
        Set the volume for the background music.

        :param volume: Volume level (0.0 to 1.0).
        """
        pygame.mixer.music.set_volume(volume)
