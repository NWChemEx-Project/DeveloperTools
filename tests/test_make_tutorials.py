import os
import sys
import unittest

# Get the path to the make_tutorials.py script and import it
current_dir = os.path.dirname(os.path.realpath(__file__))
dt_root_dir = os.path.dirname(current_dir)
scripts_dir = os.path.join(dt_root_dir, "scripts")
sys.path.append(scripts_dir)

from make_tutorials import *


class TestParseCxxFile(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(current_dir, "make_tutorials", "cxx.hpp")
        self.corr_code = [['\n', 'namespace test {\n', '\n'],
                          ['int function() { return 2; }\n', '\n',
                           '} //End namespace\n']]
        self.corr_comment = [['\n', ' A line to include\n']]

    def test_parse(self):
        comments, code, comment_first = parse_file("//", self.path)
        self.assertFalse(comment_first)
        self.assertEqual(comments, self.corr_comment)
        self.assertEqual(code, self.corr_code)


class TestWriteCxxCode(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(current_dir, "make_tutorials", "cxx.hpp")
        self.comments, self.code, self.first = parse_file("//", self.path)

    def test_block0(self):
        result = write_code(self.code[0], "C++")
        corr = ".. code:: C++\n\n    namespace test {\n\n"
        self.assertEqual(corr, result)

    def test_block1(self):
        result = write_code(self.code[1], "C++")
        corr = ".. code:: C++\n\n    int function() { return 2; }\n    \n"\
               "    } //End namespace\n\n"
        self.assertEqual(corr, result)


class TestWriteCxxComment(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(current_dir, "make_tutorials", "cxx.hpp")
        self.comments, self.code, self.first = parse_file("//", self.path)

    def test_block0(self):
        result = write_comment(self.comments[0])
        corr = " A line to include\n\n"
        self.assertEqual(corr, result)



# class TestMakeCxxTutorial(unittest.TestCase):
#     def setUp(self):
#         self.path = os.path.join(current_dir, "make_tutorials", "cxx.hpp")
#         self.comments, self.code, self.first = parse_file("//", self.path)
#
#     def test_write(self):
#         rv = write_tutorial("Cxx Parsing Test", self.first, self.comments,
#                             self.code, "C++")
#         print(rv)
#
#
# class TestParsePyFile(unittest.TestCase):
#     def setUp(self):
#         self.path = os.path.join(current_dir, "make_tutorials", "py.py")
#         self.corr_code =[['\n\ndef function():\n', '    return 2\n']]
#         self.corr_comment = [['', 'A line to include\n']]
#
#     def test_parse(self):
#         comments, code, comment_first = parse_file("#", self.path)
#         self.assertEqual(comments, self.corr_comment)
#         self.assertEqual(code, self.corr_code)
#         self.assertTrue(comment_first)


# class TestWritePyFile(unittest.TestCase):
#     def setUp(self):
#         self.path = os.path.join(current_dir, "make_tutorials", "py.py")
#         self.comments, self.code = parse_file("#", self.path)
#
#     def test_block0(self):
#         result = write_code(self.code[0], "py")
#         corr = ""
#         self.assertEqual(corr, result)
#
#     def test_block1(self):
#         result = write_code(self.code[1], "py")
#         corr = ".. code:: py\n\n    def function():\n        return 2\n\n"
#         self.assertEqual(corr, result)
#

if __name__ == "__main__":
    unittest.main(verbosity=2)
