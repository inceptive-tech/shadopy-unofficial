class ResMock:
    """used in unit tests by Session.send mock"""

    def __init__(self, json) -> None:
        self._json = json

    def json(self):
        return self._json
