import subprocess
import sys
import time
import json

url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=55.0&x=id%3D{}%26install%3Dondemand%26uc"

def download_extension(extension_id, download_folder):
    print("Downloading extension {}".format(extension_id))
    try:
        result = subprocess.call(["wget",url.format(extension_id),'-O','{}/{}-{:d}.crx'.format(download_folder, extension_id, int(time.time()))])
    except KeyboardInterrupt:
        print("Aborting...")
        return
    except:
        print("Could not download extension, skipping...")

def main(args):
    if len(args) < 3:
        print("Usage: {} [input filename] [download folder]".format(args[0]))
        return -1
    input_filename = args[1]
    download_folder = args[2]
    with open(input_filename, 'r') as input_file:
        json_data = json.loads(input_file.read())
    for name, params in sorted(json_data.items(), key=lambda x:-x[1]['rating']['users']):
        print(name,params['rating']['users'])
        download_extension(params['id'], download_folder)

if __name__ == '__main__':
    exit(main(sys.argv))