import streamlit as st
from collections import defaultdict


template1 = ["meat", "side dish", "veggies", "other"]
template2 = ["protein type", "dressing", "bitter"]


def main():
    # Store user selections in a session state
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = None

    if 'completed_items' not in st.session_state:
        st.session_state.completed_items = defaultdict(dict)
    
    # Choose a template
    template_choice = st.selectbox('Choose a template:', [''] + [f'Template {i+1}' for i, _ in enumerate([template1, template2])])
    if template_choice:
        st.session_state.selected_template = [template1, template2][int(template_choice.split()[-1])-1]
        
    # Display template items
    if st.session_state.selected_template:
        for item in st.session_state.selected_template:
            st.write(f"Choose {item}:")
            choices = workflow.get_pre_made_list(item)
            selected_choice = st.selectbox(f'{item} choice', [''] + choices, key=f'{item}_choice')
            
            # Confirm default size or change size
            col1, col2, col3 = st.beta_columns(3)
            with col1:
                if st.button(f"Confirm {workflow.get_default_serving_size(item)} for {item}"):
                    st.session_state.completed_items[item] = {
                        "choice": selected_choice,
                        "size": workflow.get_default_serving_size(item)
                    }
            with col2:
                size = st.text_input(f"Change size for {item}", value=workflow.get_default_serving_size(item))
                if st.button(f"Confirm {size} for {item}"):
                    st.session_state.completed_items[item] = {
                        "choice": selected_choice,
                        "size": size
                    }
            with col3:
                if item in st.session_state.completed_items:
                    st.success(f"{item} completed!")
        
        # Check if all items are marked completed
        if set(st.session_state.completed_items.keys()) == set(st.session_state.selected_template):
            st.success("Whole meal identification completed!")
            st.json(st.session_state.completed_items)

if __name__ == '__main__':
    main()
