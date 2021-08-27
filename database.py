import mysql.connector
db = mysql.connector.connect(user='root',
                             password='Sc_Sc_05110511',
                             host='127.0.0.1',
                             database='data')


def get_publication_keywords(publication_id):
    cursor = db.cursor()
    query = "SELECT FoS_id " \
            "FROM publication_fos " \
            "WHERE publication_id = {}".format(publication_id)
    cursor.execute(query)
    data = cursor.fetchall()

    keyword_ids = [i[0] for i in data]
    keywords = []
    for keyword_id in keyword_ids:
        query = "SELECT FoS_name " \
                "FROM fos " \
                "WHERE id = {}".format(keyword_id)
        cursor.execute(query)
        data = cursor.fetchall()
        keyword = data[0][0]
        keywords.append(keyword)
    return keywords


def get_multi_publications(n=30):
    cursor = db.cursor()
    query = "SELECT id, abstract " \
            "FROM publication " \
            "WHERE abstract IS NOT NULL " \
            "LIMIT {}".format(n)
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def main():
    # abstract = get_abstract()
    # # print(abstract)
    # keywords = get_publication_keywords()
    # # print(keywords)
    publications = get_multi_publications()
    print(publications)


if __name__ == '__main__':
    main()
