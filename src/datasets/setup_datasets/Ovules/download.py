import os
import zipfile 

# Training set
os.system('wget -O datazip.zip https://files.de-1.osf.io/v1/resources/x9yns/providers/osfstorage/?zip=')

with zipfile.ZipFile('datazip.zip', 'r') as zip_ref:
    zip_ref.extractall('train')

os.system('rm datazip.zip')


# Evaluation set
os.system('wget -O datazip.zip https://files.de-1.osf.io/v1/resources/xp5uf/providers/osfstorage/?zip=')

with zipfile.ZipFile('datazip.zip', 'r') as zip_ref:
    zip_ref.extractall('eval')

os.system('rm datazip.zip')







