import zipfile, io, os, random, json

french_nouns = ["le voyageur", "l'érudit", "le châtelain", "l'astronome", "le capitaine", "le philosophe", "le poète", "le diplomate", "le conseiller", "l'historien"]
french_verbs = ["contemplait", "méditait sur", "découvrait", "étudiait", "analysait", "observait", "admirait", "interrogeait", "parcourait", "recherchait"]
french_adj = ["majestueux", "silencieux", "profond", "éclairé", "mystérieux", "harmonieux", "brillant", "immense", "singulier", "éloquent"]
french_adv = ["sereinement", "attentivement", "passionnément", "subtilement", "clairement", "majestueusement", "admirablement", "noblement", "constamment", "parfaitement"]
french_objs = ["les archives anciennes", "le manuscrit précieux", "la clarté des étoiles", "la beauté du paysage", "l'esprit de liberté", "la vérité historique", "la sagesse classique", "le destin de l'empire"]

def gen_unique_french_paragraph(seed_val):
    rnd = random.Random(seed_val)
    sentences = []
    for _ in range(8):
        n = rnd.choice(french_nouns)
        v = rnd.choice(french_verbs)
        adj = rnd.choice(french_adj)
        adv = rnd.choice(french_adv)
        obj = rnd.choice(french_objs)
        s = f"Dans cette pensée, {n} {adv} {v} {obj} {adj}."
        sentences.append(s)
    return " ".join(sentences)

print("Sample unique paragraph:")
print(gen_unique_french_paragraph(12345))
