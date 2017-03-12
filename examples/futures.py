#!/usr/bin/env python
# -*- coding: utf-8 -*-
data = {'Agnes Heydrich B.Sc.': ('Wernigerode', '(03448) 988518'),
        'Aleksandr Scheel': ('Oschatz', '+49 (0) 3503 036019'),
        'Andrei Wulf': ('Husum', '+49(0) 302223785'),
        'Aneta Meister B.A.': ('Wernigerode', '(08812) 313304'),
        'Ayten Peukert-Ladeck': ('Rosenheim', '+49(0) 723816649'),
        'Bayram Wulf': ('Stollberg', '08234084344'),
        'Boris Tintzmann': ('Helmstedt', '+49 (0) 9361 382513'),
        'Brita auch Schlauchin-Söding': ('Herford', '+49(0)4933 76867'),
        'Cecilia Schmidtke B.A.': ('Brand', '+49 (0) 4770 088390'),
        'Cemil Dowerg': ('Neunburg vorm Wald', '+49(0)5803 34418'),
        'Cemil Knappe': ('Neustadtner Waldnaab', '0675019402'),
        'Dipl.-Ing. Gotthold Birnbaum': ('Griesbach Rottal', '00578245960'),
        'Dipl.-Ing. Markus Anders': ('Wolfach', '04473 609277'),
        'Dr. Hansjoachim Sölzer': ('Melle', '0798085044'),
        'Dr. Heinz-Peter Lindau MBA.': ('Dinslaken', '08917 31215'),
        'Dr. Melanie Huhn': ('Wittstock', '0287777101'),
        'Eckhard Berger': ('Tecklenburg', '+49(0) 616832915'),
        'Franco Hein': ('Neustadtner Waldnaab', '+49(0)4436 106543'),
        'Frau Ernestine Henck B.Eng.': ('Eisleben', '01001016899'),
        'Friedlinde Linke': ('Darmstadt', '08900 06572'),
        'Gotthold Etzler-Roskoth': ('Wolmirstedt', '+49 (0) 1093 564868'),
        'Gunhild Speer': ('Nördlingen', '04688 64192'),
        'Hans-Michael Preiß': ('Parsberg', '0607095960'),
        'Ian Krause': ('Mayen', '+49(0)6909 193055'),
        'Ildiko Seifert': ('Meiningen', '(02067) 043728'),
        'Ing. Christian Heydrich MBA.': ('Querfurt', '+49 (0) 6880 470754'),
        'Ing. Etta Pechel B.Sc.': ('Grafenau', '+49(0)8045 411926'),
        'Ing. Gregor Hoffmann': ('Helmstedt', '09899748780'),
        'Ing. Veronika Pohl B.Sc.': ('Staßfurt', '+49 (0) 7620 065901'),
        'Josef Liebelt-Ziegert': ('Stade', '05636739676'),
        'Juan Hölzenbecher': ('Witzenhausen', '+49 (0) 4642 111940'),
        'Justus Hartmann MBA.': ('Pegnitz', '09892545270'),
        'Klara Ruppert MBA.': ('Bad Freienwalde', '09553114318'),
        'Klaus Atzler MBA.': ('Sondershausen', '+49(0)7003 65357'),
        'Korbinian Trüb': ('Eggenfelden', '+49(0)2458824234'),
        'Lydia Klapp': ('Pößneck', '05485 39997'),
        'Manja Spieß': ('Oberviechtach', '+49(0)8992954003'),
        'Marijan Weihmann': ('Ribnitz-Damgarten', '+49(0)8069 64049'),
        'Mira Gotthard B.A.': ('Waldmünchen', '+49(0)9314 915830'),
        'Mirjam Ullrich': ('Marienberg', '+49(0) 293469472'),
        'Olga Bolnbach-Becker': ('Staßfurt', '+49(0) 752885340'),
        'Otmar Köhler': ('Bruchsal', '0934122052'),
        'Phillip Ortmann': ('Uelzen', '00442985101'),
        'Prof. Korbinian Klotz': ('Lübeck', '+49(0) 255070995'),
        'Prof. Marie-Therese Höfig': ('Nabburg', '+49(0)3095 91143'),
        'Prof. Tania Schmidtke MBA.': ('Erfurt', '01303 61366'),
        'Reimar Albers': ('Strasburg', '(02766) 21169'),
        'Reinald Patberg': ('Erkelenz', '04161 53783'),
        'Romy Graf': ('Kötzting', '(06255) 908206'),
        'Rose-Marie Jungfer': ('Marienberg', '+49(0)4417870897'),
        'Rudi Kroker': ('Tirschenreuth', '04146244395'),
        'Stefan Conradi': ('Staßfurt', '(09309) 58677'),
        'Sylwia Bruder': ('Kehl', '+49(0)1177 578475'),
        'Theda Misicher': ('Wismar', '08328183362'),
        'Univ.Prof. Friederike Lindner': ('Zschopau', '+49(0)9615 78454'),
        'Univ.Prof. Maik Gude B.Eng.': ('Nürtingen', '(06172) 90347'),
        'Urs Dobes': ('Lobenstein', '04931 109878'),
        'Urte Franke': ('Starnberg', '+49(0)1322933157'),
        'Valentin Rörricht B.A.': ('Wiedenbrück', '+49(0) 199099385'),
        'Viktor Gumprich B.Eng.': ('Pfaffenhofenner Ilm', '+49(0)7585283338')}

from time import sleep
from dynmen import Menu
# process_mode = 'futures' sets Menu(...) to run the
# menu process in a thread pool and return a future (from concurrent.futures) 
rofi = Menu(['rofi', '-dmenu'], process_mode='futures')
future = rofi(data)

while not future.done():
    print('doing something else')
    sleep(0.3)

print(future)
res = future.result()
print(res)


