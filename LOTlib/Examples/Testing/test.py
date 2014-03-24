
from LOTlib.Miscellaneous import unique
from LOTlib.Grammar import Grammar
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis

G = Grammar()

G.add_rule('START','',['String'],1.0)

G.add_rule('String','One',['Number'],1.0)
G.add_rule('String','Two',['Number','Number'],1.0)
G.add_rule('String','Three',['Number','Number','Number'],1.0)

G.add_rule('Number','1','i',1.0)
G.add_rule('Number','2','ii',1.0)
G.add_rule('Number','3','iii',1.0)


for i in xrange(100):
	print G.generate()

