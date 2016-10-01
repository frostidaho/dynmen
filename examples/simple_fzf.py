#!/usr/bin/env python
import dynmen

from collections import OrderedDict
from pprint import pprint
some_dict = OrderedDict((str(x), x**2) for x in range(20))
pprint(some_dict)
out_fzf = dynmen.fzf(some_dict)
pprint(out_fzf)
print('The return code from fzf was {}'.format(out_fzf.returncode))
