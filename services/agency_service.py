from pathlib import Path

import pandas as pd


class AgencyService:
    """Service to create agency.txt from GTFS."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

    def get_agency_data(self):
        """Generates the main agency."""
        return [{
            "agency_id": "unir",
            "agency_name": "UNIR - Mobilidade da Área Metropolitana do Porto",
            "agency_url": "https://www.unirmobilidade.pt",
            "agency_timezone": "Europe/Lisbon"
        }]

    def save_agency_to_gtfs(self, agency):
        """Save agency in GTFS format."""
        df = pd.DataFrame(agency)

        gtfs_columns = [
            "agency_id",
            "agency_name",
            "agency_url",
            "agency_timezone"
        ]

        df[gtfs_columns].to_csv(self.output_dir / "agency.txt", index=False)
        print(f"File 'agency.txt' created in '{self.output_dir}' with 1 agency.")