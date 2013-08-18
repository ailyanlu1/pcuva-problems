'''
Created on Jun 18, 2013

@author: Yubin Bai

Segment Tree Library
The segment tree is stored like a heap array
'''
import unittest
from numpypy import *


class SegmentTreeMin:

    def __init__(self, N):
        self.length = 1
        while self.length < 2 * N:
            self.length <<= 1
        self.tree = zeros((self.length), dtype=int)

    def buildTree(self, A):
        self._buildTree(A, 1, 0, len(A) - 1)

    def _buildTree(self, A, node, b, e):
        if b == e:
            self.tree[node] = b
        else:
            left = 2 * node
            right = 2 * node + 1
            self._buildTree(A, left, b, (b + e) // 2)
            self._buildTree(A, right, (b + e) // 2 + 1, e)
            lContent = self.tree[left]
            rContent = self.tree[right]
            if A[lContent] <= A[rContent]:
                self.tree[node] = lContent
            else:
                self.tree[node] = rContent

    def query(self, A, i, j):
        return self._query(A, 1, 0, len(A) - 1, i, j)

    def _query(self, A, node, b, e, i, j):
        '''
        find min in interval [i, j]
        '''
        if i > e or j < b:
            return -1
        if b >= i and e <= j:
            return self.tree[node]
        p1 = self._query(A, 2 * node, b, (b + e) // 2, i, j)
        p2 = self._query(A, 2 * node + 1, (b + e) // 2 + 1, e, i, j)
        if p1 == -1:
            return p2
        if p2 == -1:
            return p1
        if A[p1] <= A[p2]:
            return p1
        else:
            return p2

    def update(self, A, pos, value):
        '''
        update A[pos] to a new value
        value need to be smaller than old one
        '''
        if A[pos] < value:
            raise KeyError
        A[pos] = value

        def _update(node, p, b, e):
            if p < b or p > e:
                return
            if b == e:
                self.tree[node] = p
                return
            if A[p] < A[self.tree[node]]:
                self.tree[node] = p
            _update(node * 2, p, b, (b + e) // 2)
            _update(node * 2 + 1, p, (b + e) // 2 + 1, e)
        _update(1, pos, 0, len(A) - 1)

    def updateRange(self, A, i, j, value):
        '''
        update the values in range [i, j] of A to be bigger or equal to value
        '''
        def _update(node, b, e):
            if i > e or j < b:
                return
            if b == e:
                self.tree[node] = b
                A[b] = value
                return
            i1 = self._query(A, node, b, e, i, j)
            if A[i1] >= value:
                return
            _update(node * 2, b, (b + e) // 2)
            _update(node * 2 + 1, (b + e) // 2 + 1, e)
            self.tree[node] = i1
        _update(1, 0, len(A) - 1)


class Test(unittest.TestCase):

    def testMin(self):
        A = [8, 7, 3, 9, 5, 1, 10]
        t = SegmentTreeMin(len(A))
        t.buildTree(A)
        self.assertEqual(2, t._query(A, 1, 0, 6, 1, 3))
        t.update(A, 3, 2)
        self.assertEqual(3, t._query(A, 1, 0, 6, 1, 3))
        t.update(A, 2, 1)
        self.assertEqual(2, t._query(A, 1, 0, 6, 1, 3))

        t.updateRange(A, 0, 2, 6)
        i1 = t.query(A, 0, 2)
        self.assertEqual(6, A[i1])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
