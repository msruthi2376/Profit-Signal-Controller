import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("sales_data_sample.csv", encoding='latin1')

# Show first rows
print("Sample Data:\n", data.head())

# Create Profit Category (Target)
# If profit > average → HIGH else LOW
avg_profit = data['Profit'].mean()
data['Profit_Label'] = data['Profit'].apply(lambda x: 1 if x > avg_profit else 0)

# Features & Target
X = data[['Sales', 'Quantity', 'Discount']]
y = data['Profit_Label']

# Handle missing values if any
X = X.fillna(0)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", round(accuracy*100,2), "%")

# Show predictions
print("\nPredictions:")
for i in range(10):
    label = "HIGH PROFIT 📈" if y_pred[i] == 1 else "LOW PROFIT 📉"
    print(f"Record {i+1}: {label}")

# Total Profit Calculation
total_profit = data['Profit'].sum()
print("\nTotal Profit:", total_profit)
