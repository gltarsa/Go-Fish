require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "../game.rb"
require_relative "../result.rb"

describe Game, "Initial game setup." do
  context ".new for initial game setup: Create 6 random hands." do
    before (:each) do
      @number_of_test_hands = 6
      @hand_length = (@number_of_test_hands > 4) ? 5 : 7
      @game = Game.new(@number_of_test_hands)

      @game.hands.length.should be @number_of_test_hands
      @game.hands.length.times { |i|
          @game.hands[i].length.should be @hand_length
      }
    end # before (:each)
    
    it ".current_hand returns the index" do
      @game.current_hand.should == 0
    end

    it ".advance_to_next_hand advances the index to the next player" do
      @game.advance_to_next_hand
      @game.current_hand.should == 1
    end

    it ".advance_to_next_hand goes around in an ordered loop of hands." do
      first_hand = @game.current_hand
      @number_of_test_hands.times { @game.advance_to_next_hand }
      @game.current_hand.should eql first_hand
    end

  end # context for random hands
end # game setup tests

describe Game, "Play typical rounds." do
  context "Stack a deck with with 3 known hands." do
    before (:each) do
      @test_hand_size = 7
      @number_of_test_hands = 3
      target_hand, stacked_deck = [],[]
      target_hand[0] = "2C 2H 3C QH 5C 4H 9H".split
      target_hand[1] = "2S 2D 3S 3D 5S 4D 9C".split
      target_hand[2] = "10C 10H 10S 10D AC AH 9S".split
      @test_hand_size.downto(0) { |card_num| 
        @number_of_test_hands.times { |hand_num|
          stacked_deck << target_hand[hand_num][card_num]
        }
      }
      extra_cards = "3H".split
      extra_cards.map { |card_string|
        stacked_deck << card_string
      }
      stacked_cards_string = stacked_deck.join(" ")

      @game = Game.new(@number_of_test_hands,
                       Card.new_cards_from_s(stacked_cards_string))

      @game.hands.length.should be @number_of_test_hands
      @game.hands.length.times { |i|
        @game.hands[i].length.should be @test_hand_size
      }

      # test a few samples for validity
      @game.hands[0].cards[3].should == Card.new("Q", "H")
      @game.hands[2].cards[0].should == Card.new("10", "C")
      @game.deck.cards[0].should == Card.new("3", "H")
    end # before (:each)

    it ".ask_for_matches: ask for a card; does not get it; no cards gained." do
      # puts "-----", @game.hands[0].cards
      result = @game.ask_for_matches(@game.hands[1],"8")
      result.number_of_cards_received.should == 0
      result.cards_received_from.should == nil
    end

    it ".ask_for_matches: asks and gets 1 added to hand; victim loses card." do
      hand0_count = @game.hands[0].cards.length
      hand1_count = @game.hands[1].cards.length

      result = @game.ask_for_matches(@game.hands[1],"5")
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == @game.hands[1]

      @game.hands[0].cards.length.should == hand0_count + 1
      @game.hands[1].cards.length.should == hand1_count - 1
    end

    it ".ask_for_matches: asks, gets > 1 added to hand; victim loses same cards." do
      hand0_count = @game.hands[0].cards.length
      hand1_count = @game.hands[1].cards.length

      result = @game.ask_for_matches(@game.hands[1],"3")
      result.number_of_cards_received.should == 2
      result.cards_received_from.should == @game.hands[1]

      @game.hands[0].cards.length.should == hand0_count + 2
      @game.hands[1].cards.length.should == hand1_count - 2
    end

    it ".play_round: 1) Player asks Victim: none; Pile: Yes; Book: N/A; turn over." do
      result = @game.play_round(@game.hands[1], "6")  # hand 1 has no 6s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "6"
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == :deck
      result.number_of_books_made.should == 0

      @game.advance_to_next_hand
      @game.current_hand.should eql 1
    end

    it ".play_round: 2) Player asks Victim: gets; Pile: N/A; Book: N/A; plays again." do
      result = @game.play_round(@game.hands[1], "3")  # hand 1 has 2 x 3s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "3"
      result.number_of_cards_received.should == 2
      result.cards_received_from.should == @game.hands[1]
      result.number_of_books_made.should == 0

      @game.current_hand.should eql 0
    end

    it ".play_round: 3) Player asks Victim: gets; Pile: N/A; Book: Yes; plays again." do
      result = @game.play_round(@game.hands[1], "2")  # hand 1 has 2 x 2s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "2"
      result.number_of_cards_received.should == 2
      result.cards_received_from.should == @game.hands[1]
      result.number_of_books_made.should == 1

      @game.current_hand.should eql 0
    end

    it ".play_round: 4) Player asks Victim: no get; Pile: get; Book: no; plays again." do
      result = @game.play_round(@game.hands[1], "8")  # hand 1 has no 8s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "8"
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == :deck
      result.number_of_books_made.should == 0

      @game.current_hand.should eql 0
    end

    it ".play_round: 5) Player asks Victim: no get; Pile: get; Book: yes; plays again." do
      result = @game.play_round(@game.hands[1], "8")  # hand 1 has no 8s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "8"
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == :deck
      result.number_of_books_made.should == 0

      @game.current_hand.should eql 0
    end

    it ".ask_for_matches checks for books in initial hands" do
      result = []
      start = current = @game.current_hand
      begin
        @game.hands[current].cards.map { |card|
          result[current] = @game.ask_for_matches(@game.hands[current],
                                                  card.rank)
          break if result[current].number_of_books_made > 0
        }
      end while (current = @game.advance_to_next_hand) != start

      @game.advance_to_next_hand while @game.current_hand != 2
      result[0].number_of_books_made.should == 0
      result[1].number_of_books_made.should == 0
      result[2].number_of_books_made.should == 1
    end

    it ".play_round: checks for end of game" do
      #take last card from deck
      card = @game.deck.give_card
      @game.deck.length.should == 0

      next_card = @game.deck.give_card
      next_card.should be_nil

      # Play a round: ask for 3 from hand 2, don't get one, don't get from pile
      result = @game.play_round(@game.hands[2], "3")
      result.number_of_cards_received.should == 0
      
      result.game_over.should == true
    end

  end # context
end # Game tests
