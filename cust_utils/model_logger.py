from datetime import datetime
import os
import pandas as pd
import ast

def _str_to_dict(row):
    return ast.literal_eval(row)

def _df(excl_path, sheet_name):
    if os.path.exists(excl_path):
        existing_df = pd.read_excel(excl_path, sheet_name=sheet_name, engine='openpyxl', index_col=0)
        return existing_df

def excel_logger(data, excl_path, sheet_name='Model Stats'):
    existing_df = _df(excl_path=excl_path, sheet_name=sheet_name)

    if existing_df:
        new_index = data.index[0]

        if new_index in existing_df.index:
            existing_row = existing_df.loc[[new_index]].drop(columns='Insert D/T')
            new_row_values = data.loc[[new_index]].drop(columns='Insert D/T')

            for i in range(len(existing_row)):
                x = existing_row.iloc[[i]]
                if (x.values[0] == [str(i) for i in new_row_values.values[0]]).all():
                    print("Row already exists in the Excel file with the same values.")
                    return
        

        else:
            print("Appending the new row.")
        
        updated_df = pd.concat([existing_df, data], ignore_index=False)

    else:
        updated_df = data

    with pd.ExcelWriter(excl_path, mode='w', engine='openpyxl') as writer:
        updated_df.to_excel(writer, sheet_name=sheet_name, index=True)



def model_rank(excl_path, sheet_name):
    ext_scores = 'Metrics:Scores'
    df = _df(excl_path=excl_path, sheet_name=sheet_name)
    if df:
        rank_df = df[['M/S', 'Insert D/T']].set_index(['Insert D/T'])
        rank_df[ext_scores] = rank_df['M/S'].apply(_str_to_dict)

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