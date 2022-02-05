import sys
import readline


def displayText(*args):
    """

    :param text: text/message/string to display to the console
    :return: None
    Console display method to prevent incoming text from overriding current input lines
    The method also cleans up text for better display
    """
    line = readline.get_line_buffer()
    print(line.join(""))

    if len(line) > 0:
        sys.stdout.write("\033[1A[\033[2K")

    print("\n")
    for text in args:
        print(text)

    if len(line) > 0:
        sys.stdout.write(line)

    sys.stdout.flush()
