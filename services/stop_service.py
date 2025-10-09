import json
from pathlib import Path
from utils.http_util import HttpUtil

class StopService:
    """Service for handling individual stops or lists of stops."""

    BASE_URL = "https://paragens.amp.pt/unirmap/getparagens3?id={}"

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

    def fetch_stop_by_id(self, idparagem):
        """Fetch a single stop by its id."""
        url = self.BASE_URL.format(idparagem)
        raw = HttpUtil.get_json(url)

        if raw is None:
            print(f"Error doing GET for stop {idparagem}")
            return None

        # If raw is a JSON string, convert it
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                print(f"Cannot parse JSON for stop {idparagem}")
                return None

        # If the response is a list with features, extract the first one
        if isinstance(raw, list) and len(raw) > 0:
            feature = raw[0]
            props = feature.get("properties", {})
            geom = feature.get("geometry", {})
            coords = geom.get("coordinates", [None, None])
            return {
                "stop_id": props.get("gid"),
                "stop_name": props.get("designacao"),
                "stop_lat": coords[1],
                "stop_lon": coords[0],
                "localizacao": props.get("localizacao"),
                "cod": props.get("cod"),
                "zona_andante": props.get("zona_andante"),
                "linhas": props.get("linhas")
            }

        print(f"No stop found for id {idparagem}")
        return None

    def fetch_stops_by_list(self, stop_id_list):
        """Search multiple stops from a list of stops."""
        stops = {}
        for stop_id in stop_id_list:
            print(f"Looking to stop {stop_id}...")
            stop_data = self.fetch_stop_by_id(stop_id)
            if stop_data:
                stops[stop_id] = stop_data
        print(f"Total {len(stops)} stops obtained.")
        return stops