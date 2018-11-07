from sickle import Sickle
import json
import os

sickle = Sickle("http://export.arxiv.org/oai2")
records = sickle.ListRecords(metadataPrefix="oai_dc", set='cs')
for r in records:
    os.mkdir
