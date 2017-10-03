"""Alternative to itertools.tee .
This implementation never holds on to generated values `unnecesary',
in particular, if you do

iter2 = streamtee.tee(iter1, 2)[0]

then iter2 stops referring to an object when iter1 would have done so.
The fact that you `leak' a tee-ed stream here does not matter for memory use.
"""

from functools import singledispatch
import operator

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

    def peek(self):
        """Look to the next item in the stream, without actually advancing to it.
        May throw StopIteration at end-of-stream.
        """
        return next(self.stream)[0]

    def duplicate(self):
        """Create a duplicate of the current iterator, which has its 
        own position in the underlying data stream.
        """
        return _StreamIterator(self.stream)


@singledispatch
def as_stream_iterator(iterable):
    return _StreamIterator(_stream_from_iterator(iter(iterable)))

as_stream_iterator.register(_StreamIterator, lambda x: x)

def tee(iterable, n=2):
    stream_iter = as_stream_iterator(iterable)
    return [stream_iter] + [stream_iter.duplicate() for i in range(n-1)]
