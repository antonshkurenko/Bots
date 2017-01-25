def color(r=0, g=0, b=0):
    return int('%02x%02x%02x' % (r, g, b), 16)


def read_file(filename):
    return [line.rstrip('\n') for line in open(filename, 'r')]


def split_str_to_ints(string, separator=' '):
    return [int(s) for s in string.split(separator)]
