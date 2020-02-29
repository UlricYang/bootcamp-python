def f(n):
    s = "first"
    for i in range(n):
        s = "".join([s, s[i]])
    return s


print(f(101))
