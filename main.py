from controller.main_controller import TimeMateController
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-token', help="API Token für Authentifizierung", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    app = TimeMateController(api_token=args.api_token)
    app.run()