import os
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DC

def buat_rdf(berita_list, output_file="berita.ttl"):
    # Hapus file lama dulu kalau ada
    if os.path.exists(output_file):
        os.remove(output_file)

    g = Graph()

    BERITA = Namespace("http://beritapolitik.id/berita/")
    SCHEMA  = Namespace("http://schema.org/")

    g.bind("berita", BERITA)
    g.bind("schema", SCHEMA)
    g.bind("dc", DC)

    for i, b in enumerate(berita_list):
        subjek = URIRef(BERITA + f"artikel_{i}")

        g.add((subjek, RDF.type,     SCHEMA.NewsArticle))
        g.add((subjek, DC.title,     Literal(b["judul"])))
        g.add((subjek, DC.source,    Literal(b["url"])))
        g.add((subjek, DC.date,      Literal(b["tanggal"])))
        g.add((subjek, DC.subject,   Literal(b["kategori"])))
        g.add((subjek, DC.publisher, Literal(b["sumber"])))

    g.serialize(destination=output_file, format="turtle")
    print(f"RDF disimpan: {output_file} ({len(berita_list)} artikel)")