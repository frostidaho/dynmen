#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The following is a basic example using the tty-based
# interactive filtering tool percol (https://github.com/mooz/percol)

# Make a Menu() instance by passing a sequence containing your
# menu's command and its corresponding flags & options.
# e.g., percol = Menu(command=('percol',))
# The instance of Menu() is callable and can be given a sequence or a mapping.

import logging

# Setting up root logger to print logging msges from dynmen
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-8s %(name)-12s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# # The following example dict was created using the faker lib:
# from faker import Factory
# from pprint import pprint
# fake = Factory.create('de_DE')
# exdict = dict(((fake.name(), (fake.user_name(), fake.uri())) for i in range(40)))
# pprint(exdict)

exdict = {
    'Arnim Schüler'                        : ('qrogge', 'http://www.stahr.de/register/'),
    'Bernhardine Sauer-Dussen van'         : ('koch-iigunar', 'http://stadelmann.net/posts/search/post/'),
    'Björn Salz B.Sc.'                     : ('bhering', 'http://bolander.com/app/blog/index/'),
    'Brunhilde Neuschäfer'                 : ('kzirme', 'http://www.neuschaefer.org/about.htm'),
    'Dipl.-Ing. Marie-Louise Kabus B.Eng.' : ('luitgardmohaupt', 'http://www.mielcarek.org/category/about/'),
    'Dörte Beier'                          : ('ognatz', 'http://www.gute.org/'),
    'Elvira Warmer'                        : ('wesackelif', 'http://www.matthaei.com/explore/search.html'),
    'Erica Stolze'                         : ('bjunitz', 'http://www.moechlichen.de/category/wp-content/explore/terms/'),
    'Frank Hübel'                          : ('franca13', 'http://schaefer.de/terms/'),
    'Grazyna Birnbaum-Johann'              : ('ilkaklapp', 'http://nerger.com/wp-content/register.php'),
    'Gustav Wähner'                        : ('toralfvogt', 'http://naser.com/category/'),
    'Hans-Friedrich Mohaupt-Gertz'         : ('aumannpetra', 'http://ziegert.com/homepage.html'),
    'Heiderose Eckbauer MBA.'              : ('roemergundi', 'http://www.reichmann.net/'),
    'Herr Kai-Uwe Tröst B.A.'              : ('friedbert44', 'http://radisch.com/about/'),
    'Irmi Hiller'                          : ('konstantinoslorch', 'http://karz.de/main.htm'),
    'Jana Lindau'                          : ('stiebitzirmhild', 'http://weihmann.net/wp-content/blog/wp-content/index/'),
    'Jolanthe Reuter B.Eng.'               : ('luebsgrit', 'http://graf.de/search/explore/category/main.php'),
    'Josefine Thanel B.Eng.'               : ('xroht', 'http://www.walter.net/homepage/'),
    'Lilly Rudolph'                        : ('hendriksgerda', 'http://www.rosemann.de/posts/main/main/index/'),
    'Lilo Bolander'                        : ('hermannmarie-therese', 'http://seifert.com/main/blog/category.php'),
    'Maren Barth'                          : ('bayramehlert', 'http://gumprich.org/terms/'),
    'Maritta Weimer'                       : ('margitastroh', 'http://www.eberth.com/app/tag/tag/post/'),
    'Maurice Zorbach'                      : ('hertrampfmikhail', 'http://rust.com/privacy.jsp'),
    'Moritz Hertrampf'                     : ('gotthilf73', 'http://mans.com/privacy.php'),
    'Nico Mülichen'                        : ('marisajopich', 'http://loos.com/categories/tags/privacy/'),
    'Nora Ebert B.A.'                      : ('hellwigheinz-werner', 'http://www.kroker.com/index.html'),
    'Piotr Etzler'                         : ('pasquale12', 'http://www.schweitzer.de/register.jsp'),
    'Prof. Angelika Walter'                : ('vadimkeudel', 'http://weinhage.de/main/wp-content/terms.html'),
    'Prof. Bertram Reising'                : ('rudolfbender', 'http://schenk.org/homepage.asp'),
    'Prof. Magdalene Klotz'                : ('mielcarekanthony', 'http://zimmer.net/'),
    'Renata Röhrdanz-Holt'                 : ('baumbert', 'http://oestrovsky.de/main/explore/search/privacy.html'),
    'Rosi Jüttner'                         : ('bradisch', 'http://www.hering.de/posts/wp-content/tag/main/'),
    'Roy Killer'                           : ('eveline85', 'http://gertz.de/search.html'),
    'Thomas Löffler B.Sc.'                 : ('ilias04', 'http://schweitzer.com/explore/terms.php'),
    'Univ.Prof. Denise Mülichen B.Eng.'    : ('hettnerfranco', 'http://mangold.org/'),
    'Univ.Prof. Paolo Gorlitz'             : ('qholzapfel', 'http://www.kostolzin.net/app/wp-content/about/'),
    'Wenzel Hentschel-Pärtzelt'            : ('anja44', 'http://www.seip.com/'),
    'Wigbert Möchlichen'                   : ('kilian26', 'http://roskoth.net/category/wp-content/register/'),
    'Wilfried Förster'                     : ('kirstin09', 'http://hoerle.com/'),
    'Zdenka Bruder'                        : ('jzimmer', 'http://www.naser.com/terms.html')
}


from dynmen import Menu

percol = Menu(['percol'])
# Here we could either call percol() or percol.sort()
# the latter will sort the keys before passing them to percol
out = percol.sort(exdict)
print(out)
