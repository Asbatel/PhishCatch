import sys
import os
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from numpy import array
from fastFM import als
from sklearn.model_selection import train_test_split
from fastFM import sgd
from scipy.sparse import csr_matrix

from fastFM.datasets import make_user_item_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score


if len(sys.argv) != 2:
    print ('Usage: ml_template <dataFile>')
    sys.exit()


dataFile = sys.argv[1]
with open(dataFile) as f:
    content = f.readlines()
x = []
y = []
for line in content:
	data = line.split(';')
	vector = []
	for item in data[1].split(','):
		vector.append(int(item))
	x.append(vector)
	y.append(int(data[2]))



X = np.array(x)
Y = np.array(y)


X_train, X_test, y_train, y_test = train_test_split(X, Y)

y_labels = np.ones_like(Y)
y_labels[y < np.mean(Y)] = -1
X_train, X_test, y_train, y_test = train_test_split(X, y_labels)
fm = sgd.FMClassification(n_iter=1000, init_stdev=0.2, l2_reg_w=0, l2_reg_V=0, rank=2, step_size=0.01)
S_tr = csr_matrix(X_train)
S_te = csr_matrix(X_test)
fm.fit(S_tr, y_train)
y_pred = fm.predict(S_te)
y_pred_proba = fm.predict_proba(S_tr)


print('acc:', accuracy_score(y_test, y_pred))
