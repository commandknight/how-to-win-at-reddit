# how-to-win-at-reddit
How to Win at Reddit - Predict What posts will become popular

Team:
Jeet Nagda, 28307584, jnagda@uci.edu
Jocelyne Perez, 75243251, jocelymp@uci.edu
Timothie Fujita, 22099524, tfujita@uci.edu


Our Project is divided into two large Modules:
1.) Text_Pipeline
    + Parent Post Pipeline
        This pipeline uses the Reddit API to collect the post information and uses the MySQL Manager to upload
        the information
    + Comment Pipeline
        This pipeline attaches the IDs of all the comments of the original post and uploads them
        using the MySQL Manager into a BLOB
    + Clean Parent Post Table Pipeline
        This pipeline iterates over the databases and identifies which posts are not in English and cleans the posts
    + MySQL Manager
        This manager was the data source connection our MySQL Database
    + Comment DB Manager
        This manager was the data source connection for our SQLite Database of Reddit Comments from Kaggle.com

2.) Prediction (Classifiers)
    + Random Forest
    + SVM
    + Naive Bayes
    + Reporting - This function allows us to print out the best parameters in a readable way
    + PorterTokenizer - A custom Object we created to test Stemming
