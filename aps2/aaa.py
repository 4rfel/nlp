# create a dictionary of the inverted index
def invert_list(dic):
    inverted_dic = {}
    for key, value in dic.items():
        for item in value:
            tf = item[0]
            doc = item[1]
            if doc in inverted_dic:
                inverted_dic[doc].append((tf, key))
            else:
                inverted_dic[doc] = [(tf, key)]
        inverted_dic = {key.lower(): sorted(value) for key, value in inverted_dic.items()}
        inverted_dict = []
        for key, value in inverted_dic.items():
            txts = []
            for item in value:
                txts.append(item[1])
            # inverted_dict[key] = txts
            inverted_dict.append({key: txts})
    return inverted_dict

def edit_distance_(s1, s2, n, max_depth):
    if n > max_depth:
        return -1
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    if s1[0] == s2[0]:
        return edit_distance_(s1[1:], s2[1:], n+1, max_depth)
    return 1 + min(edit_distance_(s1, s2[1:], n+1, max_depth), edit_distance_(s1[1:], s2, n+1, max_depth))

def edit_distance(s1, s2, max_depth=3):
    return edit_distance_(s1, s2, 0, max_depth)

keywords = {"txt1": [(0.1, "heLlo"), (0.2, "aaaaaaa")], "txt2": [(0.1, "world"), (0, "hello")], "txt3": [(0.1, "!"), (0.2, "bbbbbbb"), (0.15, "ccccccc"), (0.5, "hello")]}
inverted_keywords_list = invert_list(keywords)
print(inverted_keywords_list)

# search_box = input("Enter a keyword: ")
# if (search_box in inverted_keywords_list):
#     print(inverted_keywords_list[search_box])
# else:
#     # if the keyword is not in the inverted_keywords_list, then change the search_box to the nearest keyword
#     # and print the list of files that contain that keyword using Levenshtein distance
#     # Levenshtein distance is the number of single-character edits (insertions, deletions, or substitutions)
#     # required to change one string into the other.
#     # https://en.wikipedia.org/wiki/Levenshtein_distance
    
#     # find the nearest keyword
#     min_distance = 100
#     nearest_keyword = ""
#     for keyword in inverted_keywords_list:
#         distance = edit_distance(search_box, keyword)
#         if (distance < min_distance):
#             min_distance = distance
#             nearest_keyword = keyword

#     print(f"voce quis dizer: {nearest_keyword}")

#     print(inverted_keywords_list[nearest_keyword])

