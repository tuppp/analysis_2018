import pandas as pd
import numpy as np
import sys

sys.path.append("C:/Users/Lukas Tilmann/mkp_database")

import FunctionLibraryExtended as fl

dwd, se = fl.getConnectionDWD()

acc, se_acc = fl.getConnectionAccuweathercom()

#data = fl.getResult(fl.getPostcode(26197,dwd,se),se)

#data = fl.getResult(fl.getTempAvg(Dwd,se),se)

query_2 = se_acc.query(acc).filter(acc.c.postcode==10627)

query = se.query(dwd).filter(dwd.c.postcode==10627)

#query = se.query(dwd).select_from(dwd.c.Max_temp)


print(fl.getResult(query, se))

print(fl.getResult(query_2, se_acc))

print(query)
