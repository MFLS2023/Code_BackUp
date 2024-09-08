def tree(root_label,branches=[]):
    for branch in branches:
        assert is_tree(branch)
    return [root_label]+list(branches)
## 实际上branches接受一个列表
def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree)!=list or len(tree)<1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True
##先判断是不是 列表  类型  或  长度  是否小于1  接着遍历树的分支
def is_leaf(tree):
    return not branches(tree)


def has_path(t, p):
    """Return whether tree t has a path from the root with labels p.

    >>> t2 = tree(5, [tree(6), tree(7)])
    >>> t1 = tree(3, [tree(4), t2])
    >>> has_path(t1, [5, 6])        # This path is not from the root of t1
    False
    >>> has_path(t2, [5, 6])        # This path is from the root of t2
    True
    >>> has_path(t1, [3, 5])        # This path does not go to a leaf, but that's ok
    True
    >>> has_path(t1, [3, 5, 6])     # This path goes to a leaf
    True
    >>> has_path(t1, [3, 4, 5, 6])  # There is no path with these labels
    False
    """
    if not t:  # Tree is empty
        return False
    if not p:  # Path is empty, we found a match
        return True
    if label(t) != p[0]:  # Current node's label doesn't match path
        return False

    # Recursively check each branch for the remaining path
    for branch in branches(t):
        if has_path(branch, p[1:]):
            return True

    return False  # No branch contains the path