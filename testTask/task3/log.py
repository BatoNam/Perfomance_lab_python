import random


with open('log.log', 'w') as f:
    f.writelines('META DATA:\n')
    f.writelines('200\n')
    f.write('32\n')

    for i in range(17000):
        y = random.randint(2010, 2030)
        m = random.randint(1, 12)
        if m<10:
            m = '0' + str(m)
        d = random.randint(1, 28)
        if d<10:
            d = '0' + str(d)
        h = random.randint(1, 20)
        if h<10:
            h = '0' + str(h)
        mn = random.randint(1, 59)
        if mn<10:
            mn = '0' + str(mn)
        s = random.randint(1, 59)
        if s<10:
            s = '0' + str(s)
        ms = random.randint(1, 999)
        if ms<10:
            ms = '00' + str(ms)
        elif ms<100:
            ms = '0' + str(ms)
        user = 'username' + str(random.randint(1,5))
        if random.randint(1,10) < 5:
            action = 'top up'
        else:
            action = 'scoop'
        l = random.randint(1,100)
        text = f'{y}-{m}-{d}Т{h}:{mn}:{s}.{ms}Z – [{user}] - wanna {action} {l}l\n'
        f.write(text)