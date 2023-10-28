import os
import requests, json, streamlit as st


# extract value from .streamlit/secrets.toml in line that contains suggestic_key
def get_key(name):
    with open(os.path.join(".streamlit", "secrets.toml")) as f:
        for line in f.readlines():
            if name in line:
                key = line.split("=")[1].strip().strip('"')
    return key

#key = get_key("suggestic_key")
key = st.secrets["suggestic_key"]
user = st.secrets["suggestic_user"]
url = 'https://production.suggestic.com/graphql'

headers = {
  "Authorization": "Token {0}".format(key),
  "sg-user": "{0}".format(user),
}


query = """
query RecipeSearch($searchQuery: String!, $ingredientsList: [String!]!, $cuisineType: [String!]!, $itemCount: Int!) {
  recipeSearch(
    query: $searchQuery,
    ingredients: $ingredientsList,
    cuisines: $cuisineType,
    first: $itemCount) {
    edges {
      node {
        id
        name
        nutrientsPerServing {
          calories
          protein
          fat
          carbs
          omega3
        }
      }
    }
  }
}
"""
st.text_input("Enter search query", key = "searchQuery", value = "salad")
st.text_input("Enter ingredients separated by comma ( , )", key = "ingredientsList", value = "potatoes")
st.text_input("Enter cuisine type, separated by comma ( , )", key = "cuisineType", value = "Central europe")
st.write("Cuisine list: https://docs.suggestic.com/graphql/objects/recipe/recipe-object/cuisines")
st.number_input("How many meals to show?", key = "itemCount", value = 5)

# Define the variables for the request
variables = {
  "searchQuery": st.session_state.searchQuery,
  "ingredientsList": list(st.session_state.ingredientsList.split(",")),
  "cuisineType": list(st.session_state.cuisineType.split(",")),
  "itemCount": st.session_state.itemCount
}


if st.button("Search"):
    # Execute the request
    print('-------------------------------------------------------------------------------------------')
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    # Load the response to a dictionary
    data = json.loads(response.text)
    if "errors" in data:
        st.write(data["errors"][0]["message"])  
    else:
      recipes = data["data"]["recipeSearch"]["edges"]
      st.write(f"Found {len(recipes)} recipes.")
      for recipe in recipes:
          name = recipe["node"]["name"]
          calories = recipe["node"]["nutrientsPerServing"]["calories"]
          protein = recipe["node"]["nutrientsPerServing"]["protein"]
          fat = recipe["node"]["nutrientsPerServing"]["fat"]
          carbs = recipe["node"]["nutrientsPerServing"]["carbs"]
          st.write(f"Name: {name}, Calories: {calories}, Protein: {protein}, Fat: {fat}, Carbs: {carbs}")