from google.cloud import firestore


class FirebaseManager:
    def __init__(self, service_account_path):
        self.db = firestore.Client.from_service_account_json(service_account_path)

    def set_document(self, collection_name, document_id, data):
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.set(data)
        print(f"Document '{document_id}' set in collection '{collection_name}'")

    def batch_add_initiatives(self, day, initiatives):
        """
        Adds multiple Initiative objects under a given day in the 'InitiativeList' subcollection.

        :param day: Document ID under 'WeekList' (e.g., 'Friday')
        :param initiatives: List of Initiative objects (must have .id and .to_map() methods)
        """
        batch = self.db.batch()
        root_collection = "WeekList"

        for initiative in initiatives:
            ref = self.db.collection(root_collection) \
                .document(day) \
                .collection("InitiativeList") \
                .document(initiative.id)
            data = initiative.to_map()
            data.pop("id", None)  # remove 'id' key like Flutter version
            batch.set(ref, data)

        batch.commit()
        print(f"Uploaded {len(initiatives)} initiatives to '{day}/InitiativeList'")

    def clean_initiatives(self, day):
        """
        Deletes *all* initiatives under a given day in the 'InitiativeList' subcollection.

        :param day: Document ID under 'WeekList' (e.g., 'Friday')
        """
        root_collection = "WeekList"
        subcollection = "InitiativeList"

        # Get all initiative documents under the day
        initiatives_ref = self.db.collection(root_collection) \
            .document(day) \
            .collection(subcollection)

        docs = initiatives_ref.stream()

        batch = self.db.batch()
        count = 0

        for doc in docs:
            batch.delete(doc.reference)
            count += 1
            # Firestore batch limit is 500 operations
            if count == 500:
                batch.commit()
                batch = self.db.batch()
                count = 0

        if count > 0:
            batch.commit()

        print(f"Deleted all initiatives from '{day}/{subcollection}'")

    def get_document(self, collection_name, document_id):
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print("Document not found")
            return None
