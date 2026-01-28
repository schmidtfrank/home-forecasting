from parsing import remove_commas
from parsing import remove_list_newlines
from parsing import remove_li_tag
######## RUN WITH python -m pytest testing.py
tests = ["45,000","2,2,2","58,000"]
actual = [45000,222,58000]

for i in range(len(tests)):
    val = remove_commas(tests[i])
    assert type(val) == int, "Output is not an integer."
    assert val == actual[i], f"Expected: {actual[i]} but got {val}"

test_lists = [['\n','<li>...</li>','\n'],['\n','\n'],['<li>']]
actual_lists = [['<li>...</li>'],[],['<li>']]

for i, test in enumerate(test_lists):
    new_list = remove_list_newlines(test)
    assert new_list == actual_lists[i], f"Expected: {actual_lists[i]} but got {new_list}"

test_lists = [["<li>...</li>"],["<li>hey</li>"],[],["<li>what","ok"]]
actual_lists = [["..."],["hey"],[],["what","ok"]]

for i, test in enumerate(test_lists):
    new_list = remove_li_tag(test)
    assert new_list == actual_lists[i], f"Expected: {actual_lists[i]}, but got {new_list}"