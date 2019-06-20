class Square:
    def __init__(self, side_length):
        self.side_length = side_length

    def __str__(self):
        return 'a square with sides of length {}'.format(self.side_length)
