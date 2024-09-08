def paths(m, n):
    """Return the number of paths from one corner of an
    M by N grid to the opposite corner.

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    "*** YOUR CODE HERE ***"
    def helper(i,j):
        if i==m:
            if j<n:
                return helper(i,j+1)
            elif j==n:
                return 1
        elif j==n:
            if i<m:
                return helper(i+1,j)
            elif i==m:
                return 1
        else:
            return helper(i+1,j)+helper(i,j+1)
    return helper(1,1)
print(paths(20,20))
