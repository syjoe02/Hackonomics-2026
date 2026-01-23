from django.core.management.base import BaseCommand

from accounts.adapters.events.kafka_consumer import start_kafka_consumer


class Command(BaseCommand):
    help = "Run Kafka consumer for accounts service"

    def handle(self, *args, **options):
        self.stdout.write("Starting Accounts Kafka Consumer...")
        start_kafka_consumer()
