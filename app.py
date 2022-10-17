import streamlit as st
from io import StringIO
import random
import pandas as pd
import requests
import json
from itertools import combinations

st.set_page_config(page_title="YGO Brick Calculator",
 page_icon="random",
 menu_items={
        'Report a bug': "github link"
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title('Yu-Gi-Oh! Brick Calculator')

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
    df = pd.DataFrame (main, columns=["Cards"])
    main_string = ",".join(df["Cards"])
    URL = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?id={main_string}'
    page = requests.get(URL).json()
    df_deck = pd.read_json(json.dumps(page["data"]))
    drawing_cards = st.multiselect(
    'Select your drawing cards:',
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
    
    flag = False
    opening_hands = [random.choices(deck_no_drawing_cards,k=cards_in_hand) for _ in range(5000)]
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

    st.write("Probability to brick: ")
    st.write(f"{(1 - counter / 5000):.0%}")