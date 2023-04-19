# NL2SH dataset

NL2SH (Natural Language to Semantic Hypergraph) dataset can be used to build and evaluate methods for knowledge extraction and representation based on a semantic hypergraph. Each sentence has natural language annotations and dedicated semantic hyperedge.

## 1. Sentence sources

Majority of the sentences used in this dataset are taken from the following sources:

* John Eastwood, Oxford Guide to English Grammar, Oxford University Press, 2002.
* Andrew Redford, An Introduction to English Sentence Structure, Cambridge University Press, 2009.
* Essential English Grammar, Philip Gucker, Dover Publications, Inc. New York, 1966


## 2. Annotations

Annotations will be depicted on a sentence "`Tom says that his feet hurt.`" from the NL2SH dataset in the example below.

```
# sent_i = 567
# sent = Tom says that his feet hurt.
# hyperedge = (says/Pd.sr:01:01.|f--3s:0123 tom/Cp..s.p (that/T (hurt/P.s:1:0.<pf:1 ((+/Jc.rm.rp his/Mp tom/Cp..s.p) feet/Cc..p))))
# hyperedge builder = (567.1/Pd.sr:01:01.|f--3s:0123 567.0/Cp..s.p (567.2/T (567.5/P.s:1:0.<pf:1 ((+/Jc.rm.rp 567.3/Mp 567.0/Cp..s.p) 567.4/Cc..p))))
# fields = sent_i tok_i words spaces lemmas pos tags deps heads ner roleset srl1 srl2 coref1 synset atoms
567 0 Tom  + Tom  PROPN NNP  nsubj 1 B-PERSON -       B-ARG0 -      B-MAIN0 -          tom/Cp..s.p
567 1 says + say  VERB  VBZ  ROOT  1 -        say.01  B-V    -      -       state.v.01 says/Pd.sr:01:01.|f--3s:0123
567 2 that + that SCONJ IN   mark  5 -        -       B-ARG1 -      -       -          that/T
567 3 his  + his  PRON  PRP$ poss  4 -        -       I-ARG1 B-ARG1 B-REF0  -          his/Mp
567 4 feet + foot NOUN  NNS  nsubj 5 -        -       I-ARG1 I-ARG1 -       foot.n.01  feet/Cc..p
567 5 hurt - hurt VERB  VBN  ccomp 1 -        hurt.02 I-ARG1 B-V    -       ache.v.03  hurt/P.s:1:0.<pf:1
567 6 .    - .    PUNCT .    punct 1 -        -       -      -      -       -          -
```

There are three types of lines:
* word lines containing the annotation of a token in variable number of fields separated by space characters.
* blank lines marking the sentence boundaries.
* comment lines starting with hash symbol (`#`).

Comment lines contain additional information:
* `# sent_i =` id of the sentence
* `# sent =` text of the sentence
* `# hyperedge =` hyperedge of the sentence where atom labels are words
* `# hyperedge builder =` hyperedge of the sentence where atom labels are reference to the tokens
* `# fields =` list of fields used for token annotation

Comment lines are important since they contain semantic hyperedge of the sentence.

### 2.1. NLP annotations
```
sent_i tok_i word space lemma pos   tag  dep   head ner      roleset srl1   srl2   coref1  synset     
------ ----- ---- ----- ----- ----- ---  ----- ---- -------- ------- ------ ------ ------- ---------- 
567    0     Tom  +     Tom   PROPN NNP  nsubj 1    B-PERSON -       B-ARG0 -      B-MAIN0 -          
567    1     says +     say   VERB  VBZ  ROOT  1    -        say.01  B-V    -      -       state.v.01 
567    2     that +     that  SCONJ IN   mark  5    -        -       B-ARG1 -      -       -          
567    3     his  +     his   PRON  PRP$ poss  4    -        -       I-ARG1 B-ARG1 B-REF0  -          
567    4     feet +     foot  NOUN  NNS  nsubj 5    -        -       I-ARG1 I-ARG1 -       foot.n.01  
567    5     hurt -     hurt  VERB  VBN  ccomp 1    -        hurt.02 I-ARG1 B-V    -       ache.v.03  
567    6     .    -     .     PUNCT .    punct 1    -        -       -      -      -       -          
```

* `sent_i` - id of the sentence
* `tok_i` - id of the token in the sentence
* `word` - token text
* `space` - does space follows the token (+ yes, - no)
* `lemma` - lemma of the token
* `pos` - Universal POS tags (https://universaldependencies.org/u/pos/)
* `tag` - Penn Treebank tags (https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
* `dep` - ClearNLP depedency labels (https://github.com/clir/clearnlp-guidelines/blob/master/md/specifications/dependency_labels.md)
* `head` - id of the token which is a dependency head of the current token
* `ner` - named entities (https://catalog.ldc.upenn.edu/docs/LDC2013T19/OntoNotes-Release-5.0.pdf)
* `roleset` - roleset of a verb frame (https://propbank.github.io/v3.4.0/frames/)
* `srl` - semantic role labels with IOB annotation (https://verbs.colorado.edu/propbank/EPB-Annotation-Guidelines.pdf)
* `coref` - coreference labels with IOB annotation 
* `synset` - WordNet's synsets (https://wordnet.princeton.edu)

The coreference labels consist of MAIN and REF, which are supplemented with numbers to differentiate multiple main and referent tokens. For instance, `REF1` pertains to `MAIN1`, and `REF3` pertains to `MAIN3`.

`srl` and `coref` are fields which can have multiple values per token. In our example, there are two SRL fields `srl1` and `srl2` where the former contains arguments of the verb `says`, while the latter contains arguments of the verb `hurt`.


### 2.2. Semantic hypergraph annotations

The annotations for semantic hypergraph elements primarily adhere to the annotation guidelines of the Graphbrain project (https://graphbrain.net/manual/notation.html). As the initial semantic hypergraph annotation encompasses part-of-speech and dependency annotations, our annotation expansion incorporates named entities, semantic roles, and semantic protoroles.

Atom annotations are going to be described on the following examples of semantic hyperedges.

```
(says/Pd.sr:01:01.|f--3s:0123 
  tom/Cp..s.p 
  (that/T (hurt/P.s:1:0.<pf:1 
            ((+/Jc.rm.rp his/Mp tom/Cp..s.p) feet/Cc..p))))
```

```
(stayed/Pd.sx:1t:1t.<f:123 
  (+/Jr.ma (the/Md.< man/Cc..s) 
           (came/P.-sx:114:11g.<f:1234 
             (the/Md.< man/Cc..s) 
             who/Cw 
             (to/T dinner/Cc..s))) 
  (for/Tt (several/Ma.<..d months/Cc..p.d)))
```

```
(goes/Pd.s?x:0t4:1tg.|f--3s:0134 
  (+/Ba.ma.c george/Cp..s.p 
             (+/Jc.rm.cp (my/Mp neighbour/Cc..s) 
                         george/Cp..s.p) 
  often/M 
  (to/T (the/Md.< races/Cc..p))))
```

#### 2.2.1. Atom annotations

Generally, an atom has the following parts:
1. label,
2. type and optional subtype,
3. type specific atom roles,
4. type specific additional information,
5. named entity 

The label and type are mandatory, whereas the other parts can be omitted. 
The label and type are separated by `/`, while remaining parts are dot-separated (`.`). 
Roles and additional information may contain subparts, which are separated by colons (`:`).


**Predicate atom** `says/Pd.sr:01:01.|f--3s:0123` has:
1. `says` - label
2. `Pd` - type and subtype
3. `sr:01:01` - roles derived from:
  * `sr` - dependency based roles
  * `01` - semantic roles
  * `01` - semantic protoroles
4. `f--3s:0123` - additional information containing
  * `f--3s` - morphological annotation (defined in Graphbrain project)
  * `0123`- all the srl labels for the roleset of the predicate
5. ` ` - no named entity

Dependency based roles, semantic roles and/or semantic protoroles can have empty label (`-`) which means that argument has no role label for the specific labeling scheme. For example, atom `came/P.-sx:114:11g.<f:1234` has empty dependency based role, while its semantic role and protorole are `1`.

**Dependency based roles** can be

|   | dependency    |   | dependency    |
|---|---------------|---|---------------|
|`s`| nsubj         |`o`| prt           |
|`s`| csubj         |`o`| oprd          |
|`p`| nsubjpass     |`i`| dative        |
|`p`| csubjpass     |`x`| advcl         |
|`e`| expl          |`x`| prep          |
|`a`| agent         |`x`| npadvmod      |
|`c`| acomp         |`t`| parataxis     |
|`c`| attr          |`j`| intj          |
|`o`| dobj          |`r`| xcomp         |
|`o`| pobj          |`r`| ccomp         |


**Semantic roles** can be

|   | semantic roles |   | semantic roles |
|---|----------------|---|----------------|
|`0`| ARG0           |`e`| ARGM-EXT       |
|`1`| ARG1           |`g`| ARGM-GOL       |
|`2`| ARG2           |`l`| ARGM-LOC       |
|`3`| ARG3           |`b`| ARGM-LVB       |
|`4`| ARG4           |`m`| ARGM-MNR       |
|`5`| ARG5           |`f`| ARGM-MOD       |
|`6`| ARG6           |`n`| ARGM-NEG       |
|`a`| ARGM-ADJ       |`p`| ARGM-PNC       |
|`r`| ARGM-ADV       |`h`| ARGM-PRD       |
|`c`| ARGM-CAU       |`i`| ARGM-PRP       |
|`o`| ARGM-COM       |`k`| ARGM-PRR       |
|`d`| ARGM-DIR       |`v`| ARGM-V         |
|`s`| ARGM-DIS       |`t`| ARGM-TMP       |

**Semantic protoroles** are derived from semantic roles of the specific verb's roleset.
For example, `hurt/P.s:1:0` has `1` as semantic role and `0` as semantic protorole since roleset `hurt.02` maps
`ARG1` to `PAG`. Below are semantic protoroles used.

|   | semantic protoroles |   | semantic protoroles |
|---|---------------------|---|---------------------|
|`0`| PAG                 |`e`| EXT                 |
|`1`| PPT                 |`c`| CAU                 |
|`g`| GOL                 |`o`| COM                 |
|`h`| PRD                 |`i`| PRP                 |
|`m`| MNR                 |`t`| TMP                 |
|`d`| DIR                 |`r`| ADV                 |
|`l`| LOC                 |`j`| ADJ                 |
|`q`| VSP                 |`u`| REC                 |


**Concept atom** `tom/Cp..s.p` has:
1. `tom` - label
2. `Cp` - type and subtype
3. ` ` - no roles
4. `s` - additional info (defined in Graphbrain project)
5. `p` - named entity


**Named entity** labels used are:

|   | named entity |   | named entity |
|---|--------------|---|--------------|
|`c`| CARDINAL     |`n`| NORP         |
|`d`| DATE         |`#`| ORDINAL      |
|`e`| EVENT        |`o`| ORG          |
|`f`| FAC          |`%`| PERCENT      |
|`g`| GPE          |`p`| PERSON       |
|`u`| LANGUAGE     |`r`| PRODUCT      |
|`w`| LAW          |`q`| QUANTITY     |
|`l`| LOC          |`t`| TIME         |
|`$`| MONEY        |`a`| WORK_OF_ART  |

**Modifier atom** `several/Ma.<..d` in a phrase `several months` has role `<` which means that word `several` comes before word `months`. The opposite role is `>`.

#### 2.2.2. Special atoms

Special atoms below come predefined and are often very useful:


| Atom        | Purpose          | Example                                                                  |
| ----------- | -----------------|--------------------------------------------------------------------------|
| `+/Jr`      | Relative clauses | `(+/Jr.ma (the/M man/C) (came/P (the/M man/C) who/Cw (to/T dinner/Cc)))` |
| `+/Jc`      | Coreferences     | `(+/Jc.rm his/Mp tom/Cp)`                                                |
| `+/Ba`      | Appositions      | `(+/Ba.ma george/Cp (my/Mp neighbour/Cc))`                               |

Special atom for coreference has the following roles: 

|   | coreference roles |
|---|-------------------|
|`m`| main              |
|`r`| reference         |

In the hyperedge `(+/Jc.rm.rp his/Mp tom/Cp..s.p)` atom `his/Mp` refers (reference role) to an antecedent `tom/Cp..s.p` (main role).

Additionally, it can have the following coreference information as well.

|   | coreference additional information |
|---|------------------------------------|
|`p`| proper noun                        |
|`r`| pronoun                            |
|`c`| noun                               |

Therefore, it is evident that atom `his/Mp` came from a pronoun, while `tom/Cp..s.p` came from a proper noun.

Special atom for apposition can have the following additional information.

|   | apposition additional information |
|---|-----------------------------------|
|`q`| quote - restrictive               |
|`b`| bracket - not restrictive         |
|`c`| comma - not restrictive           |

These arguments depict how the appositive is connected with a main phrase. It can be in quotes, bracket or comma separated.

## 3. Statistics

If we look at the annotation of the sentence: "`Tom says that his feet hurt.`" there are:
* 7 tokens: `Tom`, `says`, `that`, `his`, `feet`, `hurts`, `.`
* 6 words: `Tom`, `says`, `that`, `his`, `feet`, `hurts`
* 1 clause: `Tom says that his feet hurt`,
* 1 named entity: `Tom` as person,
* 1 coreference: `his` refers to `Tom`
* 6 atoms: 
  * `tom/Cp..s.p`, 
  * `says/Pd.sr:01:01.|f--3s:0123`, 
  * `that/T`, 
  * `his/Mp`, 
  * `feet/Cc..p`, 
  * `hurt/P.s:1:0.<pf:1`
* 5 subedges
  * `(says/Pd.sr:01:01.|f--3s:0123 tom/Cp..s.p (that/T (hurt/P.s:1:0.<pf:1 ((+/Jc.rm.rp his/Mp tom/Cp..s.p) feet/Cc..p))))`
  * `(that/T (hurt/P.s:1:0.<pf:1 ((+/Jc.rm.rp his/Mp tom/Cp..s.p) feet/Cc..p)))`
  * `(hurt/P.s:1:0.<pf:1 ((+/Jc.rm.rp his/Mp tom/Cp..s.p) feet/Cc..p))`
  * `((+/Jc.rm.rp his/Mp tom/Cp..s.p) feet/Cc..p)`
  * `(+/Jc.rm.rp his/Mp tom/Cp..s.p)`

The statistics for the entire NL2SH dataset are presented in the table below.


|                           | count | average |
|---------------------------|------:|--------:|
| Sentences                 |   664 |         |
| Tokens                    |  6851 |   10.32 |
| Words                     |  5968 |    8.99 |
| Clause                    |  1267 |    1.91 |
| Named entities            |   254 |    0.38 |
| Coreference (refers)      |   200 |    0.30 |
| Coreference (antecedents) |   179 |    0.27 |
| Atoms                     |  7082 |   10.67 |
| Subedges                  |  4317 |    6.50 |