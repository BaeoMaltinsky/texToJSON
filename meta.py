import json
from multiprocessing.dummy import Pool as ThreadPool
from os import mkdir

def fetch(record):
    metadata = record.metadata
    identifier = metadata['identifier'][0].split('/')[-1]
    mkdir("identifier")
    with open(identifier + "/meta.json", 'w') as file:
        json.dump(out, file)

def main():
    # specset = argv[1]
    specset = 'cs'
    sickle = Sickle("http://export.arxiv.org/oai2")
    records = sickle.ListRecords(metadataPrefix="oai_dc", set=specset,
                                 ignore_deleted=True)

    pool = ThreadPool(10)
    pool.imap_unordered(fetch, records)
    pool.close()
    pool.join()


main()
