from ui import Window
from test_brain import Test

test = Test()
window = Window(test)
window.home_ui()

# Keeps the window open
window.mainloop()
