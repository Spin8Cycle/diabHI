from datetime import datetime
import os
import pandas as pd

def excel_logger(data, excl_path, sheet_name='Model Stats'):
    if os.path.exists(excl_path):
        existing_df = pd.read_excel(excl_path, sheet_name=sheet_name, engine='openpyxl', index_col=0)
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
                    print("Index exists but column values differ. Appending the new row.")
        else:
            print("Index does not exist. Appending the new row.")
        
        updated_df = pd.concat([existing_df, data], ignore_index=False)

    else:
        updated_df = data

    with pd.ExcelWriter(excl_path, mode='w', engine='openpyxl') as writer:
        updated_df.to_excel(writer, sheet_name=sheet_name, index=True)