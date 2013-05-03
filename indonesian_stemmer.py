#!/usr/bin/env python

import os
import random
import pprint
import time
import re
import sys

opsi = {
	'SORT_INSTANCE'	: False, #sort by number of instances
	'NO_NO_MATCH'	: False, #hide no match entry
	'NO_DIGIT_ONLY'	: True,  #hide digit only
	'STRICT_CONFIX'	: False, #use strict disallowed_confixes rules
}


fp  = open('./kamus.txt')
dic = fp.readlines()
fp.close()
dicti = {}
for i in dic:
    attrib = i.lower().split('\t')
    key    = attrib[1].replace(' ','').rstrip(' \t\n\r')
    dicti[key] = { 'class': attrib[0], 'lemma': attrib[1].rstrip(' \t\n\r')}

# Define rules
VOWEL = 'a|i|u|e|o' #vowels
CONSONANT = 'b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z' #consonants
ANY = VOWEL + '|' + CONSONANT #any characters

rules = {
    'affixes': (  
        (1,('kah','lah', 'tah', 'pun')),
        (1,('mu','ku', 'nya')),
        (0,('ku','kau')),
        (1,('i','kan', 'an'))
        ),
    'prefixes': (  
		[0, "(di|ke|se)("+ANY+")(.+)", ""], # 0
		[0, "(ber|ter)("+ANY+")(.+)", ""], # 1, 6 normal
		[0, "(be|te)(r)("+VOWEL+")(.+)", ""], # 1, 6 be-rambut
		[0, "(be|te)("+CONSONANT+")({"+ANY+"}?)(er)(.+)", ""], # 3, 7 te-bersit, te-percaya
		[0, "(bel|pel)(ajar|unjur)", ""], # ajar, unjur
		[0, "(me|pe)(l|m|n|r|w|y)(.+)", ""], # 10, 20: merawat, pemain
		[0, "(mem|pem)(b|f|v)(.+)", ""], # 11 23: membuat, pembuat
		[0, "(men|pen)(c|d|j|z)(.+)", ""], # 14 27: mencabut, pencabut
		[0, "(meng|peng)(g|h|q|x)(.+)", ""], # 16 29: menggiring, penghasut
		[0, "(meng|peng)("+VOWEL+")(.+)", ""], # 17 30 meng-anjurkan, peng-anjur
		[0, "(mem|pem)("+VOWEL+")(.+)", "p"], # 13 26: memerkosa, pemerkosa
		[0, "(men|pen)("+VOWEL+")(.+)", "t"], # 15 28 menutup, penutup
		[0, "(meng|peng)("+VOWEL+")(.+)", "k"], # 17 30 mengalikan, pengali
		[0, "(meny|peny)("+VOWEL+")(.+)", "s"], # 18 31 menyucikan, penyucian
		[0, "(mem)(p)("+CONSONANT+")(.+)", ""], # memproklamasikan
		[0, "(pem)("+CONSONANT+")(.+)", "p"], # pemrogram
		[0, "(men|pen)(t)("+CONSONANT+")(.+)", ""], # mentransmisikan pentransmisian
		[0, "(meng|peng)(k)("+CONSONANT+")(.+)", ""], # mengkristalkan pengkristalan
		[0, "(men|pen)(s)("+CONSONANT+")(.+)", ""], # mensyaratkan pensyaratan
		[0, "(menge|penge)("+CONSONANT+")(.+)", ""], # swarabakti: mengepel
		[0, "(mempe)(r)("+VOWEL+")(.+)", ""], # 21
		[0, "(memper)("+ANY+")(.+)", ""], # 21
		[0, "(pe)("+ANY+")(.+)", ""], # 20
		[0, "(per)("+ANY+")(.+)", ""], # 21
		[0, "(pel)("+CONSONANT+")(.+)", ""], # 32 pelbagai, other?
		[0, "(mem)(punya)", ""], # Exception: mempunya
		[0, "(pen)(yair)", "s"], # Exception: penyair > syair
        ),
    	'disallowed_confixes' : (
    		('ber-', '-i'),
    		('ke-', '-i'),
    		('pe-', '-kan'),
    		('di-', '-an'),
    		('meng-', '-an'),
    		('ter-', '-an'),
    		('ku-', '-an'),
    	),
    	'allomorphs' : (
    		{'be' : ('be-', 'ber-', 'bel-')},
    		{'te' : ('te-', 'ter-', 'tel-')},
    		{'pe' : ('pe-', 'per-', 'pel-', 'pen-', 'pem-', 'peng-', 'peny-', 'penge-')},
    		{'me' : ('me-', 'men-', 'mem-', 'meng-', 'meny-', 'menge-')},
    	),
}

def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]
  
  
def stem(kweri):
    words = {}
    instance = {}
    paw   = re.compile(r'\W+')
    raw   = paw.split(kweri)
   
    for r in raw:
        if opsi['NO_DIGIT_ONLY'] and re.search('^\d',r):
            continue
        key = r.lower()
        words[key]= { 'count': countnonoverlappingrematches(key,kweri)}
        #words[key] = { 'count': countnonoverlappingrematches(key,kweri)}
    for k,v in words.items():
        words[k]['roots'] = stem_word(k)
        if len(words[k]['roots']) == 0 and opsi['NO_NO_MATCH']:
            del words[k]
            continue
        instance[k] = v['count']
    word_count = len(words)
    if opsi['SORT_INSTANCE']:
        keys = words.keys()
        sorted(instance)
        sorted(keys)
        sorted(words)
    else:
        words = ksort(words)
    return words

def ksort(d):
     return [(k,d[k]) for k in sorted(d.keys(), reverse=True)]
     
def stem_word(kata):
    word = kata.strip()
    roots = { word : {}}
    if word in dicti.keys():
        roots[word]['affixes'] = {}
    else:
        roots[word]['affixes'] = ''
    dash_parts = word.split('-')
    if len(dash_parts) > 1:
        for dash_part in dash_parts:
            roots[dash_part]['affixes'] = {}
    for group in rules['affixes']:
        is_suffix = group[0]
        affixes   = group[1]
        for affix in affixes:
            if is_suffix:
                pattern = "(.+)("+affix+")"
            else:
                pattern = "("+affix+")(.+)"
            add_root(roots, [is_suffix, pattern, ''])
    is_suffix = 0
    for i in range(3):
        for rule in rules['prefixes']:
            add_root(roots, rule)
    for lemma, attrib in roots.items():
        if lemma not in dicti.keys():
            del roots[lemma]
            continue
        if opsi['STRICT_CONFIX']:
            continue;
        affixes = attrib['affixes']
        for pair in rules['disallowed_confixes']:
            prefix = pair[0]
            suffix = pair[1]
            prefix_key = prefix[:2]
            if prefix_key in rules['allomorphs']:
                for allomorf in rules['allomorphs'][prefix_key]:
                    if allomorf in affixes and suffix in affixes:
                        del roots[lemma]
            else:
                if prefix in affixes and suffix in affixes:
                    del roots[lemma]
    for lemma,attrib in roots.items():
        affixes = attrib['affixes']
        attrib['lemma'] = dicti[lemma]['lemma']
        attrib['class'] = dicti[lemma]['class']
        for affix in attrib['affixes']:
            if affix[:1] == '-':
                tipe = 'suffixes'
            else:
                tipe = 'prefixes'
            attrib[tipe] = affix
        try:
            if len(attrib['suffixes']) > 1:
                ksort(attrib['suffixes'])
        except:
            pass
        roots[lemma] = attrib
    return roots

def add_root(roots,rule):
    is_suffix = rule[0]
    pattern = '^' + rule[1]
    variant = rule[2]
    is_array = lambda var: isinstance(var, (list, tuple))
    for lemma, attrib in roots.items():
        matches = re.findall(pattern,lemma)
        if len(matches) > 0:
            new_lemma = ''
            new_affix = ''
            affix_index = 1 if is_suffix else 0
            for i in range(len(matches[0])):
                if i != affix_index: new_lemma += matches[0][i]
            if variant: 
                new_lemma = variant + new_lemma
            
            new_affix += '- ' if is_suffix else ' '
            new_affix += matches[0][affix_index]+' '
            
            new_affix += ' ' if is_suffix else '- '
            new_affix = new_affix.split()
            if is_array(attrib['affixes']):
                new_affix = attrib['affixes'] + new_affix
            roots[new_lemma] = { 'affixes': new_affix}
                        
if __name__ == '__main__':
    question = raw_input('> ')
    while (question != 'quit'):
        try:
            print stem(question)
            question = raw_input('> ')
        except:
            sys.exit(1)
