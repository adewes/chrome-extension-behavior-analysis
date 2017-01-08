import os
import sys
import json

from proxy.proxy import HTTPProcess
from extension.test import test_extension

if __name__ == '__main__':
    
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: {} [json filename] [extension directory] [report directory]\n".format(sys.argv[0]))
        exit(-1)
    
    json_filename = sys.argv[1]
    extension_directory = sys.argv[2]
    report_directory = sys.argv[3]
    
    downloaded_extensions = {}

    for filename in os.listdir(extension_directory):
        if filename.endswith('.crx'):
            basename, extension = filename.split('.')
            extension_id, download_time = basename.split('-')
            if extension_id in downloaded_extensions:
                if int(download_time) < downloaded_extensions[extension_id][1]:
                     continue
            downloaded_extensions[extension_id] = (os.path.join(extension_directory, filename), int(download_time))
    

    with open(json_filename,'r') as json_file:
        json_data = json.loads(json_file.read())

    proxy = HTTPProcess("localhost",8899)
    
    proxy.start()

    try:

        for extension_name, params in sorted(json_data.items(), key=lambda x:-x[1]['rating']['users']):
            if params['id'] in downloaded_extensions:
                extension_filename, download_time = downloaded_extensions[params['id']]
                report_filename = os.path.join(report_directory,'{}-{}.json'.format(params['id'], download_time))
                if not os.path.exists(report_filename):
                    print("Testing extension {}".format(extension_name))
                    try:
                        test_extension(proxy, extension_filename, report_filename)
                    except KeyboardInterrupt:
                        raise
                    except:
                        pass
    finally:
        proxy.terminate()
        proxy.join()
