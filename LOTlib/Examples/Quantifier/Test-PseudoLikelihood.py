# -*- coding: utf-8 -*-
"""
	Try a pseudolikelihood -- score just present/absent for each word, ignoring the size principle. 
	This does terribly.. you really need a full size principle likelihood. 
	
	We could probably prove that any likelihood function that does not consider alternatives will not arrive at the correct set of meanings. Any function only of the truth value, which does not include others, will fail...
	That the truth values of X are not enough to determine meaning if the subset problem is there....
"""

from Shared import *

ALPHA = 0.9
SAMPLES = 100000
DATA_SIZE = 1000

## sample the target data
data = generate_data(DATA_SIZE)

W = 'every'

# Now to use it as a StandardExpression, we need data to have an "output" field which is true/false for whether its the target word. This is then used by StandardExpression.compute_likelihood to see if we match or not with whether a word was said (ignoring the other words -- that's why its a pseudolikelihood)
for di in data: 
	di.output = (di.word == W)
	#print (di.word == W)

FBS = FiniteBestSet(max=True, N=100)

H = StandardExpression(G, args=['A', 'B', 'S'], ALPHA=ALPHA)
# Now just run the sampler with a StandardExpression
for s in LOTlib.MetropolisHastings.mh_sample(H, data, SAMPLES, skip=10):
	#print s.lp, "\t", s.prior, "\t", s.likelihood, "\n", s, "\n\n"
	FBS.push(s, s.lp)
	
for k in reversed(FBS.get_sorted()):
	print k.lp, k.prior, k.likelihood, k
	

	