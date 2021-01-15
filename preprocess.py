import os
import argparse
from multiprocessing import Pool
from functools import partial

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--input-path", default='text')
parser.add_argument("--output-path", default='text-preprocessed')


def preprocess_fn(filename, input_path, output_path):
    path = filename[len(input_path):]
    if path.startswith("/"):
        path = path[1:]
    filedir = os.path.dirname(path)

    target_path = os.path.join(output_path, filedir)
    target_file = os.path.join(output_path, path)

    os.makedirs(target_path, exist_ok=True)

    with open(filename, encoding='utf8') as in_file, open(target_file, 'w', encoding='utf8') as out_file:
        output_doc = ''
        skip_first = False

        for line in in_file:
            line = line.strip()

            if skip_first:
                skip_first = False
                continue

            if line == '':
                continue

            if line.startswith("<doc"):
                skip_first = True
                continue

            if line.startswith("</doc"):
                if len(output_doc) > 100:
                    out_file.write(output_doc + "\n")
                output_doc = ''
                continue

            output_doc += "다.\n".join(line.split("다. ")) + "\n"


if __name__ == '__main__':
    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)

    files = [os.path.join(directory, filename) for directory, _, files in os.walk(args.input_path) for filename in files]
    with Pool() as pool:
        list(tqdm(pool.imap_unordered(partial(preprocess_fn, input_path=args.input_path, output_path=args.output_path), files), total=len(files)))
