from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# TODO cache ?

def query_datasets():
    URL = "http://hackathon2018.ontotext.com/repositories/plosh"

    QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?dataset_uri ?label  where {           
        ?dataset_uri a qb:DataSet .
        OPTIONAL{ 
            ?dataset_uri rdfs:label ?label 
            filter(langMatches(lang(?label),"fr"))
            
        }
    }
    """

    wrapper = SPARQLWrapper(URL)
    wrapper.setQuery(QUERY)
    wrapper.setReturnFormat(JSON)
    json = wrapper.query().convert()

    def label_modif(row):
        if "label" in row.keys():
            return row["label"]["value"] 
        else:
            return row["dataset_uri"]["value"]

    return [ {"label": label_modif(row), "value": label_modif(row)} for row in json["results"]["bindings"] ] 

def queryToDataFrame(results):
    results_value=results['results']['bindings']
    table=pd.DataFrame([[x[name]['value'] for x in results_value]  for name in list(results_value[0].keys())]).T
    table.columns=list(results_value[0].keys())
    return table

def query_dimensions():
    
    URL="http://hackathon2018.ontotext.com/repositories/plosh"
    sparql = SPARQLWrapper(URL)
    sparql.setReturnFormat(JSON)
    
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?dim ?label where {           
        ?s a qb:DataSet.
        ?s qb:structure ?dsd.
        ?dsd qb:component/qb:dimension ?dim.
        ?dim rdfs:label ?labelfr

        filter(langMatches(lang(?labelfr),"fr"))
        BIND(IF(BOUND(?labelfr), ?labelfr,?dim) AS ?label)
    } 
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
   
    return queryToDataFrame(results)
    
def query_measures():
    
    sparql = SPARQLWrapper("http://hackathon2018.ontotext.com/repositories/plosh")
    sparql.setReturnFormat(JSON)
    
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX mes: <http://id.insee.fr/meta/mesure/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

    SELECT ?measure ?label where {           
        ?s a qb:DataSet.
        ?s qb:structure ?dsd.
        ?dsd qb:component/qb:measure ?measure .
        ?measure rdfs:label ?labelfr

        filter(langMatches(lang(?labelfr),"fr"))
        BIND(IF(BOUND(?labelfr), ?labelfr,"NO LABEL !!!"@fr) AS ?label)
    } LIMIT 100
    """

    sparql.setQuery(query)
    results = sparql.query().convert()

    return queryToDataFrame(results)



def query_dimensions_olo(cube_label):
    
    URL="http://hackathon2018.ontotext.com/repositories/plosh"
    sparql = SPARQLWrapper(URL)
    sparql.setReturnFormat(JSON)
    
     query = """
     PREFIX qb: <http://purl.org/linked-data/cube#>
     PREFIX dct: <http://purl.org/dc/terms/>
     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

     select ?dimensionLabel 
     where {
     graph ?graph {
        ?datacube a qb:DataSet ;
                  rdfs:label|dct:title ?datacubeLabel ;
                  qb:structure/qb:component/qb:dimension ?dimension .
        optional {
            ?dimension rdfs:label ?dimensionLabel .
            filter (lang(?dimensionLabel) = "fr")
       }
       filter
        ((lang(?datacubeLabel) = "fr")
        &&
            (str(?datacubeLabel) = """+ cube_label +""")  )
     }
    }
    order by ?dimension
    limit 100
    """

    sparql.setQuery(query)
    results = sparql.query().convert()
   
    return queryToDataFrame(results)
