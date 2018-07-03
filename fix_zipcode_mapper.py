import pandas as pd
import numpy as np


postcodescities = pd.read_csv("city_to_zipcode.dat")

def map(current):
    if current == "BerlinKreuzberg":
        return "Berlin"


#postcodescities.