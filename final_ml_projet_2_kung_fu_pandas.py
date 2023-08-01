# -*- coding: utf-8 -*-
"""FINAL ML Projet 2 Kung Fu Pandas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R0mIqq0W_E18kj5uxJtwiArTbxxhkqs4

## **ETAPE 1 : IMPORTS**
"""

##from google.colab import  drive
##drive.mount('/drive')



##"""# **ETAPE 2 : MISE EN PETITES BRIQUES**"""

### Import et préparation des films
# Mange : rien
# Retourne : un DF de tous les films provenant du csv, propre avec bons types
def import_prep_dffilms():
    DF_films = pd.read_csv("df_pandas.csv")
    ##création des colonnes minuscules pour original et primary title:
    DF_films=DF_films.assign(originaltitlemin=DF_films['originalTitle'].str.lower(),primarytitlemin=DF_films['primaryTitle'].str.lower())
    ##changer les actor et actress en liste:
    DF_films['actor']=DF_films['actor'].apply(literal_eval)
    DF_films['actress']=DF_films['actress'].apply(literal_eval)
    ##pour eviter qu'il compte les sans objet comme valeur:
    DF_films['actor'] = DF_films['actor'].apply(lambda x: ''  if x == ['sans objet'] else x)
    DF_films['actress'] = DF_films['actress'].apply(lambda x: ''  if x == ['sans objet'] else x)
    ##création des 5 colonnes:
    DF_films=DF_films.assign(nb_actor=DF_films['actor'].apply(lambda x: len(x)),nb_actress=DF_films['actress'].apply(lambda x: len(x)))
    #création colonne 'nb_films_director'
    DF_films['nb_films_director'] = DF_films.groupby('director')['director'].transform('count')
    ##changer les "" en 0:
    DF_films['nb_actor'] = DF_films['nb_actor'].apply(lambda x: 0  if x == "" else x)
    DF_films['nb_actress'] = DF_films['nb_actress'].apply(lambda x: 0  if x == "" else x)
    DF_films=DF_films.assign(total_acteurs=DF_films['nb_actor']+DF_films['nb_actress'])
    DF_films=DF_films.assign(pourc_actor=(DF_films['nb_actor']/DF_films['total_acteurs'])*100,pourc_actress=(DF_films['nb_actress']/DF_films['total_acteurs'])*100)
    DF_films['pourc_actress'].fillna(0,inplace=True)
    DF_films['pourc_actor'].fillna(0,inplace=True)
    #créer une colonne 'Films_WW' pour filtrer les films diffusés dans toutes les régions (valeur 1 ou 0)
    DF_films['films_WW']=0
    for i in range(len(DF_films)):
        if "XWW" in DF_films['region'][i]:
            DF_films['films_WW'][i]=1
    ##changer la colonne genre en list:
    DF_films['genres']=DF_films['genres'].apply(lambda x: list(x.split(',')))
    #OHencod = OneHotEncoder(sparse=False)
    # je fais un OneHotEncoder avec mes liste dans genres
    mlb = MultiLabelBinarizer()
    df_genres_encod = pd.DataFrame(mlb.fit_transform(DF_films['genres']),columns=mlb.classes_, index=DF_films.index)
    # on concatène avec notre df_final précédent
    DF_films = pd.concat([DF_films, df_genres_encod], axis=1)

    return DF_films

DF_films_test = import_prep_dffilms()
##DF_films_test

### Rechercher la ligne d’un film en particulier
# Mange : une chaine de caractère qui est le nom du film + un DF de tous les films
# Retourne : les valeurs de la ligne du film concerné
def recherche_ligne1film(nomfilmrecherche, DF_films):
        nomfilmrecherche=nomfilmrecherche.lower()
        cond=DF_films["primarytitlemin"].str.contains(nomfilmrecherche)
        cond1=DF_films["originaltitlemin"].str.contains(nomfilmrecherche)  
        ligne_1film = DF_films[cond|cond1]
        while len(ligne_1film)==0:
              ligne_1film=st.text_input('Film non trouvé. Veuillez saisir un nouveau titre de film :')
              ligne_1film=ligne_1film.lower()
              cond=DF_films["primarytitlemin"].str.contains(ligne_1film)
              cond1=DF_films["originaltitlemin"].str.contains(ligne_1film)  
              ligne_1film = DF_films[cond|cond1]
        if len(ligne_1film)==1:
              return ligne_1film
        else:
            ligne_1film=ligne_1film.reset_index()
            pd.set_option('display.max_rows', None)
         

            st.write(ligne_1film[['primaryTitle','originalTitle','startYear']])
            index=st.number_input('Précisez un numéro de ligne de film parmi la liste :',min_value=0,max_value=len(ligne_1film)-1)
            # while index not in range(len(ligne_1film)):
            #       st.write('choissisez un numéro entre 0 et ',len(ligne_1film)-1,':')
            #       index=st.number_input()
            ligne_1film=pd.DataFrame(ligne_1film.iloc[index]).T
            ligne_1film=ligne_1film.sort_values('startYear',ascending=False)
            return ligne_1film

# st.write('Pour une utilisation optimale de notre application,')
# st.write('nous vous recommandons de choisir un film dont la durée est comprise entre 50 et 200 minutes')
# st.write('et qui a au moins un des genres suivants : horror, crime, thriller, film-noir.')
# nomfilmrecherche=st.text_input('Veuillez entrer un titre de film :',value=" ")
# ligne_1film_test = recherche_ligne1film(nomfilmrecherche, DF_films_test)
##ligne_1film_test

### Préparation entrainement du modèle
# Mange : un DF avec tous les films
# Retourne : un scaler entrainé + un modèle entrainé
def prep_model(DF_films):
#     ### récup des données quanti
    X = DF_films.select_dtypes('number')
    
    ### standardisation des données
    ### init
    scaler_films = StandardScaler().fit(X)
    ### entrainer
    ##scaler_films.fit(X)
    ### appliquer
    X_scaled = scaler_films.transform(X)
    X_scaled = pd.DataFrame(X_scaled, index=X.index, columns=X.columns)
    #X_scaled

    ### entrainement du modèle
    ### instancier modele
    model_films = NearestNeighbors().fit(X_scaled)
    ### entrainer modele
    ##model_films.fit(X_scaled)
    return scaler_films, model_films

# scaler_films_pretalemploi, model_films_pretalemploi = prep_model(DF_films_test)
##scaler_films_pretalemploi, model_films_pretalemploi

### Trouver les plus proches voisins d’un film en particulier
# Mange : la ligne d’un film + un DF de tous les films + scaler entrainé + modèle entrainé
# Afficher : les films qui ressemblent le plus
def filmslesplusproches(ligne_1film, DF_films, scaler_films, model_films):
    ### scaler la ligne du film
    ligne_1film_scaled = scaler_films.transform(ligne_1film[scaler_films.feature_names_in_])
    ligne_1film_scaled = pd.DataFrame(ligne_1film_scaled, index=ligne_1film.index, columns=scaler_films.feature_names_in_) # ligne optionnelle
    ### les voisins
    neigh_dist, neigh_films =  model_films.kneighbors(ligne_1film_scaled)
    filmsproches = DF_films[['primaryTitle','originalTitle','startYear','genres','region','director','actor','actress','runtimeMinutes']].iloc[neigh_films[0]]
    pd.set_option('display.max_rows', None)
    return filmsproches


from PIL import Image
image=Image.open('C:/Users/Sitra/OneDrive/Documents/projet films/la creuse.jpg')
# st.image(image)
# st.title(':red[Recommandations de films frissons] :sunglasses:')
options = st.sidebar.radio("Menu:star2:",options=['Présentation', "KPI", "Recommandations de films",])#"Actualisation des données" ])
DF_films_test = import_prep_dffilms()
#DF_films_test
def reco_films():
    st.write('Pour une utilisation optimale de notre application,nous vous recommandons de choisir un film qui a au moins un des genres suivants : horror, crime, thriller, film-noir.')
    nomfilmrecherche=st.text_input('Veuillez entrer un titre de film :',value=" ")
    ligne_1film_test = recherche_ligne1film(nomfilmrecherche, DF_films_test)
    scaler_films_pretalemploi, model_films_pretalemploi = prep_model(DF_films_test) # ici DF_films_test est pas dans la fonction mais il va aller le chercher dans le global
    return filmslesplusproches(ligne_1film_test, DF_films_test, scaler_films_pretalemploi, model_films_pretalemploi)
if options == 'Présentation' : 
    st.image(image)
    st.header(":blue[Contexte :] ")
    st.subheader(":green[_Objectifs_ :]Créer une application de services de  recommandation de films")
    st.write("Durant ce projet 2, nous avons travaillé en groupe de 5 personnes pour mettre nos compétences DATA au service d'un cinéma de la Creuse. ")
    st.header(":blue[Etape 1 :] Filtration donnée et sélection de notre genre")
    st.write('Nous avons travaillé sur un jeu de données issu de IMBD, qui est une base de données en ligne sur le cinéma mondial, mais pas seulement : il y a aussi les séries TV, les jeux vidéos…')
    st.write('Selon ces critères, nous n’avons gardé que les films (une grande majorité des médias disponibles sur cette base sont des épisodes de séries TV) en filtrant sur 4 genres :red[“_frissons_”], qui sont “Horreur”, “Thriller”, “Crime” et “Film-Noir”.')
    st.write('Nous avons travaillé près de 3 semaines et au total sur 5 bases différentes, en les nettoyant selon nos besoins pour arriver à la fin  avec plus de 50000 films.')
    
    st.header(":blue[Etape 2 :] Élaborations des KPI sur notre catalogue :red[_frissons_]")
    st.write("En se basant sur l’analyse des différentes colonnes de notre base ou mettant en évidence des corrélations selon 3 domaines : le genre, les acteurs et les durées.")
if options == 'KPI' :
   choices = st.selectbox('KPI :chart_with_upwards_trend: :',('les genres','les acteurs/actrices','la durée'))
   if choices == 'les genres' :
      df1 = DF_films_test.explode('genres')
      st.header(":blue[Répartition des genres au sein de frisson]")
      fig, ax = plt.subplots(figsize = (10,7))
      sns.countplot(data = df1, y = 'genres', order=df1['genres'].value_counts().index, color = 'blue')
      plt.xlabel('')
      plt.ylabel('')
      st.pyplot(fig)
      st.write('Nous retrouvons que notre selection compte parmis les majoritaires("crimes, Thriller et Horreur").Et un tout petit peu de genre Film-noir.')
      df2 = DF_films_test[['genres', 'decenies']]
      df2 = df2.explode('genres', ignore_index = True)
      list_decenies = ["1970's", "1980's", "1990's","2000's", "2010's", "2020's"]
      df3 = df2[df2['decenies'].isin(list_decenies)]
      st.header(":blue[Evolution du nombre de films parmi les 4 meilleurs genres 'frissons' durant les 5 dernières décénnies]")
      fig1, ax = plt.subplots(figsize = (10,7))
      sns.countplot(data = df3, x = 'genres', order=["Thriller", "Drama", "Horror", "Crime"], color = 'Orange', hue = 'decenies', hue_order=list_decenies)
      for container in ax.containers:
         ax.bar_label(container)
      plt.xlabel('')
      plt.ylabel('')
      st.pyplot(fig1)
      st.write('On a une explosion de film dans les decénnies 2010 parmis nos 3 genres les plus majoritaires.')
      
   
   
   if choices == 'les acteurs/actrices' :
       st.header(':blue[les  10 acteurs/actrices les plus cités de la selection _frisson_]')
       df_acteurs=DF_films_test.explode('actor')
       cond=df_acteurs['actor'] == ''
       df_acteurs=df_acteurs[~cond]
       fig2, ax = plt.subplots(figsize = (10,10))
       sns.countplot(data=df_acteurs,y='actor',order=df_acteurs['actor'].value_counts().iloc[:10].index,color='blue')
       plt.title('les 10 acteurs les plus cités de notre selection de film')
       plt.ylabel('')
       plt.xlabel('')
       st.pyplot(fig2)
       df_actrices=DF_films_test.explode('actress')
       cond1=df_actrices['actress'] == ''
       df_actrices=df_actrices[~cond1]
       fig3, ax = plt.subplots(figsize = (10,10))
       sns.countplot(data=df_actrices,y='actress',order=df_actrices['actress'].value_counts().iloc[:10].index,color='pink')
       plt.title('les 10 actrices les plus cités de notre selection de film')
       plt.ylabel('')
       plt.xlabel('')
       st.pyplot(fig3)

       st.write("Nous notons que l'échelle valeur des axis ne sont pas pareilles. Pour les acteurs, ça passe à 100 pour les actrices 40. Les acteurs sont plus nombreux que les actrices.")
       st.header(":blue[l'acteur(actrice)  le(la) plus cité(e )par genre de film ]")
       ##création d'un nouveau DataFrame pour avoir  les colonnes actor , actrice et genre
       df_genres_actor=DF_films_test[['actor','genres']]
       for i in df_genres_actor.columns:
           df_genres_actor=df_genres_actor.explode(i,ignore_index=True)
       mon_dico_actor={}
       for i in df_genres_actor['genres'].unique():
          cond2=df_genres_actor['genres']==i
          mon_dico_actor[i]=df_genres_actor[cond2]
       liste_acteurs =[]
       liste_genres = []
       for keys in mon_dico_actor:
           cond3=mon_dico_actor[keys]['actor']== ''
           mon_dico_actor[keys]=mon_dico_actor[keys][~cond3]
           count1 = pd.DataFrame(mon_dico_actor[keys]['actor'].value_counts().head(1))
           count1=count1.reset_index()
           liste_acteurs.append(count1['index'].iloc[0])
           liste_genres.append(keys)
           df_act = pd.DataFrame({'genre':liste_genres,
                        'acteurs':liste_acteurs})
       df_genres_actrices=DF_films_test[['actress','genres']]
       for i in df_genres_actrices.columns:
          df_genres_actrices=df_genres_actrices.explode(i,ignore_index=True)
       mon_dico_actrices={}
       for i in df_genres_actrices['genres'].unique():
          cond4=df_genres_actrices['genres']==i
          mon_dico_actrices[i]=df_genres_actrices[cond4]
       liste_actrices = []
       liste_genres1 = []
       for keys in mon_dico_actrices:
          cond5=mon_dico_actrices[keys]['actress'] == ''
          mon_dico_actrices[keys]=mon_dico_actrices[keys][~cond5]
          count = pd.DataFrame(mon_dico_actrices[keys]['actress'].value_counts().head(1))
          count=count.reset_index()
          liste_actrices.append(count['index'].iloc[0])
          liste_genres1.append(keys)
          df_actr = pd.DataFrame({'genre':liste_genres1,
                        'actrices':liste_actrices})
        
       st.write(pd.merge(df_act,df_actr,how='left',on='genre'))
       st.header(":blue[le nombre d'acteur et d'actrice par film]")
       fig3,ax=plt.subplots(figsize=(10,10))
       sns.histplot(data=DF_films_test, x="nb_actor",bins=10,color='Orange')
       sns.histplot(data=DF_films_test, x="nb_actress",bins=10,color='grey')
       plt.xlabel('')
       plt.ylabel('')
       st.pyplot(fig3) 
       st.write("Sur cet histogramme, en abscisse on a le nombre d'acteurs/actrices et en ordonné le nombre de films.En orange nous avons le nombre d'acteur par film et en gris, le nombre d'actrices par film.")
       st.write("Nous remarquons une corrélation entre le nombre d'acteurs et le nombre d'actrices.")
   if choices == 'la durée' :
       st.header(':blue[Evolution de la durée des films par decennie]')
       # réalisation d'un df avec la durée médiane des films par décennie
       df_duree_decenies = DF_films_test['runtimeMinutes'].groupby(by = DF_films_test['decenies']).median().reset_index()
       fig4,ax=plt.subplots(figsize=(10,10))
       sns.heatmap(df_duree_decenies.set_index('decenies'), 
            cmap='Oranges', 
            annot=True, 
            cbar = False)
       st.pyplot(fig4)
       st.write("Nous retrouvons une évolution de la durée du film au fil des decennies. Actuellement, un film dure en moyenne 94 minutes.")
       # mise en df des colonnes qui nous intéressent
       df_duree_nb_actors = DF_films_test[['runtimeMinutes', 'nb_actor', 'nb_actress']] 
       # En vue de graphique avec intervalle 
       temps = [49, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]
       categories = ["50 à 60", "60 à 70", "70 à 80", "80 à 90", "90 à 100", "100 à 110", "110 à 120",
             "120 à 130", "130 à 140", "140 à 150", "150 à 160", "160 à 170", "170 à 180", "180 à 190", "190 à 200", "200 à 210"]
       # création nouvelle colonne
       df_duree_nb_actors['Intervalle_duree'] = pd.cut(df_duree_nb_actors.runtimeMinutes, bins=temps , labels = categories)
       st.header(":blue[Nombre d'acteurs et d'actrices selon la durée du film]")
       fig5, ax = plt.subplots(figsize=(9, 7))

       sns.lineplot(data = df_duree_nb_actors,
                x = "Intervalle_duree", 
                y = "nb_actor", 
                color = 'royalblue', 
                label = 'actor',
                ci=None) 
       sns.lineplot(data = df_duree_nb_actors,
                x = "Intervalle_duree", 
                y = "nb_actress", 
                color = 'red',
                label = 'actress',
                ci=None)
       plt.ylabel('Personnes')
       plt.xlabel('Durée du film (en minutes)')
       plt.xticks(rotation=45) 
       plt.legend(title = 'Genre', loc = 'upper left')
       st.pyplot(fig5)
       st.write("Nous pouvons remarquer que nous avons plus d'acteurs que d'actrices dans notre selection de film'frisson' peu importe la durée.")
       df_ratings_duree = DF_films_test[['runtimeMinutes', 'averageRating']]
       note = [0,1,2,3,4,5,6,7,8,9,10]
       categories = ["0 à 1", "1 à 2", "2 à 3","3 à 4","4 à 5","5 à 6","6 à 7","7 à 8","8 à 9","9 à 10"]
       df_ratings_duree['group_rate'] =  pd.cut(df_ratings_duree.averageRating, bins=note , labels = categories)
       df_ratings_duree_group = df_ratings_duree['runtimeMinutes'].groupby(by = df_ratings_duree['group_rate']).median().reset_index()
       st.header(":blue[Durée des films par note moyenne]")
       fig6, ax = plt.subplots(figsize=(10, 10))
       plt.stem(df_ratings_duree_group['group_rate'], df_ratings_duree_group['runtimeMinutes'])
       plt.ylabel('Durée du film (en minutes)')
       plt.xlabel('Note moyenne')
       plt.xticks(rotation=45) 
       st.pyplot(fig6)
       st.write("Ici, on peu conclure que la durée de film n'interfère pas la notation de ceux-ci. Nous ne retrouvons aucune corrélation entre la durée et la notation des films.")
if options == 'Recommandations de films' :
    st.write(reco_films())
