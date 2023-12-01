import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load the dataset
file_path = r'd:\고려대 4학년 2학기\캡스톤 디자인\IAT feature\Feature Set\feature_set_last2.csv'
dataset = pd.read_csv(file_path)

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42, class_weight='balanced'))
])

param_grid = {
    'classifier__n_estimators': [100],
    'classifier__max_depth': [10],
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')

X = dataset.drop('label', axis=1)  # Features
y = dataset['label']  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_

clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Predict the response for test dataset
y_pred = grid_search.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Optimized Accuracy: {accuracy}')
print('Optimized Classification Report:')
print(report)