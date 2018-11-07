from sickle import Sickle
import json
from os import mkdir
from os.path import isdir
from urllib.request import urlopen
from io import BytesIO, StringIO
import tarfile
from multiprocessing.dummy import Pool as ThreadPool
from subprocess import run, PIPE
from sys import argv

def fetch(record):
    metadata = record.metadata
    identifier = metadata['identifier'][0].split('/')[-1]
    try:
        source = tarfile.open(fileobj=BytesIO(
            urlopen("https://arxiv.org/e-print/" + identifier).read()))
        print("something!")
    except:
        print("nothing")
        return

    texfiles = [file for file in source.getmembers() if '.tex' in file.name]
    if len(texfiles) == 0:
        return
    else:
        out = {'Meta' : metadata, 'tex': dict()}
        for f in texfiles:
            texfile = source.extractfile(f).read()
            p= run(["./parser"], stdout=PIPE, input=texfile)
            '''
            with Popen(["./parser"], stdin=PIPE, stdout=PIPE) as proc:
                stdout, _ = proc.communicate(input=texfile)
                texjson = stdout
            '''
            try:
                tex = json.loads(p.stdout)
            except:
                return
            out['tex'][f.name] = tex
        with open('./out/' + identifier + ".json", 'w') as file:
            json.dump(out, file)

def main():
    # specset = argv[1]
    specset = 'cs'
    sickle = Sickle("http://export.arxiv.org/oai2")
    records = sickle.ListRecords(metadataPrefix="oai_dc", set=specset,
                                 ignore_deleted=True)
    if not(isdir('out')):
        mkdir('out')

    pool = ThreadPool(3)
    pool.map(fetch, records)
    pool.close()
    pool.join()


main()
