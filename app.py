import pickle 
import streamlit as st

st.set_page_config(page_title = 'Game Recommender', page_icon='🎮')


games = pickle.load(open("games_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

games_list = games['Title'].values


st.header("Game Recommender! 🎲")
st.write("Level up your gaming experience! Select your previous play from over 10,000+ video games and find alternatives tailered to YOUR interests.")
selectvalue = st.selectbox("Select Your Previous Play", games_list)

results_wanted = st.slider("Up to how many games would you like to be recommended?", 1, 25, 5)

def remove(string):
    return string.replace(" ", "")

def recommend(game, limit=None):
    index = games[games['Title']==game].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    list_of_games = []
    recommended_titles = set()

    for i in distance[1:]:
        name = games.iloc[i[0]].Title
        date = games.iloc[i[0]].Release_Date
        platforms = games.iloc[i[0]].Platforms
        plays = games.iloc[i[0]].Plays
        summary = games.iloc[i[0]].Summary
        genres = games.iloc[i[0]].Genres

        if name not in recommended_titles:
            list_of_games.append([name, date, plays, platforms, summary, genres])
            recommended_titles.add(name)

        if len(list_of_games) >= limit:
            break

    return list_of_games


if st.button("Find Similar Games"):
    recommended_games = recommend(selectvalue, limit=results_wanted)
    
    if results_wanted == 1:
        st.subheader(f"Your Recommended Game 💡")
        st.markdown(f"**{results_wanted} recommended result for *'{selectvalue}'***")
    
    else:
        st.subheader(f"Your Recommended Games 💡")
        st.markdown(f"**{results_wanted} recommended results for *'{selectvalue}'***")

    st.write("")

    i = 1 
    while i <= results_wanted:
        for game in recommended_games:
            st.markdown(f"**{i}. {game[0]}**")
            st.text(f"Genres: {game[5]}")
            st.text(f"Release Date: {game[1]}")
            st.text(f"Platforms: {game[3]}")
            st.text(f"Plays: {game[2]}")
            st.write(game[4])
            link = f'https://www.google.com/search?q={remove(game[0])}'
            st.markdown(f'**[Check out this game!]({link})**')
            st.write("")
            i = i + 1
