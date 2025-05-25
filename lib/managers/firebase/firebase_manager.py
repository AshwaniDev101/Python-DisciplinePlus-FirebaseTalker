from google.cloud import firestore

from lib import logger


class FirebaseManager:


    def __init__(self, service_account_path):
        self.db = firestore.Client.from_service_account_json(service_account_path)

    # public functions
    def upload_initiative_list_to_firebase(self, day: str, data_list):
        # firebase = FirebaseManager(serviceAccountKeyPath)
        self._batch_add_initiatives(day=day, initiatives=data_list)

    def clean_initiatives(self, day):
        """
        Deletes *all* documents under 'InitiativeList' subcollection of the given day in 'WeekList',
        without deleting the subcollection itself.

        :param day: Document ID under 'WeekList' (e.g., 'Friday')
        """
        root_collection = "WeekList"
        subcollection = "InitiativeList"

        try:
            initiatives_ref = self.db.collection(root_collection).document(day).collection(subcollection)
            docs = initiatives_ref.stream()

            batch = self.db.batch()
            count = 0

            for doc in docs:
                batch.delete(doc.reference)
                count += 1
                if count == 500:
                    batch.commit()
                    batch = self.db.batch()
                    count = 0

            if count > 0:
                batch.commit()


            logger.log(f"Deleted all initiatives from '{day}/{subcollection}'")

        except Exception as e:
            logger.log(f"Failed to clean initiatives for {day}: {e}")

    # private functions
    def _set_document(self, collection_name, document_id, data):
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.set(data)
        logger.log(f"Document '{document_id}' set in collection '{collection_name}'")

    def _batch_add_initiatives(self, day, initiatives):
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
        logger.log(f"Uploaded {len(initiatives)} initiatives to '{day}/InitiativeList'")



    def _get_document(self, collection_name, document_id):
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            logger.log("Document not found")
            return None
