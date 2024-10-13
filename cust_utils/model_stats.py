import numpy as np
import pandas as pd
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate
from datetime import datetime


def model_stats(X_train:pd.DataFrame , y_train:pd.DataFrame,
                models:sklearn.pipeline.Pipeline | sklearn.base.BaseEstimator, 
                preprocessors: sklearn.pipeline.Pipeline,
                folds: int|sklearn.model_selection._split.StratifiedKFold,
                scoring:list|str|None):
    
    final_pipeline =Pipeline(
        steps=[('preprocessing', preprocessors),
               ('model', models)]
    )

    base = cross_validate(
        estimator=final_pipeline,
        X = X_train,
        y = y_train.values.ravel(),
        cv=folds,
        scoring=scoring,
        verbose=1
    )

    model_name = str(type(final_pipeline.named_steps['model']))[8:-2].split('.')[-1]
    scores = dict()
    for i in base:
        if i.startswith('test_'):
            v = np.round(base[i].mean(), 4).item()
            k = i.replace('test_','')
            scores[k] = v
    
    pre_trans = [i[1] for i in preprocessors.transformers]
    hyperparams = models.get_params()

    dt_now = datetime.now().strftime('%m/%d/%Y %H:%M')
    df = pd.DataFrame({'Model':[model_name], 
                       'M/S': [scores], 
                       'Hyperparameters': [hyperparams] ,
                       'Preprocessors':[pre_trans],
                       'Folds': [folds], 
                       'Insert D/T':dt_now})\
        .set_index('Model')

    return df