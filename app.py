import pickle
import random

# Load your Q-table
with open("blackjack.pkl", "rb") as f:
    Q = pickle.load(f)

# Card deck setup
def draw_card():
    return random.choice([1,2,3,4,5,6,7,8,9,10,10,10,10])  # 10 = J/Q/K

def draw_hand():
    return [draw_card(), draw_card()]

def usable_ace(hand):
    return 1 in hand and sum(hand) + 10 <= 21

def hand_value(hand):
    val = sum(hand)
    if usable_ace(hand):
        return val + 10
    return val

def is_bust(hand):
    return hand_value(hand) > 21

def show_hand(name, hand, hide_first=False):
    if hide_first:
        print(f"{name}: [?, {hand[1]}]")
    else:
        print(f"{name}: {hand} (value={hand_value(hand)})")

def choose_action(state):
    if state in Q:
        return max(Q[state], key=Q[state].get)  # best action
    return random.choice([0,1])  # fallback

# Play one game
def play_game():
    print("\n=== New Blackjack Game ===")

    # Initial hands
    player = draw_hand()
    dealer = draw_hand()

    show_hand("Dealer", dealer, hide_first=True)
    show_hand("Player", player)

    # State = (player_sum, dealer_upcard, usable_ace)
    state = (hand_value(player), dealer[0], usable_ace(player))

    done = False
    while not done:
        action = choose_action(state)  # 0=stick, 1=hit
        if action == 1:  # hit
            card = draw_card()
            player.append(card)
            print(f"Player hits and draws {card}")
            show_hand("Player", player)
            if is_bust(player):
                print("❌ Player busts!")
                return -1
            state = (hand_value(player), dealer[0], usable_ace(player))
        else:  # stick
            print("Player sticks")
            break

    # Dealer's turn
    show_hand("Dealer", dealer)
    while hand_value(dealer) < 17:
        card = draw_card()
        dealer.append(card)
        print(f"Dealer draws {card}")
        show_hand("Dealer", dealer)
        if is_bust(dealer):
            print("✅ Dealer busts, Player wins!")
            return 1

    # Compare final hands
    player_val = hand_value(player)
    dealer_val = hand_value(dealer)
    print(f"\nFinal Hands:")
    show_hand("Player", player)
    show_hand("Dealer", dealer)

    if player_val > dealer_val:
        print("✅ Player wins!")
        return 1
    elif player_val < dealer_val:
        print("❌ Dealer wins!")
        return -1
    else:
        print("🤝 Draw!")
        return 0

# Run one game
result = play_game()
print("Game Result:", "Win" if result==1 else "Lose" if result==-1 else "Draw")