from pathlib import Path
from services.routes_service import RoutesService

def main():
    output_dir = Path("data")

    routes_service = RoutesService(output_dir=output_dir)

    routes = routes_service.fetch_routes()
    routes_service.save_routes_to_gtfs(routes)

if __name__ == "__main__":
    main()