from collections import namedtuple

class Token(namedtuple("Token", ["sent_i", "i", "text", "space", "lemma", "pos", "tag", "dep", "head", "roleset", "synset"])):
    
    def __repr__(self):
        return self.text

class Span(tuple):

    def __new__(cls, args, label):
        obj = super().__new__(cls, args)
        obj.label = label
        return obj
    
    def __repr__(self):
        return f"{self.label} " + "".join(tok.text + (" " if tok.space else "") for tok in self)
    
    
    @property
    def start(self):
        return self[0].i
    
    @property
    def end(self):
        return self[-1].i + 1



class Sent(tuple):

    def __new__(cls, *args):
        obj = super().__new__(cls, *args)
        obj.ner = []
        obj.srl = {}
        obj.coref = {}
        obj.hyperedge = None
        return obj

    def __repr__(self):
        return "".join(tok.text + (" " if tok.space else "") for tok in self)
    

class Doc(tuple):

    def __repr__(self):
        return "\n".join(repr(sent) for sent in self)