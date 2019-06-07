import os
import sys
import unittest
import shutil

# Get the path to the make_tutorials.py script and import it
current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "make_tutorials", "src")
dt_root_dir = os.path.dirname(current_dir)
scripts_dir = os.path.join(dt_root_dir, "scripts")
sys.path.append(scripts_dir)

from make_tutorials import *


class TestParseCxxFile(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(src_dir, "cxx.hpp")
        self.corr_code = [['\n', 'namespace test {\n', '\n'],
                          ['int function() { return 2; }\n', '\n',
                           '} //End namespace\n']]
        self.corr_comment = [['\n', 'A line to include\n']]

    def test_parse(self):
        comments, code, comment_first = parse_file("//", self.path)
        self.assertFalse(comment_first)
        self.assertEqual(comments, self.corr_comment)
        self.assertEqual(code, self.corr_code)


class TestWriteCxxCode(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(src_dir, "cxx.hpp")
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
        self.path = os.path.join(src_dir, "cxx.hpp")
        self.comments, self.code, self.first = parse_file("//", self.path)

    def test_block0(self):
        result = write_comment(self.comments[0])
        corr = "A line to include\n\n"
        self.assertEqual(corr, result)


class TestWriteCxxTutorial(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(src_dir, "cxx.hpp")
        self.comments, self.code, self.first = parse_file("//", self.path)

    def test_tutorial(self):
        result = write_tutorial("cxx tutorial",
                                "C++",
                                self.comments,
                                self.code,
                                self.first)
        corr = "cxx tutorial\n"\
               "============\n\n"\
               ".. code:: C++\n\n"\
               "    namespace test {\n\n"\
               "A line to include\n\n"\
               ".. code:: C++\n\n"\
               "    int function() { return 2; }\n"\
               "    \n"\
               "    } //End namespace\n\n"
        self.assertEqual(corr, result)


class TestParsePyFile(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(src_dir, "py.py")
        self.corr_code =[['\n', '\n', "def function():\n", "    return 2\n"]]
        self.corr_comment = [['\n', 'A line to include\n']]

    def test_parse(self):
        comments, code, comment_first = parse_file('#', self.path)
        self.assertEqual(comments, self.corr_comment)
        self.assertEqual(code, self.corr_code)
        self.assertTrue(comment_first)


class TestWritePyCode(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(src_dir, "py.py")
        self.comments, self.code, self.first = parse_file("#", self.path)

    def test_block0(self):
        result = write_code(self.code[0], "py")
        corr = ".. code:: py\n\n    def function():\n        return 2\n\n"
        self.assertEqual(corr, result)


class TestWritePyComment(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(src_dir, "py.py")
        self.comment, self.code, self.first = parse_file('#', self.path)

    def test_write0(self):
        result = write_comment(self.comment[0])
        corr = "A line to include\n\n"
        self.assertEqual(corr, result)


class TestWritePyTutorial(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(src_dir, "py.py")
        self.comment, self.code, self.first = parse_file('#', self.path)

    def test_write(self):
        result = write_tutorial("python tutorial",
                                "py",
                                self.comment,
                                self.code,
                                self.first)
        corr = "python tutorial\n"\
               "===============\n\n"\
               "A line to include\n\n"\
               ".. code:: py\n\n"\
               "    def function():\n"\
               "        return 2\n\n"

        self.assertEqual(corr, result)

class TestMakeTutorials(unittest.TestCase):
    def setUp(self):
        self.input_path = src_dir
        self.output_path = os.path.join(current_dir, "make_tutorials", "test")

    def test_make_tutorials(self):
        make_tutorials(self.input_path, self.output_path)

        for x in ["cxx.rst", "index.rst", "py.rst"]:
            rst_file = os.path.join(self.output_path, x)
            self.assertTrue(os.path.exists(rst_file))

    def tearDown(self):
        if os.path.isdir(self.output_path):
            shutil.rmtree(self.output_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
