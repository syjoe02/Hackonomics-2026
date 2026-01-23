from django.core.management.base import BaseCommand

from events.consumers.outbox_to_kafka import run_worker


class Command(BaseCommand):
    help = "Send Outbox events to Kafka"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Outbox Worker..."))
        run_worker()
