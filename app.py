import contextlib
import streamlit as st
from io import StringIO
import random
import pandas as pd
import requests
import json

file = st.file_uploader("Please choose a file")

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
    if first:
        cards_in_hand = 5
    else:
        cards_in_hand = 6
    df = pd.DataFrame (main, columns=["Cards"])
    main_string = ",".join(df["Cards"])
    URL = f'https://db.ygoprodeck.com/api/v7/cardinfo.php?id={main_string}'
    page = requests.get(URL).json()
    df_deck = pd.read_json(json.dumps(page["data"]))
    one_card_combos = st.multiselect(
    'Select your one card combo cards:',
    df_deck["name"]
    )
    two_card_combos = []
    drawing_cards = st.multiselect(
    'Select your drawing cards:',
    df_deck[~df_deck.name.isin(one_card_combos)]["name"],
    )
    for card in drawing_cards:
        with contextlib.suppress(ValueError):
            while True:
                main.remove(card)
    flag = False
    opening_hands = [random.choices(df_deck["name"],k=cards_in_hand) for _ in range(5000)]
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