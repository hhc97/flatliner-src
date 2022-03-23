for i in range(22):
    if i < 5:
        print(i, 'continue i')
        continue
    print(i, 'i not continue')
    for j in range(i, 30):
        print(j)
        k = j
        print(k, 'k and j')
        while k > 15:
            k = k -  1
            if k > 20:
                print(k, 'k continue')
                continue
            print(k, 'finished k loop')
        if j < i + 5:
            print(j, 'continue j')
            continue
        print(j, 'j breaking')
        break
    if i == 17:
        print('i 17 continue')
        continue
    if i == 17 or i == 18:
        print(i, 'i break')
        break

a = 5
while a < 15:
    a = a + 1
    print(a, 'a loop')
    if a > 7:
        for b in range(a, a + 5):
            if b < a + 1:
                print(b, 'b continue')
                continue
            else:
                while b < a + 15:
                    b = b + 1
                    if b - a > 3:
                        print('b while break')
                        break
    if a < 13:
        print(a, 'a continue')
        continue
    print(a, 'a break')
    break

print('done test')
