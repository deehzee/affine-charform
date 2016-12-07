# parse.py - Generator to parse a file

from sys import stderr

def parse(filename, linenum=True):
    """Generator to parse a file."""
    with open(filename) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                data = eval(line)
                if linenum:
                    yield i + 1, data
                else:
                    yield data
            except Exception as e:
                # Print the input line number, before raising it back
                print >> stderr, e
                print >> stderr, '--> [{}:{}] {}'.format(
                        filename, i + 1, line)
                raise e
