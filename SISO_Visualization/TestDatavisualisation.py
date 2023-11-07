#df = pd.read_csv('/Users/twilliams/Downloads/Booking History-3.csv', parse_dates=['Booking From', 'Booking To'])

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import mplcursors  # Import mplcursors for tooltipspip install mplcursors
from mpldatacursor import datacursor

# Read the CSV file into a DataFrame
df = pd.read_csv('./data/Booking History-4.csv')

# Extract and convert date columns to datetime
df['Booking From'] = pd.to_datetime(df['Booking From'], format='%d/%m/%Y %H:%M')
df['Booking To'] = pd.to_datetime(df['Booking To'], format='%d/%m/%Y %H:%M')

# Define the desired date range
start_date = pd.to_datetime('2023-1-01')  # Adjust the start date
end_date = pd.to_datetime('2023-12-01')    # Adjust the end date

available_asset_names = df['Asset Name'].unique()
print("Available Asset Names:")
for i, asset_name in enumerate(available_asset_names, start=1):
    print(f"{i}. {asset_name}")

# Prompt the user to select Asset Names
selected_assets = input("Enter the numbers of the Asset Names you want to display (comma-separated): ")
selected_assets = [available_asset_names[int(x) - 1] for x in selected_assets.split(',')]

# Filter the DataFrame to include only rows within the date range and with desired Asset Names
filtered_df = df[(df['Booking From'] >= start_date) & (df['Booking To'] <= end_date) & (df['Asset Name'].isin(selected_assets))]

# Create a 'Task' column by concatenating 'Asset Name' and 'Booking ID'
filtered_df['Task'] = filtered_df['Asset Name']1, 8 ,

# Sort the filtered DataFrame by 'Booking From'
filtered_df.sort_values(by='Booking From', inplace=True)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 5))

# Plot the Gantt bars with tooltips
bars = ax.barh(filtered_df['Task'], left=filtered_df['Booking From'], width=(filtered_df['Booking To'] - filtered_df['Booking From']), color='skyblue')


# Customize the appearance
ax.set_xlabel('Timeline')
ax.set_ylabel('Tasks')
ax.set_title('Gantt Chart for Date Range: {} to {}'.format(start_date.date(), end_date.date()))

# Format the date ticks on the X-axis
date_format = mdates.DateFormatter('%Y-%m-%d %H:%M')  # Adjust the date format as desired
ax.xaxis.set_major_formatter(date_format)
ax.xaxis_date()

# Rotate the tick labels for better readability
plt.xticks(rotation=90)

# Define working hours and working days
working_hours_start = pd.Timedelta(hours=9)  # Adjust the start of working hours
working_hours_end = pd.Timedelta(hours=17)   # Adjust the end of working hours
working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']  # Adjust the working days

for day in pd.date_range(start_date, end_date):
    ax.axvline(x=mdates.date2num(day), color='gray', linestyle='--', linewidth=0.5)

# Create background rectangles for working hours
for day in pd.date_range(start_date, end_date):
    if day.strftime('%A') in working_days:
        rect = patches.Rectangle((mdates.date2num(day + working_hours_start), -1),
                                 (mdates.date2num(day + working_hours_end) - mdates.date2num(day + working_hours_start)),
                                 len(filtered_df['Task']), linewidth=0, edgecolor='none', facecolor='lightgreen', alpha=0.6)
        ax.add_patch(rect)

def update_tooltip(sel):
    index = sel.target.index
    if index < len(filtered_df):
        sel.annotation.set_text(filtered_df['Booked By'].iloc[index])
    else:
        sel.annotation.set_text("NoData")

        
# Add tooltips to the bars with booking notes
tooltip = mplcursors.cursor(bars, hover=True)
tooltip.connect("add", update_tooltip)

# Show the chart
plt.show()