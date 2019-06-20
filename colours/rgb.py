def hexstring_from_rgb(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hexstring_from_y(y):
    return hexstring_from_rgb(y, y, y)
