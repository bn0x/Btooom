<vegard1992> anyway brahs
<vegard1992> im goin on vacay
<jhpy1024> Awwww
<vegard1992> ïn its current state the net code needs to circumvent firewalls somehow
<vegard1992> look into udp hole punching
<vegard1992> it also needs some interfacing code with the game, and parsing on both servre and client side of game data
<vegard1992> as well as validation of game data
<vegard1992> so like
<vegard1992> 1 4292 room room:dongesquad420@player_bomb_shot:39595,24824
<jhpy1024> bn0x can do this :D
<vegard1992> the server must then validate that the client who sent the message is authenticated, and has joined the room "dongesquad420"
<vegard1992> then it must validate that hes allowed to shoot a bomb
<vegard1992> in other words that the player has bombs left, and "bomb shoot" is not on cooldown
<vegard1992> this is juts an example
<vegard1992> buyt the logic will apply to prety much evertyhng
<vegard1992> so keep data of every player serverside
<vegard1992> and update it with according to received information
<vegard1992> then send it to all the players
<vegard1992> so in effect u are sort of "viewing" the game from the servre
<vegard1992> then sending actions to change your caharacters data like position, or bombs
<vegard1992> it will also need some functions to create "game messages"
<vegard1992> and interface with the game
<vegard1992> theres some template stuff in there for that
<jhpy1024> I don't know where to start with any of that.
<vegard1992> im gonna commit this as a small "what to do"
<vegard1992> incase anyone decides to work on it
<jhpy1024> Okay
<vegard1992> i would recommend that u instead read up on net stuff tho
<vegard1992> like realy read up
<vegard1992> and then implementing something different
<vegard1992> possibly use TCP
<vegard1992> but that really depends on the implementation
<jhpy1024> I'm pretty busy going through a C++ book atm :P
<vegard1992> usually u will want UDP
<vegard1992> anway, end of rant
