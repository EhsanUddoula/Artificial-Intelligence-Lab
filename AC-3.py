from collections import deque

def ac3(csp):
    queue = deque(csp['arcs'])  # List of (Xi, Xj) pairs

    while queue:
        (Xi, Xj) = queue.popleft()
        if revise(csp, Xi, Xj):
            if not csp['domains'][Xi]:  # Empty domain ⇒ no solution
                return False
            for Xk in csp['neighbors'][Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj):
    revised = False
    for x in csp['domains'][Xi][:]:  # Iterate over copy to modify original
        if not any(csp['constraints'](Xi, x, Xj, y) for y in csp['domains'][Xj]):
            csp['domains'][Xi].remove(x)
            revised = True
    return revised

def not_equal_constraint(Xi, x, Xj, y):
    return x != y

# Example CSP
csp = {
    'domains': {
        'A': [1, 2, 3],
        'B': [1, 2, 3],
        'C': [1, 2, 3]
    },
    'arcs': [('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'B')],
    'neighbors': {
        'A': ['B'],
        'B': ['A', 'C'],
        'C': ['B']
    },
    'constraints': not_equal_constraint
}

result = ac3(csp)

print("AC-3 result:", result)
print("Reduced domains:", csp['domains'])

csp['domains']['C'] = [1]
result = ac3(csp)

print("AC-3 result:", result)
print("Reduced domains:", csp['domains'])
