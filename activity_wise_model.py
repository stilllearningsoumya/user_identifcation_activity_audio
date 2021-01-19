from collections import Counter
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler

def perform_feature_selection(X,y):
	forest = ExtraTreesClassifier(n_estimators=50,random_state=0)

	forest.fit(X, y)
	importances = forest.feature_importances_
	std = np.std([tree.feature_importances_ for tree in forest.estimators_],
				 axis=0)
	indices = np.argsort(importances)[::-1]

	# Print the feature ranking
	'''print("Feature ranking:")

	for f in range(X.shape[1]):
		print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))'''

	#model = SelectFromModel(forest, prefit=True)
	#X = model.transform(X)
	#print(X.shape)
	print(indices)
	return indices

def evaluate_system(filename,output_file,feature_length=10):
	in_file = pd.read_csv(filename)
	feature_names = in_file.columns[1:len(in_file.columns)-1]
	data = in_file[feature_names]

	#print(data)

	print("Features considered: ")
	print(feature_names)
	
	X = np.asanyarray(data)
	y = np.asarray(in_file['user'])
	print(X.shape)
	print("User distribution before balancing: ")
	print(str(Counter(y)))

	m = MinMaxScaler()
	X = m.fit_transform(X)

	#print(X)
	sm = SMOTE(random_state=42)
	X, y = sm.fit_resample(X, y)
	print(X.shape)

	print("User distribution before balancing: ")
	print(str(Counter(y)))

	top_k = feature_length
	indices = perform_feature_selection(X,y)
	print("**********"+str(len(indices)))
	indices = indices[0:top_k]
	X = X[:,indices]
	feature_names = np.asarray(feature_names)
	print(feature_names[indices])
	print(X.shape)

	#Classifier
	clf = RandomForestClassifier(max_depth=2, random_state=0)
	skf = StratifiedKFold(n_splits=10)

	#Cross validation
	score=[]
	for train_index, test_index in skf.split(X, y):
		#print("TRAIN:", train_index, "TEST:", test_index)
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]
		clf.fit(X_train, y_train)
		y_pred = clf.predict(X_test)
		print(y_pred)
		print(f1_score(y_test,y_pred,average='micro'))
		output_file.write(str(f1_score(y_test,y_pred,average='micro'))+",")
		score.append(f1_score(y_test,y_pred,average='micro'))
	print("Final Score: "+str(np.mean(score))+" pm "+str(np.std(score)))

def main():
	out_file = open("accuracy_scores.txt","w+")
	feature_dimensions = [20]
	for k in feature_dimensions:
		out_file.write("\n****Feature Length = "+str(k)+"*****\n")
		print("For Hammer")
		out_file.write("Hammer,")
		evaluate_system("hammer.csv",out_file,feature_length=k)
		out_file.write("\n")
		print("For Saw")
		out_file.write("Saw,")
		evaluate_system("saw.csv",out_file,feature_length=k)
		out_file.write("\n")
	out_file.flush()
	out_file.close()

if __name__ == '__main__':
	main()