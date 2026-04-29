from rdflib import Graph

def query_berita(file="berita.ttl", sumber=None):
    g = Graph()
    g.parse(file, format="turtle")

    filter_clause = ""
    if sumber:
        filter_clause = f'FILTER(?sumber = "{sumber}")'

    sparql_query = f"""
    PREFIX dc:     <http://purl.org/dc/elements/1.1/>
    PREFIX schema: <http://schema.org/>

    SELECT ?judul ?url ?tanggal ?kategori ?sumber
    WHERE {{
        ?artikel a schema:NewsArticle ;
                 dc:title     ?judul ;
                 dc:source    ?url ;
                 dc:date      ?tanggal ;
                 dc:subject   ?kategori ;
                 dc:publisher ?sumber .
        {filter_clause}
    }}
    ORDER BY DESC(?tanggal)
    """

    hasil = g.query(sparql_query)

    data = []
    for row in hasil:
        data.append({
            "Judul"   : str(row.judul),
            "Sumber"  : str(row.sumber),
            "Tanggal" : str(row.tanggal),
            "Kategori": str(row.kategori),
            "URL"     : str(row.url),
        })
    return data