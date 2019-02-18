# CPE 202 Project 3
# Name: Ashley Sutter
# Student ID: 011278952
# Date (last modified): 2/17/2019
#
# Project 3a
# Section 5
# Purpose: Compress files using huffman encoding
# additional comments: Ask if you need to turn in solution files also!!

import os.path
from os import path

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __lt__(self, other):
        return comes_before(self, other)

def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    return (a.char < b.char) if (a.freq == b.freq) else (a.freq < b.freq)

def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    new_node = HuffmanNode(a.char if a.char < b.char else b.char, a.freq + b.freq)
    new_node.set_left(a)
    new_node.set_right(b)
    return new_node

def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file"""
    with open(filename) as f:
      return cnt_freq_helper(f.read())

def cnt_freq_helper(string):
    array =[0]*256
    for character in string:
        array[ord(character)] += 1
    return array

def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""
    nodes = []
    for i in range(len(char_freq)):
        if char_freq[i] != 0:
            nodes.append(HuffmanNode(i,char_freq[i]))
    return create_huff_tree_helper(nodes)

def create_huff_tree_helper(nodes):
    if len(nodes) == 1:
        return nodes[0]
    else:
        nodes.sort() #unideal
        first = nodes.pop(0)
        second = nodes.pop(0)
        new_node = combine(first, second)
        nodes.insert(0, new_node)
        return create_huff_tree_helper(nodes)

def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location"""
    ashleys_ASCII = ['']*256
    for i in range(256):
        ashleys_ASCII[i] = create_code_helper(node, i)
    return ashleys_ASCII

def create_code_helper(node, i):
    if node == None:
        return None
    else:
        if node.char == i and is_leaf(node):
            return ''
        else:
            left = create_code_helper(node.left, i)
            right = create_code_helper(node.right, i)
            if left == None and right == None:
                return None
            elif left == None:
                return '1' + right
            elif right == None:
                return '0' + left

def is_leaf(node):
    return node.left == None and node.right == None

def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    header = []
    for i in range(len(freqs)):
        if freqs[i] != 0:
            header.append(str(i) + ' ' + str(freqs[i]))
    return ' '.join(header)


def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""
    if path.exists(in_file) == False: #Ask prof
        raise FileNotFoundError
    #readfile
    f = open(in_file, 'r')
    letters_in_file = f.read()
    x = open(out_file, "w", newline="")
    if (letters_in_file == ''):
        x.write('')
    else:
        freqs = cnt_freq(in_file)
        tree = create_huff_tree(freqs)
        ashleys_code = create_code(tree)
        header = create_header(freqs)
        #write
        results = []
        x.write(header + '\n')
        for character in letters_in_file:
            results.append(ashleys_code[ord(character)])
        x.write(''.join(results))
    x.close()
    f.close()
