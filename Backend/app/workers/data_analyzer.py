import pandas as pd 
import numpy as np

def perform_analysis(data):
    df = pd.DataFrame()
    df['date'] = data['date']
    df['datatype'] = data['datatype']
    df['station'] = data['station']
    df['attributes'] = data['attributes']
    df['value'] = data['values']

    df.dropna(axis =0, inplace = True)
    cleaned = pd.DataFrame()
    cleaned['date'] = df.date.unique()
    cleaned['T_min'] = np.nan
    cleaned['T_max'] = np.nan
    cleaned['T_avg'] = np.nan
    cleaned['Snowfall'] = np.nan
    cleaned['Snow_Depth'] = 0
    cleaned['Year'] = 0
    cleaned['Month'] = 0
    year_list = []
    month_list = []
    month_year_list = []
    year_month_list = []
    for i in range(len(df)):
        row = df.iloc[i]
        if row['datatype'] == 'TMIN':
            cleaned.loc[cleaned['date']==row['date'], 'T_min'] = float(row['value'])
            cleaned.loc[cleaned['date']==row['date'], 'Year'] = int(row['date'][:4])
            cleaned.loc[cleaned['date']==row['date'], 'Month'] = int(row['date'][5:7])
            if int(row['date'][:4]) not in year_list:
                year_list.append(int(row['date'][:4]))
            if int(row['date'][5:7]) not in month_list:
                month_list.append(int(row['date'][5:7]))
            if len(year_month_list) == 0:
                year_month_list.append(int(row['date'][:4]))
                month_year_list.append((int(row['date'][5:7]), int(row['date'][:4])))
            else:
                if month_year_list[-1] != (int(row['date'][5:7]), int(row['date'][:4])):
                    month_year_list.append((int(row['date'][5:7]), int(row['date'][:4])))
                    year_month_list.append(int(row['date'][:4]))
        elif row['datatype'] == 'TMAX':
            cleaned.loc[cleaned['date']==row['date'], 'T_max'] = float(row['value'])
        elif row['datatype'] == 'TAVG':
            cleaned.loc[cleaned['date']==row['date'], 'T_avg'] = float(row['value'])
        elif row['datatype'] == 'SNOW':
            cleaned.loc[cleaned['date']==row['date'], 'Snowfall'] = float(row['value'])
        elif row['datatype'] == 'SNOWD':
            cleaned.loc[cleaned['date']==row['date'], 'Snow_Depth'] = float(row['value'])
    
    print(cleaned)
    average_low, average_temp, average_high, total_snow_yearly, total_snow_monthly, avg_snow_depth = [], [], [], [], [], []
    print(year_list)
    print(month_list)
    for year in year_list:
        filtered_y = cleaned[cleaned['Year']==year]
        total_snow_yearly = filtered_y['Snowfall'].astype('float64').sum()
        for month in month_list:
            filtered_m = filtered_y[filtered_y['Month']==month]
            if len(filtered_m) != 0:
                average_low.append(filtered_m['T_min'].mean())
                average_high.append(filtered_m['T_max'].mean())
                average_temp.append(filtered_m['T_avg'].mean())
                total_snow_monthly.append(filtered_m['Snowfall'].astype('float64').sum())
                avg_snow_depth.append(filtered_m['Snow_Depth'].mean())
    
    return {
        'years': year_list,
        'month': month_list, 
        'year_month': year_month_list,
        'month_year': month_year_list,
        "total_snow_yearly": total_snow_yearly,
        'average_low': average_low,
        'average_high': average_high,
        'average_temp': average_temp,
        'total_snow_month': total_snow_monthly,
        'avg_snow_depth': avg_snow_depth
    }