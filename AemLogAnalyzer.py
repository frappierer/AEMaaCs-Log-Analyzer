import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

def parse_log_entry(line):
    parts = line.split()
    ip = parts[1]
    user = parts[2]
    timestamp = datetime.strptime(parts[3], '%d/%b/%Y:%H:%M:%S')
    return user, ip, timestamp

def process_log_files(folder_path):
    daily_users = defaultdict(set)
    daily_ips = defaultdict(set)
    hourly_activity = defaultdict(lambda: defaultdict(int))
    
    for filename in os.listdir(folder_path):
        if filename.startswith("author_aemaccess_") and filename.endswith(".log"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                for line in file:
                    user, ip, timestamp = parse_log_entry(line)
                    date = timestamp.date()
                    hour = timestamp.hour
                    daily_users[date].add(user)
                    daily_ips[date].add(ip)
                    hourly_activity[date][hour] += 1

    return daily_users, daily_ips, hourly_activity

def plot_hourly_activity(hourly_activity, plot_filename='hourly_activity.jpg'):
    num_days = len(hourly_activity)
    plt.figure(figsize=(15, 3 * num_days))
    
    for i, (date, hours) in enumerate(sorted(hourly_activity.items())):
        times = list(range(24))
        counts = [hours[h] for h in times]
        
        plt.subplot(num_days, 1, i + 1)
        plt.plot(times, counts, marker='o', label=f'Date: {date}')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Requests')
        plt.title(f'Hourly Requests on {date}')
        plt.xticks(times)
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close()

def create_excel(daily_users, daily_ips, hourly_activity, plot_filename):
    summary_data = []
    for date in daily_users:
        total_requests = sum(hourly_activity[date].values())
        summary_data.append([date, len(daily_users[date]), len(daily_ips[date]), total_requests])

    # Flatten hourly_activity for detailed user and IP data
    users_data = []
    ips_data = []
    for date, hours in hourly_activity.items():
        for user in daily_users[date]:
            users_data.append([date, user, sum(hours.values())])
        for ip in daily_ips[date]:
            ips_data.append([date, ip, sum(hours.values())])

    # Create DataFrames
    df_summary = pd.DataFrame(summary_data, columns=['Date', 'Number of Unique Users', 'Unique IP Addresses', 'Total Requests'])
    df_users = pd.DataFrame(users_data, columns=['Date', 'User', 'Number of Requests'])
    df_ips = pd.DataFrame(ips_data, columns=['Date', 'IP Address', 'Number of Requests'])

    # Save DataFrames to an Excel file with multiple sheets
    excel_filename = 'aem_access_log_analysis.xlsx'
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        df_users.to_excel(writer, sheet_name='Users', index=False)
        df_ips.to_excel(writer, sheet_name='IP Addresses', index=False)

    # Add plot image to the Excel file
    book = load_workbook(excel_filename)
    sheet = book['Summary']
    img = Image(plot_filename)
    sheet.add_image(img, 'E2')  # Adjust cell as needed
    book.save(excel_filename)

folder_path = '/Users/martinaltmann/Downloads/AEM Access logs'
daily_users, daily_ips, hourly_activity = process_log_files(folder_path)

plot_filename = 'hourly_activity.jpg'
plot_hourly_activity(hourly_activity, plot_filename)
create_excel(daily_users, daily_ips, hourly_activity, plot_filename)
