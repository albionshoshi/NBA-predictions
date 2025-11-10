import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

nba_clustered = pd.read_csv("../../Data/after_clustering/NBA_Clustered.csv")
college_stats = pd.read_csv("../../Data/Testing Set/NCAA_2020_2025.csv")

merged_data = pd.merge(
    college_stats,
    nba_clustered[['PLAYER', 'Cluster', 'Cluster_Label']],
    left_on='Name',
    right_on='PLAYER',
    how='inner'
)

college_features = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'FT%', 'TOV']
early_nba_features = ['PTS', 'MP', 'FG%', 'eFG%']
all_features = college_features + early_nba_features

X = merged_data[all_features].copy()
y = merged_data['Cluster'].copy()
X.fillna(X.mean(), inplace=True)

# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train model
log_reg = LogisticRegression(
    multi_class='multinomial',
    solver='lbfgs',
    max_iter=1000,
    random_state=42,
    class_weight='balanced'
)
log_reg.fit(X_train_scaled, y_train)

# 6. Evaluate
y_test_pred = log_reg.predict(X_test_scaled)
test_accuracy = accuracy_score(y_test, y_test_pred)

cluster_names = ['Superstar', 'Starter', 'Role Player', 'Bench', 'Bust']
print(f"Test Accuracy: {test_accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred, target_names=cluster_names))

# 7. Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=cluster_names, yticklabels=cluster_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Logistic Regression Confusion Matrix')
plt.show()

# 8. Feature Importance
feature_importance = pd.DataFrame({
    'Feature': all_features,
    'Importance': np.abs(log_reg.coef_).mean(axis=0)
}).sort_values('Importance', ascending=False)
print("\nTop Features:")
print(feature_importance.head(10))

# 9. Save model
joblib.dump(log_reg, 'logistic_regression_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("\nModel training complete!")