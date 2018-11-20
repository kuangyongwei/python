import sys
import select


def test():
    rlist = [sys.stdin]
    while True:
        res, _, _ = select.select(rlist, [], [])
        print("=========")
        for x in res:
            if x is sys.stdin:
                buf = input("")
                print("接收到了", buf)


if __name__ == '__main__':
    test()
