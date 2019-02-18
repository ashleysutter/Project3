import unittest
import filecmp
import subprocess
from huffman import *
import time

class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        #file1 test
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
        #emptyfile test
        huffman_encode('empty_file.txt', 'empty_file_out.txt')
        err = subprocess.call("diff -wb empty_file_out.txt empty_file_soln.txt", shell = True)
        self.assertEqual(err, 0)
        #multiline test
        huffman_encode('multiline.txt', 'multiline_out.txt')
        err = subprocess.call("diff -wb multiline_out.txt multiline_soln.txt", shell = True)
        self.assertEqual(err, 0)
        #file2 test
        huffman_encode('file2.txt', 'file2_out.txt')
        err = subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell = True)
        self.assertEqual(err, 0)
        #declaration test
        huffman_encode('declaration.txt', 'declaration_out.txt')
        err = subprocess.call("diff -wb declaration_out.txt declaration_soln.txt", shell = True)
        self.assertEqual(err, 0)
        #War&Peace test 
#        start = time.time()
#        huffman_encode('file_WAP.txt', 'file_WAP_out.txt')
#        end = time.time()
#        self.assertTrue(end-start < 5)

    def test_cnt_freq_02(self):
        self.assertEqual(cnt_freq("file1.txt")[97:101], [4, 3, 2, 1])

    def test_cnt_freq_helper(self):
        self.assertEqual(cnt_freq_helper("ddddddddddddddddccccccccbbbbaaff")[97:104], [2, 4, 8, 16, 0, 2, 0]) 

    def test_comes_before(self):
        a = HuffmanNode('a', 1) 
        b = HuffmanNode('b', 1)
        c = HuffmanNode('c', 2)
        d = HuffmanNode('d', 0)
        self.assertTrue(comes_before(a,b))
        self.assertFalse(comes_before(b,a))
        self.assertTrue(comes_before(a,c))
        self.assertTrue(comes_before(d,a))
        self.assertFalse(comes_before(c,d))

    def test_create_huff_tree_02(self):
        tree = create_huff_tree(cnt_freq_helper("aaaabbbccd"))
        self.assertEqual(tree.left.char, 97)
        self.assertEqual(tree.left.freq, 4)
        self.assertEqual(tree.char, 97)
        self.assertEqual(tree.freq, 10)
        self.assertEqual(tree.right.right.char, 99)
        self.assertEqual(tree.right.right.freq, 3)
        self.assertEqual(tree.right.right.left.char, 100)
        self.assertEqual(tree.right.right.left.freq, 1)

    def test_create_code_02(self):
        tree = create_huff_tree(cnt_freq_helper("aaaabbbccd"))
        self.assertEqual(create_code(tree)[97:101], ['0', '10', '111', '110'])

    def test_create_header_02(self):
        self.assertEqual(create_header(cnt_freq_helper('aaabbbbcc')),'97 3 98 4 99 2')

    def test_huffman_encode_02(self):
        try:
            huffman_encode('fake_file', 'outout_file')
        except FileNotFoundError as e:
            self.assertEqual(str(e), "")

if __name__ == '__main__': 
   unittest.main()
