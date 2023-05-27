* General machine learning practices

# [Machine Learning Scripting](https://github.com/ashioyajotham/ML-Algorithms/blob/main/ML%20Scripting.ipynb)
* For our first file, we use the `IRIS` dataset, considered as the "hello world" of machine learning to classify flowers in Python through the command-line.
  It is basically similar to using Jupyter notebooks but slightly different in syntax and easier.
* The machine learning algorithms include:
         - `Support Vector Machine (SVM)`
         - `KNeighbors Classifier (KNN)`
         - `Decision Tree Classifier (CART)`
         - `Linear Discriminant Analysis (LDA)`
         - `Logistic Regression (LR)`
         - `Gaussian Naive Bayes (NB)`
        
 * The evaluation metrics include:
         - `Accuracy Score`
         - `Confusion Matrix`
         - `Classification Report`

* Model generalization performance:
         - `StratifiedKFold`




# [Modelling Non-Linear Features-Target Relationship](https://github.com/ashioyajotham/ML-Algorithms/blob/main/linear-regression-non-linear-btn-data-and-target.ipynb)
* Linear regression with non-linear link between data and target
* The deployment of scikit-learn in linear models in this case, Linear Regression
* Machine learning modelling alogorithms:
         - Linear Regression
         - Decision Tree Regressor
         
* Dealing with non-linearity;
        i) choose a model that can natively deal with non-linearity,
       ii) engineer a richer set of features by including expert knowledge which can
                be directly used by a simple linear model, or
      iii) use a "kernel" to have a locally-based decision function instead of a
            global linear decision function.

CC: [inria Machine learning in Python with scikit-learn](https://inria.github.io/scikit-learn-mooc/)
    (https://www.inria.fr/en/mooc-scikit-learn)
    
    
    

# [Orinary Least Squares (OLS) algorithm](https://github.com/ashioyajotham/ML-Algorithms/blob/main/ols-models.ipynb)
* This case we take a closer look at the OLS model from the `statsmodels` library




# [Titanic](https://github.com/ashioyajotham/ML-Algorithms/blob/main/titanic-classification.ipynb)
* Of course it can't be complete without the "hello world" of machine learning. Here we look at `Random Classifiers` and `Logistic Regression`



# Linear Regression
*  linear regression was developed in the field of statistics and is studied as a model for understanding the relationship between input and output numerical variables, but has been borrowed by machine learning. It is both a statistical algorithm and a machine learning algorithm.
*  Linear regression is a linear model, e.g. a model that assumes a linear relationship between the input variables (x) and the single output variable (y). More specifically, that y can be calculated from a linear combination of the input variables (x).
*  When there is a single input variable (x), the method is referred to as simple linear regression. When there are multiple input variables, literature from statistics often refers to the method as multiple linear regression.
*  Different techniques can be used to prepare or train the linear regression equation from data, the most common of which is called Ordinary Least Squares. It is common to therefore refer to a model prepared this way as [Ordinary Least Squares Linear Regression or just Least Squares Regression](https://github.com/ashioyajotham/Daily-ML/blob/main/ols-models.ipynb).
