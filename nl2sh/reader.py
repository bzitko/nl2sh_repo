import re
from collections import namedtuple
from .language import Token, Span, Sent, Doc
from .hypergraph import Edge

ColumnInfo = namedtuple("ColumnInfo", "i, name, type, calc_size, to_txt")
COLUMN_DATA = {"sent_i": (0, "", int, lambda sent: 1, 
                          None),
               "tok_i":  (1, "", int, lambda sent: 1, 
                          lambda tok: [str(tok.i - tok.sent.start)]),
               "words":  (2, "orth_", str, lambda sent: 1, 
                          lambda tok: [tok.orth_ if tok.orth_.strip() else "\ "]),
               "spaces": (3, "whitespace_", str, lambda sent: 1, 
                          lambda tok: ["+" if tok.whitespace_ == " " else "-"]),
               "lemmas": (4, "lemma_", str, lambda sent: 1, 
                          lambda tok: [tok.lemma_ if tok.lemma_.strip() else "\ "]),
               "pos":    (5, "pos_", str, lambda sent: 1, 
                          lambda tok: [tok.pos_]),
               "tags":   (6, "tag_", str, lambda sent: 1, 
                          lambda tok: [tok.tag_]),
               "deps":   (7, "dep_", str, lambda sent: 1, 
                          lambda tok: [tok.dep_]),
               "heads":  (8, "head.i", int, lambda sent: 1, 
                          lambda tok: [str(tok.head.i - tok.sent.start)]),
               "ner":    (9, "ent", str, lambda sent: 1, 
                          lambda tok: [f"{tok.ent_iob_}-{tok.ent_type_}" if tok.ent_type else "-"]),
               "roleset": (10, "_.roleset", str, lambda sent: 1, 
                           lambda tok: [tok._.roleset or "-"]),
               "srl":     (11, "_.srl", str, lambda sent: len(sent._.srl), 
                           lambda tok: [tok._.srl[v] if tok._.srl[v] != "O" else "-" for v in sorted(tok._.srl)]),
               "coref":   (12, "_.coref", str, lambda sent: len(sent._.coref), 
                           lambda tok: [item if item != "O" else "-" for item in tok._.coref]),
               "synset":  (13, "_.synset", str, lambda sent: 1, 
                           lambda tok: [tok._.synset if tok._.synset else "-"]),
               "atoms":    (14, "_.atom", str, lambda sent: 1,
                           lambda tok: [str(tok._.atom) if tok._.atom else "-"])}

COLUMN_DATA = {col: ColumnInfo(*item) for col, item in COLUMN_DATA.items()}

REGEXS = {"ner": r"[BI]-(CARDINAL|DATE|EVENT|FAC|GPE|LANGUAGE|LAW|LOC|MONEY|NORP|ORDINAL|ORG|PERCENT|PERSON|PRODUCT|QUANTITY|TIME|WORK_OF_ART)",
          "roleset": r"\w+\.\d\d",
          "srl": r"[BI](-[RC])?-(ARG0|ARG1|ARG2|ARG3|ARG4|ARG5|ARG6|ARGM-ADJ|ARGM-ADV|ARGM-CAU|ARGM-COM|ARGM-DIR|ARGM-DIS|ARGM-DSP|ARGM-EXT|ARGM-GOL|ARGM-LOC|ARGM-MNR|ARGM-MOD|ARGM-PNC|ARGM-PRD|ARGM-PRP|ARGM-REC|ARGM-TMP|V)",
          "coref": r"[BI]-(MAIN|REF)\d+",
          "synset": r"\w+\.\w\.\d\d",
          "atoms": r"[^/]+/.+"}

REGEXS = {k: re.compile(v) for k, v in REGEXS.items()}

def _convert_rows_to_columns(rows):
    if not rows:
        return {}
    columns = {col_i: [] for col_i in range(len(rows[0]))}

    for items in rows:
        for col_i, item in enumerate(items):
            columns[col_i].append(item) 
    return columns

def _discover_column_types(columns):
    column_type_by_i = {}
    for col_i, items in columns.items():
        for item in items:
            for name, regex in REGEXS.items():
                if regex.fullmatch(item):
                    column_type_by_i[col_i] = name
                    break    
    return column_type_by_i  

def _column_to_spans(sent_start, column):
    span_start = label = None
    spans = []
    for row_i, item in enumerate(column + ["-"]):
        if item.startswith(("B", "-")):
            if span_start is not None:
                spans.append((sent_start + span_start, sent_start + row_i, label))
            if item.startswith("B"):
                span_start = row_i
                label = item[2:]
            else:
                span_start = label = None
    return spans

def _column_to_set_ids(sent_start, column):
    set_ids = []
    for row_i, item in enumerate(column):
        if item != "-":
            set_ids.append((sent_start + row_i, item))
    return set_ids      

def txt2data(txt):
    data = {col: [] 
            for col in COLUMN_DATA 
            if COLUMN_DATA[col].name}

    rest_items = {} # key is sent_start, values are rows
    sent_start = 0
    tok_counter = 0
    for line in txt.split("\n"):
        if not line:
            continue

        if line[0] == "#":
            for cmnt in ["sent_i", "sent", "hyperedge builder", "hyperedge"]:
                if line.startswith(f"# {cmnt} = "):
                    data[cmnt] = line[len(cmnt) + 5:].strip()
                    if cmnt == "sent_i":
                        data[cmnt] = int(data[cmnt])
                    
        elif line[0].isnumeric():
            items = line.split()
            data["sent_i"] = items[0]
            if items[COLUMN_DATA["tok_i"].i] == "0":
                sent_start = tok_counter
                rest_items[sent_start] = []

            data["words"].append(items[COLUMN_DATA["words"].i])
            data["spaces"].append("+" == items[COLUMN_DATA["spaces"].i])
            data["lemmas"].append(items[COLUMN_DATA["lemmas"].i])
            data["pos"].append(items[COLUMN_DATA["pos"].i])
            data["tags"].append(items[COLUMN_DATA["tags"].i])
            data["deps"].append(items[COLUMN_DATA["deps"].i])
            data["heads"].append(sent_start + int(items[COLUMN_DATA["heads"].i]))

            rest_items[sent_start].append(items[COLUMN_DATA["heads"].i + 1:])
            tok_counter += 1

    for sent_start, rows in rest_items.items():
        columns = _convert_rows_to_columns(rows)
        column_type_by_i = _discover_column_types(columns)
        
        # extract data from columns
        for col_i in sorted(column_type_by_i):
            col_type = column_type_by_i[col_i]
            column = columns[col_i]
            if col_type in {"ner"}:
                data[col_type] = _column_to_spans(sent_start, column)
            elif col_type in {"srl", "coref"}:
                spans = _column_to_spans(sent_start, column)
                data[col_type].append(spans)
            elif col_type in {"roleset", "synset", "atoms"}:
                set_ids = _column_to_set_ids(sent_start, column)
                data[col_type] += set_ids
    return data


def data2sent(data):
    rolesets = {i: rs for i, rs in data["roleset"]}
    synsets = {i: ss for i, ss in data["synset"]}

    tokens = []
    for i in range(len(data["words"])):
        tok = Token(sent_i=data["sent_i"], 
                    i=i,
                    text=data["words"][i],
                    space=data["spaces"][i],
                    lemma=data["lemmas"][i],
                    pos=data["pos"][i],
                    tag=data["tags"][i],
                    dep=data["deps"][i],
                    head=data["heads"][i],
                    roleset=rolesets.get(i),
                    synset=synsets.get(i),)
        tokens.append(tok)
    
    for i in range(len(tokens)):
        tokens[i] = tokens[i]._replace(head=tokens[tokens[i].head])
    
    sent = Sent(tokens)

    # ner
    sent.ner = tuple(Span(sent[start:end], label)  for start, end, label in data["ner"])
        
    # srl
    for srl in data["srl"]:
        verb, spans = None, []
        for start, end, label in srl:
            span = Span(sent[start:end], label)
            if label == "V":
                verb = span
            else:
                spans.append(span)
        sent.srl[verb] = tuple(spans)

    # coref
    for coref in data["coref"]:
        main, spans = None, []
        for start, end, label in coref:
            if label.startswith("MAIN"):
                main = Span(sent[start:end], "MAIN")
            else:
                spans.append(Span(sent[start:end], "REF"))
        
        for span in spans:
            sent.coref[span] = main
            
    return sent


def read_dataset(filename):
    sents = []
    cnt = 0
    with open(filename) as fp:
        txt = ""
        for line in fp:
            if line != "\n":
                txt += line
            else:
                txt = txt.strip()
                if not txt:
                    continue
                data = txt2data(txt)
                sent = data2sent(data)
                sent.hyperedge = Edge.parse(data["hyperedge"])
                sents.append(sent)
                txt = ""
                cnt += 1

    return Doc(sents)

