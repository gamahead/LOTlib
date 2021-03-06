"""
	Inference - sample from the prior (as a baseline comparison)
"""
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis

def prior_sample(h0, data, N):
	"""
		Just use the grammar and returntype of h0 to sample from the prior
		NOTE: Only implemented for LOTHypothesis
	"""
	assert isinstance(h0, LOTHypothesis)
	
	# extract from the grammar
	G = h0.grammar 
	rt = h0.value.returntype
	
	for i in xrange(N):
		if LOTlib.SIG_INTERRUPTED: break
	
		h = LOTHypothesis(G, start=rt)
		h.compute_posterior(data)
		
		yield h
		
		
if __name__ == "__main__":
	
	from LOTlib.Examples.Number.Shared import *
	
	data = generate_data(500)
	h0 = NumberExpression(G)	
	for h in prior_sample(h0, data, 10000):
		#h.revert() # undoes the craziness with the prior
		print q(get_knower_pattern(h)), h.lp, h.prior, h.likelihood, q(h)
		