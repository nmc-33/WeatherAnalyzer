import altair as alt
import pandas as pd
from tasks import start_consumer
import json
from database import get_processed_weather_data_by_id, save_html_data
from datetime import datetime


def analyze_callback(ch, method, properties, body):
    print('pulled from processed queue')
    hold = json.loads(body)
    processed_id = hold['processed_id']
    weather_id = hold['weather_id']
    print(f'processed: {processed_id}, weather: {weather_id}')
    data = get_processed_weather_data_by_id(processed_id)
    if data:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        results = visualization(data)
        save_html_data(results, weather_id)
        print('sent html data to database')


def start_visualizer():
    start_consumer('processed_queue', analyze_callback)


def visualization(inputs):
    # return {
    #     'years': year_list,
    #     'month': month_list, 
    #     "total_snow_yearly": total_snow_yearly,
    #     'average_low': average_low,
    #     'average_high': average_high,
    #     'average_temp': average_temp,
    #     'total_snow_month': total_snow_monthly,
    #     'avg_snow_depth': avg_snow_depth
    # }
    df_year = pd.DataFrame()
    df_year['Year'] = inputs['years']
    df_year['Snowfall'] = inputs['total_snow_yearly']

    df_month = pd.DataFrame()
    df_month['months'] = [x[0] for x in inputs['month_year']]
    print (inputs['month_year'])
    df_month['years'] = [x[1] for x in inputs['month_year']]
    df_month['date'] = [datetime.strptime(str(x[1]) + "/" + str(x[0]), "%Y/%m") for x in inputs['month_year']]
    df_month['total_snow'] = inputs['total_snow_month']
    df_month['average_snow_depth'] = inputs['avg_snow_depth']
    df_month['average_low_temp'] = inputs['average_low']
    df_month['average_high_temp'] = inputs['average_high']
    df_month['average_temp'] = inputs['average_temp']


    year_snow_chart = alt.Chart(df_year).mark_line(point=True).encode(
        x=alt.X('Year:N', title='Year'),          # X-axis with title
        y=alt.Y('Snowfall', title='Snowfall (inches)'),  # Y-axis with custom label
        tooltip=['Year', 'Snowfall']  # Tooltip to show Year and Snowfall
    ).properties(
        title='Yearly Snowfall Data',
        width=300,
        height=400
    )

    month_snow_chart = alt.Chart(df_month).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%b %Y')),          # X-axis with title
        y=alt.Y('total_snow', title='Snowfall (inches)'),  # Y-axis with custom label
        tooltip=['date', 'total_snow']  # Tooltip to show Year and Snowfall
    ).properties(
        title='Monthly Snowfall Data',
        width=300,
        height=400
    )

    month_snow_depth_chart = alt.Chart(df_month).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%b %Y')),          # X-axis with title
        y=alt.Y('average_snow_depth', title='Average Snow Depth (inches)'),  # Y-axis with custom label
        tooltip=['date', 'average_snow_depth']  # Tooltip to show Year and Snowfall
    ).properties(
        title='Monthly Average Snow Depth',
        width=300,
        height=400
    )

    month_average_low_temp_chart = alt.Chart(df_month).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%b %Y')),          # X-axis with title
        y=alt.Y('average_low_temp', title='Average Low Temperature (F)'),  # Y-axis with custom label
        tooltip=['date', 'average_low_temp']  # Tooltip to show Year and Snowfall
    ).properties(
        title='Monthly Average Low Temperature',
        width=300,
        height=400
    )


    month_average_high_temp_chart = alt.Chart(df_month).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%b %Y')),          # X-axis with title
        y=alt.Y('average_high_temp', title='Average High Temperature (F)'),  # Y-axis with custom label
        tooltip=['date', 'average_high_temp']  # Tooltip to show Year and Snowfall
    ).properties(
        title='Monthly Average High Temperature',
        width=300,
        height=400
    )


    month_average_temp_chart = alt.Chart(df_month).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%b %Y')),          # X-axis with title
        y=alt.Y('average_temp', title='Average Temperature (F)'),  # Y-axis with custom label
        tooltip=['date', 'average_temp']  # Tooltip to show Year and Snowfall
    ).properties(
        title='Monthly Average Temperature',
        width=300,
        height=400
    )

    charts = alt.vconcat(
        (year_snow_chart | month_snow_chart | month_snow_depth_chart), 
        (month_average_temp_chart | month_average_low_temp_chart | month_average_high_temp_chart)
        )

    return {"charts": charts.to_html()}