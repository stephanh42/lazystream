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

def _flatten_stream_from_reversed_list(lst):
    while lst:
        yield from lst.pop()

_empty_iterator = iter(())

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

    def bind(self, f):
        """The callable f takes a single argument and
        returns an iterator. Essentially we return
        (y for x in self for y in f(x))
        as a stream iterator.
        """
        return as_stream_iterator(y for x in self for y in f(x))

    def concatenate(self, other):
        """Concatenate another iterator to this iterator
        and return the concatenated iterator.
        The two input iterators should not be used anymore
        and will be consumed by the combined iterator.
        """
        return as_stream_iterator(_flatten_stream_from_reversed_list([other, self]))

@singledispatch
def as_stream_iterator(iterable):
    return _StreamIterator(_stream_from_iterator(iter(iterable)))

as_stream_iterator.register(_StreamIterator, lambda x: x)

def tee(iterable, n=2):
    if n <= 0:
        return []
    stream_iter = as_stream_iterator(iterable)
    return [stream_iter] + [stream_iter.duplicate() for i in range(n-1)]

empty = as_stream_iterator(())
