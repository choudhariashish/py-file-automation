# Some references.
#
# p = subprocess.Popen('ls -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# for line in p.stdout.readlines():
#     print(line)
# retval = p.wait()
#

# pip3 install wget

import subprocess, os, sys
from os import path
import argparse
import logging
import wget
import shutil
import tarfile


# http://127.0.0.0:8000/release-1/package_one.tar.gz

logging.basicConfig(level=logging.INFO)

SERVER_PATH = 'http://127.0.0.1:8000'
RELEASE = 'release-1'



class FileManager:
    def __init__(self, rootdir, server_path):
        self.root = rootdir
        self.downloads_path = path.join(self.root, 'downloads')
        self.server = server_path

        self.packages = ['package_one.tar.gz', 'package_two.tar.gz']

        if path.exists(self.root):
            logging.info('Working directory..ok')
        else:
            sys.exit('Path does not exist-> ' + self.root)


    def fetchPackages(self):
        # Remove existing packages.
        self.removePackages()

        if False == self.makeDir(self.downloads_path):
            sys.exit('Check permissions, could not make a directory at-> ' + self.downloads_path)

        for pack in self.packages:
            url = self.server + '/' + path.join(RELEASE, pack)
            logging.info('Downloading...' + pack)
            try:
                wget.download(url, out='downloads')
            except:
                sys.exit('Failed fetching package-> ' + pack)
            print('\n')
        self.decompressPackages()


    def decompressPackages(self):
        for pack in self.packages:
            filename = path.join(self.downloads_path, pack)
            logging.info('Decompressing...' + filename)
            file = tarfile.open(filename)
            file.extractall(self.downloads_path)
            file.close()


    def removePackages(self):
        logging.info('Removing existing packages')
        self.removeDir(self.downloads_path)


    def removeDir(self, path):
        if os.path.exists(self.downloads_path):
            shutil.rmtree(self.downloads_path)


    def makeDir(self, path):
        os.mkdir(path)
        if os.path.exists(path):
            return True
        else:
            return False


if __name__ == '__main__':

    manager = FileManager(os.getcwd(), SERVER_PATH)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', type=str, required=True, choices=['prepare-ws'], help='An operation to perform')
    args = parser.parse_args()


    if args.command == 'prepare-ws':
        manager.fetchPackages()
