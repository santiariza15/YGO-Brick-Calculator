import streamlit as st
from io import StringIO
import random
import pandas as pd
import requests
import json
from itertools import combinations
import matplotlib.pyplot as plt

st.set_page_config(page_title="YGO Brick Calculator",
 page_icon="random",
 menu_items={
        'Report a bug': "https://github.com/santiariza15/YGO-Brick-Calculator",
        'About': "This is a brick calculator using 5000 random opening hands as a test."
    }
)
st.title('Yu-Gi-Oh! Brick Calculator')
with st.expander("See explanation"):
    st.write("""
        This calculator uses your uploaded deck in YDK format and creates a sample of
        5000 different possible starting hands. Based on the information you provide on
        the select boxes, the calculator provides you with a brick percentage.
    """)
file = st.file_uploader("Please choose a file",type="ydk")

if file is not None:
    stringio = StringIO(file.getvalue().decode("utf-8"))
    deck = stringio.read().splitlines()
    main = []
    for card in deck:
        if card.isnumeric():
            main.append(card)
        if "extra" in card or "side" in card:
            break
    first = st.checkbox('Going first: ', True)
    cards_in_hand = 5 if first else 6
    df = pd.DataFrame (main, columns=["cards"])
    main_string = ",".join(df["cards"])
    URL = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?id={main_string}'
    page = requests.get(URL).json()
    df_deck = pd.read_json(json.dumps(page["data"]))
    drawing_cards = st.multiselect(
    'Select your cards with drawing effects:',
    df_deck["name"],
    help = "Select the cards that make you draw. This reduces the size of the deck in calculations."
    )
    deck_no_drawing_cards = df_deck[~df_deck.name.isin(drawing_cards)]["name"].to_list()
    one_card_combos = st.multiselect(
    'Select your one card combo cards:',
    deck_no_drawing_cards,
    help = "Select the cards that single handedly jump start your engine."
    )
    list_removed = drawing_cards + one_card_combos
    deck_names_no_one_combos = df_deck[~df_deck.name.isin(list_removed)]["name"].to_list()
    two_card_combos = st.multiselect(
    'Select the pair of two card combos:',
    list(combinations(deck_names_no_one_combos, 2)),
    help = "Select the pair of cards needed for your engine to start."
    )
    #deck_no_drawing_cards_ids = df_deck[df_deck.name.isin(deck_no_drawing_cards)]["id"].to_list()
    all_deck_ids = ([int(x) for x in df.cards.to_list()])
    #set_dndci = set(deck_no_drawing_cards_ids)
    #all_deck_ids = [x for x in all_deck_ids if x in set_dndci]
    all_deck = [df_deck[df_deck.id == x]["name"].to_list()[0] for x in all_deck_ids]
    flag = False
    opening_hands = [random.choices(all_deck,k=cards_in_hand) for _ in range(5000)]
    counter = 0
    for hand in opening_hands:
        for cards in one_card_combos:
            if cards in hand:
                counter += 1
                flag = True
                break
        if flag == True:
            flag = False
            continue
        for cards in two_card_combos:
            if cards[0] in hand and cards[1] in hand:
                counter += 1
                flag = True
                break
        if flag == True:
            flag = False
            continue
        for cards in drawing_cards:
            if cards in hand:
                counter += 0.5
                flag = True
                break
        if flag == True:
            flag = False

    st.write("Probability to brick: ")
    st.write(f"{(1 - counter / 5000):.0%}")

    col1, col2 = st.columns(2, gap="small")
    with col1:
        if st.button("Check your opening hands"):
            st.write(opening_hands)
    with col2:
        if st.button("Check the opening hand distribution"):
            flat_list = [item for sublist in opening_hands for item in sublist]
            fig, ax = plt.subplots()
            ax.hist(flat_list, bins=len(main)+1, orientation='horizontal', align="mid")
            st.pyplot(fig, True)