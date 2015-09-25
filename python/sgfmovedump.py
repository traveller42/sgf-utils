"""Dump a list of the moves in a game record

Derived from show_sgf.py in gomill examples

"""

import sys
from optparse import OptionParser

from gomill import sgf
from gomill import sgf_moves

def human_point(column, row):
    """Return the human-readable version of the point."""
    column_array = "ABCDEFGHJKLMNOPQRSTUVWXYZ"

    return column_array[column] + str(row + 1)

def show_sgf_file(pathname, move_number):
    """
    Print the moves of the leftmost branch in the first game in the file.

    Arguments:
    pathname -- path of SGF file
    move_number -- optional move at which to stop printing moves
    """
    file_handle = open(pathname)
    sgf_src = file_handle.read()
    file_handle.close()
    try:
        sgf_game = sgf.Sgf_game.from_string(sgf_src)
        handicap = sgf_game.get_handicap()
    except ValueError:
        raise StandardError("bad sgf file")

    try:
        _, plays = sgf_moves.get_setup_and_moves(sgf_game)
    except ValueError, err:
        raise StandardError(str(err))
    if move_number is not None:
        move_number = max(0, move_number)
        plays = plays[:move_number]

    current_move_number = 0
    root_node = sgf_game.get_root()
    if handicap != None:
        print "Handicap is", handicap
        print "Handicap stones are"
        handicap_stones = root_node.get('AB')
        for row, col in handicap_stones:
            print human_point(col, row),
        current_move_number += 1
        print
        print "Moves"
        print "1:".rjust(4), "B ----",
    for colour, move in plays:
        if (current_move_number % 2) == 0:
            print
        current_move_number += 1
        if move is None:
            print str(current_move_number).rjust(3) + ":", colour.upper(),\
	    "Pass",
            continue
        row, col = move
        print str(current_move_number).rjust(3) + ":", colour.upper(),\
        human_point(col, row).ljust(4),
    print

DESCRIPTION = """\
Show the moves from an SGF file. If a move number is specified, the moves will be
shown up to that move number.
"""

def main(argv):
    """Process the command line arguments and dispatch show_sgf_file()"""
    parser = OptionParser(usage="%prog <filename> [move number]",
                          description=DESCRIPTION)
    _, args = parser.parse_args(argv)
    if not args:
        parser.error("not enough arguments")
    pathname = args[0]
    if len(args) > 2:
        parser.error("too many arguments")
    if len(args) == 2:
        try:
            move_number = int(args[1])
        except ValueError:
            parser.error("invalid integer value: %s" % args[1])
    else:
        move_number = None
    try:
        show_sgf_file(pathname, move_number)
    except StandardError, err:
        print >>sys.stderr, "sgfmovedump:", str(err)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

