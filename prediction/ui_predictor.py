if __name__ == "__main__":
    print("Welcome to HOW TO WIN AT REDDIT")
    print("1.) RandomForestPipeline")
    print("2.) SVMPipeline")
    print("3.) NaiveBayesPipeline")

    flag = True
    while (flag == True):
        selection = input("Please select an option ")
        selection = int(selection)
        if selection == 1:
            # run RandomForestPipeline
            from prediction.random_forest_pipeline import rf_pipeline

            rf_pipeline()
            flag = False
        elif selection == 2:
            # run SVMPipeline
            from prediction.svm_pipeline import svm_accuracy

            svm_accuracy()
            flag = False
        elif selection == 3:
            # Run NaiveBayesPipeline
            from prediction.naive_bayes_predictor import bernoulli_nb_pipeline

            bernoulli_nb_pipeline()
            flag = False
        else:
            print("INVALID SELECTION")
