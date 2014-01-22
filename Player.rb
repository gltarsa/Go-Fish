class Player
  attr_reader :number, :name, :hand, :socket

  def initialize(number = nil, name = nil, socket = nil)
    @number = number
    @name = name
    @socket = socket
    @messages = []
  end

  def tell (msg)
    @messages << msg
  end

  def messages (consume = false)
    # consider consumption to be marking messages as seen so that a
    # history can be kept

    # consider marking groups of messages with an EOM marker so that
    # history can be in groups of lines rather than individual lines.

    messages = @messages
    @messages = [] if consume
    messages
  end

  def messages?
    !@messages.empty?
  end

end #Player

