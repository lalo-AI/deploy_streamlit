import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

key_dict = json.loads(st.secrets["textkey"])
# creds = service_account.Credentials.from_service_account_info(key_dict)
creds = credentials.Certificate (key_dict)
if not firebase_admin._apps:
    firebase_admin.initialize_app(creds)

# db = firestore.Client(credentials=creds, project="names-project-demo")
# Initialize Firestore
db = firestore.client()
dbNames = db.collection(u"names")

st.header("Nuevo registro")

index = st.text_input("Index")
name = st.text_input("Name")
sex = st.selectbox('Select Sex',('F', 'M', 'Other'))

submit = st.button("Crear nuevo registro")

# Once the name has submitted, upload it to the database
if index and name and sex and submit:
  doc_ref = db.collection("names").document(name)
  doc_ref.set({
      "index": index,
      "name": name,
      "sex": sex
    })
  st.sidebar.write("Registro insertado correctamente")

# ...
def loadByName(name):
  names_ref = dbNames.where(u'name', u'==', name)
  currentName = None
  for myname in names_ref.stream():
    currentName = myname
  return currentName

# Codificar la busqueda de un documento

st.sidebar.subheader("Buscar nombre")
nameSearch = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Buscar")

if btnFiltrar:
  doc = loadByName(nameSearch)
  if doc is None:
    st.sidebar.write("Nombre no existe")
  else:
    st.sidebar.write(doc.to_dict())

# ...
# Codificar la eliminación de un documento, este proceso deberá probarse
# después de la búsqueda del documento... 

st.sidebar.markdown("""---""")
btnEliminar = st.sidebar.button("Eliminar")

if btnEliminar:
  deletename = loadByName(nameSearch)
  if deletename is None:
    st.sidebar.write(f"{nameSearch} no existe")
  else:
    dbNames.document(deletename.id).delete()
    st.sidebar.write(f"{nameSearch} eliminado")

#...
# Codificar proceso para actualizar un documento
st.sidebar.markdown("""---""")
newname = st.sidebar.text_input("Actualizar nombre")
btnActualizar = st.sidebar.button("Actualizar")

if btnActualizar:
  updatename = loadByName(nameSearch)
  if updatename is None:
    st.write(f"{nameSearch} no existe")
  else:
    myupdatename = dbNames.document(updatename.id)
    myupdatename.update({
        "name": newname
        })

# ...

names_ref = list(db.collection(u'names').stream())
names_dict = list(map(lambda x: x.to_dict(), names_ref))
column_order = ["name", "index", "sex"]
names_dataframe = pd.DataFrame(names_dict, columns=column_order)

if "seex" in names_dataframe.columns:
    names_dataframe.drop("seex", axis=1, inplace=True)

st.dataframe(names_dataframe)
