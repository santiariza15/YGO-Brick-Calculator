import random 

def get_main(deck_ydk):
    with open(deck_ydk, 'r') as f:
        deck = f.read().splitlines()
    main = []
    for card in deck:
        if card.isnumeric():
            main.append(card)
        if "extra" in card or "side" in card:
            break
    return main

deck = get_main("Floowandereeze.ydk")
opening_hands = [random.choices(deck,k=5) for _ in range(5000)]
counter = 0
one_card_combos = ['18940725']
two_card_combos = [['54334420', '28126717'], ['80433039', '28126717'], ['17827173', '28126717'],
['54334420', '69087397'], ['80433039', '69087397'], ['17827173', '69087397'],
['54334420', '73628505'], ['80433039', '73628505'], ['17827173', '73628505']]
#drawing_cards = ['55521751', '98645731', '49238328']
flag = False
odds = []
for hand in opening_hands:
    for cards in one_card_combos:
        if cards in hand:
            counter += 1
            flag = True
            odds.append(counter/5000 * 100)
    if flag == True:
        flag = False
        continue
    for cards in two_card_combos:
        if cards[0] in hand and cards[1] in hand:
            counter += 1
            flag = True
            odds.append(counter/5000 *100)
    if flag == True:
        flag = False
        continue
    # for cards in drawing_cards:
    #     if cards in hand:
    #         count_draw += 1
print(counter/5000 * 100)
