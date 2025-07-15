from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --------- Modèle Capitaine ----------
class Capitaine(BaseModel):
    id: int
    nom: str
    experience: int 
    specialite: str

# --------- Modèle Bateau ----------
class Bateau(BaseModel):
    id: int
    nom: str
    type: str
    longueur: float
    capacite: int
    en_service: bool
    capitaine_id: Optional[int] = None  

class Trajet(BaseModel):
    id: int
    bateau_id: int
    capitaine_id: int
    depart: str
    arrivee: str
    distance: float

trajets_db: List[Trajet] = []
# --------- Bases de données fictives ---------
bateaux_db: List[Bateau] = []
capitaines_db: List[Capitaine] = []

# --------- Routes BATEAU ----------
@app.get("/bateaux", response_model=List[Bateau])
def lister_bateaux():
    return bateaux_db

@app.get("/bateaux/{bateau_id}", response_model=Bateau)
def lire_bateau(bateau_id: int):
    for bateau in bateaux_db:
        if bateau.id == bateau_id:
            return bateau
    raise HTTPException(status_code=404, detail="Bateau non trouvé")

@app.post("/bateaux", response_model=Bateau)
def ajouter_bateau(bateau: Bateau):
    bateaux_db.append(bateau)
    return bateau

@app.put("/bateaux/{bateau_id}", response_model=Bateau)
def modifier_bateau(bateau_id: int, updated: Bateau):
    for i, bateau in enumerate(bateaux_db):
        if bateau.id == bateau_id:
            bateaux_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Bateau non trouvé")

@app.delete("/bateaux/{bateau_id}")
def supprimer_bateau(bateau_id: int):
    for i, bateau in enumerate(bateaux_db):
        if bateau.id == bateau_id:
            del bateaux_db[i]
            return {"message": f"Bateau {bateau_id} supprimé"}
    raise HTTPException(status_code=404, detail="Bateau non trouvé")

# --------- Routes CAPITAINE ----------
@app.get("/capitaines", response_model=List[Capitaine])
def lister_capitaines():
    return capitaines_db

@app.get("/capitaines/{capitaine_id}", response_model=Capitaine)
def lire_capitaine(capitaine_id: int):
    for capitaine in capitaines_db:
        if capitaine.id == capitaine_id:
            return capitaine
    raise HTTPException(status_code=404, detail="Capitaine non trouvé")

@app.post("/capitaines", response_model=Capitaine)
def ajouter_capitaine(capitaine: Capitaine):
    capitaines_db.append(capitaine)
    return capitaine

@app.put("/capitaines/{capitaine_id}", response_model=Capitaine)
def modifier_capitaine(capitaine_id: int, updated: Capitaine):
    for i, capitaine in enumerate(capitaines_db):
        if capitaine.id == capitaine_id:
            capitaines_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Capitaine non trouvé")

@app.delete("/capitaines/{capitaine_id}")
def supprimer_capitaine(capitaine_id: int):
    for i, capitaine in enumerate(capitaines_db):
        if capitaine.id == capitaine_id:
            del capitaines_db[i]
            # Supprimer la liaison dans les bateaux
            for bateau in bateaux_db:
                if bateau.capitaine_id == capitaine_id:
                    bateau.capitaine_id = None
            return {"message": f"Capitaine {capitaine_id} supprimé"}
    raise HTTPException(status_code=404, detail="Capitaine non trouvé")

# ✅ Liste des bateaux en service
@app.get("/bateaux/en_service", response_model=List[Bateau])
def bateaux_en_service():
    return [b for b in bateaux_db if b.en_service]

# ✅ Recherche par type de bateau
@app.get("/bateaux/search", response_model=List[Bateau])
def rechercher_par_type(type: str = Query(..., alias="type")):
    return [b for b in bateaux_db if b.type.lower() == type.lower()]


# ✅ Tri par capacité
@app.get("/bateaux/tri", response_model=List[Bateau])
def trier_par_capacite(ordre: str = Query("asc", alias="ordre")):
    return sorted(
        bateaux_db,
        key=lambda b: b.capacite,
        reverse=(ordre == "desc")
    )



# --------- Route de liaison ----------
@app.post("/bateaux/{bateau_id}/capitaine/{capitaine_id}")
def affecter_capitaine(bateau_id: int, capitaine_id: int):
    bateau = next((b for b in bateaux_db if b.id == bateau_id), None)
    capitaine = next((c for c in capitaines_db if c.id == capitaine_id), None)

    if not bateau:
        raise HTTPException(status_code=404, detail="Bateau non trouvé")
    if not capitaine:
        raise HTTPException(status_code=404, detail="Capitaine non trouvé")

    bateau.capitaine_id = capitaine_id
    return {"message": f"Capitaine {capitaine_id} affecté au bateau {bateau_id}"}

# --------- Route pour voir les bateaux d’un capitaine ----------
@app.get("/capitaines/{capitaine_id}/bateaux", response_model=List[Bateau])
def bateaux_du_capitaine(capitaine_id: int):
    return [b for b in bateaux_db if b.capitaine_id == capitaine_id]

# --------- ROUTES TRAJETS ----------
@app.post("/trajets", response_model=Trajet)
def ajouter_trajet(trajet: Trajet):
    # Vérifie si le bateau existe
    bateau = next((b for b in bateaux_db if b.id == trajet.bateau_id), None)
    if not bateau:
        raise HTTPException(status_code=404, detail="Bateau non trouvé")

    # Vérifie si le capitaine existe
    capitaine = next((c for c in capitaines_db if c.id == trajet.capitaine_id), None)
    if not capitaine:
        raise HTTPException(status_code=404, detail="Capitaine non trouvé")

    trajets_db.append(trajet)
    return trajet

@app.get("/trajets", response_model=List[Trajet])
def lister_trajets():
    return trajets_db

@app.get("/trajets/{trajet_id}", response_model=Trajet)
def lire_trajet(trajet_id: int):
    for trajet in trajets_db:
        if trajet.id == trajet_id:
            return trajet
    raise HTTPException(status_code=404, detail="Trajet non trouvé")

@app.get("/capitaines/{capitaine_id}/trajets", response_model=List[Trajet])
def trajets_du_capitaine(capitaine_id: int):
    return [t for t in trajets_db if t.capitaine_id == capitaine_id]

@app.get("/bateaux/{bateau_id}/trajets", response_model=List[Trajet])
def trajets_du_bateau(bateau_id: int):
    return [t for t in trajets_db if t.bateau_id == bateau_id]
@app.put("/trajets/{trajet_id}", response_model=Trajet)
def modifier_trajet(trajet_id: int, updated: Trajet):
    for i, t in enumerate(trajets_db):
        if t.id == trajet_id:
            trajets_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Trajet non trouvé")

@app.delete("/trajets/{trajet_id}")
def supprimer_trajet(trajet_id: int):
    for i, t in enumerate(trajets_db):
        if t.id == trajet_id:
            del trajets_db[i]
            return {"message": f"Trajet {trajet_id} supprimé"}
    raise HTTPException(status_code=404, detail="Trajet non trouvé")

@app.get("/trajets/recherche", response_model=List[Trajet])
def recherche_par_port_depart(depart: str = Query(..., alias="depart")):
    return [t for t in trajets_db if t.depart.lower() == depart.lower()]


@app.get("/trajets/longs", response_model=List[Trajet])
def trajets_longue_distance():
    return [t for t in trajets_db if t.distance > 500]


@app.get("/trajets/tri-distance", response_model=List[Trajet])
def trier_trajets_par_distance(ordre: str = Query("asc", alias="ordre")):
    return sorted(
        trajets_db,
        key=lambda t: t.distance,
        reverse=(ordre == "desc")
    )


