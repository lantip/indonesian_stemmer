#!/usr/bin/env python

from indonesian_stemmer import ILStemmer
stemmer = ILStemmer()
stemmer.OPTION['NO_NO_MATCH'] = False
stemmer.OPTION['NO_DIGIT_ONLY'] = False
stemmer.OPTION['ALLOW_HASHTAGS'] = True

text = 'memperingati tujuh #belasan'
print 'NO SORT_INSTANCE'
print('stemmed with suffix and prefix:', stemmer.stem(text))
print('stemmed root only:', stemmer.stem_root(text))

stemmer.OPTION['NO_NO_MATCH'] = True
stemmer.OPTION['NO_DIGIT_ONLY'] = True
stemmer.OPTION['ALLOW_HASHTAGS'] = False
stemmer.OPTION['SORT_INSTANCE'] = True
print "SORT_INSTANCE True"
print('stemmed with suffix and prefix:', stemmer.stem(text))
print('stemmed root only:', stemmer.stem_root(text))
