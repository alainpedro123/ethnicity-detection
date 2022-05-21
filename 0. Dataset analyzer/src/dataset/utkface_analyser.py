"""UTKFace Dataset Analyser

Processes UTKFace dataset and generate data insights based on associated metadata

Usage:
  utkface_analyser.py -i <input_path>
  utkface_analyser.py (-h | --help)
  utkface_analyser.py --version

Options:
  -i, --input <input_path>                          UTKFace dataset directory
  -h --help                                         Show this screen
  --version                                         Show version
"""
from operator import add
from pathlib import Path
from typing import List, Tuple, Dict

import matplotlib.pyplot as plt
import numpy as np
from docopt import docopt

GENDERS = ['Male', 'Female']
ETHNICITY = ['Caucasoid', 'Negroid', 'Mongoloid', 'Australoid', 'Others']


def get_images_in_path(path: Path) -> List[Path]:
    return [path / image for image in path.glob('*') if image.suffix in ['.bmp', '.png', '.jpg']]


def get_metadata(images: List[Path]) -> Tuple[Dict, Dict, Dict]:
    age_metadata = {i: {
        'gender': {key: 0 for key in GENDERS},
        'ethnicity': {key: 0 for key in ETHNICITY},
        'total': 0
    } for i in range(1, 117)}
    gender_metadata = {}
    ethnicity_metadata = {}

    for image in images:
        age, gender, ethnicity, _ = get_file_metadata(image)
        # print(F'Age: {age} - Gender: {gender} - Ethnicity: {ethnicity} - Date: {date}')

        if age not in age_metadata:
            age_metadata[age] = {
                'gender': {key: 0 for key in GENDERS},
                'ethnicity': {key: 0 for key in ETHNICITY},
                'total': 0
            }

        age_metadata[age]['gender'][gender] += 1
        age_metadata[age]['ethnicity'][ethnicity] += 1
        age_metadata[age]['total'] += 1

        if gender not in gender_metadata:
            gender_metadata[gender] = {
                'age': {key: 0 for key in range(1, 117)},
                'ethnicity': {key: 0 for key in ETHNICITY},
                'total': 0
            }

        gender_metadata[gender]['age'][age] += 1
        gender_metadata[gender]['ethnicity'][ethnicity] += 1
        gender_metadata[gender]['total'] += 1

        if ethnicity not in ethnicity_metadata:
            ethnicity_metadata[ethnicity] = {
                'age': {key: 0 for key in range(1, 117)},
                'gender': {key: 0 for key in GENDERS},
                'total': 0
            }

        ethnicity_metadata[ethnicity]['gender'][gender] += 1
        ethnicity_metadata[ethnicity]['age'][age] += 1
        ethnicity_metadata[ethnicity]['total'] += 1

    return age_metadata, gender_metadata, ethnicity_metadata


def get_file_metadata(image: Path) -> Tuple[int, str, str, int]:
    age, gender, ethnicity, date = map(int, str(image.stem).split('_'))
    gender = GENDERS[gender]
    ethnicity = ETHNICITY[ethnicity]

    return age, gender, ethnicity, date


def plot_genders_by_ethnicity(metadata):
    labels = ETHNICITY

    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()
    width = 0.35  # the width of the bars

    men_means = [metadata[ETHNICITY[i]]['gender']['Male'] for i in range(len(labels))]
    women_means = [metadata[ETHNICITY[i]]['gender']['Female'] for i in range(len(labels))]

    rects1 = ax.bar(x - width / 2, men_means, width, label='Men')
    rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of Pictures')
    ax.set_title('Number of Pictures by ethnicity and gender')
    ax.set_xticks(x, labels)
    ax.legend()

    fig.tight_layout()
    return fig


def plot_ethnicity_by_age(metadata, labels):
    fig, ax = plt.subplots()
    width = 0.75

    bottom = [0] * len(labels)
    for ethnicity in ETHNICITY:
        data = [metadata[i]['ethnicity'][ethnicity] for i in labels]
        ax.bar(labels, data, width, bottom=bottom, label=ethnicity)
        bottom = list(map(add, bottom, data))

    ax.set_ylabel('Number of Pictures')
    ax.set_xlabel('Age')
    ax.set_title(F'Number of pictures per age (from {labels[0]} to {labels[-1]}) and ethnicity')

    ax.legend()
    return fig


def plot_gender_by_age(metadata, labels):
    fig, ax = plt.subplots()
    width = 0.75

    bottom = [0] * len(labels)
    for gender in GENDERS:
        data = [metadata[i]['gender'][gender] for i in labels]
        ax.bar(labels, data, width, bottom=bottom, label=gender)
        bottom = list(map(add, bottom, data))

    ax.set_ylabel('Number of Pictures')
    ax.set_xlabel('Age')
    ax.set_title(F'Number of pictures per age (from {labels[0]} to {labels[-1]}) and gender')

    ax.legend()
    return fig


def plot_ethnicity_by_gender(metadata):
    labels = GENDERS

    fig, ax = plt.subplots()
    width = 0.75

    bottom = [0] * len(labels)
    for ethnicity in ETHNICITY:
        data = [metadata[i]['ethnicity'][ethnicity] for i in labels]
        ax.bar(labels, data, width, bottom=bottom, label=ethnicity)
        bottom = list(map(add, bottom, data))

    ax.set_ylabel('Number of Pictures')
    ax.set_title(F'Number of pictures per gender and ethnicity')

    ax.legend()
    return fig


if __name__ == "__main__":
    # Arguments processing
    arguments = docopt(__doc__, version='UTKFace Dataset Analyser 1.0')
    input_path = Path(arguments['--input'])

    # Process images and generate metadata
    images = get_images_in_path(input_path)
    age_metadata, gender_metadata, ethnicity_metadata = get_metadata(images)

    # Generate visualizations
    age_range = range(1, 81)
    plot_ethnicity_by_age(age_metadata, age_range)
    plot_gender_by_age(age_metadata, age_range)
    plot_genders_by_ethnicity(ethnicity_metadata)
    plot_ethnicity_by_gender(gender_metadata)

    # Show visualizations
    plt.show()
