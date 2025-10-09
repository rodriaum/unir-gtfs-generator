import requests
import pandas as pd
from pathlib import Path

class RoutesService:
    BASE_URL = "https://paragens.amp.pt/acarto2/getcarreiras?idop={}"

    def __init__(self, output_dir: Path, operators=None):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.operators = operators or ["UT1", "UT2", "UT3", "UT4", "UT5"]

    def fetch_routes(self):
        """Search all routes (lines) from all operators."""
        all_routes = []

        for op in self.operators:
            url = self.BASE_URL.format(op)
            print(f"Searching for {op} routes...")

            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"Error getting data from {op}: {e}")
                continue

            for item in data:
                all_routes.append({
                    "route_id": item.get("codamp"),
                    "agency_id": item.get("ut"),
                    "route_short_name": item.get("idcarr"),
                    "route_long_name": item.get("designa"),
                    "route_type": 3,  # 3 = bus
                    "municipality": item.get("mun"),
                    "tipo": item.get("tipo")
                })

        print(f"Total of {len(all_routes)} routes obtained.")
        return all_routes

    def save_routes_to_gtfs(self, routes):
        """Saves routes in GTFS format."""
        df = pd.DataFrame(routes)
        gtfs_columns = [
            "route_id",
            "agency_id",
            "route_short_name",
            "route_long_name",
            "route_type"
        ]

        for col in gtfs_columns:
            if col not in df.columns:
                df[col] = ""

        df[gtfs_columns].to_csv(self.output_dir / "routes.txt", index=False)
        print(f"File 'routes.txt' created in '{self.output_dir}' with {len(df)} lines.")