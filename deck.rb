class Deck
  attr_reader :cards

  def initialize(test_deck = [])
    @cards = []
    @books = []

    unless test_deck.empty?
      @cards = test_deck
    else
      @cards = Card::SUITS.map { |suit| 
        Card::RANKS.map { |rank|
          Card.new(rank,suit)
        }
      }.flatten
    end
  end

  def length
    @cards.length
  end

  def ==(deck)
    @cards == deck.cards
  end

  def shuffle
    @cards.shuffle!
  end

  def give_card
    @cards.pop
  end

  def receive_card(newcard)
    @cards.unshift(newcard)
  end

  # def deal(number, hands)
  #   number = @cards.length if number == 0
  #   number.times {
  #     hands.map { |hand|
  #       hand.receive_card(give_card)
  #       }
  #   }
  # end

end # Deck
