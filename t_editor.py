import streamlit as st
import gcsfs
import json

def get_gcs(key,blob_path):
    fs = gcsfs.GCSFileSystem(token=key)
    
    # Use the file-like interface
    with fs.open(f'{blob_path}', 'r', encoding = 'utf-8') as f:
        content = f.read()
    return json.loads(content)

def write_gcs(key, blob_path, data):
    fs = gcsfs.GCSFileSystem(token=key)
    # Use the file-like interface
    with fs.open(f'{blob_path}', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(data))
    return True

import streamlit as st

def display_structure(structure_data):
    """Display the selected structure in a nice way."""
    st.write(structure_data["tname"])
    for comp, details in structure_data["meal_comps"].items():
        st.write(f"{comp}: {details['name']} - {details['size']}")




# MAIN ------------------------------------------------------------------------

key = r'C:\Projects\Python\2_Experimental\Projekty\4_nutrii\food-collector\.streamlit\gcs_gymbro.json'
# Constants
BLOB_NAME = f"food-bro/f_templ.json"
data = get_gcs(key,BLOB_NAME)
print(data)

# Display available structures
selected_structure = st.selectbox("Select a structure:", list(data.keys()))
display_structure(data[selected_structure])

# Add/Delete structures
new_tname = st.text_input("Add new structure with tname:")
if st.button("Add Structure"):
    data[new_tname] = {
        "tname": new_tname,
        "meal_comps": {}
    }
    write_gcs(key, BLOB_NAME, data)

if st.button("Delete Selected Structure"):
    del data[selected_structure]
    write_gcs(key, BLOB_NAME, data)

# Add/Delete meal_comps
new_comp_name = st.text_input("Add new meal_comp name:")
if st.button("Add Meal Comp"):
    data[selected_structure]["meal_comps"][new_comp_name] = {
        "name": None,
        "size": None
    }
    write_gcs(key, BLOB_NAME, data)

selected_comp = st.selectbox("Select a meal_comp to delete:", list(data[selected_structure]["meal_comps"].keys()))
if st.button("Delete Selected Meal Comp"):
    del data[selected_structure]["meal_comps"][selected_comp]
    write_gcs(key, BLOB_NAME, data)


