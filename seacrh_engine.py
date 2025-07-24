#!/usr/bin/python
import glob
from pathlib import Path
import logging
import cProfile
import pstats
import argparse

from typing import Tuple, List, Iterator, Optional

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


def direct_search(
        file_path_iter: List[str],
        search_param: str
) -> Tuple[int, List[str]]:
    tc_id = ["****-****"] * 200  # This is how you reserve more place in memory, increase efficiency.
    counter = 0
    for file_path in file_path_iter:
        p_id = None
        search_flag = False
        file_text = Path(file_path).read_text().splitlines()
        for line in file_text:

            if line.find("Polarion ID:") != -1:
                p_id = line.split(":")[-1].strip()
                continue

            if line.find(search_param) != -1:
                search_flag = True
                continue

            if p_id is not None and search_flag is not False:
                tc_id[counter] = p_id
                break

    all_ids = list(set(tc_id))
    all_ids.remove("****-****")

    return all_ids


def direct_search_original(
        file_path_iter: List[str],
        search_param: str
) -> Tuple[int, List[str]]:
    tc_id = []
    counter = 0
    for file_path in file_path_iter:
        p_id = None
        search_flag = False
        file_text = Path(file_path).read_text().splitlines()
        for line in file_text:

            if line.find("Polarion ID:") != -1:
                p_id = line.split(":")[-1].strip()
                continue

            if line.find(search_param) != -1:
                search_flag = True
                continue

            if p_id is not None and search_flag is not False:
                tc_id.append(p_id)
                counter += 1
                break

    return tc_id


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", type=str, nargs=1, help="Path to the folder")
    parser.add_argument("-sp", "--search_param", type=str, nargs=1, help="Search pattern")

    args = parser.parse_args()

    with cProfile.Profile() as profile:
        all_test_files = glob.iglob(
            pathname=f"{args.path}/test_cases/**/test_*.py",
            recursive=True
        )

        searching_text = args.search_param

        tc_ids = direct_search_original(
            file_path_iter=all_test_files,
            search_param=searching_text
        )

        # logging.info(f"Searh results for: {searching_text}")
        # logging.info(f"Used in test cases {count}:")
        # logging.info(f"{tc_ids}")

        # count_o, tc_ids_o = direct_search(
        #    file_path_iter=all_test_files,
        #    search_param=searching_text
        # )

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()
