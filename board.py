from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


SYMBOLS = ('X', 'O')


def symbol_generator():
    while True:
        for symbol in SYMBOLS:
            yield symbol


class Board(GridLayout):

    grid = None

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

        self.cols = 3
        self.rows = 3
        self.symbols = symbol_generator()

        self.grid = [[None for col in range(self.cols)] for row in range(self.rows)]

        self.draw_tiles()

    def draw_tiles(self):
        """
            Adds the tiles to the grid (widgets to the gridset)
        """
        for row in range(self.rows):
            for col in range(self.cols):
                tile = Button()
                tile.bind(on_press=self.onclick)
                self.grid[row][col] = tile
                self.add_widget(tile)

    def onclick(self, instance):
        """
            Handles a click on a tile
        """
        if instance.text:
            return None

        symbol = self.symbols.next()
        instance.text = symbol

        self.check_status()

    def check_status(self):
        """
            Checks board status
        """
        winner = self.get_winner()

        if winner:
            print '%s won the game' % winner

    def get_winner(self):
        """
            Returns winning symbol or None
        """
        values = [[col.text for col in row] for row in self.grid]

        # check horizontal
        for row in values:
            result = self.is_same_symbol(row)
            if result:
                return result

        # check vertical
        for row in [list(row) for row in zip(*values)]:
            result = self.is_same_symbol(row)
            if result:
                return result

        # check forward diagonal
        forward_diagonal = [row[col] for col, row in enumerate(values)]
        result = self.is_same_symbol(forward_diagonal)
        if result:
            return result

        # check backwards diagonal
        backwards_diagonal = [row[-col-1] for col, row in enumerate(values)]
        result = self.is_same_symbol(backwards_diagonal)
        if result:
            return result

        return None

    def is_same_symbol(self, row):
        for symbol in SYMBOLS:
            if [symbol for _ in range(self.cols)] == row:
                return symbol
        return False
