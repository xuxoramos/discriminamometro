import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import tree
import pandas as pd
import os

class MagicLoop():
    
    def __init__(self):
        
        return
    
    def correr_magic_loop(self, npClassifier, npDictHyperParams, X_train, Y_train, nbrCv, strScoring):

        npResultados = np.array([])
        for i, classifier in enumerate(npClassifier):
            dictHyperParams = npDictHyperParams[i]
            grid_search = GridSearchCV(classifier,
                                       dictHyperParams,
                                       scoring=strScoring,
                                       cv=nbrCv,
                                       n_jobs=-1,
                                       verbose=3
                                       )
            grid_search.fit(X_train, Y_train)
            npResultados = np.append(npResultados, grid_search)

            # de los valores posibles que pusimos en el grid, cuáles fueron los mejores
            print('grid_search.best_params_: ', grid_search.best_params_)

            # mejor score asociado a los modelos generados con los diferentes hiperparametros
            # corresponde al promedio de los scores generados con los cv
            print('grid_search.best_score_: ', grid_search.best_score_)

            best_model = grid_search.best_estimator_


        return best_model, npResultados
    
    def prep_modelos(self, npModelos):

        npArrayModelos = np.array([])
        for strModelo in npModelos:

            if strModelo == 'DECTREE':
                classifier = tree.DecisionTreeClassifier()
            if strModelo == 'RANDOMF':
                classifier = RandomForestClassifier()
            if strModelo == 'XGBOOST':
                classifier = GradientBoostingClassifier()

            npArrayModelos = np.append(npArrayModelos, classifier)

        return npArrayModelos