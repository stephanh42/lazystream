"""Alternative to itertools.tee .
This implementation never holds on to generated values `unnecesary',
in particular, if you do

iter2 = streamtee.tee(iter1, 2)[0]

then iter2 stops referring to an object when iter1 would have done so.
The fact that you `leak' a tee-ed stream here does not matter for memory use.
"""

from functools import singledispatch
import operator

@singledispatch
def _stream_from_iterator(iterator):
    result = (next(iterator), _stream_from_iterator(iterator))
    iterator = None
    while True:
        yield result

class _StreamIterator(object):
    def __init__(self, stream):
        self.stream = stream

    def __next__(self):
        result, self.stream = next(self.stream)
        return result

    def __iter__(self):
        return self

_stream_from_iterator.register(_StreamIterator,
        operator.attrgetter("stream"))

def tee(iterable, n=2):
    stream = _stream_from_iterator(iter(iterable))
    return [_StreamIterator(stream) for i in range(n)]

