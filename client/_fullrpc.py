# Script that should be placed in: C:\NatLink\NatLink\MacroSystem\ so it will
# be picked up by NatLink

from natlink import OutOfRange
from natlinkutils import GrammarBase

def getAllWords(resObj):
  choices = []
  n = 0
  while True:
    try:
      choices.append(resObj.getWords(n))
    except OutOfRange:
      return choices
    n += 1

# Set up a catchall grammar. The whole idea is to forward everything to the
# server, so we don't do any processing here.
class CatchallGrammar(GrammarBase):
  def __init__(self):
    GrammarBase.__init__(self)
    GrammarBase.load(self,
	                 """<dgndictation> imported;
                         <catchall> exported = <dgndictation>;""",
					 allResults=1,
           hypothesis=1)

  def gotResultsObject(self, recogType, resObj):
    print(type(resObj))
    print("recogType {}, choices {}".format(recogType, getAllWords(resObj)))

  def gotHypothesis(self, words):
    print("hypothesis {}".format(words))

grammar = CatchallGrammar()
grammar.activate("catchall", exclusive=1)

def unload():
  grammar.unload()
