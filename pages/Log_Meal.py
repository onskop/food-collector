import streamlit as st
import json
import gcsfs
import time

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

def append_gcs(key, blob_path, data):
    fs = gcsfs.GCSFileSystem(token=key)
    # Use the file-like interface
    with fs.open(f'{blob_path}', 'r', encoding = 'utf-8') as f:
        content = f.read()
    if content == "":
        content = "[]"
    content = json.loads(content)
    content.append(data)
    with fs.open(f'{blob_path}', 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(content))
    return True



# MAIN ------------------------------------------------------------------------
key = r'C:\Projects\Python\2_Experimental\Projekty\4_nutrii\food-collector\.streamlit\gcs_gymbro.json'
BLOB_NAME = f"food-bro/f_templ.json"
data = get_gcs(key, BLOB_NAME)
choices = get_gcs(key, "food-bro/meal_components.json")


st.write("Choose template:")
template_names = [template['name'] for template in data['templates']]
selected_template = st.selectbox("Select a template:", template_names)

if "loaded" not in st.session_state:
    st.session_state["loaded"] = False
if "minst" not in st.session_state:
    st.session_state["minst"] = None

if st.button("Create meal from template"):
#create copy of selected template into a meal instance
    print(data['templates'])
    st.session_state.minst = [d for d in data['templates'] if d['name']==selected_template][0]
    st.session_state.mcomps = st.session_state.minst['meal_comps'].keys()
    st.session_state["loaded"] = True

if st.session_state["loaded"]:
# Display available components
    st.write("Identify components:")
    col1, col2, col3 = st.columns(3)
    st.session_state.completed_items = {}
    for comp, details in st.session_state.minst["meal_comps"].items():

        with col2:
            st.write("       ")
            if comp in choices:
                st.session_state.minst["meal_comps"][comp]["name"] = st.selectbox(f"Select {comp}:", choices[comp], index = None)
            else:
                st.selectbox(f"Select {comp}:", [None])
            st.session_state.minst["meal_comps"][comp]["size"] = st.text_input(f"Enter size",key = comp ,value=0)
        with col1:
            st.header(f"{comp.capitalize()}:")
            st.write(f"Name: {details['name']}")
            st.write(f"Size: {details['size']}")
        with col3:
            st.write("       ")
            #write success if the component is selected
            if details['name'] is not None:
                st.success("Completed")
                st.session_state.completed_items[comp] = True
            else:
                st.session_state.completed_items[comp] = False
            st.write("       ")



    # Check if all meal_comps are marked completed
    if len(st.session_state.completed_items) == len(st.session_state.minst["meal_comps"]):
        st.success("Whole meal identification completed!")
        if st.button("Save new meal"):
            # Save to GCS
            # Add datetime to the meal instance in format YYYY-MM-DD HH:MM:SS
            st.session_state.minst['datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            newmeal = st.session_state.minst
            append_gcs(key, "food-bro/meals.json", newmeal)
            # Reset session state
            st.session_state.completed_items = {}
            st.session_state.selected_template = None
            st.session_state.loaded = False
            st.session_state.minst = None
            st.success("Saved to GCS!")
            st.rerun()


