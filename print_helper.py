def print_abstract(abstract, n=150):
    length = len(abstract)
    times = int(length / n)
    print("ABSTRACT: ")
    if length < n:
        print("\"" + abstract + "\"")
    else:
        print("\"" + abstract[:n])
    for i in range(1, times):
        print(abstract[i * n: (i + 1) * n])
    print(abstract[times * n:] + "\"")


def print_result(publication_id, abstract, keywords, ref_keywords):
    print("PUBLICATION: " + str(publication_id))
    print_abstract(abstract)
    print("My Result: " + str(keywords))
    print("Ref Result: " + str(ref_keywords))
