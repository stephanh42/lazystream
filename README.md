# streamtee, a memory-efficient alternative to itertools.tee

## Introduction

This is an alternative to `itertools.tee`.
It has the same interface but 

This implementation never holds on to generated values "unnecesarily",
in particular, if you do

iter2 = streamtee.tee(iter1, 2)[0]

then iter2 stops referring to an object when iter1 would have done so.
The fact that you `leak' a tee-ed stream here does not matter for memory use.

The `test.py` file generates two files `streamtee.out` and `itertools.out`.
By comparing these you will notice that the output is identical *except*
that streamtee.out shows that objects are being deleted earlier.

## Implementation

The implementation is based on the functional language concept of "lazy streams".
We convert from a Python iterator to a lazy stream. Then the lazy stream is
converted back to the desired number of Python iterators.
