import glob
from pathlib import Path
from typing import List, Iterator, Set, Optional
from seacrh_engine import direct_search_original


def get_methods_names(
        framework_files: List[str],
        search_param
) -> List[str]:
    found_methods = []
    for file_path in framework_files:
        if file_path.startswith("test_"):
            continue

        file_text = Path(file_path).read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(file_text):
            if line.find(search_param) != -1 and line.startswith("def") is not True:
                file_text_modified = file_text[0:line_number]
                file_text_modified.reverse()
                for reversed_line in file_text_modified:
                    if reversed_line.startswith("def"):
                        method = reversed_line.removeprefix("def").strip().split("(")[0]
                        found_methods.append(method + "(")
                        continue

    return found_methods


def in_direct_search(
        # test_pool_path: Iterator,
        framework_files: List[str],
        all_methods: Set[str],
        depth: int = 1
) -> Optional[Set[str]]:
    if depth > MAX_DEPTH:
        return all_methods

    print(f"Depth - {depth}")

    found_methods = set()

    for method in all_methods:
        all_methods = get_methods_names(framework_files=framework_files,
                                        search_param=method)
        if all_methods is not None:
            found_methods.update(all_methods)

    print(found_methods)

    search_results = in_direct_search(
        # test_pool_path=all_test_files,
        framework_files=framework_files,
        all_methods=found_methods,
        depth=depth + 1
    )
    # print(search_result)
    # if search_result:
    #     found_methods.extend(search_result)
    if found_methods is not None:
        found_methods.update(search_results)
    return found_methods

    # polarion_ids = set()
    # tc_ids = direct_search_original(
    #        file_path_iter=test_pool_path,
    #        search_param=search_param
    #   )
    # if tc_ids is not []:
    #    polarion_ids.update(tc_ids)


if __name__ == '__main__':
    MAX_DEPTH = 6
    all_test_files = glob.glob(
        pathname="C:/Users/dovydas.menkevicius/data/test_cases/**/test_*.py",
        recursive=True
    )

    framework_documents = glob.glob(
        pathname="C:/Users/dovydas.menkevicius/data/**/*.py",
        recursive=True
    )

    methods = in_direct_search(
        framework_files=framework_documents,
        all_methods={"reconnect_shunts("})

    tc_ids = []

    for method in methods:
        tc_id = direct_search_original(
            file_path_iter=all_test_files,
            search_param=method
        )

