import LOTlib

from MetropolisHastings import mh_sample

from copy import copy
from random import randint, random
from math import exp
from random import random

#def temperature_ladder(min=1.0,max=1.5,steps=5,log=True)


# This staircases, so that each temperature is swapped with the one directly above
# skipping skips within each level!
def parallel_tempering_sample(inh, data, steps, proposer=None, within_steps=10, temperatures=(1.0,1.1,1.2,1.3,1.4), swaps=1, yield_all=False):
	"""
		If we yeild all, we yield everything from every step of every chain
	"""
	
	# a bunch of hypotheses, one for each temperature
	samples = map(copy, [ inh ] * len(temperatures) )
	
	for mhi in xrange(steps):
		
		for i in xrange(len(temperatures)):
			
			# update this sample
			for s in mh_sample(samples[i], data, within_steps, proposer=proposer, skip=0, temperature=temperatures[i]):
				if yield_all: yield s
				samples[i] = s # should only be called once, since we skip within step 
		
		for sw in xrange(swaps):
			frm = randint(0, len(temperatures)-2)
			
			# get the joint probability -- since temperature is only on the likelihood, everything cancels
			r = (samples[frm].lp) / temperatures[frm+1] + (samples[frm+1].lp) / temperatures[frm] - (samples[frm].lp) / temperatures[frm] + (samples[frm+1].lp) / temperatures[frm+1]
			
			if r>0 or random() < exp(r):
				samples[frm], samples[frm+1] = samples[frm+1], samples[frm]
		
		yield samples[0] # give from the lowest chain
		if LOTlib.SIG_INTERRUPTED: break
