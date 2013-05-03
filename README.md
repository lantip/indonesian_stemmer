Ivan Lantip Stemmer
==================
Sebuah Pengakar Bahasa Indonesia berbasis bahasa pemrograman Python, dikembangkan dari pengakar karya Ivan Lanin (https://github.com/ivanlanin/pengakar)

Requirements:
-------------
* Python >= 2.7.3

Penggunaan:
-----------

	In [1]: from indonesian_stemmer import ILStemmer
	In [2]: stemmer = ILStemmer()
	In [3]: stemmer.stem('memperingati tujuh belasan')
	Out[3]: 'tujuh memper-ingat-i belas-an'
	In [4]: stemmer.stem('penanaman')
	Out[4]: 'pen-tanam-an '
