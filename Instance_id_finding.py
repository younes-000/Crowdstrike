# ce script doit permettre de te donner une liste d'instcen id et de me renvoyer les nom des machines dans un fichier  hostname_trouvés


from falconpy import Hosts
from colorama import Fore, Style
from colorama import init
import pandas as pd
# Initialiser colorama ppour pouvoir l'utiliser
init()


# les identifiants
client_id = "here"
client_secret = "here"

falcon = Hosts(client_id=client_id, client_secret=client_secret)  # Connexion
print("can you put the path of your document")
filename = input("please write your path the document should have the xlsx extension  ")
df = pd.read_excel(filename, engine='openpyxl') # permet de récuperer les informations du document internet_facing.xlsx (Choisir le document)



colonne = df['Asset ID'].tolist() # je recupere la colonne asset Id ou se trouve les instances ID (en fonction de la colonne ou se trouve les instances ID ) 
print(colonne)

instance_ids = [] # j'inistialise la variable instance_ids
instance_ids.extend(colonne) # j'ajoute toutes les données dans la variable instance_ids
# Initialiser les compteurs



total_hosts_trouves = 0 # les hosts trouvées lorsque le script est lancée
total_hosts_non_trouves = 0 # les hosts qui ne sont pas trouvées lorsque le script est lancé




with open("machine_trouvees.txt", "w") as fichier_trouvees, open("machine_non_trouvees.txt", "w") as fichier_non_trouvees: # on ouvre le fichier en mode write afin de mettre dedans les fichiers trouvées

 for instance_id in instance_ids:
        # Récupération des données à partir de l'instance ID
        response = falcon.query_devices_by_filter(filter=f"instance_id:'{instance_id}'") # j'effectue uen boucle pour récuperer les données d'instances ID en utilisant le filtre
        print(response)
        total_serveur = 0 
        
        if response and "body" in response and "resources" in response["body"] and response["body"]["resources"]:
           
            Host_IDs = response["body"]["resources"]  # récupération des Hosts id 

            # Boucle sur les Host_ID pour récupérer toutes les informations
            for Host_ID in Host_IDs:
                # Récupération des détails à partir du Host ID
                response_host_id = falcon.get_device_details(ids=Host_ID)
            
                # Vérification de la réponse et extraction des informations
                if 'body' in response_host_id and 'resources' in response_host_id['body']:
                    instance_ids_found = [resource['instance_id'] for resource in response_host_id['body']['resources'] if 'instance_id' in resource]  # Récupération des instance ID
                    hostnames = [resource['hostname'] for resource in response_host_id['body']['resources'] if 'hostname' in resource]  # Récupération des hostnames
                    
                    # Dans cette partie on va faire une vérification des données
                    if hostnames and instance_ids_found:
                        message = f"Hostname: {hostnames[0]} | Instance ID: {instance_ids_found[0]} | Host ID: {Host_ID}\n" # on recupere les informations concernant les hosts trouvés
                        message_fichier = instance_ids_found[0]
                        print(Fore.GREEN + message + Style.RESET_ALL) # on affiche le message 
                        fichier_trouvees.write(message)  # on écrit le message dans le fichier crée préalablement
                        total_serveur += 1
                        total_hosts_trouves += 1  # On incrémente avec plus 1
                    else:
                        message = f"Aucun hostname trouvé pour l'instance ID: {instance_id} et Host ID: {Host_ID}\n" # on récupere les informations concernant les hosts non trouvés
                        print(Fore.RED + message + Style.RESET_ALL)
                        message_fichier2 = f"instance_id : {instance_id}\n"
                        fichier_non_trouvees.write(message_fichier2)  # affichage dans le fichier des machines non trouvées
                        total_hosts_non_trouves += 1  # Incrémentation du compteur de hosts non trouvés
                else:
                    message = f"Aucun détail trouvé pour le Host ID: {Host_ID}\n"
                    print(Fore.RED + message + Style.RESET_ALL)
                    message_fichier3 = f"instance_id{Host_ID}\n"
                    fichier_non_trouvees.write(message_fichier3)  # affichage dans le fichier des machines non trouvées
                    total_hosts_non_trouves += 1  # Incrémentation du compteur de hosts non trouvés
        else:
            message = f"Aucune donnée trouvée pour l'instance ID: {instance_id}\n"
            print(Fore.RED + message + Style.RESET_ALL)
            message_fichier4 = f"instance_id : {instance_id}\n"
            fichier_non_trouvees.write(message_fichier4)  # affichage dans le fichier des machines non trouvées
            total_hosts_non_trouves += 1



total_hosts = total_hosts_trouves + total_hosts_non_trouves # on calcule la totalité des hosts de la liste
if total_hosts > 0: # on fait une condition pour confirmer que c'est supérieur à 0
    pourcentage_trouves = (total_hosts_trouves / total_hosts) * 100 # on calcule le pourcentage pour les hosts trouvés
    pourcentage_non_trouves = (total_hosts_non_trouves / total_hosts) * 100 # on calcule le pourcentage pour les hosts non trouvés

    print(f"\nTotal de hosts trouvés: {total_hosts_trouves}")
    print(f"Total de hosts non trouvés: {total_hosts_non_trouves}")
    print(f"Pourcentage de hosts trouvés: {pourcentage_trouves:.2f}%")
    print(f"Pourcentage de hosts non trouvés: {pourcentage_non_trouves:.2f}%")
else:
    print("Aucun host trouvé ou non trouvé.")
