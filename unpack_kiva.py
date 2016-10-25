import zipfile
import json
import os

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError # Python 2 compatibility

kiva_root = 'kiva-data/'
kiva_folders = ['loans', 'lenders', 'loans_lenders']

def mkdirs():
    os.mkdir(kiva_root)
    for f in map(lambda x: kiva_root + x,
                 kiva_folders):
        if not os.path.isdir(f):
            os.mkdir(f)


def reformat_json(json_obj):
    return json.dumps(json_obj, sort_keys=True, separators=(',', ':'))


def unpack_kiva(filename="kiva_ds_json.zip"):
    if not zipfile.is_zipfile(filename):
        raise TypeError("Unable to unpack zip - Corrupted file?")

    z = zipfile.ZipFile(filename)
    names = z.namelist()
    for json_name in filter(lambda x: 'json' in x, names):
        try:
            json_file = z.open(json_name)
            json_string = json_file.read().decode('utf8')
            json_obj = json.loads(json_string)
            # Get `loan`, `lender`, etc.
            obj_type = json_name.split('/')[0]
            json_content = json_obj[obj_type]
            formatted = [reformat_json(j) for j in json_content]
            with open(kiva_root + json_name, 'w+') as output:
                output.write('\n'.join(formatted))
        except JSONDecodeError:
            print("Error decoding file {}".format(json_name))

def merge_kiva():
    for folder in kiva_folders:
        files = os.listdir(kiva_root + folder)
        out_handle = open(kiva_root + folder + '.json', 'w+')
        for f in files:
            in_handle = open(os.path.join(kiva_root, folder, f), 'r')
            for line in in_handle:
                out_handle.write(line)


if __name__ == '__main__':
    mkdirs()
    unpack_kiva()
    merge_kiva()
