class Card
  attr_reader :rank, :suit

  # define constants so we can use the same literal string everywhere
  RANKS = %w(2 3 4 5 6 7 8 9 10 J Q K A)
  SUITS = %w(C D H S)

  def initialize(myrank, mysuit)
    @rank = myrank
    @suit = mysuit
end

  def value
    RANKS.index(@rank)
  end

  # def suit_value
  #   SUITS.index(@suit)
  # end

  def to_s
    "#{@rank}-#{@suit}"
  end

  def ==(card)
    rank == card.rank && suit == card.suit
  end


  # Returns an array of Playing Cards based on the given strings
  # The RE splits sequences similar to: 5S 5-S 10-C 10C, etc. into three
  # elements: Whole String, Rank and Suit.
  CARD_REGEXP = /(10|[2-9]|[JQKA])\W*[of]*\W*([CHSD])/i
  def self.new_from_hand_strings(*hand_strings)
    number_of_hands = hand_strings.length
    hand_strings = hand_strings.map { |string| string = string.split }

    hand_size = hand_strings[0].length
    
    stacked_deck = []
    
    deck_array = []
    hand_size.downto(1) { |card_num| 
      hand_strings.length.times { |hand_num|
        deck_array << new_card_from_s(hand_strings[hand_num][card_num-1])
      }
    }
    deck_array.reverse
  end




  private
  # Returns an array of Playing Cards, based on a space separated string.
  def self.new_card_from_s(string)
    if rank_suit=CARD_REGEXP.match(string)
      Card.new(rank_suit[1], rank_suit[2])
    end
  end
end # Card
