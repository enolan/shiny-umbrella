import json
import socket
import time
from threading import *
from uuid import uuid4

import natlink
from natlinkutils import GrammarBase

from natlinkmgr import NatLinkMgr
import RPC

with NatLinkMgr() as mgr:

    rpc_sock = socket.create_connection(("10.0.2.2", 43238))

    def getAllWords(resObj):
        choices = []
        n = 0
        while True:
            try:
                choices.append(resObj.getWords(n))
            except natlink.OutOfRange:
                return choices
            n += 1

    class PastUtterances(object):
        def __init__(self):
            self.utterancesByUUID = {}
            self.ringBufferIdx = 0
            self.ringBufferMaxSize = 10
            self.ringBuffer = []

        def add(self, uuid, resObj):
            self.utterancesByUUID[uuid] = resObj
            if len(self.ringBuffer) == self.ringBufferMaxSize:
                del self.utterancesByUUID[self.ringBuffer[self.ringBufferIdx]]
                self.ringBuffer[self.ringBufferIdx] = uuid
            else:
                self.ringBuffer.append(uuid)
            self.ringBufferIdx += 1
            if self.ringBufferIdx >= self.ringBufferMaxSize:
                self.ringBufferIdx = 0
            print(
                "Added to ring buffer\nuuid buffer contents now: {}\n map contents now: {}\nBuffer size {}, idx {}".
                format(self.ringBuffer, self.utterancesByUUID,
                       len(self.ringBuffer), self.ringBufferIdx))

    pastUtterances = PastUtterances()

    # Set up a catchall grammar. The whole idea is to forward everything to the
    # server, so we don't do any processing here.
    class CatchallGrammar(GrammarBase):
        def __init__(self):
            GrammarBase.__init__(self)
            GrammarBase.load(
                self,
                """<dgndictation> imported;
               <catchall> exported = <dgndictation>;""",
                allResults=1,
                hypothesis=1)

        def gotResultsObject(self, recogType, resObj):
            print("recogType {}, choices {}".format(recogType,
                                                    getAllWords(resObj)))
            generatedId, msgDict = RPC.utterance(getAllWords(resObj))
            RPC.sendMsg(msgDict, rpc_sock)
            pastUtterances.add(generatedId, resObj)

        def gotHypothesis(self, words):
            print("hypothesis {}".format(words))

    grammar = CatchallGrammar()
    mgr.activateGrammar(grammar, "catchall", 1)

    natlink.waitForSpeech(0)
