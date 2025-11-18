import json
from typing import List
from .config import get_sqs_client, settings

def send_batches_to_sqs(batches: List[dict]):
    sqs = get_sqs_client()
    queue_url = settings.SQS_QUEUE_URL

    messages = []
    for batch in batches:
        messages.append({
            "Id": batch["id"],
            "MessageBody": json.dumps(batch),
        })

    # SQS aceita máx 10 mensagens por lote
    for i in range(0, len(messages), 10):
        chunk = messages[i:i+10]
        sqs.send_message_batch(
            QueueUrl=queue_url,
            Entries=chunk,
        )
