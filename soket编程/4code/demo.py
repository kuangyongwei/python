import sys
import select


def test():
    rlist = [sys.stdin]

    while True:
        res, _, _ = select.select(rlist, [], [])
        for x in res:
            if x is sys.stdin:
                buf = input("")
                print("得到了", buf)


test()

