# Copyright Istio Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bs4 import BeautifulSoup
from urllib import request
import os
import wget
import datetime

cwd = os.getcwd()
perf_data_path = cwd + "/perf_data/"
current_release = os.getenv('CUR_RELEASE')
today = datetime.date.today()


def download_benchmark_csv(days):
    if not os.path.exists(perf_data_path):
        os.makedirs(perf_data_path)

    url_prefix = "https://gcsweb.istio.io/gcs/"
    gcs_bucket_name = "istio-build/perf"
    url = url_prefix + gcs_bucket_name
    try:
        page = request.urlopen(url)
    except Exception as e:
        print(e)
        exit(1)
    cur_release_names = []
    master_release_names = []
    soup = BeautifulSoup(page, 'html.parser')
    cur_dateset = set()
    master_dateset = set()
    for link in soup.find_all('a'):
        href_str = link.get('href')
        if href_str == "/gcs/istio-build/":
            continue
        download_prefix = "https://storage.googleapis.com/"
        for day_interval in list(range(1, days)):
            prev_date = today - datetime.timedelta(day_interval)
            release_name = href_str.split("/")[4][15:]
            filename = release_name + ".csv"
            d = prev_date.strftime("%Y%m%d")

            if d not in cur_dateset and d in release_name and current_release in release_name:
                cur_dateset.add(d)
                if len(cur_release_names) < days:
                    cur_release_names.insert(0, release_name)
                if not check_exist(filename):
                    download_url = download_prefix + href_str[5:] + "benchmark.csv"
                    try:
                        wget.download(download_url, perf_data_path + release_name + ".csv")
                    except Exception as e:
                        cur_release_names.pop(0)
                        print(e)
            if d not in master_dateset and d in release_name and "master" in release_name:
                master_dateset.add(d)
                if len(master_release_names) < days:
                    master_release_names.insert(0, release_name)
                if not check_exist(filename):
                    download_url = download_prefix + href_str[5:] + "benchmark.csv"
                    try:
                        wget.download(download_url, perf_data_path + release_name + ".csv")
                    except Exception as e:
                        master_release_names.pop(0)
                        print(e)

    delete_outdated_files(cur_release_names + master_release_names)
    cur_release_dates = [[]] * len(cur_release_names)
    """
    The following section is to parse the cur_release_name (e.g. 'release-1.4.20200109-16.929d965ee418ae5146da39194475e24c3c4656e0')
    , and master_release_name (e.g. 'master.20200113-00.2e3abf0')
    In order to get an array of array named 'cur_release_dates' and 'master_release_dates'
    Each array in the dates matrix looks like: [ year, month, day, YY/MM/DD"]
    ['2020', '01', '13', '20200113']
    """
    for i in range(len(cur_release_names)):
        cur_release = cur_release_names[i]
        sub_str = cur_release[len(current_release) + 1:].split("-")[0]
        cur_release_dates[i] = generate_date_array(sub_str)

    master_release_dates = [[]] * len(master_release_names)
    for i in range(len(master_release_names)):
        master_release = master_release_names[i]
        sub_str = master_release[len("master") + 1:].split("-")[0]
        master_release_dates[i] = generate_date_array(sub_str)

    return cur_release_names, cur_release_dates, master_release_names, master_release_dates


def delete_outdated_files(release_names):
    filenames = []
    for release in release_names:
        filenames.append(release + ".csv")
    for f in os.listdir(perf_data_path):
        if f not in filenames:
            os.remove(perf_data_path + f)


def check_exist(filename):
    for f in os.listdir(perf_data_path):
        if f == filename:
            return True
    return False


def generate_date_array(date_str):
    year = date_str[0:4]
    month = date_str[4:6]
    date = date_str[6:8]
    return [year, month, date, date_str]