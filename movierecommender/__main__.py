import app
import argparse
import utils
import warnings as stfu
import logging

def main():
    stfu.filterwarnings("ignore")
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="Path to JSON file containing user data")
    args = parser.parse_args()
    user_data = utils.read_json(args.json)
    recommended = app.recommend_movies(user_data)
    # add _recommended to the end of file name
    utils.write_json(file_path=args.json[:-5] + "_recommended.json", data=recommended)

if __name__ == "__main__":
    main()