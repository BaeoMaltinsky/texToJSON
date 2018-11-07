from sickle import Sickle
import json
from os import mkdir
from urllib.request import urlopen
from io import BytesIO
from tarfile import TarFile
# from multiprocessing.dummy import Pool as ThreadPool
from subprocess import run
from sys import argv

def fetch(record):
    metadata = record.metadata
    identifier = metadata['identifier'][0].split('/')[-1]
    source = TarFile(BytesIO(
        openurl("https://arxiv.org/e-print/" + indentifier).readlines()))
    texfiles = [file for file in source.getmembers() if '.tex' in file]
    if len(texfiles) == 0:
        return
    else:
        out = {'Meta' : metadata, 'tex': dict()}
        for f in texfiles:
            texfile = BytesIO(source.extractfile(f))
            tex = json.loads(run("./parser", stdin=texfile, capture_output=True))
            out['tex'][f.name] = tex
        with open('./out/' + identifier + ".json") as file:
            json.dump(out, file)

def main():
    # specset = argv[1]
    specset = 'cs'
    sickle = Sickle("http://export.arxiv.org/oai2")
    records = sickle.ListRecords(metadataPrefix="oai_dc", set=specset)

    for r in records:
        fetch(r)


main()
