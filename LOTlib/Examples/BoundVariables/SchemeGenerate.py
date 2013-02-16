
"""
	A LOTlib example for bound variables.
	
	This generates random scheme code with cons, cdr, and car, and evaluates it on some simple list structures. 
	No inference here--just random sampling from a grammar.
"""

from LOTlib.PCFG import PCFG
from LOTlib.Hypothesis import *

G = PCFG()

# A very simple version of lambda calculus
G.add_rule('EXPR', 'apply_', ['FUNC', 'EXPR'], 1.0)
G.add_rule('EXPR', 'x', [], 5.0)
G.add_rule('FUNC', 'lambda', ['EXPR'], 1.0, bv=['EXPR'])

G.add_rule('EXPR', 'cons_', ['EXPR', 'EXPR'], 1.0)
G.add_rule('EXPR', 'cdr_',  ['EXPR'], 1.0)
G.add_rule('EXPR', 'car_',  ['EXPR'], 1.0)

example_input = [   [], [[]], [ [], [] ], [[[]]]  ]

## Generate some and print out unique ones
seen = set()
for i in xrange(10000):
	x = G.generate('EXPR')
	
	if x not in seen:
		seen.add(x)
		print x.log_probability(), x
		f = evaluate_expression(x)
		for ei in example_input:
			print "\t", ei, " -> ", f(ei)




