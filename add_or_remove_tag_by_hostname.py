from falconpy import Hosts
from falconpy import UserManagement
from colorama import Fore, Style
from colorama import init
import pandas as pd

print("bienvenue le script va permettre de pouvoir ajouter le tag que vous voulez en fonction de l'hostname que vous mettez ")
# les identifiants
client_id = "here"
client_secret = "here"


falcon = Hosts(client_id=client_id, client_secret=client_secret) # Pour la connexion

print("Vous pouvez entrer plusieurs hostnames pour les trouver.") # definition du projet
hostnames = []  # Liste des hostnames 

# Collecte des hostnames
while True:
    hostname = input("Entrez un hostname : ") # entrer un nom 
    hostnames.append(hostname) # ajouter un nom 
    
    ajouter_plus = input("Voulez-vous ajouter un autre hostname ? (oui/non) : ").strip().lower() # hostname ajouter
    if ajouter_plus != 'oui': # demande une permission
        break # quitte

print("Hostnames à rechercher :", hostnames) # j'affiche  les hostnames 

# Demande si l’utilisateur souhaite ajouter ou retirer un tag 
while True:
    choice = input("Souhaitez-vous ajouter ou retirer un tag? (add/remove) : ").strip().lower() # pour demander un add ou remove adapte l'entrée de l'utilisateur
    if choice in ['add', 'remove']:
        break
    print("Choix invalide. Veuillez entrer 'add' ou 'remove'.") # si le choix est pas bon 


tag_choice = input("Entrez le tag que vous souhaitez appliquer aux hostnames trouvés : ") # ici on initie la variable pour l'entrée du tag
tag_list = [tag_choice] # on le place dans une liste

# Boucle pour chaque hostname pour récupérer les informations et appliquer le tag
for hostname in hostnames: 
    print(f"\nRecherche pour le hostname : {hostname}")  # recherche le hostname
    
    # Étape 1: Récupérer l'ID de l'hôte
    response = falcon.query_devices_by_filter( 
        filter=f"hostname:'{hostname}'", # on filtre par hostname
        limit=1
    )

    # Si la requête est réussie et des appareils sont trouvés
    if response.get("status_code") == 200 and response.get("body", {}).get("resources"): # si la reponse est bonne je récupère le host ID de l'hostname
        host_id = response["body"]["resources"][0] # on récupere le premier élément 
        print(f"ID de l'hôte trouvé : {host_id}") # le host ID 

        # Récupération des détails de l'hôte
        details_response = falcon.get_device_details(ids=[host_id]) # on récupère les détails 
        details = details_response.get("body", {}).get("resources", [{}])[0] if details_response.get("status_code") == 200 else {} # ici on récupere toutes les informations
        
        print("Voici les informations de l'hote :") # Informations
        print(f"Hostname : {details.get('hostname', 'N/A')}")
        print(f"Local IP : {details.get('local_ip', 'N/A')}")
        print(f"External IP : {details.get('external_ip', 'N/A')}")
        print(f"Device ID : {details.get('device_id', 'N/A')}")
        print(f"Instance ID : {details.get('instance_id', 'N/A')}")
        print(f"Machine Domain : {details.get('machine_domain', 'N/A')}")
        print(f"Platform Name : {details.get('platform_name', 'N/A')}")
        print(f"Platform ID : {details.get('platform_id', 'N/A')}")
        print(f"Groups : {details.get('groups', 'N/A')}")
        print(f"Tags : {details.get('tags', 'N/A')}")
        print(f"Config ID Base : {details.get('config_id_base', 'N/A')}")

        # On ajoute ou on retire le tag
        tag_response = falcon.update_device_tags(action_name=choice, ids=[host_id], tags=tag_list) # ici nous mettons le choix de l'utilisateur
        if tag_response.get("status_code") == 200 or tag_response.get("status_code") == 202 : # code 200 = affichage réussie
            print(f"Tag '{tag_choice}' résolu avec succès à {hostname}.") # résultat
        else:
            print(f"Erreur lors de l'opération de {choice} du tag : Code {tag_response['status_code']}") 
    else:
        print(f"Aucun appareil trouvé ou erreur de requête pour le hostname {hostname} (Code : {response.get('status_code')})")
