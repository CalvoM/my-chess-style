import os
from typing import override

import requests
from django.core.management import BaseCommand
from django.core.management.base import CommandParser

from style_predictor.models import ChessOpening

DATA_DIR = "data"
LOCAL_ECO_FILE = DATA_DIR + "/{}.tsv"
ECO_DOWNLOAD_URL = "https://raw.githubusercontent.com/lichess-org/chess-openings/refs/heads/master/{}.tsv"


class Command(BaseCommand):
    """We import chess openings from either online or already stored local file.

    It checks for the flag --skip-download, which tells the program to not download
    but use local files.
    If the flag is not set, then it tries downloading from github and stores to the file.
    Later, we store the data to the database.
    """

    help = "Imports ECO chess openings from lichess TSV files"

    @override
    def add_arguments(self, parser: CommandParser) -> None:
        _ = parser.add_argument(
            "--skip-download",
            action="store_true",
            help="Skip download and just save downloaded files to DB.",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        os.makedirs(DATA_DIR, exist_ok=True)
        tsv_file_options = ["a", "b", "c", "d", "e"]
        if not kwargs.get("skip_download", False):
            for i in tsv_file_options:
                file_url = ECO_DOWNLOAD_URL.format(i)
                file = LOCAL_ECO_FILE.format(i)
                try:
                    self.stdout.write(self.style.HTTP_INFO(f"Downloading {file_url}"))
                    response = requests.get(file_url, timeout=60)
                    response.raise_for_status()
                    with open(file, "w", encoding="utf-8") as f:
                        _ = f.write(response.text)
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Downloaded latest {file} file.")
                    )
                except Exception as e:
                    if not os.path.exists(file):
                        self.stderr.write(
                            "Download failed and no local backup available."
                        )
                        raise e
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠️Download failed ({e}). Falling back to local {file}."
                        )
                    )
        total_count = 0
        all_openings: list[ChessOpening] = []
        for i in tsv_file_options:
            file = LOCAL_ECO_FILE.format(i)
            self.stdout.write(self.style.HTTP_INFO(f"Processing {file}"))
            count = 0
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if count == 0:
                        # skip the line with title/column headers
                        count += 1
                        continue
                    eco_code, name, moves = line.strip().split("\t")
                    all_openings.append(
                        ChessOpening(eco_code=eco_code, full_name=name, moves=moves)
                    )
                    count += 1
            total_count += count
        ChessOpening.objects.bulk_create(all_openings)

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {total_count} openings."))
