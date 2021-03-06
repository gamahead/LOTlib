
from LOTlib.Examples.Number.Shared import *

TARGET_FILE = "tmp-hypotheses.pkl" # load a small file. The large one is only necessary if we want the "correct" target likelihood and top N numbers; if we just look at Z we don't need it!
DATA_FILE = "data/evaluation-data.pkl"

TARGET_SAMPLES = 500
DATA_SIZE = 300

# make and save the data
data = generate_data(DATA_SIZE)
pickle_save(data, DATA_FILE)

initial_hyp = NumberExpression(G)

q = FiniteBestSet(10000)
for h in LOTlib.Inference.MetropolisHastings.mh_sample(initial_hyp, data, TARGET_SAMPLES, skip=0):
	q.add(h, h.lp)

q.save(TARGET_FILE)