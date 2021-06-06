import os
import argparse
from multiprocessing import Pool
from functools import partial

from kss import split_sentences
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
        heading = ''
        subheading = ''
        content = ''

        for line in in_file:
            line = line.strip()

            if line.startswith("<doc"):
                continue

            if line.startswith("</doc"):
                if content != '':
                    out_file.write(_stringify_doc(heading, subheading, content))
                heading = ''
                subheading = ''
                content = ''
                continue

            if line.startswith("## "):
                if content != '':
                    out_file.write(_stringify_doc(heading, subheading, content))

                subheading = line[3:].strip()
                content = ''
                continue

            if heading == '':
                heading = line
            elif line != '':
                content += "\n".join(split_sentences(line, safe=True)) + "\n"


def _stringify_doc(heading, subheading, content):
    if subheading:
        heading = f"{heading} - {subheading}"

    return f"{heading}\n{content}\n"

if __name__ == '__main__':
    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)

    files = [os.path.join(directory, filename) for directory, _, files in os.walk(args.input_path) for filename in files]
    with Pool() as pool:
        list(tqdm(pool.imap_unordered(partial(preprocess_fn, input_path=args.input_path, output_path=args.output_path), files), total=len(files)))
