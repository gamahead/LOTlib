"""
	TODO: Split up likelihood so that decayed versions are separate
"""

import numpy
from copy import copy, deepcopy
import LOTlib
from LOTlib.Miscellaneous import *


class Hypothesis(object):
	"""
		A hypothesis is bundles together a value (hypothesis value) with a bunch of remember state, like posterior_score, prior, likelihood
		This class is typically a superclass of the thing you really want.
		
		Temperatures:
			A Hypothesis defaulty has a prior_temperature and likelihood_temperature. These are taken into account in setting the 
			posterior_score (for computer_prior and compute_likelihood), in the values returned by these, AND in the stored values
			under self.prior and self.likelihood
	"""
	
	def __init__(self, value=None, prior_temperature=1.0, likelihood_temperature=1.0):
		
		self.set_value(value) # to zero out prior, likelhood, posterior_score
		self.prior, self.likelihood, self.posterior_score = [-Infinity, -Infinity, -Infinity] 
		self.prior_temperature=prior_temperature
		self.likelihood_temperature=likelihood_temperature		
		self.stored_likelihood = None
		
		# keep track of some calls (Global variable)
		POSTERIOR_CALL_COUNTER = 0
	
	def set_value(self, value): 
		""" Sets the (self.)value of this hypothesis to value"""
		self.value = value
		
	def __copy__(self):
		""" Returns a copy of myself by calling copy() on self.value """
		return Hypothesis(value=self.value.copy())
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# All instances of this must implement these:
		
	def compute_prior(self):
		""" computes the prior and stores it in self.prior"""
		assert False, "*** Must implement compute_prior"

	def compute_single_likelihood(self, datum):
		assert False, "*** Must implement compute_single_likelihood"
	
	# And the main likelihood function just maps compute_single_likelihood over the data
	def compute_likelihood(self, data):
		""" 
		Compute the likelihood of the *array* d, with the specified likelihood decay
		This also stores the *undecayed* non-culmulative likelihood of each data point in self.stored_likelihood
		"""
		self.likelihood = sum(map( self.compute_single_likelihood, data))/self.likelihood_temperature
		
		self.posterior_score = self.prior + self.likelihood
		return self.likelihood
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Methods for accessing likelihoods etc. on a big arrays of data
		
	def propose(self): 
		""" Generic proposal used by MCMC methods"""
		assert False,  "*** Must implement propose"
	
	# this updates last_prior and last_likelihood
	def compute_posterior(self, d):
		LOTlib.BasicPrimitives.LOCAL_PRIMITIVE_OPS = 0 # Reset this
		p = self.compute_prior()
		l = self.compute_likelihood(d)
		self.posterior_score = p+l
		return [p,l]
		
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# optional implementation
	# if you do gibbs sampling you need:
	def enumerative_proposer(self): pass
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	## These are just handy:
	def __str__(self):
		return str(self.value)
	def __repr__(self): return str(self)
		
	# for hashing hypotheses
	def __hash__(self): return hash(self.value)
	def __cmp__(self, x): return cmp(self.value,x)
	
	# this is for heapq algorithm in FiniteSample, which uses <= instead of cmp
	# since python implements a "min heap" we can compar elog probs
	def __le__(self, x):     return (self.posterior_score <= x.posterior_score)
	def __eq__(self, other): return (self.value.__eq__(other.value))
	def __ne__(self, other): return (self.value.__ne__(other.value))


