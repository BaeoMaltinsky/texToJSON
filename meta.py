from sickle import Sickle

sickle = Sickle("http://export.arxiv.org/oai2")
records = sickle.ListRecords(metadataPrefix="oai_dc", set='cs')
for i in range(10):
    print(records.next())
