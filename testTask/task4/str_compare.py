import re
import sys


def is_equal(s1: str, s2: str) -> str:
    template = r'.*'.join(re.split(r'\*+', s2))
    if re.fullmatch(template, s1) is None:
        return False
    return True

def is_equal_EvilBrother(s1: str, s2: str) -> str:
    template = r'.*'.join(re.split(r'\*+', s2))
    result = re.search(template, s1)
    if result is None:
        return False
    if len(s1) == result.end()-result.start():
        return True
    return False


if __name__=="__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print('\n\tПример строки: "python3.8 str_compare.py "строка_без*" "строка_с*""\n')
        raise Exception('Ошибка в строке запуска')
    s1 = sys.argv[1]
    s2 = sys.argv[2]
    print(is_equal(s1,s2))

    # print(is_equal_EvilBrother(s1,s2))