from . import BaseController
from views.home_view import HomeView

class HomeController(BaseController):
    def __init__(self):
        super().__init__(HomeView)
