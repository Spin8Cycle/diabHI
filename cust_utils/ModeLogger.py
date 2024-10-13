import numpy as np
from datetime import datetime
import os
import pandas as pd
import ast
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate


class ModeLogger:
    def __init__(self, file_path, sheet_name='Model Stats'):
        self.file_path = file_path
        self.sheet_name = sheet_name
        

    def _str_to_dict(self, row):
        return ast.literal_eval(row)
    
    def _df(self, file_path, sheet_name):
        if os.path.exists(self.file_path):
            df = pd.read_excel(self.file_path, 
                                        sheet_name=self.sheet_name, 
                                        engine='openpyxl', 
                                        index_col=0)
            return df
        
    def train(self, 
            X_train:pd.DataFrame, y_train:pd.DataFrame,
            models:sklearn.pipeline.Pipeline | sklearn.base.BaseEstimator, 
            preprocessors: sklearn.pipeline.Pipeline,
            folds: int|sklearn.model_selection._split.StratifiedKFold,
            scoring:list|str|None
        ):
        self.models = models
        self.preprocessors = preprocessors
        self.folds = folds
        self.scoring = scoring


        self.final_pipeline =Pipeline(
        steps=[('preprocessing', preprocessors),
               ('model', models)]
        )

        self.base = cross_validate(
            estimator=self.final_pipeline,
            X = X_train,
            y = y_train.values.ravel(),
            cv=folds,
            scoring=scoring,
            verbose=1
        )

        #return (self.base, self.final_pipeline, self.models, self.preprocessors, self.folds, self.scoring)

    def model_stats(self):
        model_name = str(type(self.final_pipeline.named_steps['model']))[8:-2].split('.')[-1]
        scores = dict()
        for i in self.base:
            if i.startswith('test_'):
                v = np.round(self.base[i].mean(), 4).item()
                k = i.replace('test_','')
                scores[k] = v
        
        pre_trans = [i[1] for i in self.preprocessors.transformers]
        hyperparams =  self.models.get_params()

        dt_now = datetime.now().strftime('%m/%d/%Y %H:%M')
        self.stats = pd.DataFrame({'Model':[model_name], 
                        'M/S': [scores], 
                        'Hyperparameters': [hyperparams] ,
                        'Preprocessors':[pre_trans],
                        'Folds': [self.folds], 
                        'Insert D/T':dt_now})\
            .set_index('Model')

        return self.stats

    def stats_to_excel(self, ext_data=None):
        
        if ext_data:
            self.new_data = ext_data
        else:
            self.new_data = self.stats

        existing_df = self._df(file_path=self.file_path, 
                               sheet_name=self.sheet_name)
        if os.path.exists(self.file_path):
            new_index = self.new_data.index[0]
            if new_index in existing_df.index:
                existing_row = existing_df.loc[[new_index]].drop(columns='Insert D/T')
                new_row_values = self.new_data.loc[[new_index]].drop(columns='Insert D/T')

                for i in range(len(existing_row)):
                    x = existing_row.iloc[[i]]
                    if (x.values[0] == [str(i) for i in new_row_values.values[0]]).all().any():
                        print("Row already exists in the Excel file with the same values.")
                        return
            else:
                print("Appending the new row.")

        else:
            updated_df = self.new_data
        
        with pd.ExcelWriter(self.file_path, mode='w', engine='openpyxl') as writer:
            updated_df.to_excel(writer, sheet_name=self.sheet_name, index=True)

    def show_rank(self):
        ext_scores = 'Metrics:Scores'
        existing_df = self._df(file_path=self.file_path, 
                               sheet_name=self.sheet_name)
        
        if os.path.exists(self.file_path):
            rank_df = existing_df[['M/S', 'Insert D/T']].set_index(['Insert D/T'])
            rank_df[ext_scores] = rank_df['M/S'].apply(self._str_to_dict)

            vals = []
            ind = []
            for i in rank_df[[ext_scores]].iterrows():
                ind.append(i[0])
                vals.append(i[1].values[0])

            rdf = pd.DataFrame(data=vals, index=ind)
            rdf['rank'] = rdf.rank(axis=0, ascending=False).mean(axis=1)

            return rdf
        else:
            print('Data source does not exist')
