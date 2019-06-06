import os


def parse_file(cc, filename):
    """
    This function actually parses the test. It does so using some pretty simple
    logic. Consequentially, you can't deviate too much from the expected format.
    Specifically we assume:

     - The start of the tutorial block (i.e., "<comment_char>TUTORIAL") is the
       first non-whitespace token on the line.
     - The start of a skipping directive (i.e.,
       "<comment_char>TUTORIAL_START_SKIP") is the first non-whitespace token on
       the line.
     - The end of a skipping directive (i.e.,
       "<comment_char>TUTORIAL_STOP_SKIP") is the first non-whitespace token on
       the line.
       C++ is the first non-whitespace token on the line.
     - all comment blocks are continuous (no blank lines in the middle)

    :param cc: The character denoting the comment
    :param filename: The full path to the file
    :return: A list of tutorial comments and code blocks
    """

    # These are parsing strings we'll need to look for
    tutor_start = cc + "TUTORIAL"
    tutor_skip_start = cc + "TUTORIAL_START_SKIP"
    tutor_skip_stop = cc + "TUTORIAL_STOP_SKIP"

    comments = []  # Will be the comments we find
    code = [[]]  # Will be the code snippets we fine
    in_comment = False  # True signals we are in a tutorial comment block
    skipping = False
    which_first = None

    with open(filename, 'r') as input_file:
        for line in input_file:
            no_ws = line.lstrip()  # The line w/o proceeding whitespace

            # Dispatch conditions
            is_skip_start = tutor_skip_start == no_ws[:len(tutor_skip_start)]
            is_skip_stop = tutor_skip_stop == no_ws[:len(tutor_skip_stop)]
            is_tutor_start = tutor_start == no_ws[:len(tutor_start)]
            is_comment = cc == line.lstrip()[:len(cc)]

            # Actually do the dispatching
            if skipping:  # Currently skipping
                if is_skip_stop:  # and we were told to stop
                    skipping = False
            elif is_skip_stop:  # Not skipping, but told to stop
                raise Exception("TUTORIAL_STOP_SKIP w/o TUTORIAL_START_SKIP")
            elif is_skip_start:  # Told to start skipping
                skipping = True
            elif is_tutor_start:  # Told to start tutorial comment
                if which_first is None:
                    which_first = True
                if in_comment:
                    raise Exception("Can't nest TUTORIAL sections")
                comments.append([])  # Start a new comment block
                in_comment = True
            elif is_comment and in_comment:  # Part of tutorial comment
                comments[-1].append(no_ws[2:])  # Add line w/o comment character
            elif in_comment:  # 1st line outside a comment block
                in_comment = False
                code.append([])
                code[-1].append(line)
            else:  # n-th line outside a comment block
                if which_first is None:
                    which_first = False
                code[-1].append(line)

    return comments, code, which_first


def write_code(block, lang):
    """
    Given a code block from the parsed file this function will turn it into the
    corresponding  reST code. This function will automatically remove any
    proceeding or trailing blank lines from the parsed code block.

    :param block: The code block to print out.
    :param lang: The language of the code snippet
    :return: A string suitable for printing in a reST file
    """
    a_tab = " "*4
    start = 0
    end = len(block)

    # Strip off any proceeding or trailing blank lines
    for line in block:
        if line.strip():
            break
        start += 1

    if start == end:  # Early termination for blank blocks
        return ""

    for line in reversed(block):
        if line.strip():
            break
        end -= 1

    # Assemble the actual code block
    output = ".. code:: {}\n\n".format(lang)

    for line in block[start: end]:
        output += a_tab + line
    output += '\n'

    return output


def write_comment(block):
    start = 0
    end = len(block)

    # Strip off any proceeding or trailing blank lines
    for line in block:
        if line.strip():
            break
        start += 1

    if start == end:  # Early termination for blank blocks
        return ""

    for line in reversed(block):
        if line.strip():
            break
        end -= 1

    output = ""
    for line in block[start : end]:
        output += line
    output += '\n'
    return output


def write_tutorial(name, first, comments, code, lang):
    """
    Given the parsed comments and code blocks this function will write out the
    full reST page for the tutorial.

    :param name: The name of the tutorial. Will be used for the title.
    :param frist: True if a comment was first and false if a code block was
    :param comments: A list of the comment blocks.
    :param code: A list of the code blocks.
    :param lang: The language for the reST code snippets
    :return:
    """

    first_list = comments if first else code
    second_list = code if first else comments
    n_first = len(first_list)
    n_second = len(second_list)

    # Write the title of the tutorial
    output = name + '\n'
    output += '='*(len(name) - 1) + "\n\n"

    for i in range(n_first):
        if first:
            output += write_comment(comments[i])
        else:
            write_code(code[i], lang)
        if i >= n_second:
            continue
        if first:
            output += write_code(code[i], lang)
        else:
            output += write_comment(comments[i])

    return output

# def make_tutorials(input, output) :
#     """
#     Given a full path to a directory, this function will parse each .py and
#     .hpp file it finds. This process is repeated recursively for each
#     subdirectory.
#
#     For a given C++ file this script looks for blocks like:
#
#     //TUTORIAL
#     //
#     //
#     // Some documentation for the tutorial
#     //
#
#     and Python blocks like:
#
#     #TUTORIAL
#     #
#     #
#     # Some documentation for the tutorial
#     #
#
#     :param dir: The full path to the directory containing the tutorials.
#     :return:
#     """
#
#     #Define the comment characters for each language
#     py_comm = '#'
#     c_comm  = "//"
#
#
#     #Make output directory if it does not exist
#     if not os.path.exists(output):
#         os.mkdir(output)
#
#     filenames = []
#
#     for filename in os.listdir(input):
#         if not filename.endswith(".hpp"):
#             continue
#         infile = os.path.join(input, filename)
#         filenames.append(filename.split(".")[0])
#         outfile = os.path.join(output, filenames[-1] + ".rst")
#         print(outfile)
#         comments, code = parse_file(infile)
#         with open(outfile, 'w') as output_file:
#             good_name = filenames[-1].replace('_', ' ').title()
#             tutorial_name = good_name + " Tutorial\n"
#             output_file.write(tutorial_name)
#             output_file.write('='*(len(tutorial_name) - 1) + "\n\n")
#             write_tutorial(output_file, comments, code)
#
#     with open(os.path.join(output, "index.rst"), 'w') as index_file:
#         index_file.write("List of Tutorials\n")
#         index_file.write("=================\n\n")
#         index_file.write(".. toctree::\n")
#         index_file.write("    :maxdepth: 2\n")
#         index_file.write("    :caption: Contents:\n\n")
#         for file in filenames:
#             index_file.write("    " + file +"\n")
#
#
#
# def main():
#     docs_dir = os.path.dirname(os.path.realpath(__file__))
#     root_dir = os.path.dirname(docs_dir)
#     examples_dir = os.path.join(root_dir, "tests", "examples")
#     tutorial_dir = os.path.join(docs_dir, "source", "tutorials")
#
#     if not os.path.exists(tutorial_dir):
#         os.mkdir(tutorial_dir)
#
#     write_tutorials(examples_dir, tutorial_dir)
#     subprocess.call(["make", "html"])
#
# if __name__ == "__main__" :
#     main()
