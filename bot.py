import os
from dotenv import load_dotenv

import discord
import random

import battleship

def format_board(board):

    board = [[board[i][j] if board[i][j] in ['a', 'b', 'c', 'd', 'e'] else ('X' if board[i][j] == 2 else ('O' if board[i][j] == 1 else ' ')) for j in range(8)] for i in range(8)]

    return f"""```    1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    -   -   -   -   -   -   -   -
A | {board[0][0]} | {board[0][1]} | {board[0][2]} | {board[0][3]} | {board[0][4]} | {board[0][5]} | {board[0][6]} | {board[0][7]}
-   -   -   -   -   -   -   -   -
B | {board[1][0]} | {board[1][1]} | {board[1][2]} | {board[1][3]} | {board[1][4]} | {board[1][5]} | {board[1][6]} | {board[1][7]}
-   -   -   -   -   -   -   -   -
C | {board[2][0]} | {board[2][1]} | {board[2][2]} | {board[2][3]} | {board[2][4]} | {board[2][5]} | {board[2][6]} | {board[2][7]}
-   -   -   -   -   -   -   -   -
D | {board[3][0]} | {board[3][1]} | {board[3][2]} | {board[3][3]} | {board[3][4]} | {board[3][5]} | {board[3][6]} | {board[3][7]}
-   -   -   -   -   -   -   -   -
E | {board[4][0]} | {board[4][1]} | {board[4][2]} | {board[4][3]} | {board[4][4]} | {board[4][5]} | {board[4][6]} | {board[4][7]}
-   -   -   -   -   -   -   -   -
F | {board[5][0]} | {board[5][1]} | {board[5][2]} | {board[5][3]} | {board[5][4]} | {board[5][5]} | {board[5][6]} | {board[5][7]}
-   -   -   -   -   -   -   -   -
G | {board[6][0]} | {board[6][1]} | {board[6][2]} | {board[6][3]} | {board[6][4]} | {board[6][5]} | {board[6][6]} | {board[6][7]}
-   -   -   -   -   -   -   -   -
H | {board[7][0]} | {board[7][1]} | {board[7][2]} | {board[7][3]} | {board[7][4]} | {board[7][5]} | {board[7][6]} | {board[7][7]}```"""

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

active_games = {}

@client.event
async def on_ready():
    global guild
    guild = client.guilds[0]
    print(f'{client.user} has successfully connected to {guild.name} (guild id: {guild.id})')

@client.event
async def on_message(message):
    #print(message.content)
    if message.author == client.user:
        return
    if str(message.channel.type) == 'private':
        #handle board setup
        #print('ACCESSING GAME ', message.author.id)
        game = active_games[message.author.id]
        if message.content == '!random':
            game.boardSetupRandom(message.author.id)
            game.playersStatus[message.author.id] = True
            await message.author.send('Your board has been set up. Here it is:')
            await message.author.send(format_board(game.boardsPrivate[message.author.id]))

            if game.playersStatus[game.player1ID] and game.playersStatus[game.player2ID]:
                battleship_channel = discord.utils.get(guild.text_channels, name='battleship')
                await battleship_channel.send(f'<@{game.player1ID}> and <@{game.player2ID}>. Your game is ready!')
                await battleship_channel.send(f'<@{game.player1ID}> Here is your tracking board:\n{format_board(game.boardsTracking[game.player1ID])}')
                await battleship_channel.send(f'<@{game.player2ID}> Here is your tracking board:\n{format_board(game.boardsTracking[game.player2ID])}')
                await battleship_channel.send(f'<@{game.player1ID}> You go first!')
        elif message.content == '!board':
            await message.author.send(format_board(game.boardsPrivate[message.author.id]))

        return
    if message.channel.name != 'battleship':
        return

    if message.content.startswith('!hit'):
        hitloc = (ord(message.content.split(' ')[1][0]) - 65, int(message.content.split(' ')[1][1]) - 1)
        game = active_games[message.author.id]
        
        ret = game.hit(message.author.id, hitloc)
        if ret == -1:
            await message.channel.send(f'<@{message.author.id}> wait your turn!')
            return

        if ret == 0:
            await message.channel.send(f'<@{message.author.id}> missed!\n{format_board(game.boardsTracking[message.author.id])}')
        elif ret == 1:
            await message.channel.send(f'<@{message.author.id}> direct hit!\n{format_board(game.boardsTracking[message.author.id])}')
        elif ret == 2:
            await message.channel.send(f'<@{message.author.id}> direct hit and SINK!\n{format_board(game.boardsTracking[message.author.id])}')
        elif ret == 3:
            await message.channel.send(f'<@{message.author.id}> direct hit and SINK AND GAME OVER!')
            await message.channel.send(f'<@{message.author.id}> wins!')
            await message.channel.send(f'<@{game.player1ID}> Here is your final board:\n{format_board(game.boardsPrivate[game.player1ID])}')
            await message.channel.send(f'<@{game.player2ID}> Here is your final board:\n{format_board(game.boardsPrivate[game.player2ID])}')
            del active_games[game.player1ID]
            del active_games[game.player2ID]

    if message.content.startswith('!battleship'):
        player_oppID = message.content.split(' ')[1][3:-1]
        user = client.get_user(int(player_oppID))
        if message.author.id in active_games or user.id in active_games:
            await message.channel.send(f"<@{message.author.id}> you can't do that! One of you is in an active game. Do !end to end it.")
            return

        await user.send(f"You've been invited to a game of Battleship by {message.author.name}. Set up your board!\nUse !random for a random board.")
        await message.author.send(f"You've started a game of Battleship with {user.name}. Set up your board!\nUse !random for a random board.")
        
        game = battleship.Battleship(user.id, message.author.id)
        active_games[user.id] = game
        active_games[message.author.id] = game
        #print('ADDING GAME TO DICT')
        #print(active_games)
        #print(user.id)
        #print(message.author.id)
    
    if message.content == '!help':
        help_string = """Battleship Help

Commands:
Use !battleship <@user> to initiate a game with a user. Ex. !battleship @dg
Use !hit <coordinates> to launch an attack. Ex. !hit A1
Use !random to generate a random board. (dm)
Use !board to see your board. (dm)
Use !end to end your current game.

You can only have one game going on at once."""
        
        await message.channel.send(help_string)

    if message.content == '!end':
        game = active_games[message.author.id]
        await message.channel.send(f'<@{message.author.id}> has ended the game.')
        await message.channel.send(f'<@{game.player1ID}> Here is your final board:\n{format_board(game.boardsPrivate[game.player1ID])}')
        await message.channel.send(f'<@{game.player2ID}> Here is your final board:\n{format_board(game.boardsPrivate[game.player2ID])}')
        del active_games[game.player1ID]
        del active_games[game.player2ID]

client.run(TOKEN)