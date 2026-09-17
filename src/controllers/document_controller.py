from src.models.mongo import log_model
from src.models.postgres import document_model, senior_model
from src.utils.response_utils import error, success


def list_documents(senior_id=None): return success(document_model.list_all(senior_id))


def get_document(document_id):
    document = document_model.get_by_id(document_id)
    return success(document) if document else error("Document not found", 404)


def create_document(data):
    try: senior_id = int(data["senior_id"])
    except (TypeError, ValueError): return error("senior_id must be an integer")
    if not senior_model.get_by_id(senior_id): return error("Senior citizen not found", 404)
    data["senior_id"] = senior_id
    document = document_model.create(data)
    log_model.create("document_added", metadata={"document_id": document["id"], "senior_id": senior_id})
    return success(document, "Document added", 201)


def update_document(document_id, data):
    document = document_model.update(document_id, data)
    if not document: return error("Document not found", 404)
    log_model.create("document_updated", metadata={"document_id": document_id})
    return success(document, "Document updated")


def delete_document(document_id):
    deleted = document_model.delete(document_id)
    if not deleted: return error("Document not found", 404)
    log_model.create("document_deleted", metadata={"document_id": document_id})
    return success(message="Document deleted")
