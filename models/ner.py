from collections import Counter
import spacy
# import en_core_web_sm

def ner_spacey(df):
    
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(''.join(df['text'].tolist()))

    # extract the entities based on their categories

    person_list = []
    norp_list= []
    fac_list =[]
    org_list = []
    gpe_list=[]
    loc_list=[]
    product_list=[]
    event_list=[]

    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            person_list.append(ent.text)

        elif ent.label_ == 'NORP':  # nationalities or religious or political groups
            norp_list.append(ent.text)

        elif ent.label_ == 'FAC':  # buildings, airports
            fac_list.append(ent.text)

        elif ent.label_ == 'ORG':  # companies, institutions
            org_list.append(ent.text)

        elif ent.label_ == 'GPE':  # countries, cities
            gpe_list.append(ent.text)

        elif ent.label_ == 'LOC':  # non-gpe locations (ex: mountains)
            loc_list.append(ent.text)

        elif ent.label_ == 'PRODUCT':  # objects, vehicules...
            product_list.append(ent.text)

        elif ent.label_ == 'EVENT':  # battles,sports events etc
            event_list.append(ent.text)


   #  Counter(person_list).most_common(5) = ( name of the entity, number of occurence)
   # We only need the first element of the tuple
    person_counts = [i[0] for i in Counter(person_list).most_common(5)] 
    norp_counts = [i[0] for i in Counter(norp_list).most_common(5)] 
    fac_counts = [i[0] for i in Counter(fac_list).most_common(5)]
    org_counts = [i[0] for i in Counter(org_list).most_common(5)]
    gpe_counts =[i[0] for i in Counter(gpe_list).most_common(5)] 
    loc_counts = [i[0] for i in Counter(loc_list).most_common(5)]
    product_counts = [i[0] for i in Counter(product_list).most_common(5)]
    event_counts = [i[0] for i in Counter(event_list).most_common(5)] 

    return person_counts,norp_counts,fac_counts,org_counts,gpe_counts,loc_counts,product_counts,event_counts

