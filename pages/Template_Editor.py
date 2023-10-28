import streamlit as st
import gcsfs
from gcsfs import FilesConnection
import json

def get_gcs(key,blob_path):
    #fs = gcsfs.GCSFileSystem(token=key)
    fs = st.experimental_connection('gcs', type=FilesConnection)
    
    # Use the file-like interface
    with fs.open(f'{blob_path}', 'r', encoding = 'utf-8') as f:
        content = f.read()
    return json.loads(content)

def write_gcs(key, blob_path, data):
    #fs = gcsfs.GCSFileSystem(token=key)
    fs = st.experimental_connection('gcs', type=FilesConnection)
    # Use the file-like interface
    with fs.open(f'{blob_path}', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(data))
    return True


def manage_meal_comps(data, selected_template):
    # Find the selected template in the data
    for template in data['templates']:
        if template['name'] == selected_template:
            # Using st.columns to place items side by side
            col1, col2 = st.columns(2)
            
            # Text input fields for new meal_comp item in the first column
            new_meal_comp = col1.text_input("New Meal Comp (e.g., 'protein'):")
            if new_meal_comp and new_meal_comp not in template['meal_comps']:
                if col1.button('Add New Meal Comp'):
                    template['meal_comps'][new_meal_comp] = {"name": None, "size": None}
                    col1.success(f"Added new meal_comp '{new_meal_comp}'!")
                    write_gcs(key, BLOB_NAME, data)
                    st.rerun()
            
            # Selectbox to select and delete an existing meal_comp item in the second column
            meal_comp_names = list(template['meal_comps'].keys())
            selected_meal_comp = col2.selectbox("Select a Meal Comp to delete:", meal_comp_names)
            if col2.button('Delete Selected Meal Comp'):
                del template['meal_comps'][selected_meal_comp]
                write_gcs(key, BLOB_NAME, data)
                col2.success(f"Deleted meal_comp '{selected_meal_comp}'!")
                st.rerun()




# MAIN ------------------------------------------------------------------------
if __name__ == "__main__":
    key = r'C:\Projects\Python\2_Experimental\Projekty\4_nutrii\food-collector\.streamlit\gcs_gymbro.json'
    # Constants
    BLOB_NAME = f"food-bro/f_templ.json"
    data = get_gcs(key, BLOB_NAME)

    # Using st.columns for "Add New Template" and "Delete Selected Template"
    col1, col2 = st.columns(2)
    # Display available structures
    template_names = [template['name'] for template in data['templates']]
    selected_template = col1.selectbox("Select a template:", template_names)
    for template in data['templates']:
        if template['name'] == selected_template:
            col1.write(f"Template Name: {selected_template}")
            for comp, details in template['meal_comps'].items():
                col2.write(f"{comp.capitalize()}:")
                col2.write(f"  - Name: {details['name']} - Size: {details['size']}")



    # Add New Template in the first column
    col1.subheader("Add New Template")
    new_template_name = col1.text_input("Enter new template name:")
    if col1.button("Add Template"):
        if new_template_name and new_template_name not in template_names:
            data['templates'].append({"name": new_template_name, "meal_comps": {}})
            col1.success(f"Added new template '{new_template_name}'!")
            write_gcs(key, BLOB_NAME, data)
        else:
            col1.error("Template name is empty or already exists!")

    # Delete selected template in the second column
    if col2.button("Delete Selected Template"):
        data['templates'] = [template for template in data['templates'] if template['name'] != selected_template]
        write_gcs(key, BLOB_NAME, data)
        col2.success(f"Deleted template '{selected_template}'!")

    st.write("------")
    st.write("Manage Meal Comps:")

    # Add and Delete meal_comp items in the selected template
    manage_meal_comps(data, selected_template)
