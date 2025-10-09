from pathlib import Path
import json
from utils.http_util import HttpUtil


class LinesService:
    BASE_URL = "https://paragens.amp.pt/unirmap/getlinhas?idcarr={}"

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

    def fetch_lines_by_id_career(self, id_career):
        url = self.BASE_URL.format(id_career)
        raw = HttpUtil.get_json(url)

        if raw is None:
            return []

        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                print(f"Unable to parse JSON for idcarr {id_career}")
                return []

        if not isinstance(raw, list):
            return []

        if len(raw) == 0:
            print(f"No lines found for idcarr {id_career}")

        return raw

    def fetch_lines_for_all_careers(self, idcarr_list):
        all_data = {}
        for idcarr in idcarr_list:
            print(f"Fetching line for idcarr {idcarr}...")
            data = self.fetch_lines_by_id_career(idcarr)
            if data:
                all_data[idcarr] = data
        print(f"Total {len(all_data)} idcarr processed.")
        return all_data

    def get_all_id_stop(self, idcarr_list):
        all_lines_dict = self.fetch_lines_for_all_careers(idcarr_list)
        id_stop_set = set()

        for features in all_lines_dict.values():
            for feature in features:
                props = feature.get("properties", {})
                stop_id = props.get("idparagem")
                if stop_id:
                    id_stop_set.add(stop_id)

        return list(id_stop_set)