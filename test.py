from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm

print 'hi'

iris = datasets.load_iris()
X = iris.data
y = iris.target

X = X[y != 0, :2]
y = y[y != 0]

n_sample = len(X)

np.random.seed(0)
order = np.random.permutation(n_sample)
print n_sample
X = X[order]
y = y[order].astype(np.float)
print X
print y
X_train = X[:.9 * n_sample]
y_train = y[:.9 * n_sample]
X_test = X[.9 * n_sample:]
y_test = y[.9 * n_sample:]

clf = svm.SVC(kernel='linear', gamma=10)
clf.fit(X_train, y_train)
clf.predict(digits.data[-1:])
