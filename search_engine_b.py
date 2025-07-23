import glob
from pathlib import Path
from typing import List, Iterator, Set, Optional
from seacrh_engine import direct_search_original


def get_methods_names(
        framework_files: Iterator,
        search_param
) -> List[str]:
    found_methods = []
    for file_path in framework_files:
        if file_path.startswith("test_"):
            continue

        file_text = Path(file_path).read_text(encoding="utf-8").splitlines()

        for line_number, line in enumerate(file_text):
            if line.find(search_param) != -1:
                print(line)
                file_text_modified = file_text[0, 5]
                file_text_modified.reverse()
                for reversed_line in file_text_modified:
                    if reversed_line.startswith("def"):
                        found_methods.append(reversed_line.removeprefix("def").strip())

    return found_methods


def in_direct_search(
        test_pool_path: Iterator,
        framework_files: Iterator,
        search_param: str,
        depth: int = 1
) -> Optional[Set[str]]:
    if depth > MAX_DEPTH:
        return

    polarion_ids = set()
    tc_ids = direct_search_original(
            file_path_iter=test_pool_path,
            search_param=search_param
        )
    if tc_ids is not []:
        polarion_ids.update(tc_ids)

    all_methods = get_methods_names(framework_files=framework_documents,
                                    search_param=search_param)


if __name__ == '__main__':
    MAX_DEPTH = 6
    all_test_files = glob.iglob(
        pathname="C:/Users/dovydas.menkevicius/data/test_cases/**/test_*.py",
        recursive=True
    )

    framework_documents = glob.iglob(
        pathname="C:/Users/dovydas.menkevicius/data/**/*.py",
        recursive=True
    )

    in_direct_search(
        test_pool_path=all_test_files,
        framework_files=framework_documents,
        search_param="cleaning.start_cleaning("
    )
