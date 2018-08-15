import spacy
import random
import annoy
import string
from wordfilter import Wordfilter
from itertools import islice

from spacy.lang.en.stop_words import STOP_WORDS as stop_words
wf = Wordfilter()


def prepare_nlp():
    nlp = spacy.load('en_core_web_md') # or en_core_web_md
    qualified = [item for item in nlp.vocab if item.has_vector and item.is_alpha]

    lexmap = []
    t = annoy.AnnoyIndex(300)
    for i, item in enumerate(islice(sorted(qualified, key=lambda x: x.prob, reverse=True), 100000)):
        t.add_item(i, item.vector)
        lexmap.append(item)
    t.build(25)

    p = annoy.AnnoyIndex(50)
    phonmap = []
    phonlookup = {}

    for i, line in enumerate(open("./cmudict-0.7b-simvecs")):
        word, vec_raw = line.split("  ")
        word = word.lower().rstrip("(0123)")
        vec = [float(v) for v in vec_raw.split()]
        p.add_item(i, vec)
        phonmap.append(word)
        phonlookup[word] = vec
    p.build(25)


    return nlp, lexmap, phonmap, phonlookup, t, p

def similarsemantic(t, nlp, word, n, lexmap):
    seen = set()
    count = 0
    for i in t.get_nns_by_vector(nlp.vocab[word].vector, 100):
        this_word = lexmap[i].orth_.lower()
        if this_word not in seen and word != this_word:
            seen.add(this_word)
            count += 1
            yield this_word
            if count >= n:
                break

def similarphonetic(phonlookup, phonmap, t, word, n):
    count = 0
    if word not in phonlookup:
        return
    for i in t.get_nns_by_vector(phonlookup[word], 100):
        if word != phonmap[i] and not(wf.blacklisted(phonmap[i])):
            count += 1
            yield phonmap[i]
            if count >= n:
                break

def phonwalk(phonlookup, phonmap, p, current=None):
    seen = set()
    if current is None:
        current = random.choice(list(phonlookup.keys()))

    current = current.rstrip(string.punctuation)
    try:
        seen.add(tuple(phonlookup[current]))
        while True:
            selected = [s for s in similarphonetic(phonlookup, phonmap, p, current, 100) \
                        if tuple(phonlookup[s]) not in seen and len(s) in [7, 8, 9]][0]
            yield selected
            seen.add(tuple(phonlookup[selected]))
            current = selected
    except GeneratorExit:
        return
    except:
        while True:
            yield current


def semanticwalk(nlp, lexmap, t, current=None):
    seen = set()
    if current is None:
        current = nlp.vocab[random.choice(lexmap).text].text

    current = current.rstrip(string.punctuation)
    seen.add(current)
    while True:
        selected = [s for s in similarsemantic(t, nlp, current, 100, lexmap) if s not in seen][0]
        yield selected
        seen.add(selected)
        current = selected

def donothing(word):
    while True:
        yield word

def sentencewalk(sentence, nlp, lexmap, phonmap, phonlookup, t, p, nwalks):
    sentence = sentence.split(" ")

    arr = []
    for i, word in enumerate(sentence):
        if word in stop_words:
            arr.append(donothing(word))
        elif i % 2 == 0:
            arr.append(semanticwalk(nlp, lexmap, t, current=word))
        else:
            arr.append(phonwalk(phonlookup, phonmap, p, current=word))

    sentences_arr = []
    for i in range(nwalks):
        final = " ".join([next(f) for f in arr])+"."
        sentences_arr.append(final)

    return sentences_arr
