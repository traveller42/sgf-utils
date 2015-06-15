"""Dump a list of the moves in a game record

Derived from show_sgf.py in gomill examples

"""

import sys
from optparse import OptionParser

from gomill import ascii_boards
from gomill import sgf
from gomill import sgf_moves

def human_point(column, row):
    column_array = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    
    return column_array[column] + str(row + 1)

def show_sgf_file(pathname, move_number):
    f = open(pathname)
    sgf_src = f.read()
    f.close()
    try:
        sgf_game = sgf.Sgf_game.from_string(sgf_src)
        handicap = sgf_game.get_handicap()
    except ValueError:
        raise StandardError("bad sgf file")

    try:
        board, plays = sgf_moves.get_setup_and_moves(sgf_game)
    except ValueError, e:
        raise StandardError(str(e))
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
	    print human_point(col, row)
	current_move_number += 1
	print "Moves"
	print "1: B --"
    for colour, move in plays:
	current_move_number += 1
        if move is None:
	    print str(current_move_number) + ":", colour.upper(), "Pass"
            continue
        row, col = move
        print str(current_move_number) + ":", colour.upper(), human_point(col, row)
        try:
            board.play(row, col, colour)
        except ValueError:
            raise StandardError("illegal move in sgf file")

#    print ascii_boards.render_board(board)
    print

_description = """\
Show the moves from an SGF file. If a move number is specified, the moves will be
shown up to that move number.
"""

def main(argv):
    parser = OptionParser(usage="%prog <filename> [move number]",
                          description=_description)
    opts, args = parser.parse_args(argv)
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
    except Exception, e:
        print >>sys.stderr, "show_sgf:", str(e)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

