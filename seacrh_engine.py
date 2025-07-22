import glob
import pathlib
import logging
from typing import Tuple, List, Iterator

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


def direct_search(
        file_path_iter: Iterator,
        search_param: str
) -> Tuple[int, List[str]]:

    tc_id = []
    counter = 0
    for file_path in file_path_iter:
        p_id = None
        search_flag = False
        file_text = pathlib.Path(file_path).read_text().splitlines()
        for line in file_text:

            if line.find("Polarion ID:") != -1:
                p_id = line.split(":")[-1].strip()
                continue

            if line.find(search_param) != -1:
                search_flag = True
                continue

            if p_id is not None and search_flag is not False:
                counter += 1
                tc_id.append(p_id)
                break

    return counter, tc_id


# tc_id = []
# count = 0
# for file_path in all_test_files:
#     p_id = None
#     seach_flag = False
#     with open(file_path, "r") as file:
#         for line in file:
#             if p_id != None and seach_flag == True:
#                 count += 1
#                 tc_id.append(p_id)
#                 break
#             else:
#                 if line.find("Polarion ID:") != -1 and p_id == None:
#                     p_id = line.split()[-1]
#                 if line.find(searching_text) != -1:
#                     seach_flag = True
#
# stop_time = time.time()

if __name__ == '__main__':
    all_test_files = glob.iglob(
        pathname="C:/Users/dovydas.menkevicius/data/test_cases/**/test_*.py",
        recursive=True
    )

    searching_text = "cleaning.start_cleaning("

    count, tc_ids = direct_search(
        file_path_iter=all_test_files,
        search_param=searching_text
    )

    logging.info(f"Searh results for: {searching_text}")
    logging.info(f"Used in test cases {count}:")
    logging.info(f"{tc_ids}")
    # logging.info(f"Time taken : {stop_time - start_time} s")

