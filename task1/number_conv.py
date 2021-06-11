import sys
from multipledispatch import dispatch


@dispatch(str, str)
def itoBase(nb: str, base: str) -> str:
    # Works up to 18-iary number system
    result = ""
    symbols = "0123456789ABCDEFGH"
    print(len(symbols))
    nb = int(nb)
    x = int(base)
    print(type(nb), type(x))
    while nb >= x:
        result += symbols[nb % x]
        nb = nb // x

    result = symbols[nb] + result[::-1]
    return result

@dispatch(str, str, str)
def itoBase(nb: str, baseSrc: str, baseDst: str) -> str:
    # Works up to 18-iary number system
    result = ""
    symbols = "0123456789ABCDEFGH"

    nb_10 = 0
    init_power = 0
    for i in nb[::-1]:
        nb_10 += symbols.index(i)*int(baseSrc)**init_power
        init_power += 1

    x = int(baseDst)
    while nb_10 >= x:
        result += symbols[nb_10 % x]
        nb_10 = nb_10 // x

    result = symbols[nb_10] + result[::-1]
    return result

if __name__=="__main__":
    if not(3<= len(sys.argv) <= 4):
        print('\nПример строки: "python3.8 number_conv.py число_10 система_исчисления_перевода')
        print('\tИЛИ')
        print('Пример строки: "python3.8 number_conv.py число система_исчисления_числа система_исчисления_перевода\n')
        raise Exception('Ошибка в строке запуска')
    print(sys.argv[1], sys.argv[2])
    print(itoBase(*sys.argv[1:]))