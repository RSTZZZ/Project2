"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, 2013, 2014, 2015, 2016
# Zachary Yang
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

# global variables
zero = '0'
one = '1'
two = '2'
e = 'e'
empty = ''
bar = '|'
dot = '.'
star = '*'
left = '('
right = ')'


def is_regex(s):
    '''(Str) -> Bool
    A function that takes the string s and only returns True
    iff its a valid regular expression
    REQ: None
    >>> is_regex('0')
    True
    >>> is_regex('1')
    True
    >>> is_regex('2')
    True
    >>> is_regex('e')
    True
    >>> is_regex('0*')
    True
    >>> is_regex('2************')
    True
    >>> is_regex('(0.1)')
    True
    >>> is_regex('(2|e)')
    True
    >>> is_regex('(0*.1*)')
    True
    >>> is_regex('(0.(2|e))')
    True
    >>> is_regex('((0.1)|(2.e)*)')
    True
    >>> is_regex('3')
    False
    >>> is_regex('*0')
    False
    >>> is_regex('((0|e|e))')
    False
    >>> is_regex('00')
    False
    >>> is_regex('0.0')
    False
    >>> is_regex('(0.e****')
    False
    '''
    result = False
    # length 1 of string
    if len(s) == 1:
        # must be one of these four
        result = (s in [zero, one, two, e])
    # length 2 of string
    elif len(s) > 1 and s[-1] == star:
        # check if before star is a valid regex
        result = is_regex(s[:-1])
    elif len(s) >= 5:
        # locate the rightmost left parenthesis
        # locate the leftmost right parenthesis
        # take out the . or | inside it
        # replace the whole thing by a 0
        # check the rest
        if s.__contains__(left):
            l_index = s.rfind(left)
            if s.__contains__(right):
                # so you can find the leftmost right parenthesis after
                # that rightmost left parenthesis
                # you have to add the indexes you took out
                r_index = s[l_index:].find(right) + len(s[:l_index])
                # check the inner, part
                inner = s[l_index + 1: r_index]
                index = 0
                if inner.__contains__(bar):
                    index = inner.find(bar)
                elif inner.__contains__(dot):
                    index = inner.find(dot)
                # check before the . and | and the part afterwards
                (inner_front, inner_back) = (inner[:index], inner[index + 1:])
                # check if both inners are valid regex
                cond1 = is_regex(inner_front) and is_regex(inner_back)
                # check the rest of the string
                # replace what was inside as a valid char
                rest = s[:l_index] + zero + s[r_index + 1:]
                result = cond1 and is_regex(rest)
    return result


def regex_match(r, s):
    '''(RegexTree, Str) -> Bool
    A function that takes in the string s and tree rooted at r.
    If the string and the tree matches, return true
    REQ: r is a proper RegexTree, as in it uses Leaf, BarTree, StarTre
         and DotTree only
    >>> regex_match(Leaf('0'), '0')
    True
    >>> regex_match(Leaf('1'), '1')
    True
    >>> regex_match(Leaf('2'), '2')
    True
    >>> regex_match(Leaf('e'), '')
    True
    >>> regex_match(StarTree(Leaf('0')), '')
    True
    >>> regex_match(StarTree(Leaf('0')), '0')
    True
    >>> regex_match(StarTree(Leaf('0')), '00000000')
    True
    >>> regex_match(BarTree(Leaf('0'), Leaf('1')), '0')
    True
    >>> regex_match(BarTree(Leaf('0'), Leaf('1')), '1')
    True
    >>> regex_match(DotTree(Leaf('0'), Leaf('e')), '0')
    True
    >>> regex_match(DotTree(Leaf('e'), Leaf('e')), '')
    True
    >>> s = ''
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '0'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '1'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '01'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '10'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '010101'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '101010'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '01001010'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '01010102'
    >>> regex_match(StarTree(BarTree(Leaf('0'), Leaf('1'))), s)
    False
    >>> s = ''
    >>> regex_match(StarTree(DotTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '01'
    >>> regex_match(StarTree(DotTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '0101010101'
    >>> regex_match(StarTree(DotTree(Leaf('0'), Leaf('1'))), s)
    True
    >>> s = '0110101010'
    >>> regex_match(StarTree(DotTree(Leaf('0'), Leaf('1'))), s)
    False
    >>> s = '1'
    >>> regex_match(DotTree(StarTree(Leaf('0')), Leaf('1')), s)
    True
    >>> s = '00001'
    >>> regex_match(DotTree(StarTree(Leaf('0')), Leaf('1')), s)
    True
    >>> s = '1'
    >>> regex_match(DotTree(StarTree(BarTree(Leaf('0'), Leaf('1'))),\
    Leaf('1')), s)
    True
    >>> s = '01'
    >>> regex_match(DotTree(StarTree(BarTree(Leaf('0'), Leaf('1'))),\
    Leaf('1')), s)
    True
    >>> s = '101'
    >>> regex_match(DotTree(StarTree(BarTree(Leaf('0'), Leaf('1'))),\
    Leaf('1')), s)
    True
    >>> s = '01011110110101'
    >>> regex_match(DotTree(StarTree(BarTree(Leaf('0'), Leaf('1'))),\
    Leaf('1')), s)
    True
    >>> regex_match(DotTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '02')
    True
    >>> regex_match(DotTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '12')
    True
    >>> regex_match(DotTree(DotTree(Leaf('0'), Leaf('1')), Leaf('2')), '012')
    True
    >>> regex_match(RegexTree('0', []), '0')
    False
    >>> regex_match(BarTree(StarTree(Leaf('0')), Leaf('1')), '')
    True
    >>> regex_match(BarTree(StarTree(Leaf('0')), Leaf('1')), '0')
    True
    >>> regex_match(BarTree(StarTree(Leaf('0')), Leaf('1')), '1')
    True
    >>> regex_match(BarTree(StarTree(Leaf('0')), Leaf('1')), '000000')
    True
    >>> regex_match(BarTree(StarTree(Leaf('0')), Leaf('1')), '11111')
    False
    >>> regex_match(BarTree(StarTree(Leaf('0')), Leaf('1')), '00001')
    False
    >>> regex_match(BarTree(DotTree(Leaf('0'), Leaf('1')), Leaf('2')), '2')
    True
    >>> regex_match(BarTree(DotTree(Leaf('0'), Leaf('1')), Leaf('2')), '01')
    True
    >>> regex_match(BarTree(DotTree(Leaf('0'), Leaf('1')), Leaf('2')), '012')
    False
    >>> regex_match(BarTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '0')
    True
    >>> regex_match(BarTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '1')
    True
    >>> regex_match(BarTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '2')
    True
    >>> regex_match(BarTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '01')
    False
    >>> regex_match(BarTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '02')
    False
    >>> regex_match(BarTree(BarTree(Leaf('0'), Leaf('1')), Leaf('2')), '12')
    False
    '''
    # intial result is False
    result = False
    if type(r) == Leaf:
        # check if same symbol, since only one
        symbol = r.get_symbol()
        if symbol == e:
            result = (s == empty)
        else:
            result = (s == symbol)
    elif type(r) == StarTree:
        # it must be a repeating series of watever the child is
        # get the child
        child = r.get_child()
        # since its a regex + *, it can be empty
        cond1 = (s == '')
        # if child is leaf
        if type(child) == Leaf:
            # check all the way to the end, to see if its repeating
            # the same thing
            # count is the index, cond is to be more efficient, so as to
            # stop the loop once cond2 is False
            count = 0
            cond = True
            while count < len(s) and cond:
                cond2 = regex_match(child, s[count])
                count += 1
                if not cond2:
                    cond = False
        # See if its a BarTree or DotTree
        elif type(child) == BarTree or type(child) == DotTree:
            # start at index 1, and go down
            count = 0
            # cond to make loop efficient
            cond = True
            # go through the loop, and check if from the beginning to count
            # is equal to the child regex
            while count <= len(s) and cond:
                cond2 = regex_match(child, s[:count])
                # if true, we want to see if its the end of the string
                # if not the end of the string, we start at the end
                # and continue checking
                if cond2:
                    if count < len(s):
                        s = s[count:]
                        count = 0
                    else:
                        cond = False
                # if false, we add one to count
                else:
                    count += 1
        # if its a star again, get the child, and nothing happens to it
        elif type(child) == StarTree:
            child = r.get_child()
            cond2 = regex_match(child, s)
        # must satistfy cond1 or cond2 from each case
        result = cond1 or cond2
    # if its a BarTree
    elif type(r) == BarTree:
        # get left and right child
        left_child = r.get_left_child()
        right_child = r.get_right_child()
        # must match either the left child, or the right child
        result = regex_match(left_child, s) or regex_match(right_child, s)
    # if its a DotTree
    elif type(r) == DotTree:
        # get left adn right child
        left_child = r.get_left_child()
        right_child = r.get_right_child()
        # if left_child is a leaf, you know the s[0] is the one to be checked
        if type(left_child) == Leaf:
            # this is if s is not the proper length, u just return false
            # get the left and right
            if len(s) > 0:
                l = s[0]
            else:
                l = empty
            r = s[1:]
            # check left with s[0]
            # check right with the rest
            result = (regex_match(left_child, l) and
                      regex_match(right_child, r))
        # if BarTree, DotTree or StarTree
        elif (type(left_child) == BarTree) or (type(left_child) == DotTree):
            # start at index 1
            count = 0
            # cond is to make loop efficient, stop when cond1 is True
            cond = True
            # go down until you match leftchild
            while count < len(s) and cond:
                cond1 = regex_match(left_child, s[:count])
                if cond1:
                    cond = False
                else:
                    count += 1
            r = s[count:]
            result = cond1 and regex_match(right_child, r)
        elif (type(left_child) == StarTree):
            # look at right child first, see if it correct
            # take out the end part of the string that matches to right child
            count = len(s)
            cond = True
            while count >= 0 and cond:
                cond1 = regex_match(right_child, s[count:])
                if cond1:
                    # if right_child is a StarTree, you continue from the end
                    # of the string, going left, cuz it can repeat
                    if count > 0 and type(right_child) == StarTree:
                        s = s[:count]
                        count = len(s)
                    else:
                        cond = False
                else:
                    count -= 1
            # if right_child is a StarTree, its automatically True, cuz
            # right_child could be an empty_str
            if type(right_child) == StarTree:
                cond1 = True
            if cond1:
                # start at index 1
                count = 0
                # cond is to make loop efficient, stop when cond1 is True
                cond = True
                # go down until you match leftchild
                if count == len(s):
                    # if empty, then still true, cuz its a r*
                    cond2 = True
                # else check until the end, to see if it matches
                while count < len(s) and cond:
                    cond2 = regex_match(left_child, s[:count])
                    if cond2:
                        if count < len(s):
                            s = s[count:]
                            count = 0
                        else:
                            cond = False
                    else:
                        count += 1
                result = cond2
            else:
                result = False
    return result


def build_regex_tree(regex):
    '''(Str) -> RegexTree
    A function that takes a valid regex and builds the corresponding
    regular expression tree and returns its root.
    REQ: regex must be a valid regex
    >>> build_regex_tree('0')
    Leaf('0')
    >>> build_regex_tree('1')
    Leaf('1')
    >>> build_regex_tree('2')
    Leaf('2')
    >>> build_regex_tree('e')
    Leaf('e')
    >>> build_regex_tree('0*')
    StarTree(Leaf('0'))
    >>> build_regex_tree('0**')
    StarTree(StarTree(Leaf('0')))
    >>> build_regex_tree('(0.1)')
    DotTree(Leaf('0'), Leaf('1'))
    >>> build_regex_tree('(2|e)')
    BarTree(Leaf('2'), Leaf('e'))
    >>> build_regex_tree('(0.1)*')
    StarTree(DotTree(Leaf('0'), Leaf('1')))
    >>> build_regex_tree('((0.1)|2)')
    BarTree(DotTree(Leaf('0'), Leaf('1')), Leaf('2'))
    >>> build_regex_tree('((0.1)|(2.e*))')
    BarTree(DotTree(Leaf('0'), Leaf('1')), DotTree(Leaf('2'),\
 StarTree(Leaf('e'))))
    '''
    # if valid regex is of one length
    result = None
    if len(regex) == 1:
        # just make it a Leaf
        result = Leaf(regex)
    # if it has a star in the back
    elif regex[-1] == star:
        # make it into a StarTree, with the child, of the stuff in front
        result = StarTree(build_regex_tree(regex[:-1]))
    # if it is valid, it must be longer than 5
    elif len(regex) >= 5:
        # find the first right parenthesis, and the rightmost parenthesis
        if regex[0] == left:
            (l_index, r_index) = (0, -1)
            # u want to find the right operator
            cond = True
            while cond:
                # find the first bar or dot
                op_index = (find_op(regex[l_index + 1:]) +
                            (len(regex[:l_index + 1])))
                # now you want to see if you there to check if
                # there is any left
                # parenthesis
                temp = regex[l_index + 1:op_index]
                if left in temp:
                    # ur new left index is the operator, cuz you
                    # want to find the next operator
                    l_index = op_index
                else:
                    cond = False
            # got r1 and r2
            r1 = regex[1:op_index]
            r2 = regex[op_index + 1:-1]
            operator = regex[op_index]
            # nothing should be behind r_index
            # create the tree
            if operator == bar:
                result = BarTree(build_regex_tree(r1), build_regex_tree(r2))
            elif operator == dot:
                result = DotTree(build_regex_tree(r1), build_regex_tree(r2))
    return result


def all_regex_permutations(s):
    '''(Str) -> Set of Str
    This function takes in the string, and spits out all the permutations
    of a valid regex.
    REQ: None
    # since it calls on perms, we can assume that perms gives out a
    valid regex
    >>> all_regex_permutations('0')
    {'0'}
    >>> all_regex_permutations('1')
    {'1'}
    >>> all_regex_permutations('2')
    {'2'}
    >>> all_regex_permutations('e')
    {'e'}
    >>> all_regex_permutations('2*')
    {'2*'}
    >>> x = all_regex_permutations('(1.0)')
    >>> x.__eq__({'(1.0)', '(0.1)'})
    True
    >>> x = all_regex_permutations('(1.0)*')
    >>> x.__eq__({'(1*.0)', '(1.0*)', '(1.0)*', '(0*.1)', '(0.1*)', \
'(0.1)*'})
    True
    >>> x = all_regex_permutations('(1.0)**')
    >>> x.__eq__({'(0.1**)', '(1*.0)*', '(1.0*)*', '(0*.1)*', '(0.1*)*', \
'(1*.0*)', '(1.0**)', '(1.0)**', '(1**.0)', '(0*.1*)', '(0.1)**', '(0**.1)'})
    True
    '''
    # find how many of each there are
    l_count = s.count(left)
    r_count = s.count(right)
    d_count = s.count(dot)
    b_count = s.count(bar)
    star_count = s.count(star)
    non_leaf = [left, right, dot, star, bar]
    # you want it to just have leaf
    leaf = clean_valid_str(s, non_leaf)
    # make the parenthesis
    # create string in the format of # of left + # of rights
    # must have equal number of l_count and r_count
    s = set()
    cond = (l_count == r_count)
    if cond:
        temp = ''
        for i in range(l_count):
            temp += left
        for i in range(r_count):
            temp += right
        s = parenthesis_helper(temp)
    # add the operator
    cond2 = (l_count == (d_count + b_count))
    if cond and cond2:
        temp = ''
        for i in range(d_count):
            temp += dot
        for i in range(b_count):
            temp += bar
        s = operator_helper(s, temp)
    # add the numbers
    if cond and cond2:
        if s == set() and len(leaf) == 1:
            s = {leaf}
        else:
            s = letter_insert(s, leaf)
    # check is_regex cuz not all permutations result in correct
    # regex (not enough leaves)
    # if leaves is not right, it is stopped here too
    result = set()
    for value in s:
        if '(.' not in value and\
           '.)' not in value and\
           '|)' not in value and\
           '(|' not in value:
            result.add(value)
    # add the stars
    if cond and cond2:
        s = insert_star(result, star_count)
    return s


def find_op(regex):
    '''(str) -> int
    Given a string, it returns the first | or .
    inside it, will return -1 if not found
    REQ: None
    >>> find_op('890')
    -1
    >>> find_op('(0.1)')
    2
    >>> find_op('0.1|2')
    1
    >>> find_op('9080912|')
    7
    >>> find_op('989|213.')
    3
    '''
    # find bar and dot index
    b_index = regex.find(bar)
    d_index = regex.find(dot)
    # if bar is -1, then op_index is d_index
    if b_index == -1:
        op_index = d_index
    # if dot is -1, then op_index is b_index
    elif d_index == -1:
        op_index = b_index
    # if b_index < d_index, op_index = b_index
    elif (b_index < d_index):
        op_index = b_index
    # else, just op_index = d_index
    else:
        op_index = d_index
    return op_index


def clean_valid_str(s, valid_char):
    '''(Str, List of Str) -> Str
    This function takes in a string, and strips all valid characters
    in the list out of the string
    REQ: None
    >>> clean_valid_str('123', ['1'])
    '23'
    >>> clean_valid_str('000000', ['0', '1'])
    ''
    >>> clean_valid_str('123123',['123'])
    ''
    '''
    for char in valid_char:
        s = s.replace(char, '')
    return s


def parenthesis_helper(s):
    '''(Str) -> Set of Str
    This function creates all the correct form of the parenthesis in a valid
    regex. VERY OP IN MY OPINION
    REQ: s must have the same amount of left and right parenthesis
    >>> parenthesis_helper('()')
    {'()'}
    >>> parenthesis_helper('(())')
    {'(())'}
    >>> x = parenthesis_helper('((()))')
    >>> x.__eq__({'((()))', '(()())'})
    True
    '''
    # if no parenthesis, return empty set
    if len(s) == 0:
        result = set()
    # if len of 2, it must be '()'
    elif len(s) == 2:
        result = {'()'}
    # if multiple of 2 (since left and right must be the same amount)
    elif (len(s) % 2) == 0:
        # take away the outer first
        s = s[1:-1]
        # get the inner
        inner = parenthesis_helper(s)
        # initialize result
        result = set()
        # add the outer parenthesis back
        for value in inner:
            result.add(left + value + right)
        # if inside is greater than 4, there is another case
        # its a () with the permutations of the rest of the str
        if len(s) >= 4:
            # so take away outer ()
            s = s[1:-1]
            # see permutations of it
            inner = parenthesis_helper(s)
            # add ( () value ) and ( value ())
            for value in inner:
                result.add(left + '()' + value + right)
                result.add(left + value + '()' + right)
    return result


def operator_helper(s, o):
    '''(Set of Str, Str) -> Set of Str
    This function goes through each of the set. it will add an operator
    which is the dots and bars to where it can be added.
    REQ: must have at least ()
    REQ: must have correct number of operators
    >>> operator_helper({'()'}, '.')
    {'(.)'}
    >>> x = operator_helper({'(())'}, '.|')
    >>> x.__eq__({'(.(|))', '((.)|)', '(|(.))', '((|).)' })
    True
    '''
    # loop through each operator
    for char in o:
        # temperary
        temp = set()
        # go through values in s
        for value in s:
            # specific rule is either its a (
            # or its ) and not at the end
            i = 0
            while i < len(value):
                if value[i] == left or (value[i] == right and
                                        i != len(value) - 1):
                    temp.add(value[:i + 1] + char + value[i + 1:])
                i += 1
            # give temp to s
        s = temp
    # another temp set
    temp = set()
    # weed out simple ones, where the operators is doubled, or you see ()
    for value in s:
        if not ('()' in value) and\
           not ('.|' in value) and\
           not ('..' in value) and\
           not ('|.' in value) and\
           not ('||' in value):
            temp.add(value)
    # initialize the result
    result = set()
    # for each, go trhough the op_limiter, which see if there is an operator
    # in each (), and only one for each ()
    for value in temp:
        if op_limiter(value):
            result.add(value)
    return result


def op_limiter(s):
    '''(Str) -> Bool
    This function takes in a str, and looks if for each (), there is one
    corresponding operator
    REQ: None
    >>> op_limiter('')
    False
    >>> op_limiter('(.)')
    True
    >>> op_limiter('((.)|')
    True
    >>> op_limiter('((.).(.))')
    True
    '''
    # find the innermost left bracket
    l_index = s.rfind(left)
    # find the innermost right bracket, that corresponds to this left bracker
    r_index = s[l_index:].find(right) + len(s[:l_index])
    # look at inner
    inner = s[l_index:r_index + 1]
    # inisde must be length of 3 cuz (.) or (|)
    cond = len(inner) == 3
    if cond:
        # check the rest
        rest = s[:l_index] + s[r_index + 1:]
        # if empty, result is True
        if rest == '':
            result = True
        # if not empty, check the rest if still follow rules
        else:
            result = op_limiter(rest)
    else:
        result = False
    return result


def letter_insert(s, char):
    '''(Set of Str, Str) -> Set of Str
    This function take in s and adds the char accordingly
    REQ: s should have at least length of 3
    REQ: must have enough char
    >>> x = letter_insert({'(.)'}, '20')
    >>> x.__eq__({'(2.0)', '(0.2)'})
    True
    >>> x = letter_insert({'((.)|)'}, '203')
    >>> x.__eq__({'(2.0)', '(0.2)'})
    True
    >>> x.__eq__({'((2.0)|3)', '((0.2)|3)', '((3.2)|0)', '((3.0)|2)', \
    '((2.3)|0)', '((0.3)|2)'})
    True
    '''
    # go through each characters
    for c in char:
        # initialize a temporary set
        temp = set()
        # go through each value in s
        for value in s:
            # loop though the length of s
            i = 0
            while i < len(value) - 1:
                # you can only add letter if its ( .
                # or its . )
                cond1 = (value[i] == left) and (value[i + 1] in [dot, bar])
                cond2 = (value[i] in [dot, bar]) and (value[i + 1] == right)
                if cond1 or cond2:
                    combo = value[:i + 1] + c + value[i+1:]
                    temp.add(combo)
                i += 1
        # make s into the temporary set
        s = temp
    return s


def insert_star(s, star_count):
    '''(Set of Str, Int) -> Set of Str
    This functions is the handy function that adds stars to where you can
    add stars and still be valid.
    REQ: None
    >>> x = insert_star({'(0.1)'}, 1)
    >>> x.__eq__({'(0*.1)', '(0.1*)' '(0.1)*'})
    True
    '''
    # create temporary, let it equal to s
    temp1 = s
    # go through the number of stars needed
    for count in range(star_count):
        # create another temp
        temp3 = set()
        # go throught the permutation in temp1
        for permutation in temp1:
            # create an temp2 to hold one round of permutation
            temp2 = set()
            # go from index 1
            index = 1
            # see if u can add star
            while index <= len(permutation):
                value = permutation[:index]
                # cond is that is must be leaf,right or star
                if value[-1] in [zero, one, two, e, right, star]:
                    temp2.add(permutation[:index] + star +
                              permutation[index:])
                index += 1
            # add the set to the bigger temp, so one round of star
            temp3 = temp3.union(temp2)
        # temp1 == the round, so next round is updated
        temp1 = temp3
    return temp1
