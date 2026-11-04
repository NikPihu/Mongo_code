print("Developed by: Nikunj Tangle")
print("Submitted to: Vaishali Ingale Mam")


# import
# load
# missing and duplicate values
# correlation store in selected values
# linear regression for different train sizes
# linear regression (70/30)
# polynomial regression
# compare


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score


df=pd.read_csv("housing.csv")

print("No. of rows:", df.shape[0])
print("No. of columns:", df.shape[1])

print(df.head())


#mising values
print("Number of missing entries:", df.isnull().sum(),"\n")

#duplicated values
print("Number of duplicated entries: ", df.duplicated().sum())


target="median_house_value"

cor=df.corr(numeric_only=True)
cor=cor[target]
cor=cor.drop(target)
cor=cor.abs()
cor=cor.sort_values(ascending=False)

selected_values=list(cor.index[:2])

print(cor,"\n")
print(selected_values)


split_results=[]

#loading the model
linear_model=LinearRegression()

for train_size in np.round(np.arange(0.1,1.0,0.1),1):
    X_train,X_test,Y_train,Y_test=train_test_split(
        
        df[[selected_values[0]]],
        df["median_house_value"],
        train_size=train_size,
        random_state=42
    )
    
    linear_model.fit(X_train,Y_train)
    
    train_pred=linear_model.predict(X_train)
    test_pred=linear_model.predict(X_test)
    
    split_results.append(
        {
            "Training_Percentage": int(train_size*100),
            "Testing_Percentage": int(round((1-train_size)*100)),
            "Train_MSE": mean_squared_error(Y_train,train_pred),
            "Test_MSE": mean_squared_error(Y_test,test_pred),
        }
    )
    
split_results_df=pd.DataFrame(split_results)
    
print(
    split_results_df[[
        "Training_Percentage",
        "Testing_Percentage",
        "Train_MSE",
        "Test_MSE"
    ]]
)


plt.plot(split_results_df["Training_Percentage"],split_results_df["Train_MSE"],marker="o",label="Train MSE")
plt.plot(split_results_df["Training_Percentage"],split_results_df["Test_MSE"],marker="o",label="Test MSE")
plt.xlabel("Training Percentage")
plt.ylabel("MSE")
plt.legend()
plt.show()


X_train,X_test,Y_train,Y_test=train_test_split(
    df[[selected_values[0]]],
    df["median_house_value"],
    test_size=0.3,
    random_state=42
)

linear_model.fit(X_train,Y_train)

linear_train_pred=linear_model.predict(X_train)
linear_test_pred=linear_model.predict(X_test)

#equation
print("Median_House_Value=", f"{linear_model.coef_[0]:.4f}*{selected_values[0]}+{linear_model.intercept_:.4f}")

print("Train MSE:", mean_squared_error(Y_train,linear_train_pred))
print("Test MSE:", mean_squared_error(Y_test,linear_test_pred))


plt.scatter(X_train[selected_values[0]],Y_train,s=5,label="Actual Train")
plt.scatter(X_test[selected_values[0]],Y_test,s=5,label="Actual test")
plt.plot(X_test[selected_values[0]],linear_test_pred,color="red",label="Prediction")

plt.legend()
plt.show()


X=df[selected_values]
Y=df["median_house_value"]

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=42
)


polynomial_model=make_pipeline(StandardScaler(),PolynomialFeatures(degree=2),LinearRegression())
polynomial_model.fit(X_train,Y_train)
polynomial_pred=polynomial_model.predict(X_test)


ax=plt.figure().add_subplot(111,projection="3d")
ax.scatter(X_test[selected_values[0]],X_test[selected_values[1]],Y_test,s=5)
ax.plot_trisurf(X_test[selected_values[0]],X_test[selected_values[1]],polynomial_pred,color="red",alpha=0.4)
ax.set_xlabel(selected_values[0])
ax.set_ylabel(selected_values[1])
ax.set_zlabel("median_house_value")
plt.show()


results_df=pd.DataFrame({
    "Model":["Linear Regression","Polynomial Regression"],
    "MSE":[
        mean_squared_error(Y_test,linear_test_pred),
        mean_squared_error(Y_test,polynomial_pred)
    ],
    "MAE":[
        mean_absolute_error(Y_test,linear_test_pred),
        mean_absolute_error(Y_test,polynomial_pred)
    ],
    "R2 Score":[
        r2_score(Y_test,linear_test_pred),
        r2_score(Y_test,polynomial_pred)
    ]
    
}).set_index("Model")
print(results_df.round(4))


results_df.plot(
    kind="bar",
    subplots=True,
    layout=(1,3),
    figsize=(12,5),
)
plt.tight_layout()
plt.show()
