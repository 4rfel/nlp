# create a dictionary of the inverted index
def invert_list(dic):
    inverted_dic = {}
    # montando a lista invertida
    for word, value in dic.items():
        for item in value:
            tf = item[0]
            doc = item[1]
            if doc in inverted_dic:
                inverted_dic[doc].append((tf, word))
            else:
                inverted_dic[doc] = [(tf, word)]

    # ordenando de forma decrescente com base no tf
    inverted_dic = {key.lower(): sorted(value, reverse=True) for key, value in inverted_dic.items()}

    # criando o dicionario de keywords no formato desejado {"keyword": (word, [title, title, title])}"}
    inverted_dict = []
    for word, value in inverted_dic.items():
        titles = []
        for item in value:
            titles.append(item[1])
        inverted_dict.append({"keyword": (word, titles)})
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

keywords = {"txt1": [(1, "aaa"), (2, "bbb"), (3, "ccc")], "txt2": [(3, "aaa"), (1, "bbb"), (2, "ccc")], "txt3": [(2, "aaa"), (3, "bbb"), (1, "ccc")]}
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

