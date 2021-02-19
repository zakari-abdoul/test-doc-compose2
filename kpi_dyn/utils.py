from django.template.loader import render_to_string
from django.conf import settings

def my_serialize(query_set):
    new_path = settings.MEDIA_ROOT + "/file/test.txt"
    f = open(new_path, "r")
    xml = render_to_string("xml_template.xml", {'query_set': query_set})

    return

def sommeTotal(serializer_part):

    globalmontant = 0
    for data in serializer_part:
        print("montant : "+str(data["montant"]))
        globalmontant= globalmontant + data["montant"]
    return globalmontant

def handle_uploaded_file(f):
    # new_path = settings.MEDIA_ROOT + "/file/test.txt"
    # with open(new_path, 'r') as file:
    #     data = file.read().replace('\n', '')
    #     print(data)
    output = " "
    job_titles = [line.decode('utf-8').strip() for line in f.chunks()]
    # for chunk in f.chunks():
    #     output += chunk.decode('ascii')
    #return output.replace("\n", "").replace("\r", "")
    return job_titles.replace("\n", "").replace("\r", "")