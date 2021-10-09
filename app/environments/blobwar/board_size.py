import argparse

__DEFAULT_SIZE__=8
__MIN_SIZE__=5
__MAX_SIZE__=10

def get_size():
    return __DEFAULT_SIZE__
    # # Setup argparse to show defaults on help
    # formatter_class = argparse.ArgumentDefaultsHelpFormatter
    # parser = argparse.ArgumentParser(formatter_class=formatter_class)
    # parser.add_argument("--board_size", "-s", type=int, default=__DEFAULT_SIZE__, help="The size of board square(6*6 or 8*8)")
    # args = parser.parse_args()
    # size=args.board_size
    # assert size <=__MAX_SIZE__ and size>=__MIN_SIZE__, f"Game Board size should be comprised between {__MIN_SIZE__} and {__MAX_SIZE__}"

    # return size

