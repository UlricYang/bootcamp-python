import copy

origin = [1, 2, [3, 4]]
cp1 = copy.copy(origin)
cp2 = copy.deepcopy(origin)

print(cp1 == cp2)

origin[2][0] = "hey!"
print(cp1)
print(cp2)
