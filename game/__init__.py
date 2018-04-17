from .ctx import *
from .main import *

pygame.init()
main_window = pygame.display.set_mode(dim)

app = GameWindow(main_window)
app.run()

pygame.quit()