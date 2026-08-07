import csv

from django.core.management.base import BaseCommand

from flights.models import Airport


class Command(BaseCommand):
    help = "Import airports from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="data/airports.csv",
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        imported = 0

        with open(file_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                iata_code = row["iata_code"].strip()

                if not iata_code:
                    continue

                if row["scheduled_service"] != "yes":
                    continue

                Airport.objects.update_or_create(
                    iata_code=iata_code,
                    defaults={
                        "name": row["name"],
                        "city": row["municipality"],
                        "country": row["iso_country"],
                    },
                )

                imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {imported} airports."
            )
        )