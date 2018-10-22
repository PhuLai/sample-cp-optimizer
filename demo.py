def total_value(items, max_weight):
    return  sum([x[2] for x in items]) if sum([x[1] for x in items]) <= max_weight else 0
 
cache = {}
def solve(items, max_weight):
    if not items:
        print("NOT ITEMS")
        return ()
    if (items,max_weight) not in cache:
        print("==Start==")
        print(items)
        print("Max weight: ", max_weight)
        head = items[0]
        tail = items[1:]
        include = (head,) + solve(tail, max_weight - head[1])
        dont_include = solve(tail, max_weight)
        print("Include: ", include)
        print("Don't include: ", dont_include)
        if total_value(include, max_weight) > total_value(dont_include, max_weight):
            answer = include
        else:
            answer = dont_include
        print("Answer: ", answer)
        print("items: ", items)
        print("idx: ", (items,max_weight))
        print("==End==")
        cache[(items,max_weight)] = answer
    return cache[(items,max_weight)]
 
items = (
    ("map", 4, 150), ("compass", 3, 35), ("water", 2, 200), ("sandwich", 8, 160),
    )
max_weight = 10
 
solution = solve(items, max_weight)
print("items:")
for x in solution:
    print(x[0])
print("value:", total_value(solution, max_weight))
print("weight:", sum([x[1] for x in solution]))