import sys
import os
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from numpy import array
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

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


# prepare cross validation
k = 4
kfold = KFold(k, True, 1)

X = np.array(x)
Y = np.array(y)

totalAccuracy = 0.0
totalPrecision = 0.0
totalSpecificity = 0.0
totalRecall = 0.0

for train_index, test_index in kfold.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = Y[train_index], Y[test_index]

    classifier1 = LogisticRegression(random_state = 0)
    classifier2 = SVC(kernel='linear', degree=7, probability=True)
    classifier3 = KNeighborsClassifier(n_neighbors=7)
    classifier4 = RandomForestClassifier(n_estimators=62, bootstrap = True, max_features = 'sqrt')

    maxVote = VotingClassifier(estimators=[('lr', classifier1), ('svc', classifier2), ('knn', classifier3), ('rf', classifier4)], voting='soft')
    maxVote.fit(X_train, y_train)
    y_pred = maxVote.predict(X_test)

    TN, FP, FN, TP = confusion_matrix(y_test, y_pred).ravel()

    Accuracy = (TP + TN) / (TP + TN + FP + FN)
    Recall = TP / (TP + FN)
    Specificity = TN / (FN + TN)
    Precision = TP / (TP + FP)
    totalAccuracy += Accuracy
    totalRecall += Recall
    totalSpecificity += Specificity
    totalPrecision += Precision

    print ('Accuracy: ' + str(Accuracy))
    print ('Recall: ' + str(Recall))
    print ('Specificity: ' + str(Specificity))
    print ('Precision: ' + str(Precision))

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))


print ('Total Accuracy: ' + str(totalAccuracy / k))
print ('Total Recall: ' + str(totalRecall / k))
print ('Total Specificity: ' + str(totalSpecificity / k))
print ('Total Precision: ' + str(totalPrecision / k))


filename = 'phishing_model.sav'
pickle.dump(maxVote, open(filename, 'wb'))
