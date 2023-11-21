# AEM as a Cloud Service Log Analyzer

## Overview

The AEM Log Analyzer is a powerful tool for processing and analyzing Adobe Experience Manager (AEM) Author access logs. It helps IT consultants and web administrators gain valuable insights from log data, enabling data-driven decision-making and optimization of AEM sites.

## Features

- **Log Parsing**: Parse AEM access logs to extract essential information.
- **User and IP Analysis**: Track unique users and IP addresses over time.
- **Request Trends**: Visualize request trends with interactive graphs.
- **Excel Export**: Export analyzed data to Excel for further analysis.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (install via `pip`): `pandas`, `matplotlib`, `openpyxl`

### Usage

1. Download the request logs. Eg. Go the https://experience.adobe.com/#/@client/cloud-manager/landing.html and download the logs. (Should be something like author_aemaccess_2023-11-14.log)
2. Place your AEM access log files in a specified folder. eg. "AEM Access logs"
3. Edit the folder path in py script (folder_path = '/Users/martinaltmann/Downloads/AEM Access logs)
4. Run the script to process the log files.
5. The Excel will have three sheets. Summary, Users, IP Addresses. 

### Screenshots

<img width="1558" alt="image" src="https://github.com/frappierer/AEMaaCs-Log-Analyzer/assets/4376185/7af1932c-bd2a-471b-b48d-66350bfe8387">

<img width="1162" alt="image" src="https://github.com/frappierer/AEMaaCs-Log-Analyzer/assets/4376185/57428c0c-de6e-4646-8bf0-ccbb9a735908">

<img width="1030" alt="image" src="https://github.com/frappierer/AEMaaCs-Log-Analyzer/assets/4376185/02e087e7-945c-4cd0-8fb0-125a7c237efe">



