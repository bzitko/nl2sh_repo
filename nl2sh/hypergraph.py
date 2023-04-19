import re

class Atom(str):

    __slots__ = ("label", "type", "roles", "morph", "ent")

    __str2atom__ = (("%", "%25"), ("/", "%2f"), (" ", "%20"), ("(", "%28"), (")", "%29"), (".", "%2e"), ("*", "%2a"), ("&", "%26"), ("@", "%40"))

    def __new__(cls, *args, **kwargs):
        txt = args[0].rstrip(". ")
        self = super().__new__(cls, txt)

        parts = txt.split("/")
        label = parts[0]
        fillers = [label]
        parts = "" if len(parts) == 1 else parts[1]
        fillers += parts.split(".")
        fillers += [""] * (len(self.__slots__) - len(fillers))

        for s, f in zip(self.__slots__, fillers):
            setattr(self, s, f)

        return self

    @classmethod
    def _encode(cls, txt):
        for k, v in cls.__str2atom__:
            txt = txt.replace(k, v)
        return txt

    @classmethod
    def _decode(cls, txt):
        for k, v in cls.__str2atom__:
            txt = txt.replace(v, k)
        return txt

    @property
    def text(self):
        return self._decode(self.label)

    def is_atom(self):
        return True

    def __len__(self):
        return 0

    def __repr__(self):
        return self

    def simplify(self, type=True, roles=False, morph=False, ent=False):
        txt = self.label
        if type or roles or morph or ent:
            txt += "/"
        parts = [self.type if type else "",
                 self.roles if roles else "",
                 self.morph if morph else "",
                 self.ent if ent else ""]
        parts = ".".join(parts)
        parts = parts.rstrip(" .")
        txt += parts
        return Atom(txt)

    def atoms(self):
        yield self

    def subedges(self):
        yield self


class Edge(tuple):

    def is_atom(self):
        return False

    def __repr__(self):
        return "(" + " ".join(repr(item) for item in self) + ")"

    def simplify(self, type=True, roles=False, morph=False, ent=False):
        return Edge(item.simplify(type, roles, morph, ent) for item in self)

    def atoms(self):
        for item in self:
            if item.is_atom():
                yield item
            else:
                yield from item.atoms()

    def subedges(self):
        yield self
        if not self.is_atom():
            for item in self:
                yield from item.subedges()


    @staticmethod
    def parse(txt):
        # cleaning
        txt = re.sub(r" {2,}", " ", txt.strip())

        # tokenization
        tokens = []
        atom = ""
        for item in txt + " ":
            if item in "()":
                if atom:
                    tokens.append(atom)
                    atom = ""
                tokens.append(item)
            elif item == " ":
                if atom:
                    tokens.append(atom)
                    atom = ""
            else:
                atom += item

        # parsing
        i = 0  # token
        c = 0  # open parenthees counter
        stack = {} # for storing edges

        while i < len(tokens):
            t = tokens[i]  # token
            if t == "(":
                c += 1
                stack[c] = []
            elif t == ")":
                edge = Edge(stack.pop(c))
                if c > 1:
                    stack[c - 1].append(edge)
                else:
                    return edge
                c -= 1
            else:
                if c == 0:
                    return Atom(t)
                else:
                    stack[c].append(Atom(t))
            i += 1
