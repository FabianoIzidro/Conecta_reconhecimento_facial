from firebase_admin import credentials, db, initialize_app 


# Inicialização do firebase
credencial = credentials.Certificate("serviceAccountKey.json")
firebase = initialize_app(credencial, {
    'databaseURL': 'https://porta-citec-alunos-default-rtdb.firebaseio.com/'
})

def abrirPorta():
  """Fecha a porta da frente do citec"""
  db.reference("Portas").child("Porta 1").set(False)

def fecharPorta():
  """Abre a porta da frente do citec"""
  db.reference("Portas").child("Porta 1").set(True)
