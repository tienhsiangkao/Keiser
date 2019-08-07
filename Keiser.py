#Copyright (C) [2019] by [Tianxiang "Ronnie" Gao] <[tienhsiangkao@gmail.com]>
#
#Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.#
#
#THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
from argparse import ArgumentParser

import re
import pandas as pd
import numpy as np
import time
import sys
from zipfile import ZipFile
import sys

filename = sys.argv[1]
if len(sys.argv) == 3:
  timezone = sys.argv[2]
else:
  pass




start = time.time()


#filename = '05Aug2.KMZ'

def kmz_parser(filename):

    kmz = ZipFile(filename, 'r')
    kml = kmz.open('doc.kml', 'r').read()

    t = []
    lon = []
    lat = []
    alt = []

    obj = kml.decode().split('<Placemark>')

    for lines in obj[1:]:
        text = lines.split('<BR>')[6]
        temp0 = str(re.findall("= \S*",text))[4:-2]
        text = lines.split('<BR>')[8]
        temp1 = str(re.findall("= \S*"+' \D*',text))[4:-2]
        t.append(pd.pandas.to_datetime(temp0+' '+ temp1, utc= True))

        text = re.split('<coordinates>|</coordinates>',lines)[-2].split(',')

        x, y, z = text
        lon.append(x)
        lat.append(y)
        alt.append(z)

    data = pd.DataFrame(data=np.transpose(np.array([lon, lat, alt])),index=t,
                        columns=['lon', 'lat', 'alt'])
    return data

def tz_convert(data, timezone='US/Pacific'):
    data = data.tz_convert(timezone)
    data.index = pd.DatetimeIndex([i.replace(tzinfo=None) for i in data.index])
    return data

data = kmz_parser(str(filename))
try:
    timezone
    data = tz_convert(data, timezone)
except:
    data = tz_convert(data)



data.to_csv(filename[:-4]+'.csv')
