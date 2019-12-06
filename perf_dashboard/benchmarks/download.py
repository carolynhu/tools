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
import urllib.request
from bs4 import BeautifulSoup
import datetime
import wget
import os

cwd = os.getcwd()
# print(cwd)
perf_data_path = cwd + "/perf_data/"
current_release = "release-1.4"


def download_benchmark_csv():
    gcs_prefix = "https://gcsweb.istio.io/"
    url = gcs_prefix + "gcs/istio-build/perf/"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    today = datetime.date.today()
    cur_release_names = []
    master_release_names = []
    for day_interval in list(range(1, 11)):
        prev_date = today - datetime.timedelta(day_interval)
        d = prev_date.strftime("%Y%m%d")
        for link in soup.find_all('a'):
            href_str = link.get('href')
            csv_url = gcs_prefix + href_str + "benchmark.csv"
            if d in href_str and current_release in href_str:
                release_str = href_str.split("/")[4][15:]
                cur_release_filename = release_str + "-benchmark.csv"
                cur_release_names.append(release_str)
                if not check_exist(cur_release_filename):
                    wget.download(csv_url, perf_data_path + cur_release_filename)
            if d in href_str and "master" in href_str:
                release_str = href_str.split("/")[4][15:]
                master_filename = release_str + "-benchmark.csv"
                master_release_names.append(release_str)
                if not check_exist(master_filename):
                    wget.download(csv_url, perf_data_path + master_filename)
    return cur_release_names, master_release_names


def check_exist(input_file):
    for filename in os.listdir(perf_data_path):
        if filename == input_file:
            return True
    return False


def delete_outdated_file():
    today = datetime.date.today()
    for filename in os.listdir(perf_data_path):
        for branch in [current_release, "master"]:
            prev_date = today - datetime.timedelta(7)
            d = prev_date.strftime("%Y%m%d")
            if branch in filename and d in filename:
                os.remove(perf_data_path + filename)
