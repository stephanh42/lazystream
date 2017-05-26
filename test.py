import streamtee
import itertools

class Test:
    def __init__(self, n, file):
        self.n = n
        self.file = file

    def __repr__(self):
        return "Test(%d)" % self.n

    def __del__(self):
        self.file.write("Test(%d) deleted\n" % self.n)

def test_iter(n, file):
    try:
        for i in range(n):
            file.write("Create Test(%d)\n" % i)
            yield Test(i, file)
    finally:
        file.write("test_iter done\n")

def test(tee, file):
    import copy
    i1, i2 = tee(test_iter(10, file))
    i3 = copy.copy(i1)
    for obj in i1:
        file.write("i1: %r\n" % obj)
    del obj
    for obj in i3:
        file.write("i3: %r\n" % obj)
    del obj
    for i in range(4):
        file.write("i2: %r\n" % next(i2))
    file.write("del i2\n")
    del i2
    file.write("del i1\n")
    del i1



if __name__ == "__main__":
    with open("streamtee.out", "w") as f:
        test(streamtee.tee, f)
    with open("itertools.out", "w") as f:
        test(itertools.tee, f)
