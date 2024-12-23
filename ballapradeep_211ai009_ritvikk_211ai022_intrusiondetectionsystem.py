# -*- coding: utf-8 -*-
"""BallaPradeep_211AI009_RitvikK_211AI022_IntrusionDetectionSystem (3).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RuH6WD-BGY6tH9Puk7Z0dagaUeHWyFkm

#Intrusion Detection System(IDS)<br>
1. Balla Pradeep - 211AI009
2. Ritvik K      - 211AI022

Importing libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn import tree
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from scipy.stats import kendalltau
from sklearn.metrics import precision_score,recall_score ,f1_score,roc_curve, auc,confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib
from scipy.stats import randint as sp_randint


pd.set_option('display.max_columns',None)
warnings.filterwarnings('ignore')
# %matplotlib inline

pip show scikit-learn

"""Reading Dataset and Exploring"""

data_train=pd.read_csv("/content/drive/MyDrive/KDDTrain+.txt")
data_train.head()

data_test=pd.read_csv("/content/drive/MyDrive/nsl-kdd dataset/KDDTest+.txt")
data_test.head()

columns = (['duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent','hot'
,'num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root','num_file_creations'
,'num_shells','num_access_files','num_outbound_cmds','is_host_login','is_guest_login','count','srv_count','serror_rate'
,'srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count'
,'dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate','dst_host_srv_diff_host_rate','dst_host_serror_rate'
,'dst_host_srv_serror_rate','dst_host_rerror_rate','dst_host_srv_rerror_rate','outcome','level'])

# Assign name for columns
data_train.columns = columns
data_train.head()

# Assign name for columns
data_test.columns = columns
data_test.head()

data_train.info()

data_test.info()

#check for duplicates
print(data_train.duplicated().sum())

#checking for missing values
data_train.isnull().sum()

data_train.shape

#attacks
data_train['outcome'].value_counts()

"""Function helps to classify different class labels into attack_types"""

Dos = ['land','neptune','smurf','pod','back','teardrop']
Probe = ['portsweep','ipsweep','satan','nmap']
U2R = ['buffer_overflow','loadmodule','perl','rootkit']

def encode_attack(vec):
    if vec in Dos:
        return "Dos"
    elif vec in Probe:
        return "Probe";
    elif vec in U2R:
        return "U2R"
    elif vec == "normal":
        return "normal"
    else:
        return "R2L"

"""Creating new variable called "attack_type" where it classified different "class" labels to Dos, Probe, U2R, R2L and Normal"""

def encode_outcome(vec):
    if vec == "normal":
        return "normal"
    else:
        return "attack"

data_train['outcome_type'] = data_train['outcome'].apply(encode_outcome)

data_test['outcome_type'] = data_test['outcome'].apply(encode_outcome)

data_test.groupby('attack_type').size()

"""Percentage of data hold by different attack types"""

percent_data = (data_train.groupby('attack_type').size())/data_train.shape[0] * 100
percent_data

"""Amount of different attack types hold the data
graph represents that "Normal" data holds 53.4%, "Dos" hold 36.46%, "Probe" attack type hold 9.2% of data and rest "R2L" and "U2R" are less than 1% data holds.
"""

percent_data_test = (data_test.groupby('attack_type').size())/data_test.shape[0] * 100
percent_data_test

fig = plt.figure(figsize = (10,8))
r_ = [round(each, 2) for each in percent_data.values]
ax = fig.add_subplot(111)
ax.bar(percent_data.index, percent_data.values, color = ['darkred', 'teal', 'gold', 'lightseagreen', "mediumaquamarine"], edgecolor = 'black')
ax.set_xticklabels(percent_data.index, rotation = 45)
ax.set_xlabel("Attack type", fontsize = 20)
ax.set_ylabel("Count", fontsize = 20)
ax.set_title("Attacks type data counts training", fontsize = 20)

for i in range(len(percent_data.values)):
    plt.annotate(str(r_[i]), xy=(percent_data.index[i],r_[i]+1), ha='center', va='bottom')

fig = plt.figure(figsize = (10,8))
r_ = [round(each, 2) for each in percent_data_test.values]
ax = fig.add_subplot(111)
ax.bar(percent_data_test.index, percent_data_test.values, color = ['darkred', 'teal', 'gold', 'lightseagreen', "mediumaquamarine"], edgecolor = 'black')
ax.set_xticklabels(percent_data_test.index, rotation = 45)
ax.set_xlabel("Attack type", fontsize = 20)
ax.set_ylabel("Count", fontsize = 20)
ax.set_title("Attacks type data counts training", fontsize = 20)

for i in range(len(percent_data_test.values)):
    plt.annotate(str(r_[i]), xy=(percent_data_test.index[i],r_[i]+1), ha='center', va='bottom')

"""Pie chart: Different types of attack types in data"""

group_data = data_train.groupby('attack_type').size()
plt.figure(figsize = (10,8))
group_data.plot(kind='pie')
plt.title("Different types of attack types in data")
plt.ylabel("")
plt.show()

"""Different Protocol types"""

plt.subplots(figsize=(10,8))
data_train['protocol_type'].value_counts(normalize = True)
data_train['protocol_type'].value_counts(dropna = False).plot.bar(color=['teal', 'lightseagreen', 'gold', 'olive'])
plt.show()

data_train.shape

data_test.shape

"""Different protocols dependencies on attack types"""

fig = plt.figure(figsize = (10,8))
avg_pro = pd.crosstab(data_train['protocol_type'], data_train['attack_type'])
avg_pro.div(avg_pro.sum(1).astype(float), axis = 0).plot(kind = 'bar', stacked = True, color = ['indigo', 'gold', 'teal', 'olive', 'slategrey'])

plt.title('Dependency of "Protocols" in Attack types', fontsize = 20)
plt.xlabel('Protocol Types', fontsize = 20)
plt.legend()
plt.show()

"""Data preprocessing scaling and one hot encoding"""

def attack_encode(value):
    if value == 'normal':
        return 0;
    elif value == "Dos":
        return 1;
    elif value == 'Probe':
        return 2;
    elif value == 'R2L':
        return 3;
    else:
        return 4;

def outcome_encode(value):
    if value == 'normal':
        return 0;
    else:
        return 1;

data_train['outcome_code'] = data_train['outcome_type'].apply(outcome_encode)

data_test['outcome_code'] = data_test['outcome_type'].apply(outcome_encode)

data_train

"""Dropping class and attack_type variables as it was encoded in "intrusion_code"
"""

data_train = data_train.drop(columns = ['outcome','level'])
data_test = data_test.drop(columns = ['outcome','level'])

data_train = data_train.drop(columns = ['outcome_type'])
data_test = data_test.drop(columns = ['outcome_type'])

corr_df = data_train.corr()[data_train.corr().index]
fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(corr_df, cmap='viridis', annot=True, annot_kws={"size": 11})
plt.show()

"""Feature Selection Techniques

Dense_fr feature selection method(As per Base Paper) using Mutual information and kendalls correlation
"""

data_train.corr()['outcome_code'].sort_values(ascending = False)

# Select only categorical variables
category_df = data_train.select_dtypes('object')

# One hot encode the variables
dummy_df = pd.get_dummies(category_df)

# Put the label column back in the dataframe
dummy_df['outcome_code'] =data_train['outcome_code']

dummy_df

# Correlations in one-hot encoded dataframe
dummy_df.corr()['outcome_code'].sort_values(ascending=False)

data_train = data_train.drop(columns=['num_outbound_cmds', 'srv_count', 'dst_bytes', 'src_bytes',
                                  'land', 'is_host_login', 'urgent', 'num_failed_logins', 'num_shells'])
data_test = data_test.drop(columns=['num_outbound_cmds', 'srv_count', 'dst_bytes', 'src_bytes',
                                  'land', 'is_host_login', 'urgent', 'num_failed_logins', 'num_shells'])

data_train

data_test

train_df_onehot = pd.get_dummies(data_train)
test_df_onehot = pd.get_dummies(data_test)

print (train_df_onehot.shape)
print (test_df_onehot.shape)

set(train_df_onehot.columns).difference(set(test_df_onehot))

train_df_onehot

# Extract the target variable (outcome) and features

dense_train = train_df_onehot
X = dense_train.drop('outcome_code', axis=1)  # Features
y = dense_train['outcome_code']  # Target

X

# Compute Mutual Information (MI) scores for each feature
mi_scores = mutual_info_classif(X, y, random_state=42)
print("MI Scores for each feature:")
for feature, score in zip(X.columns, mi_scores):
    print(f"{feature}: {score:.4f}")

# Compute Kendall's Correlation Coefficients for each feature
correlation_scores = []
for col in X.columns:
    corr, _ = kendalltau(X[col], y)
    correlation_scores.append(corr)
print("Kendall's Correlation Coefficients for each feature:")
for feature, score in zip(X.columns, correlation_scores):
    print(f"{feature}: {score:.4f}")

# Combine MI and Kendall's Correlation Scores
mi_ranked_indices = np.argsort(mi_scores)[::-1]
corr_ranked_indices = np.argsort(correlation_scores)[::-1]

# Divide MI and Kendall's Correlation into three parts as per Dense_FR approach
part1 = int(0.3 * len(X.columns))
part2 = int(0.6 * len(X.columns))

mi_part1 = mi_ranked_indices[:part1]
mi_part2 = mi_ranked_indices[part1:part2]
mi_part3 = mi_ranked_indices[part2:]

corr_part1 = corr_ranked_indices[:part1]
corr_part2 = corr_ranked_indices[part1:part2]
corr_part3 = corr_ranked_indices[part2:]

# Compute intersections of MI and Kendall's Correlation for each part
mc1 = list(set(mi_part1) & set(corr_part1))
mc2 = list(set(mi_part2) & set(corr_part2))
mc3 = list(set(mi_part3) & set(corr_part3))

# Compute Union of MC1, MC2, and MC3 to get the optimal feature subset
optimal_feature_subset = list(set(mc1) | set(mc2) | set(mc3))

print("Optimal Feature Subset")
print("Number of selected features:", len(optimal_feature_subset))

# Sort the features in optimal_feature_subset by Kendall's Correlation score
optimal_feature_subset_sorted_by_corr = sorted(optimal_feature_subset, key=lambda feature_idx: correlation_scores[feature_idx], reverse=True)

# Print the ranked features
print("\nOptimal Features Sorted by Kendall's Correlation Score:")
for feature_idx in optimal_feature_subset_sorted_by_corr:
    print(f"{X.columns[feature_idx]},{correlation_scores[feature_idx]:.4f}")

# Get the top 15 features based on Kendall's Correlation score
top_corr_features = [X.columns[feature_idx] for feature_idx in optimal_feature_subset_sorted_by_corr[:15]]

top_corr_features

dense_train = dense_train[top_corr_features]
dense_train

corr_df = dense_train.corr()[dense_train.corr().index]
fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(corr_df, cmap='viridis', annot=True, annot_kws={"size": 11})
plt.show()

"""2nd feature selection SPARSE_FR from base paper"""

# Assuming data_train contains your dataset

# Extract the target variable (outcome) and features
sparse_train = train_df_onehot
X_sparse = sparse_train.drop('outcome_code', axis=1)  # Features
y_sparse = sparse_train['outcome_code']  # Target

# Compute Mutual Information (MI) scores for each feature
mi_scores_sparse = mutual_info_classif(X_sparse, y_sparse, random_state=42)

# Compute Kendall's Correlation Coefficients for each feature
correlation_scores_sparse = []
for col in X_sparse.columns:
    corr, _ = kendalltau(X_sparse[col], y_sparse)
    correlation_scores_sparse.append(corr)

# Combine MI and Kendall's Correlation Scores
mi_ranked_indices_sparse = np.argsort(mi_scores_sparse)[::-1]
corr_ranked_indices_sparse = np.argsort(correlation_scores_sparse)[::-1]

# Divide MI and Kendall's Correlation into three parts as per Sparse_FR approach
part1_sparse = int(0.3 * len(X_sparse.columns))
part2_sparse = int(0.6 * len(X_sparse.columns))

mi_part1_sparse = mi_ranked_indices_sparse[:part1_sparse]
mi_part2_sparse = mi_ranked_indices_sparse[part1_sparse:part2_sparse]

corr_part1_sparse = corr_ranked_indices_sparse[:part1_sparse]
corr_part2_sparse = corr_ranked_indices_sparse[part1_sparse:part2_sparse]

# Compute intersections of MI and Kendall's Correlation for each part
mc1_sparse = list(set(mi_part1_sparse) & set(corr_part1_sparse))
mc2_sparse = list(set(mi_part2_sparse) & set(corr_part2_sparse))

# Compute Union of MC1 and MC2 to get the optimal feature subset
optimal_feature_subset_sparse = list(set(mc1_sparse) | set(mc2_sparse))

print("Optimal Feature Subset (Sparse_FR)")
print("Number of selected features:", len(optimal_feature_subset_sparse))

# Sort the features in optimal_feature_subset by Kendall's Correlation score
optimal_feature_subset_sorted_by_corr_sparse = sorted(optimal_feature_subset_sparse, key=lambda feature_idx: correlation_scores_sparse[feature_idx], reverse=True)

# Print the ranked features

print("\nOptimal Features Sorted by Kendall's Correlation Score:")
for feature_idx in optimal_feature_subset_sorted_by_corr_sparse:
    print(f"{X_sparse.columns[feature_idx]},{correlation_scores_sparse[feature_idx]:.4f}")

# Get the top 20 features based on Kendall's Correlation score
top_corr_features_sparse = [X_sparse.columns[feature_idx] for feature_idx in optimal_feature_subset_sorted_by_corr_sparse[:15]]

top_corr_features_sparse

# Extract the target variable (outcome) and features

sparse_train = train_df_onehot
sparse_test = test_df_onehot

sparse_train  = sparse_train[top_corr_features_sparse]
sparse_test  = sparse_test[top_corr_features_sparse]

sparse_train

sparse_test

unique_flags = data_train['service'].unique()
print(unique_flags)

unique_flags = data_train['flag'].unique()
print(unique_flags)

unique_flags = data_train['protocol_type'].unique()
print(unique_flags)

data_test



corr_df_sparse = sparse_train.corr()[sparse_train.corr().index]
fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(corr_df_sparse, cmap='viridis', annot=True, annot_kws={"size": 11})
plt.show()

"""MOdels"""

from sklearn.preprocessing import StandardScaler # for stardardizing the data to the normal scale
from sklearn.model_selection import train_test_split # for splitting data into train and test
from sklearn.tree import DecisionTreeClassifier # Decision Tree model classifier
from sklearn.ensemble import RandomForestClassifier # RandomForest model classification
from sklearn.linear_model import LogisticRegression # Logistic Regression
from sklearn.metrics import classification_report,confusion_matrix # classification report purposes

"""
Preparing X (feature set variables) and y(target variable)

"""

X_tr = sparse_train
y_tr = data_train['outcome_code']

X_te = sparse_test
y_te = data_test['outcome_code']

X_tr.shape , X_te.shape

from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(test_y, predict_y):

    # C = 2,2  matrix, each cell (i,j) represents number of points of class i are predicted class j
    C = confusion_matrix(test_y, predict_y)
    print("Number of misclassified points ",(len(test_y)-np.trace(C))/len(test_y)*100)
    A =(((C.T)/(C.sum(axis=1))).T)
    B =(C/C.sum(axis=0))


    labels = [0,1]
    cmap=sns.light_palette("green")

    #Confusion matrix

    print("-"*50, "Confusion matrix", "-"*50)
    plt.figure(figsize=(10,5))
    sns.heatmap(C, annot=True, cmap=cmap, fmt=".3f", xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Class')
    plt.ylabel('Original Class')
    plt.show()

    #Precision matrix

    print("-"*50, "Precision matrix", "-"*50)
    plt.figure(figsize=(10,5))
    sns.heatmap(B, annot=True, cmap=cmap, fmt=".3f", xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Class')
    plt.ylabel('Original Class')
    plt.show()
    print("Sum of columns in precision matrix",B.sum(axis=0))

    #Recall matrix


    print("-"*50, "Recall matrix"    , "-"*50)
    plt.figure(figsize=(10,5))
    sns.heatmap(A, annot=True, cmap=cmap, fmt=".3f", xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Class')
    plt.ylabel('Original Class')
    plt.show()
    print("Sum of rows in precision matrix",A.sum(axis=1))

def hyperparameter_of_the_model(model,parameters,X_train,y_train):

    #use gridsearch to test all values
    clf = RandomizedSearchCV(model,
                             parameters,
                             n_iter=5,
                             cv=10 ,
                             refit = True,
                             verbose = 3,
                             scoring='roc_auc',
                             return_train_score=True,
                             n_jobs=-1)


    #fit model to data
    clf.fit(X_train, y_train)

    #find the best tuned parameters
    best_parameter=clf.best_estimator_
    print("Best hyper parameter of the model is " , best_parameter)

"""Logistic regression
Find the best hyper parameter
"""

#Parameter input values
parameters = {
    'C': [0.00001,0.0001, 0.001,0.01,0.1,1,5,10,50,100],
    'max_iter': list(range(100,800,100))
}

#model input
model = LogisticRegression()

hyperparameter_of_the_model(model,parameters,X_tr,y_tr)

"""Train the model with best parameters"""

#train with best hyperparameters
final_model=LogisticRegression(C=50, max_iter=200)

#model train
final_model.fit(X_tr , y_tr)

#save model
joblib.dump(final_model, r'C:\Users\pradeep\Desktop\ml_models\LogisticRegression_without_sampling.joblib')

#predict the model output

y_train_pred = final_model.predict(X_tr)

y_test_pred = final_model.predict(X_te)

print('Train f1 score',f1_score(y_tr,y_train_pred))

print("*-"*25)

print('Test f1 score',f1_score(y_te,y_test_pred))

print('Train precision score',precision_score(y_tr,y_train_pred))

print("*-"*25)

print('Test precision score',precision_score(y_te,y_test_pred))

print('Train accuracy score',accuracy_score(y_tr,y_train_pred))

print("*-"*25)

print('Test accuracy score',accuracy_score(y_te,y_test_pred))

print('Train recall score',recall_score(y_tr,y_train_pred))

print("*-"*25)

print('Test recall score',recall_score(y_te,y_test_pred))

#Confusion Matrix

print(" Train confusion matrix ")
plot_confusion_matrix(y_tr, y_train_pred)

print(" Test confusion matrix ")
plot_confusion_matrix(y_te, y_test_pred)

final_model = joblib.load(r'C:\Users\pradeep\Desktop\ml_models\LogisticRegression_without_sampling.joblib')

"""Random Forest
Find the best hyper parameter
"""

#Parameter input values
parameters = {"n_estimators":sp_randint(105,125),
              "max_depth": sp_randint(10,15),
              "min_samples_split": sp_randint(110,190),
              "min_samples_leaf": sp_randint(25,65)}

#model input
model=RandomForestClassifier()

hyperparameter_of_the_model(model,parameters,X_tr,y_tr)

#train with best hyperparameters
final_model=RandomForestClassifier(max_depth=14, min_samples_leaf=50, min_samples_split=133,n_estimators=113)

#model train
final_model.fit(X_tr , y_tr)

#save model
joblib.dump(final_model, r'C:\Users\pradeep\Desktop\ml_models\RandomForestClassifier_without_sampling.joblib')

#predict the model output

y_train_pred = final_model.predict(X_tr)

y_test_pred = final_model.predict(X_te)

print('Train f1 score',f1_score(y_tr,y_train_pred))

print("*-"*25)

print('Test f1 score',f1_score(y_te,y_test_pred))

print('Train precision score',precision_score(y_tr,y_train_pred))

print("*-"*25)

print('Test precision score',precision_score(y_te,y_test_pred))

print('Train recall score',recall_score(y_tr,y_train_pred))

print("*-"*25)

print('Test recall score',recall_score(y_te,y_test_pred))

#Confusion Matrix

print(" Train confusion matrix ")
plot_confusion_matrix(y_tr, y_train_pred)

"""Standardizing data using StandardScaler"""

scaler = StandardScaler().fit(X)
X = scaler.transform(X)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, classification_report, confusion_matrix, accuracy_score
import joblib

# Create an instance of DecisionTreeClassifier() called dtree and fit it to the training data.
dtree = DecisionTreeClassifier(criterion='gini', max_depth=None)
dtree.fit(X_tr, y_tr)

predictions = dtree.predict(X_te)

# Calculate precision, recall, and accuracy for both the training and test sets
train_precision = precision_score(y_tr, dtree.predict(X_tr))
test_precision = precision_score(y_te, predictions)

train_recall = recall_score(y_tr, dtree.predict(X_tr))
test_recall = recall_score(y_te, predictions)

train_accuracy = accuracy_score(y_tr, dtree.predict(X_tr))
test_accuracy = accuracy_score(y_te, predictions)

# Confusion Matrix
print("Test confusion matrix")
cm = confusion_matrix(y_te, predictions)
print(cm)
print("Accuracy of prediction:", round((cm[0, 0] + cm[1, 1]) / cm.sum(), 3))

# Tabular representation of precision, recall, and accuracy
import pandas as pd

results = pd.DataFrame({
    'Set': ['Train', 'Test'],
    'Precision': [train_precision, test_precision],
    'Recall': [train_recall, test_recall],
    'Accuracy': [train_accuracy, test_accuracy]
})

print(results)

# Save the model
joblib.dump(dtree, r'C:\Users\pradeep\Desktop\ml_models\DecisionTreeClassifier_without_sampling.joblib')

import seaborn as sns
import matplotlib.pyplot as plt

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', cbar=False)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Save the model
joblib.dump(dtree, r'C:\Users\pradeep\Desktop\ml_models\KNN_classifier.joblib')

from sklearn.metrics import ConfusionMatrixDisplay

# Parameter input values
parameters = {
    "criterion": ['gini', 'entropy'],
    "max_depth": [None, 10, 15, 20],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

# Model input
model = DecisionTreeClassifier()

hyperparameter_of_the_model(model, parameters, X_tr, y_tr)

# Best hyperparameters
best_params = {
    "criterion": 'gini',
    "max_depth": None,
    "min_samples_split": 2,
    "min_samples_leaf": 1
}

# Train with best hyperparameters
final_model = DecisionTreeClassifier(**best_params)
final_model.fit(X_tr, y_tr)

# Save model
joblib.dump(final_model, r'C:\Users\pradeep\Desktop\ml_models\DecisionTreeClassifier.joblib')

# Predict the model output
y_train_pred = final_model.predict(X_tr)
y_test_pred = final_model.predict(X_te)

print("Train precision score:", precision_score(y_tr, y_train_pred))
print("Test precision score:", precision_score(y_te, y_test_pred))

print("Train recall score:", recall_score(y_tr, y_train_pred))
print("Test recall score:", recall_score(y_te, y_test_pred))

# Confusion Matrix
print("Train confusion matrix:")
disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_te, y_test_pred), display_labels=final_model.classes_)
disp.plot(cmap=plt.cm.Blues, values_format='d')

# Accuracy
train_accuracy = accuracy_score(y_tr, y_train_pred)
test_accuracy = accuracy_score(y_te, y_test_pred)

# F1 Score
train_f1 = f1_score(y_tr, y_train_pred)
test_f1 = f1_score(y_te, y_test_pred)

print("Train F1 Score:", train_f1)
print("Test F1 Score:", test_f1)

print("Train Accuracy:", train_accuracy)
print("Test Accuracy:", test_accuracy)

"""(ii) KNN Classification"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

# Create and fit the KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_tr, y_tr)

# Make predictions on the test set
pred = knn.predict(X_te)

# Print classification report and confusion matrix
print(classification_report(y_te, pred))
cm1 = confusion_matrix(y_te, pred)
print(cm1)
print("Accuracy of prediction:", round((cm1[0, 0] + cm1[1, 1]) / cm1.sum(), 3))

# Display confusion matrix
disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=knn.classes_)
disp1.plot(cmap=plt.cm.Blues, values_format='d')
plt.title('Confusion Matrix for KNN Model')
plt.show()

import pickle

with open('KNN.pkl', 'wb') as file:
    pickle.dump(knn, file)

# Create an instance of KNeighborsClassifier() called knn and fit it to the training data
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_tr, y_tr)

# Predictions
y_train_pred = knn.predict(X_tr)
y_test_pred = knn.predict(X_te)

# Accuracy, Precision, Recall, and F1 Score
train_accuracy = accuracy_score(y_tr, y_train_pred)
test_accuracy = accuracy_score(y_te, y_test_pred)
train_precision = precision_score(y_tr, y_train_pred)
test_precision = precision_score(y_te, y_test_pred)
train_recall = recall_score(y_tr, y_train_pred)
test_recall = recall_score(y_te, y_test_pred)
train_f1 = f1_score(y_tr, y_train_pred)
test_f1 = f1_score(y_te, y_test_pred)

# Print Accuracy, Precision, Recall, and F1 Score
print("Train Accuracy:", train_accuracy)
print("Test Accuracy:", test_accuracy)
print("Train Precision:", train_precision)
print("Test Precision:", test_precision)
print("Train Recall:", train_recall)
print("Test Recall:", test_recall)
print("Train F1 Score:", train_f1)
print("Test F1 Score:", test_f1)

import pandas as pd

# Create a dictionary to store the results of each model
results = {
    'Model': ['Random Forest', 'Decision Tree', 'K-Nearest Neighbors','Logistic Regression'],
    'F1 Score': [0.9796847179398099, 0.991985018083105, 0.9754116108469527,0.9590309574249983 ],
    'Precision': [0.9981063622688258, 0.9993076829880402,0.9908500642255107,0.9606393538008694],
    'Recall': [0.9619307521746546,0.9847688896469384,0.9604468702029678,0.9574279379157428]
}

# Create a DataFrame from the results dictionary
results_df = pd.DataFrame(results)

# Display the results
print("TRAIN DATA")
print(results_df)

import matplotlib.pyplot as plt

models = ['Random Forest', 'Decision Tree', 'K-Nearest Neighbors', 'Logistic Regression']
f1_scores =  [0.9796847179398099, 0.991985018083105, 0.9754116108469527, 0.9590309574249983]
precisions =  [0.9981063622688258, 0.9993076829880402, 0.9908500642255107, 0.9606393538008694]
recall = [0.9619307521746546, 0.9847688896469384, 0.9604468702029678, 0.9574279379157428]

# Create a bar plot for F1 scores
plt.figure(figsize=(10, 6))
plt.bar(models, f1_scores, color='skyblue', label='F1 Score')
plt.xlabel('Models')
plt.ylabel('F1 Score')
plt.title('Comparison of F1 Score for Different Models')
plt.legend()

# Create a bar plot for precision
plt.figure(figsize=(10, 6))
plt.bar(models, precisions, color='lightcoral', label='Precision')
plt.xlabel('Models')
plt.ylabel('Precision')
plt.title('Comparison of Precision for Different Models')
plt.legend()

# Create a bar plot for recall
plt.figure(figsize=(10, 6))
plt.bar(models, recall, color='lightgreen', label='Recall')
plt.xlabel('Models')
plt.ylabel('Recall')
plt.title('Comparison of Recall for Different Models')
plt.legend()

# Show the plots
plt.show()

import pandas as pd

# Create a dictionary to store the results of each model
results_test = {
    'Model': ['Random Forest', 'Decision Tree', 'K-Nearest Neighbors','Logistic Regression'],
    'F1 Score': [0.7151841868823, 0.7358586559363581, 0.7503222242680906,0.7211293682018051 ],
    'Precision': [0.9094407696933253, 0.904984,0.9165542060278903,0.8879516698962726],
    'Recall': [0.5893079800498753, 0.621259,0.6351309226932669,0.607076059850374]
}

# Create a DataFrame from the results dictionary
results_test_df = pd.DataFrame(results_test)

# Display the results
print("TEST DATA")
print(results_test_df)

import matplotlib.pyplot as plt

models = ['Random Forest', 'Decision Tree', 'K-Nearest Neighbors', 'Logistic Regression']
f1_scores = [0.7151841868823, 0.7358586559363581, 0.7503222242680906, 0.7211293682018051]
precision = [0.9094407696933253, 0.904984, 0.9165542060278903, 0.8879516698962726]
recall = [0.5893079800498753, 0.621259, 0.6351309226932669, 0.607076059850374]

# Create a bar plot for F1 scores
plt.figure(figsize=(10, 6))
plt.bar(models, f1_scores, color='skyblue', label='F1 Score')
plt.xlabel('Models')
plt.ylabel('F1 Score')
plt.title('Comparison of F1 Score for Different Models')
plt.legend()

# Create a bar plot for precision
plt.figure(figsize=(10, 6))
plt.bar(models, precision, color='lightcoral', label='Precision')
plt.xlabel('Models')
plt.ylabel('Precision')
plt.title('Comparison of Precision for Different Models')
plt.legend()

# Create a bar plot for recall
plt.figure(figsize=(10, 6))
plt.bar(models, recall, color='lightgreen', label='Recall')
plt.xlabel('Models')
plt.ylabel('Recall')
plt.title('Comparison of Recall for Different Models')
plt.legend()

# Show the plots
plt.show()

import pandas as pd

selected_features = ['flag', 'serror_rate', 'diff_srv_rate', 'srv_serror_rate',
                     'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_diff_srv_rate',
                     'count', 'service', 'dst_host_count', 'rerror_rate',
                     'srv_rerror_rate', 'dst_host_rerror_rate', 'protocol_type',
                     'dst_host_srv_rerror_rate']

# Create a new DataFrame with only the selected features
new_df = data_train[selected_features]

# Now new_df contains only the columns specified in selected_features

new_df