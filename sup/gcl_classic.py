import gcsfs
import json

def read_gcs(bucket_name, blob_name, key_path):

    fs = gcsfs.GCSFileSystem(token=key_path)
    
    # Use the file-like interface
    with fs.open(f'{bucket_name}/{blob_name}', 'r', encoding = 'utf-8') as f:
        content = f.read()
        
    return content

def initialize_gcs(token_path):
    return gcsfs.GCSFileSystem(token=token_path)

def create_folder(fs, bucket_name, folder_name):
    # GCS uses flat namespace, so folders are emulated by objects ending in a "/"
    path = f"{bucket_name}/{folder_name}/"
    with fs.open(path, "w") as f:
        f.write("")

def delete_folder(fs, bucket_name, folder_name):
    path = f"{bucket_name}/{folder_name}/"
    fs.rm(path, recursive=True)

def create_file(fs, bucket_name, file_name, content):
    path = f"{bucket_name}/{file_name}"
    with fs.open(path, "w") as f:
        f.write(content)

def delete_file(fs, bucket_name, file_name):
    path = f"{bucket_name}/{file_name}"
    fs.rm(path)

def move_file(fs, bucket_name, source_file, destination_file):
    src_path = f"{bucket_name}/{source_file}"
    dest_path = f"{bucket_name}/{destination_file}"
    fs.mv(src_path, dest_path)

def copy_file(fs, bucket_name, source_file, destination_file):
    src_path = f"{bucket_name}/{source_file}"
    dest_path = f"{bucket_name}/{destination_file}"
    fs.cp(src_path, dest_path)

def download_file(fs, bucket_name, file_name, local_path):
    path = f"{bucket_name}/{file_name}"
    fs.get(path, local_path)

def upload_file(fs, bucket_name, file_name, local_path):
    path = f"{bucket_name}/{file_name}"
    fs.put(local_path, path)




# Path to the service account key
svc_key = r'C:\Projects\Python\2_Experimental\Projekty\4_nutrii\food-collector\.streamlit\gcs_gymbro.json'
file = 'f_templ.json'


fs = gcsfs.GCSFileSystem(token=svc_key)

content = {
    "tname": "classic",
    "meal_comps": {
        "main": {
            "name": None,
            "size": None,
        },
        "side": {
            "name": None,
            "size": None,
        },
        "veggies": {
            "name": None,
            "size": None,
        },
        "other": {
            "name": None,
            "size": None,
        }
    }
}
create_file(fs, 'food-bro', file, json.dumps(content, indent=2))
