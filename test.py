#!/usr/bin/env python

from indonesian_stemmer import ILStemmer
stemmer = ILStemmer()

text = 'memperingati tujuh belasan'
print 'NO SORT_INSTANCE'
print('stemmed with suffix and prefix:', stemmer.stem(text))
print('stemmed root only:', stemmer.stem_root(text))

stemmer.OPTION['SORT_INSTANCE'] = True
print "SORT_INSTANCE True"
print('stemmed with suffix and prefix:', stemmer.stem(text))
print('stemmed root only:', stemmer.stem_root(text))
