import json
import os

from django.core.management import BaseCommand
from django.test import Client


class Command(BaseCommand):
    help = "Generates OpenAPI json file."

    def handle(self, *args, **kwargs):
        client = Client()
        response = client.get("/api/v1/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            output_path = os.path.join("openapi", "openapi.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(schema, f, indent=2)
            self.stdout.write(
                self.style.SUCCESS(f"✅ OpenAPI schema saved to {output_path}")
            )
        else:
            self.stderr.write(f"Failed to fetch OpenAPI schema: {response.status_code}")
