import pickle
import sys
import os
import pickle
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from extract_features import Extract



if len(sys.argv) != 2:
    print('Usage: python check_url.py <url>')
    sys.exit()


url_input = sys.argv[1]

def testURL(url):
    extract = Extract(url)
    featureList = extract.inspectURL()
    print(featureList)
    tolerance = 19 - len(featureList)

    while tolerance > 0:
	featureList.append(0)
        tolerance-=1


    shapedArray = np.array(featureList)
    finalShape = shapedArray.reshape(1, -1)
    filename = 'phishing_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(finalShape)

    print("Checking -> " + url)
    print(result)
    if int(result) == 1:
        print("phishing")
    else:
        print ("benign")


testURL(url_input)
