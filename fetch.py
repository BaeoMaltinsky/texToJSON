from sickle import Sickle
import json
from os import mkdir
from urllib.request import openurl
from io import BytesIO
from tarfile import TarFile
from multiprocessing.dummy import Pool as ThreadPool
from subprocess import run
from sys import argv as args

def fetch(record):
    metadata = record.metadata
    identifier = metadata['identifier'][0].split('/')[-1]
    source = TarFile(BytesIO(
        openurl("https://arxiv.org/e-print/" + indentifier).readlines()))
    texfiles = [file in source.getmembers() if '.tex' in file]
    if len(texfiles) == 0:
        return
    else:
        mkdir(identifier)
        with open(indentifier + '/meta.json', 'w') as outfile:
            json.dump(metadata, outfile)
        for f in texfiles:
            texfile = BytesIO(source.extractfile(f))
            with open("".join([indentifier, '/', f, '.json']), 'w') as out:
                run("./parser", stdin=texfile, stdout=out)


def main():
    specset = args[1]
    sickle = Sickle("http://export.arxiv.org/oai2")
    records = sickle.ListRecords(metadataPrefix="oai_dc", set=spectset)

    pool = ThreadPool(10)
    pool.map(fetch, records)


main()
