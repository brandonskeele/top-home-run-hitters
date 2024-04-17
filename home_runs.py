import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Home Run Leaders")

url = "https://github.com/brandonskeele/top-home-run-hitters/raw/main/home_runs.csv"
home_runs = pd.read_csv(url).set_index("Unnamed: 0")
home_runs.index.names = ["Ranking"]



tab1, tab2 = st.tabs(["Search by Name", "Search by Ranking"])

with tab1:
    # plot_df = name_df[name_df["sex"] == "M"]
    # fig_m = px.line(plot_df, x="year", y="n")
    # st.plotly_chart(fig_m)
    name = st.text_input("Insert a name", value="Shohei Ohtani")
    num = home_runs[home_runs["Player Name"] == name].index[0]
    
    if num < 5:
        place_hr = home_runs[0:10].copy()
    elif num > 995:
        place_hr = home_runs[991:1000].copy()
    else:
        place_hr = home_runs[num-5:num+5].copy()

    for col in place_hr.columns:
        val = place_hr[col][num]
        place_hr[col][num] = f'<b><span style="background-color: #ADD8E6">{val}</span></b>'

    place_hr.drop(columns="Player Quote", inplace=True)

    st.markdown(place_hr.to_html(escape=False),unsafe_allow_html=True)

with tab2:
    num = int(st.number_input("Insert a number", value=5, placeholder="Type a number...", min_value=1, max_value=1000, step=1))

    if num < 5:
        place_hr_num = home_runs[0:10].copy()
    elif num > 995:
        place_hr = home_runs[991:1000].copy()
    else:
        place_hr_num = home_runs[num-5:num+5].copy()

    for col in place_hr_num.columns:
        val = place_hr_num[col][num]
        place_hr_num[col][num] = f'<b><span style="background-color: #ADD8E6">{val}</span></b>'

    place_hr_num.drop(columns="Player Quote", inplace=True)

    st.markdown(place_hr_num.to_html(escape=False),unsafe_allow_html=True)

bat_hand = home_runs.groupby(by = ["Batting Hand"]).count()
on = st.toggle("Show Average Rankings")

st.header("Count of Players per Batting Hand")

if on:
    ave_rank = home_runs.reset_index()[["Ranking", "Batting Hand"]].groupby(by = ["Batting Hand"]).mean()

    fig, ax = plt.subplots()
    bars = ax.bar(x = bat_hand.index.values, height = bat_hand["Player Name"].values, color = ["#26547C", "#EF476F", "#FFD166"])

    for bar, rank in zip(bars, ave_rank["Ranking"].values):
        height = bar.get_height()
        ax.annotate(f'{round(rank, 4)}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
        textcoords="offset points", ha='center', va='bottom')

    st.pyplot(fig)
else:
    fig, ax = plt.subplots()
    ax.bar(x = bat_hand.index.values, height = bat_hand["Player Name"].values, color = ["#26547C", "#EF476F", "#FFD166"])
    st.pyplot(fig)


group = st.selectbox("How would you like to group the players in the list?", ("Batting Hand", "College"))
aggregate = st.selectbox("How would you like to aggregate the number of home-runs hit in each group?", ("Mean", "Total"))

if aggregate == "Mean":
    calc_home_runs = home_runs[["Home Runs", group]].groupby(by = [group]).mean().sort_values(by = ["Home Runs"], ascending = False)
    st.header(f"Average Number of Home-Runs by {group}")
elif aggregate == "Total":
    calc_home_runs = home_runs[["Home Runs", group]].groupby(by = [group]).sum().sort_values(by = ["Home Runs"], ascending = False)
    st.header(f"Total Number of Home-Runs by {group}")

st.table(calc_home_runs)