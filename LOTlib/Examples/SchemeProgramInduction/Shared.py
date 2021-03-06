from LOTlib.Grammar import Grammar
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.DataAndObjects import FunctionData
from LOTlib.Inference.MetropolisHastings import mh_sample
from math import log

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# A simple grammar for scheme, including lambda

G = Grammar()

# A very simple version of lambda calculus
G.add_rule('START', '', ['EXPR'], 1.0)
G.add_rule('EXPR', 'apply_', ['FUNC', 'EXPR'], 1.0)
G.add_rule('EXPR', 'x', None, 5.0)
G.add_rule('FUNC', 'lambda', ['EXPR'], 1.0, bv_type='EXPR', bv_args=None)

G.add_rule('EXPR', 'cons_', ['EXPR', 'EXPR'], 1.0)
G.add_rule('EXPR', 'cdr_',  ['EXPR'], 1.0)
G.add_rule('EXPR', 'car_',  ['EXPR'], 1.0)

G.add_rule('EXPR', '[]',  None, 1.0)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# A class for scheme hypotheses that just computes the input/output pairs with the appropriate probability
class SchemeFunction(LOTHypothesis):
	
	# Prior, proposals, __init__ are all inherited from LOTHypothesis
	
	def compute_single_likelihood(self, datum, response):
		# We'll just use a string comparison on outputs here, for ease
		if str(response) == str(datum.output):  
			return log(self.ALPHA)
		else:                       
			return log(1.0-self.ALPHA)
			
