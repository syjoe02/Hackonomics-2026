from django.core.management.base import BaseCommand
from events.consumers.outbox_to_kafka import process_outbox_events

class Command(BaseCommand):
    help = "Send Outbox events to Kafka"

    def handle(self, *args, **options):
        self.stdout.write("Processing Outbox events...")
        process_outbox_events()
        self.stdout.write("Done.")