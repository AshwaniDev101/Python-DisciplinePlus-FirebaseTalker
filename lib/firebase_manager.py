from google.cloud import firestore

db = firestore.Client.from_service_account_json("discipline-plus-serviceAccountKey.json")

doc_ref = db.collection("users").document("ashwin123")
doc_ref.set({
    "name": "Ashwin",
    "email": "ashwin@example.com"
})


doc_ref = db.collection("users").document("ashwin123")
doc = doc_ref.get()

if doc.exists:
    print(doc.to_dict())
else:
    print("Document not found")