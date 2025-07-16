from locust import HttpUser, task, between
import random

class BateauCapitaineUser(HttpUser):
    wait_time = between(1, 3)

    last_bateau_id = None
    last_capitaine_id = None
    last_trajet_id = None

    @task(2)
    def creer_capitaine(self):
        capitaine_id = random.randint(1000, 9999)
        data = {
            "id": capitaine_id,
            "nom": f"Capitaine {capitaine_id}",
            "experience": random.randint(1, 30),
            "specialite": random.choice(["voilier", "cargo", "pêche"])
        }
        response = self.client.post("/capitaines", json=data)
        if response.status_code == 200:
            self.last_capitaine_id = capitaine_id

    @task(2)
    def creer_bateau(self):
        bateau_id = random.randint(1000, 9999)
        data = {
            "id": bateau_id,
            "nom": f"Bateau {bateau_id}",
            "type": random.choice(["voilier", "cargo", "pêche"]),
            "longueur": round(random.uniform(10.0, 50.0), 2),
            "capacite": random.randint(5, 300),
            "en_service": True,
            "capitaine_id": None
        }
        response = self.client.post("/bateaux", json=data)
        if response.status_code == 200:
            self.last_bateau_id = bateau_id

    @task(2)
    def creer_trajet(self):
        if self.last_bateau_id and self.last_capitaine_id:
            trajet_id = random.randint(1000, 9999)
            data = {
                "id": trajet_id,
                "bateau_id": self.last_bateau_id,
                "capitaine_id": self.last_capitaine_id,
                "depart": random.choice(["Marseille", "Tanger", "Gênes"]),
                "arrivee": random.choice(["Casablanca", "Nice", "Palermo"]),
                "distance": round(random.uniform(100.0, 1500.0), 2)
            }
            response = self.client.post("/trajets", json=data)
            if response.status_code == 200:
                self.last_trajet_id = trajet_id

    @task(2)
    def lister_bateaux(self):
        self.client.get("/bateaux")

    @task(2)
    def lister_capitaines(self):
        self.client.get("/capitaines")

    @task(1)
    def lister_bateaux_en_service(self):
        self.client.get("/bateaux/en_service")

    @task(1)
    def rechercher_bateaux_par_type(self):
        bateau_type = random.choice(["voilier", "cargo", "pêche"])
        self.client.get(f"/bateaux/search?type={bateau_type}")

    @task(1)
    def trier_bateaux_par_capacite(self):
        ordre = random.choice(["asc", "desc"])
        self.client.get(f"/bateaux/tri?ordre={ordre}")

    @task(1)
    def modifier_bateau(self):
        if self.last_bateau_id:
            data = {
                "id": self.last_bateau_id,
                "nom": f"Bateau Modifié {self.last_bateau_id}",
                "type": "modifié",
                "longueur": 42.0,
                "capacite": 200,
                "en_service": False,
                "capitaine_id": self.last_capitaine_id
            }
            self.client.put(f"/bateaux/{self.last_bateau_id}", json=data)

    

    @task(1)
    def modifier_capitaine(self):
        if self.last_capitaine_id:
            data = {
                "id": self.last_capitaine_id,
                "nom": f"Capitaine Modifié {self.last_capitaine_id}",
                "experience": 99,
                "specialite": "toutes"
            }
            self.client.put(f"/capitaines/{self.last_capitaine_id}", json=data)


    @task(1)
    def lier_capitaine_au_bateau(self):
        if self.last_bateau_id and self.last_capitaine_id:
            self.client.post(f"/bateaux/{self.last_bateau_id}/capitaine/{self.last_capitaine_id}")

    @task(1)
    def bateaux_du_capitaine(self):
        if self.last_capitaine_id:
            self.client.get(f"/capitaines/{self.last_capitaine_id}/bateaux")

    # 🔽 TRAJETS 🔽

   
    @task(1)
    def lister_trajets(self):
        self.client.get("/trajets")

    @task(1)
    def modifier_trajet(self):
        if self.last_trajet_id and self.last_bateau_id and self.last_capitaine_id:
            data = {
                "id": self.last_trajet_id,
                "bateau_id": self.last_bateau_id,
                "capitaine_id": self.last_capitaine_id,
                "depart": "Modifié",
                "arrivee": "Modifié",
                "distance": 888.8
            }
            self.client.put(f"/trajets/{self.last_trajet_id}", json=data)



    @task(1)
    def trajets_du_capitaine(self):
        if self.last_capitaine_id:
            self.client.get(f"/capitaines/{self.last_capitaine_id}/trajets")

    @task(1)
    def trajets_du_bateau(self):
        if self.last_bateau_id:
            self.client.get(f"/bateaux/{self.last_bateau_id}/trajets")

    @task(1)
    def recherche_trajets_par_depart(self):
        port = random.choice(["Marseille", "Tanger", "Gênes"])
        self.client.get(f"/trajets/recherche?depart={port}")

    @task(1)
    def trajets_longue_distance(self):
        self.client.get("/trajets/longs")

    @task(1)
    def trier_trajets_par_distance(self):
        ordre = random.choice(["asc", "desc"])
        self.client.get(f"/trajets/tri-distance?ordre={ordre}")

    @task(1)
    def supprimer_bateau(self):
        if self.last_bateau_id:
            self.client.delete(f"/bateaux/{self.last_bateau_id}")
            self.last_bateau_id = None

    @task(1)
    def supprimer_capitaine(self):
        if self.last_capitaine_id:
            self.client.delete(f"/capitaines/{self.last_capitaine_id}")
            self.last_capitaine_id = None


    @task(1)
    def supprimer_trajet(self):
        if self.last_trajet_id:
            self.client.delete(f"/trajets/{self.last_trajet_id}")
            self.last_trajet_id = None