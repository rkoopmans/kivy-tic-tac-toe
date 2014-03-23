from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


SYMBOLS = ('X', 'O')


def symbol_generator():
    while True:
        for symbol in SYMBOLS:
            yield symbol


class Board(GridLayout):

    grid = None
    symbols = None

    def __init__(self, cols=3, **kwargs):
        super(Board, self).__init__(**kwargs)

        self.cols = cols
        self.rows = cols
        self.symbols = symbol_generator()

        self.grid = [[None for col in range(self.cols)] for row in range(self.rows)]

        self._draw_tiles()

    def _draw_tiles(self):
        """
            Adds the tiles to the grid (widgets to the gridset)
        """
        for row in range(self.rows):
            for col in range(self.cols):
                tile = Button()
                tile.bind(on_press=self._onclick)
                self.grid[row][col] = tile
                self.add_widget(tile)

    def _onclick(self, instance):
        """
            Handles a click on a tile
        """
        if instance.text:
            return None

        instance.text = self.symbols.next()

        self._check_status()

    def _check_status(self):
        """
            Checks board status
        """
        winner = self._get_winner()

        if winner:
            close_button = Button(text='Close')

            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='%s won the game!' % winner))
            content.add_widget(close_button)

            popup = Popup(title='%s won!' % winner,
                                content=content,
                                size_hint=(.8, .8)).open()

            close_button.bind(on_release=popup.dismiss)

            self._restart_board()

    def _get_winner(self):
        """
            Returns winning symbol or None
        """
        values = [[col.text for col in row] for row in self.grid]

        # check horizontal
        for row in values:
            result = self._is_same_symbol(row)
            if result:
                return result

        # check vertical
        for row in [list(row) for row in zip(*values)]:
            result = self._is_same_symbol(row)
            if result:
                return result

        # check forward diagonal
        forward_diagonal = [row[col] for col, row in enumerate(values)]
        result = self._is_same_symbol(forward_diagonal)
        if result:
            return result

        # check backwards diagonal
        backwards_diagonal = [row[-col-1] for col, row in enumerate(values)]
        result = self._is_same_symbol(backwards_diagonal)
        if result:
            return result

        return None

    def _is_same_symbol(self, row):
        for symbol in SYMBOLS:
            if [symbol for _ in range(self.cols)] == row:
                return symbol
        return False

    def _restart_board(self):
        for row in self.grid:
            for col in row:
                col.text = ''
