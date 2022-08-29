import urllib
import json
import glob
import os
from pathlib import Path
import pandas as pd

resp_text = urllib.request.urlopen('https://xn--d1aqf.xn--p1ai/ajax/itm_weekly_report.php').read().decode('UTF-8')
json_obj = json.loads(resp_text)

dates = json_obj['dates'];

Path("export").mkdir(parents=True, exist_ok=True)

for date in dates:
   urllib.request.urlretrieve('https://xn--d1aqf.xn--p1ai/ajax/itm_weekly_report.php?reportType=creditor&date=' + date +'&format=xlsx',
                              "export/" + date.replace(".","_") + ".xlsx")  
