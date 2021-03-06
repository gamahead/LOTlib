from LOTHypothesis import LOTHypothesis
from LOTlib.Miscellaneous import *
from copy import copy, deepcopy

class GaussianLOTHypothesis(LOTHypothesis):
	"""
		Like LOTHypothesis but has a Gaussian likelihood
	"""
	
	def __init__(self, G, value=None, f=None, prior_temperature=1.0, proposal_function=None): 
		self.__dict__.update(locals()) # must come first or else proposal_function is overwritten
		LOTHypothesis.__init__(self, G, value=value, f=f, proposal_function=proposal_function)
		
		
	def compute_single_likelihood(self, datum, response):
		""" Compute the likelihood with a Gaussian"""
		return normlogpdf(response, datum.output, datum.ll_sd)