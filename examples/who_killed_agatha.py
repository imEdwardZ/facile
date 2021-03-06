# Someone in Dreadsbury Mansion killed Aunt Agatha. Agatha, the butler, and
# Charles live in Dreadsbury Mansion, and are the only ones to live there. A
# killer always hates, and is no richer than his victim. Charles hates noone
# that Agatha hates. Agatha hates everybody except the butler. The butler hates
# everyone not richer than Aunt Agatha. The butler hates everyone whom Agatha
# hates. Noone hates everyone. Who killed Agatha? 
#
# Originally from F. J. Pelletier:
#   Seventy-five problems for testing automatic theorem provers.
#   Journal of Automated Reasoning, 2: 216, 1986.

from facile import *

n = 3
agatha, butler, charles = 0, 1, 2

killer = variable(range(3))
victim = variable(range(3))

# flattened
hates  = array(Variable.binary() for i in range(n) for j in range(n))
richer = array(Variable.binary() for i in range(n) for j in range(n))

# Agatha, the butler, and Charles live in Dreadsbury Mansion, and
# are the only ones to live there.

# A killer always hates, and is no richer than his victim.
constraint(hates[killer*n + victim] == 1)
constraint(richer[killer*n + victim] == 0)

# No one is richer than him-/herself
for i in range(n):
    constraint(richer[i*n + i] == 0)

# (contd...) if i is richer than j then j is not richer than i
#  (i != j) => (richer[i,j] = 1) <=> (richer[j, i] = 0),
for i in range(n):
    for j in range(n):
        if i != j:
            constraint((richer[i*n + j] == 1) == (richer[j*n + i] == 0))

# Charles hates noone that Agatha hates.
#  (hates[agatha, i] = 1) => (hates[charles, i] = 0),
for i in range(n):
    constraint((hates[agatha*n + i] == 1) <= (hates[charles*n + i] == 0))

# Agatha hates everybody except the butler.
constraint(hates[agatha*n + charles] == 1)
constraint(hates[agatha*n + agatha] == 1)
constraint(hates[agatha*n + butler] == 0)

# The butler hates everyone not richer than Aunt Agatha.
#   (richer[i, agatha] = 0) => (hates[butler, i] = 1),
for i in range(n):
    constraint((richer[i*n + agatha] == 0) <= (hates[butler*n + i] == 1))

# The butler hates everyone whom Agatha hates.
#   (hates[agatha, i] = 1) => (hates[butler, i] = 1),
for i in range(n):
    constraint((hates[agatha*n + i] == 1) <= (hates[butler*n + i] == 1))

# Noone hates everyone.
#   (sum j: hates[i, j]) <= 2,
for i in range(n):
    constraint(sum([hates[i*n + j] for j in range(n)]) <= 2)

# Who killed Agatha?
constraint(victim == agatha)

assert solve(list(hates) + list(richer) + [victim, killer])

msg = "{} killed Agatha."
print (msg.format(["Agatha", "The butler", "Charles"][killer.value()]))
