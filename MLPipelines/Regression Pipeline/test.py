# Authors: CS-World Domination Summer19 - DM
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import utils
from sklearn import datasets
from sklearn import preprocessing
from sklearn import model_selection # MinMaxScaler,StandardScaler
from sklearn.feature_selection import f_regression,mutual_info_regression,SelectKBest
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
# Importing various ML algorithms
from sklearn import metrics, svm
from sklearn import linear_model
from sklearn import cross_decomposition
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor,RandomForestRegressor

# NOTE: I strongly recommend that you look at the README and its additional resources before 
#       looking at my code and as a reference if you get confused at any point

def onehot(df):
    """One hot encodes the features: cylinders and origin"""
    # One-hot encode cylinders
    cyl4 = []
    cyl6 = []
    cyl8 = []
    for num in df['cylinders']:
        cyl8.append(1) if 8 == num else cyl8.append(0)
        cyl6.append(1) if 6 == num else cyl6.append(0)
        cyl4.append(1) if 4 == num else cyl4.append(0)
    df['cyl4'] = pd.Series(cyl4)
    df['cyl6'] = pd.Series(cyl6)
    df['cyl8'] = pd.Series(cyl8)
    df = df.drop('cylinders', axis=1)
    # One-hot encode origin
    amer = []
    euro = []
    jap = []
    for num in df['origin']:
        amer.append(1) if 1 == num else amer.append(0)
        euro.append(1) if 2 == num else euro.append(0)
        jap.append(1) if 3 == num else jap.append(0) 
    df['american'] = pd.Series(amer)
    df['european'] = pd.Series(euro)
    df['japanese'] = pd.Series(jap)
    df = df.drop('origin', axis=1)
    return df

def featurefy(df):
    """ Modifies the missing values in the horsepower feature. Also creates two new features, diesel and station wagon,
        from car name"""
    # NOTE: Six values are missing horsepower, so we replace those values with the column mean below
    #       Alternatively you could just drop the entries with missing data using: df = df.dropna()
    df['horsepower'] = df['horsepower'].replace('?', np.NaN)
    df['horsepower'] = df['horsepower'].map(np.float64)
    df['horsepower'].fillna( df['horsepower'].mean(), inplace=True )
    # Create new features
    dieselList = []
    swList = []
    for name in df['car name']:
        dieselList.append(1) if "diesel" in name else dieselList.append(0)
        swList.append(1) if ("(sw)" in name) or ("wagon" in name) else swList.append(0)
    df['diesel'] = pd.Series(dieselList)
    df['station wagon'] = pd.Series(swList)
    return df

def multicollCheck(df):
    """ Checks for multicollinearity using VIF scores, the included link explains when checking is important"""
    print("\n+++ Checking for multicollinearity! +++\n")
    print("NOTE: I was unable to get the warning to go away, so that task is left to the reader!")
    # https://stats.stackexchange.com/questions/168622/why-is-multicollinearity-not-checked-in-modern-statistics-machine-learning#168631
    # https://blog.minitab.com/blog/adventures-in-statistics-2/what-are-the-effects-of-multicollinearity-and-when-can-i-ignore-them
    # https://blog.minitab.com/blog/understanding-statistics/handling-multicollinearity-in-regression-analysis
    # Check for multicollinearity!
    # A rule of thumb is that if there are VIF scores of more than five to ten, your variables are multicollinear!!!
    # However, do know that (rarely) you can have low VIF's and still have multicollinearity...
    df = df.drop('mpg', axis=1)
    # Drop the one-hot variables so they aren't checked: dummy variables will always have high VIF's
    df = df.drop('cyl4', axis=1)
    df = df.drop('cyl6', axis=1)
    df = df.drop('cyl8', axis=1)
    df = df.drop('american', axis=1)
    df = df.drop('european', axis=1)
    df = df.drop('japanese', axis=1)
    # https://stackoverflow.com/questions/42658379/variance-inflation-factor-in-python
    # Intercept
    X = add_constant(df)
    vif = pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])],index=X.columns)
    print(vif)
    return

def featureSelect(df):
    """ Univariate feature selection using scikit's SelectKBest and f_regression"""
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.f_regression.html#sklearn.feature_selection.f_regression
    df = df.drop('diesel', axis=1)
    df = df.drop('origin', axis=1)
    featureList = list(df.columns.values)
    array = df.values
    X = array[:,1:]
    Y = array[:,0 ]
    print(X.shape)
    print(featureList[1:])
    print(X[0])
    # feature extraction: using either f_regression or mutual_info_regression, select the k best features
    test = SelectKBest(f_regression, k=3).fit_transform(X, Y)
    print(test.shape)
    print(test[0])
    print()
    return

    # return df

def loadData(size):
    """Loads data from a csv and gets it into a workable format.
       The size param specifies how much of the data you want split into testing/training"""
    
    # Read the file w/header as row 0
    df = pd.read_csv('auto-complete.csv', header=0)
    df2 = pd.read_csv('auto-missing.csv', header=0)

    # Create/modify new features and drop unused ones
    df = featurefy(df)
    df = df.drop('car name', axis=1)
    df = df.drop('model year', axis=1)
    visualizeData(df)
    df = onehot(df)
    # Visualize Data
    
    # Check for multicollinearity
    multicollCheck(df)
    # Drop features with high VIF's (unnecessary step)
    df = df.drop('displacement', axis=1)

    # featureSelect(df)

    # NOTE: There were missing mpg values in the original data, found some/made best guess online using fuelly.com
    df2 = featurefy(df2)
    df2 = onehot(df2)
    df2 = df2.drop('model year', axis=1)
    df2 = df2.drop('car name', axis=1)
    # df2 = df2.drop('station wagon', axis=1)
    df2 = df2.drop('displacement', axis=1)
    X_unknown = df2.iloc[:,1:].values
    y_unknown = df2[ 'mpg' ].values
    
    # Organizing data into training/testing

    # .values converts df to numpy array
    X_known = df.iloc[:,1:].values           # iloc == "integer locations" of rows/cols
    y_known = df[ 'mpg' ].values             # individually addressable columns (by name)

    # It's good practice to scramble/shuffle your data!
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X_known, y_known, test_size=size, shuffle=True, random_state=None)

    return X_known, y_known, X_unknown, y_unknown, X_train, y_train, X_test, y_test

def scaleData(X_train, X_test):
    """Scales data in two different ways"""
    # https://www.kaggle.com/discdiver/guide-to-scaling-and-standardizing

    # Fits to range (0 to 1)
    """Normalization is useful when your data has varying scales and the algorithm 
    you are using does not make assumptions about the distribution of your data, 
    such as k-nearest neighbors and artificial neural networks."""
    # https://machinelearningmastery.com/normalize-standardize-machine-learning-data-weka/
    # mm_scaler = preprocessing.MinMaxScaler()
    # X_train[:4] = mm_scaler.fit_transform(X_train[:4])
    # X_test[:4] = mm_scaler.fit_transform(X_test[:4])
    
    # Fits to range (-1 to 1)
    """Standardization is useful when your data has varying scales and the algorithm 
    you are using does make assumptions about your data having a Gaussian distribution, 
    such as linear regression, logistic regression and linear discriminant analysis"""
    # https://machinelearningmastery.com/normalize-standardize-machine-learning-data-weka/
    s_scaler = preprocessing.StandardScaler()
    X_train[:,:3] = s_scaler.fit_transform(X_train[:,:3])
    X_test[:,:3] = s_scaler.fit_transform(X_test[:,:3])

    return X_train, X_test

def visualizeData(df):
    """It is often a good idea to visualize your data before you start working with it.
       See the link for the example I used. There's a lot more out there too."""
    # https://machinelearningmastery.com/visualize-machine-learning-data-python-pandas/
    from pandas.plotting import scatter_matrix
    # scatter_matrix(df)
    # df.hist()
    # df.plot(kind='density', subplots=True, layout=(4,4), sharex=False)
    plt.show()
    return

def boxPlot(results, names, metric):
    """ This box plot shows the spread of the data, NOT the confidence interval!!! 
        The box extends from the lower to upper quartile values of the data, with a line at the median. 
        The whiskers extend from the box to show the range of the data. Dots are outliers"""
    fig = plt.figure()
    fig.suptitle('Algorithm '+metric+' Comparison')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    plt.show()
    return

def crossValidation(X_train, y_train):
    "Do cross validation tests on your data to help determine the best model and the best params"
    print("\n\n+++ Starting algorithm comparison through cross-validation! +++")
    # Make a list models to cross-validate
    models = []
    models.append( ("Decision Trees     ",DecisionTreeRegressor()) )
    models.append( ("Random Forests     ",RandomForestRegressor(n_estimators=20)) )
    models.append( ("Very Random Forests",ExtraTreesRegressor(n_estimators=20)) )
    models.append( ("OLS                ",linear_model.LinearRegression()) )
    models.append( ("SVR                ",svm.SVR(gamma="scale")) )
    models.append( ("BayesianRidge      ",linear_model.BayesianRidge()) )
    models.append( ("PassiveAggressive  ",linear_model.PassiveAggressiveRegressor()) )
    models.append( ("SGD                ",linear_model.SGDRegressor()) )
    # models.append( ("ARD                ",linear_model.ARDRegression()) )

    # Loop through and evaluate each model
    r2Results = []
    maeResults = []
    rmseResults = []
    names = []
    rankList = []
    # NOTE: See different scoring params: https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
    scoring = ['r2','neg_mean_absolute_error', 'neg_mean_squared_error']
    print("\n*** Results show the means (of the cross-validating) for each scoring metric, with standard deviation in parenthesis")
    print("\nAlgorithm          : R Squared, Mean Absolute Error, Root Mean Squared Error")
    for name, model in models:
        kfold = model_selection.KFold(n_splits=5, random_state=None)
        cv_scores = model_selection.cross_validate(model, X_train, y_train, cv=kfold, scoring=scoring)
        r2 = cv_scores["test_r2"]
        mae = (-1)*cv_scores["test_neg_mean_absolute_error"]
        mse = (-1)*cv_scores["test_neg_mean_squared_error"]
        rmse = np.array(list(map(lambda x: math.sqrt(x), mse)))
        r2Results.append(r2)
        maeResults.append(mae)
        rmseResults.append(rmse)
        names.append(name.strip())
        rankList.append([name.strip(), r2.mean()])
        print( "%s: %0.3f (%0.3f)," % (name, r2.mean(), r2.std()),
               "%.3f (%0.3f)," % (mae.mean(), mae.std()),
               "%.3f (%0.3f)" % (rmse.mean(), rmse.std()) )
    # Summarization/Analysis of results
    rankList = sorted( rankList, key=lambda x: x[1], reverse=True )
    print("\nThe best algorithm after ranking r2 is: "+rankList[0][0])
    # boxPlot(r2Results, names, "R Squared")             # Larger (higher) is better
    # boxPlot(maeResults, names, "Mean Absolute Error")  # Smaller (lower) is better
    # boxPlot(rmseResults, names, "Mean Squared Error")   # Smaller (lower) is better
    return

def trainModel(X_train, y_train, X_test, y_test):
    "Stub: This is where you would fine-tune a single model."
    pass

def predictUnknown(X_known, y_known, X_unknown, y_unknown):
    """Makes predictions on the unknown data"""
    print("\n\n+++ Starting the prediction of unknown data! +++")
    model = ExtraTreesRegressor(n_estimators=20)
    # model = linear_model.LinearRegression()
    model.fit(X_known, y_known)
    predictions = model.predict(X_unknown)
    print("Note that since the actual values are mostly a best-guess estimation of mine and that "+
    "Regression tends to give imprecise predictions, \nyou should expect 'larger' errors.\n")
    print("Prediction         :",list(map(lambda x: float("%.1f"%x),predictions)))
    print("Actual             :",list(map(lambda x: float("%.3f"%x), y_unknown)))
    ErrorList = []
    for i in range(len(predictions)):
        ErrorList.append(predictions[i]-y_unknown[i])
    ErrorList[-1] = "Na"
    print("Absolute Error     :",list(map(lambda x: x if type(x)==str else float("%.1f"%x), ErrorList)))
    print("Mean Absolute Error: ",round(mean_absolute_error(y_unknown[:-1],predictions[:-1]), 1))
    return


def main():
    (X_known, y_known, X_unknown, y_unknown,
    X_train, y_train, X_test, y_test) = loadData(0.20)  # Loads the csv file, input sets training size

    (X_train, X_test) = scaleData(X_train, X_test) # W/O scaling, SGD and PassAgg get some ridiculous r2 values

    crossValidation(X_train, y_train)                       # Compare different algorithms
    trainModel(X_train, y_train, X_test, y_test)            # Run the best algorithm on the test/train data
    predictUnknown(X_known, y_known, X_unknown, y_unknown)
if __name__ == "__main__":
    main()
