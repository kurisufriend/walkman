# walkman
appx. 70 line discord bot that can enqueue ytdl sources for playing in a voice channel

requires discord.py and youtube_dl
### if you (for whatever reason) want to run this, you should be able to understand the commands yourself from a quick glance at the code

instead, this area will be used for a rant:

discord's current implementation of voice channels is, while possibly suitable in mundane usecases, poorly designed and actively hostile to bots.
as passed down form out IRC forefathers, a client gets every incoming message in the same way and sorts it out on their end. similarly, the location a message is sent to is just one parameter for a generic 'send message' command.
voice channels, as I understand them, are independent UDP connections, separate from the regular websocket connection. because kidsthesedays can't into sharin their IP addresses, the connection on both ends is to discord server and they limit clients to one voice client per oauth/server. the HUGE music bot providers like FredBoat have to keep track of TONS of different tokens for sharding (because you can't be logged into the same token twice other than when you can) and still need SEPARATE discord applications running effectively separate bots so that multiple channels can listen to different music. the entire implementation is poor when looking at it from the angle of the usual method.

neway thanks for readin' my blog have a nice day