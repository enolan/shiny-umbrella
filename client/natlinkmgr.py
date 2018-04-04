import natlink


class NatLinkMgr(object):
    def __init__(self):
        self.grammars = []

    def __enter__(self):
        natlink.natConnect(True)
        return self

    def __exit__(self, exType, exValue, traceback):
        for g in self.grammars:
            g.unload()
        natlink.natDisconnect()

    def activateGrammar(self, grammar, ruleName, exclusive):
        self.grammars.append(grammar)
        grammar.activate(ruleName, exclusive=exclusive)
