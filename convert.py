import os
import sys
import logging
import argparse

# from csv_convert import to_json, to_csv
# from xlsx_convert import to_json, to_xlsx

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    parser = argparse.ArgumentParser(description="Convertit un fichier CSV <-> JSON.")
    parser.add_argument("input_file", help="Chemin du fichier .csv ou .json à convertir.")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        logging.error(f"Le fichier '{args.input_file}' n'existe pas.")
        sys.exit(1)

    ext = os.path.splitext(args.input_file)[1].lower()

    try:
        # if ext == ".csv":
        #     output = to_json(args.input_file)
        # elif ext == ".json":
        #     output = to_xlsx(args.input_file)
        # elif ext == ".xlsx":
        #     output = to_json(args.input_file)
        # else:
        #     logging.error("Extension de fichier non supportée. Veuillez fournir un fichier .csv, .json ou .xlsx.")
            sys.exit(1)

        logging.info(f"Conversion réussie : '{args.input_file}' -> '{output}'.")

    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()