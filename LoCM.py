import sys

PLAYER_PARAMS = ["player_health", "player_mana", "player_deck", "player_rune", "player_draw"]
CARD_PARAMS = ["card_number", "instance_id", "location", "card_type", "cost", "attack", "defense",
               "abilities", "my_health_change", "opponent_health_change", "card_draw"]
INT_PARAMS = ["card_number", "instance_id", "location", "card_type", "cost", "attack", "defense",
              "my_health_change", "opponent_health_change", "card_draw"]
DRAFT_COUNTER = 30
OPTIMAL_MANA_DIST = {0: 3, 1: 4, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 1, 9: 1, 12: 1}


class Game:
    players = {"me": {}, "op": {}}
    board = []
    my_board = []
    my_board_used = []
    op_board = []
    op_board_alive = []
    my_hand = []
    player_deck = []
    player_mana_dist = dict(zip(range(13), [0] * 13))
    print_list = []
    draft_options = []

    def add_to_hand(self, card):
        self.my_hand.append(card)

    def add_to_my_board(self, card):
        self.my_board.append(card)
        self.my_board_used.append(False)

    def add_to_op_board(self, card):
        self.op_board.append(card)
        self.op_board_alive.append(True)

    def add_to_draft(self, card):
        self.draft_options.append(card)

    def perform_draft(self):
        print("Performing draft, draftcount:" + str(DRAFT_COUNTER), file=sys.stderr, flush=True)
        diffs = [OPTIMAL_MANA_DIST[c["cost"]] - self.player_mana_dist[c["cost"]] for c in self.draft_options]
        print(diffs, file=sys.stderr, flush=True)
        for idx, _ in enumerate(diffs):
            if self.draft_options[idx]["card_type"] != 0:
                diffs[idx] = -10
            elif self.draft_options[idx]["attack"] == 0:
                diffs[idx] = -5

        max_idx = diffs.index(max(diffs))
        self.player_mana_dist[self.draft_options[max_idx]["cost"]] += 1
        self.print_list.append("PICK " + str(max_idx))

    def perform_action(self):
        print("Performing action", file=sys.stderr, flush=True)
        self.attack()
        while self.summon():
            pass

    def attack(self):
        # Find available targets
        guards = {idx: card for idx, card in enumerate(self.op_board) if
                  "G" in card["abilities"] and self.op_board_alive[idx]}
        len_guards = len(guards)
        while len_guards > 0 and not all(self.my_board_used):
            if not guards:
                guards = dict(zip(range(len(self.op_board)), self.op_board))
            for gidx, guard in guards.items():
                seconds = None
                thirds = None
                for idx, card in enumerate(self.my_board):
                    if not self.my_board_used[idx] and self.op_board_alive[gidx]:
                        if card["attack"] >= guard["defense"] & card["defense"] > guard["defense"]:
                            self.print_list.append("ATTACK {} {} GoodTrade!".format(card["instance_id"], guard["instance_id"]))
                            self.op_board_alive[gidx] = False
                            self.my_board_used[idx] = True
                            seconds = None
                        elif card["attack"] >= guard["defense"]:
                            seconds, seconds_idx = card, idx
                        elif thirds is None or thirds["attack"] < card["attack"]:
                            thirds, thirds_idx = card, idx
                if self.op_board_alive[gidx] and seconds is not None:
                    self.print_list.append("ATTACK {} {} FairTrade!".format(seconds["instance_id"], guard["instance_id"]))
                    self.op_board_alive[gidx] = False
                    self.my_board_used[seconds_idx] = True
                elif self.op_board_alive[gidx] and thirds is not None:
                    self.print_list.append("ATTACK {} {} Whatevs...".format(thirds["instance_id"], guard["instance_id"]))
                    self.my_board_used[thirds_idx] = True

            guards = {idx: card for idx, card in enumerate(self.op_board) if
                      "G" in card["abilities"] and self.op_board_alive[idx]}
            len_guards = len(guards)

        self.yolo()

    def yolo(self):
        # YOLO
        for idx, card in enumerate(self.my_board):
            if not self.my_board_used[idx]:
                self.print_list.append("ATTACK {} -1 yolo!".format(card["instance_id"]))
                self.my_board_used[idx] = True

    def summon(self):
        playable_cards = {
            card["instance_id"]: card["cost"]
            for card in self.my_hand
            if card["cost"] <= self.players["me"]["player_mana"]
        }
        print(playable_cards, file=sys.stderr, flush=True)
        if len(playable_cards) > 0:
            inst = max(playable_cards, key=(lambda k: playable_cards[k]))
            self.players["me"]["player_mana"] -= playable_cards[inst]
            updated_hand = []
            for card in self.my_hand:
                if inst == card["instance_id"]:
                    if "C" in card["abilities"]:
                        self.my_board_used.append(False)
                    else:
                        self.my_board_used.append(True)
                else:
                    updated_hand.append(card)
            self.my_hand = updated_hand
            self.print_list.append("SUMMON " + str(inst))
            return True
        else:
            return False

    def shout(self):
        print("; ".join(self.print_list))
        self.players = {"me": {}, "op": {}}
        self.board = []
        self.my_board = []
        self.my_board_used = []
        self.op_board = []
        self.op_board_alive = []
        self.my_hand = []
        self.print_list = []
        self.draft_options = []


# game loop
g = Game()
while True:
    for key in g.players.keys():
        inp = [int(j) for j in input().split()]
        g.players[key].update(zip(PLAYER_PARAMS, inp))
    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    for i in range(opponent_actions):
        card_number_and_action = input()
    card_count = int(input())
    for i in range(card_count):
        card_input = dict(zip(CARD_PARAMS, [i for i in input().split()]))
        for INT_PARAM in INT_PARAMS:
            card_input[INT_PARAM] = int(card_input[INT_PARAM])
        if DRAFT_COUNTER > 0:
            g.add_to_draft(card_input)
        elif card_input["location"] == 0:
            g.add_to_hand(card_input)
        elif card_input["location"] == 1:
            g.add_to_my_board(card_input)
        elif card_input["location"] == -1:
            g.add_to_op_board(card_input)
    if DRAFT_COUNTER <= 0:
        g.perform_action()
    else:
        g.perform_draft()
    g.shout()
    if DRAFT_COUNTER == 0:
        print(g.player_mana_dist, file=sys.stderr, flush=True)
    DRAFT_COUNTER -= 1
    g.draft_options = []

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
