import glob
from pathlib import Path
from typing import List, Set, Optional
from seacrh_engine import direct_search_original
import cProfile
import pstats


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
            if line.startswith("def") is not True and search_param in line:
                file_text_modified = file_text[0:line_number]
                file_text_modified.reverse()
                for reversed_line in file_text_modified:
                    if reversed_line.startswith("def"):
                        method_name = reversed_line.removeprefix("def").strip().split("(")[0]
                        found_methods.append(method_name + "(")
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

    for found_method in all_methods:
        all_methods = get_methods_names(framework_files=framework_files,
                                        search_param=found_method)
        if all_methods is not None:
            found_methods.update(all_methods)

    print(found_methods)

    search_results = in_direct_search(
        framework_files=framework_files,
        all_methods=found_methods,
        depth=depth + 1
    )

    if found_methods is not None:
        found_methods.update(search_results)
    return found_methods


if __name__ == '__main__':
    import timeit

    t1 =timeit.default_timer()
    # with cProfile.Profile() as profile:
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

    # Assuiming that I am going to use 3 threads
    # plit_count = len(methods) / 3

    # just for learning purposes dealing with pools in hardcoded way.

    # list_methods = list(methods)
    #
    # t1_pool = list_methods[:200]
    # t2_pool = list_methods[201: 400]
    # t3_pool = list_methods[401:]
    #
    # all_tc_ids = set()
    #
    #
    # def worker(file_path: List[str],
    #            search_param: List[str]):
    #     for param in search_param:
    #         ids = direct_search_original(
    #             file_path_iter=file_path,
    #             search_param=param
    #         )
    #
    #         if ids is not None:
    #             all_tc_ids.update(ids)

    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument("-tc", "--thread_count", type=int, required=True, help="Sets threads count" )
    # args = parser.parse_args()

    # t1 = threading.Thread(target=worker, args=(all_test_files, t1_pool))
    # t2 = threading.Thread(target=worker, args=(all_test_files, t2_pool))
    # t3 = threading.Thread(target=worker, args=(all_test_files, t3_pool))
    #
    # t1.start()
    # t2.start()
    # t3.start()
    #
    # print(t1)
    # print(t2)
    # print(t3)
    #
    # t1.join()
    # t2.join()
    # t3.join()

    all_tc_ids = set()
    for method in methods:
        tc_id = direct_search_original(
            file_path_iter=all_test_files,
            search_param=method
        )

        if tc_id is not None:
            all_tc_ids.update(tc_id)

    print(all_tc_ids)
    print(len(all_tc_ids))

    # strings are immutable, string methods returns changed string.

    # results = pstats.Stats(profile)
    # results.sort_stats(pstats.SortKey.TIME)
    # results.print_stats()
    t2 = timeit.default_timer()

    print(f"Time take - {t2-t1}")
