from django.db import connection, transaction
from collaboration.models import Document, Operation, Snapshot


def apply_operations(operations: list[Operation], content: str):
    updated_content = content
    for op in operations:
        op_type, char, pos = op.operation_type, op.character, op.position
        if op_type == "INSERT":
            # 0123456789
            updated_content = updated_content[:pos] + char + updated_content[pos:]
            # updated_content = ""
        elif op_type == "DELETE":
            # 0123456789
            updated_content = updated_content[:pos] + updated_content[pos + 1 :]
    return updated_content


# will call snapshot job function here
def snapshot_job():
    docs = Document.objects.all()
    for doc in docs:
        # assuming document.content to have latest content
        content = doc.content

        document_id = doc.id
        snapshot = Snapshot.objects.filter(
            document_id=document_id, active=True
        ).order_by("-created_on")
        last_op_id = snapshot[0].upto_operation_id if snapshot.exists() else 0
        pending_operations = Operation.objects.filter(
            document_id=document_id,
            id__gt=last_op_id,
        ).order_by("id")

        if pending_operations.exists():

            # aggregation function here...
            updated_content = apply_operations(pending_operations, content=content)
            last_operation_id = pending_operations.last().id
            with transaction.atomic():
                Snapshot.objects.filter(
                    document_id=document_id,
                ).order_by(
                    "-created_on"
                ).update(active=False)
                Snapshot.objects.create(
                    document_id=document_id,
                    content=updated_content,
                    upto_operation_id=last_operation_id,
                    active=True,
                )
                setattr(doc, "content", updated_content)
                doc.save()
