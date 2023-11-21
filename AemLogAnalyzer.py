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
    daily_user_activity = defaultdict(lambda: defaultdict(int))
    daily_ip_activity = defaultdict(lambda: defaultdict(int))
    
    for filename in os.listdir(folder_path):
        if filename.startswith("author_aemaccess_") and filename.endswith(".log"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                for line in file:
                    user, ip, timestamp = parse_log_entry(line)
                    date = timestamp.date()
                    daily_users[date].add(user)
                    daily_ips[date].add(ip)
                    daily_user_activity[date][user] += 1
                    daily_ip_activity[date][ip] += 1

    return daily_users, daily_ips, daily_user_activity, daily_ip_activity

def plot_user_activity(user_activity, plot_filename='user_activity.jpg'):
    dates = list(user_activity.keys())
    counts = [sum(v.values()) for v in user_activity.values()] # Sum per day

    plt.figure(figsize=(10, 5))
    plt.plot(dates, counts, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Requests')
    plt.title('Total Requests Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close()

def create_excel(daily_users, daily_ips, daily_user_activity, daily_ip_activity, plot_filename):
    summary_data = []
    for date in daily_users:
        summary_data.append([date, len(daily_users[date]), len(daily_ips[date]), sum(daily_user_activity[date].values())])

    # Flatten the dictionaries into sorted lists of tuples for DataFrame
    users_data = sorted(
        [(date, user, daily_user_activity[date][user]) for date in daily_user_activity for user in daily_user_activity[date]],
        key=lambda x: (x[0], -x[2])  # Sort by date, then by number of requests descending
    )
    ips_data = sorted(
        [(date, ip, daily_ip_activity[date][ip]) for date in daily_ip_activity for ip in daily_ip_activity[date]],
        key=lambda x: (x[0], -x[2])  # Sort by date, then by number of requests descending
    )

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
daily_users, daily_ips, daily_user_activity, daily_ip_activity = process_log_files(folder_path)

plot_filename = 'user_activity.jpg'
plot_user_activity(daily_user_activity, plot_filename)
create_excel(daily_users, daily_ips, daily_user_activity, daily_ip_activity, plot_filename)
