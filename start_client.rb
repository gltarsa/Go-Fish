require_relative "./fishserver.rb"
require_relative "./fishclient.rb"

def display_server_messages
  @thread_id = Thread.new {
    loop do
      puts @client.receive_message
    end
  }
end

welcome = <<EOF
Welcome to the Fish Server

Play will begin when all the players have joined the game.  Please Wait.

When the game begins, you will be notified and the players will be listed.
When it is your turn, you may request a rank from any player in any of
the following ways:

   Player 1 do you have any 3s?
   1 3?

If your input is not understood you will be asked to provide it again.

Now, to begin...

EOF

def get_server_name(args)
  server_name = args.length > 0 ? args[0] : nil

  while server_name.nil?
    print "What is the name of your server (default: 'localhost')? "
    server_name = gets.chomp.strip
    server_name = "localhost" if server_name.empty?
  end
  puts "server name is #{server_name}"
  server_name
end

def connect_to_server(args)
  server_name = get_server_name(args)

  begin
    puts "Creating FishClient to #{server_name}"
    @client = FishClient.new(server_name); break

  rescue Errno::ECONNREFUSED
    puts "#{server_name} is not accepting connections (Errno::ECONNREFUSED)"
    server_name = nil

  rescue SocketError
    puts "#{server_name} does not appear to be a valid node name. (SocketError)"
    server_name = nil

  ensure
    args = nil
  end while server_name = get_server_name()
end


# Does not block, displays any messages coming in from the server

print welcome

connect_to_server(ARGV)

display_server_messages

#puts @client.receive_line
#puts @client.receive_message

while true do
  @client.send_line(STDIN.gets.chomp)
  begin
    @client.socket.recv(0)
  rescue Errno::ECONNRESET
    puts "The Server has closed the connection unexpectedly"
    break
  end
end

puts "exiting..."
exit


while not EOF

  get_line
  result = parse_line
  process_locally if local
  process_on_server if remote
end


puts "test complete"
