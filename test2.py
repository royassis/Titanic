from pcg.imports2 import *
import re


#Data cleaning and preprocessing#
#-------------------------------#

#Load df from file
dframe = pd.read_csv("train.csv")

#Split Cabin column into floor and rooms columns
newframe = dframe.Cabin.str.split(" ", expand=True)
dframe.Cabin= dframe.Cabin.str.extract('(\w)')
newframe = newframe.apply(lambda x: x.str.extract('(\d+)'))
frame = pd.concat([dframe, newframe],axis=1)

#Turn NA values to -1 in order to be used in learning algorithms
frame.fillna(-1, inplace = True)

#Groupby Ticket and then give each person the count of the group
dframe[dframe.Ticket.duplicated(keep=False)].sort_values("Ticket")
grp = dframe[dframe.Ticket.duplicated(keep=False)].groupby("Ticket").size() #people with the same ticket



#Maching learning#
#----------------#

# Split-out validation dataset
array = dframe.values
X = array[:,1:7]
Y = array[:,0]
X,Y = X,Y.astype(float)
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

# Test options and evaluation metric
seed = 7
scoring = 'accuracy'

models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = model_selection.KFold(n_splits=10, random_state=seed)
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
	print(msg)


for x,y in enumerate(dframe.columns):
	print (x,y,dframe.iloc[x,x])




#Homemade functions#
#------------------#

def NullColumnPrec(dframe):
	for i in dframe.columns:
		print (i, dframe[dframe[i].isnull()].shape[0]/dframe.shape[0])

def UniqueColumnPrec(dframe):
	arr = []
	for i in dframe.columns:
		number = dframe[i].unique().shape[0] / dframe.shape[0]
		arr.append([i,number])
	return arr

	for i in arr :
		print(i, "{:.2f}".format(i[0]))

#Does not work, work in progress
def text2number(dframe):
	columns = dframe.dtypes[dframe.dtypes == object].index
	dict = {}
	arr=[]
	for i in columns:
		for j in dframe[i].unique():
			arr.append(j)

	for i, j in enumerate(arr):
		dict[j] =i
	return  dict