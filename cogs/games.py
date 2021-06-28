import asyncio
import random
import typing

import discord
import discord_slash.model
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.cog_ext import cog_component
from discord_slash.utils import manage_commands, manage_components
from discord_slash.model import ButtonStyle

guild_ids = [764683397528158259]


def duplicates(lst, item):
    return [i for i, x in enumerate(lst) if x == item]


def create_board():
    """Creates the tic tac toe board"""
    buttons = []
    for i in range(9):
        buttons.append(
            manage_components.create_button(
                style=ButtonStyle.grey,
                label="‎",
                custom_id=f"tic_tac_toe_button||{i}"))
    action_rows = manage_components.spread_to_rows(*buttons, max_in_row=3)
    return action_rows


def checkWin(b, m):
    return ((b[0] == m and b[1] == m and b[2] == m) or  # H top
            (b[3] == m and b[4] == m and b[5] == m) or  # H mid
            (b[6] == m and b[7] == m and b[8] == m) or  # H bot
            (b[0] == m and b[3] == m and b[6] == m) or  # V left
            (b[1] == m and b[4] == m and b[7] == m) or  # V centre
            (b[2] == m and b[5] == m and b[8] == m) or  # V right
            (b[0] == m and b[4] == m and b[8] == m) or  # LR diag
            (b[2] == m and b[4] == m and b[6] == m))  # RL diag


def checkDraw(b):
    return ' ' not in b


def getBoardCopy(b):
    dupeBoard = []
    for j in b:
        dupeBoard.append(j)
    return dupeBoard


def testWinMove(b, mark, i):
    bCopy = getBoardCopy(b)
    bCopy[i] = mark
    return checkWin(bCopy, mark)


def testForkMove(b, mark, i):
    bCopy = getBoardCopy(b)
    bCopy[i] = mark
    winningMoves = 0
    for j in range(0, 9):
        if testWinMove(bCopy, mark, j) and bCopy[j] == ' ':
            winningMoves += 1
    return winningMoves >= 2


def getComputerMove(b):
    # Check computer win moves
    for i in range(0, 9):
        if b[i] == ' ' and testWinMove(b, 'enemy', i):
            return i
    # Check player win moves
    for i in range(0, 9):
        if b[i] == ' ' and testWinMove(b, 'player', i):
            return i
    # Check computer fork opportunities
    for i in range(0, 9):
        if b[i] == ' ' and testForkMove(b, 'X', i):
            return i
    # Check player fork opportunities, incl. two forks
    playerForks = 0
    for i in range(0, 9):
        if b[i] == ' ' and testForkMove(b, '0', i):
            playerForks += 1
            tempMove = i
    if playerForks == 1:
        return tempMove
    elif playerForks == 2:
        for j in [1, 3, 5, 7]:
            if b[j] == ' ':
                return j
    # Play center
    if b[4] == ' ':
        return 4
    # Play side for special case
    norm = b[0] == "player" and b[4] == "enemy" and b[8] == "player" and len(duplicates(b, ' ')) == 6 or b[6] == "player" and b[4] == "enemy" and b[2] == "player" and len(duplicates(b, ' ')) == 6
    if norm:
        for i in [1, 3, 5, 7]:
            if b[i] == ' ':
                return i
    # Play a corner
    for i in [0, 2, 6, 8]:
        if b[i] == ' ':
            return i
    #Play a side
    for i in [1, 3, 5, 7]:
        if b[i] == ' ':
            return i


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @cog_ext.cog_slash(
        name="tic-tac-toe",
        description="Play Tic-Tac-Toe",
        guild_ids=guild_ids,
    )
    async def ttt_start(self, ctx: SlashContext):
        await ctx.send(content=f"{ctx.author.mention}'s Tic-Tac-Toe game!",
                       components=create_board())

    @commands.command(aliases=["ttt"])
    async def tictactoe(self, ctx):
        await ctx.send(content=f"{ctx.author.mention}'s Tic-Tac-Toe game!",
                       components=create_board())

    def determine_board_state(self, components: list):
        board = []
        for i in range(3):
            row = components[i]["components"]
            for button in row:
                if button["style"] == 2:
                    board.append(' ')
                elif button["style"] == 1:
                    board.append("player")
                elif button["style"] == 4:
                    board.append("enemy")

        return board

    def determine_win_state(self, board: list):
        if board[0] == board[1] == board[2] != ' ':  # row 1
            return board[0]
        if board[3] == board[4] == board[5] != ' ':  # row 2
            return board[3]
        if board[6] == board[7] == board[8] != ' ':  # row 3
            return board[6]
        if board[0] == board[3] == board[6] != ' ':  # col 1
            return board[0]
        if board[1] == board[4] == board[7] != ' ':  # col 2
            return board[1]
        if board[2] == board[5] == board[8] != ' ':  # col 3
            return board[2]
        if board[0] == board[4] == board[8] != ' ':  # diag 1
            return board[0]
        if board[2] == board[4] == board[6] != ' ':  # diag 2
            return board[2]
        return None

    @cog_component(components=create_board())
    async def process_turn(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        winner_ = None
        try:
            if ctx.author.id != ctx.origin_message.mentions[0].id:
                return
        except:
            return
        button_pos = int(ctx.custom_id.split("||")[-1])
        components = ctx.origin_message.components

        board = self.determine_board_state(components)

        if board[button_pos] == ' ':
            board[button_pos] = "player"
            winner = self.determine_win_state(board)
            if winner:
                winner = ctx.author.mention if winner == "player" else self.bot.user.mention
                winner_ = True

            if not winner:
                if board.count(' ') == 0:
                    winner = "Nobody"
                    winner_ = True
            # ai pos
            move = getComputerMove(board)
            if move != None or winner_ != True:
                board[move] = "enemy"
        else:
            return

        if winner_ == None:
            winner = self.determine_win_state(board)
            if winner:
                winner = ctx.author.mention if winner == "player" else self.bot.user.mention

            if not winner:
                if board.count(' ') == 0:
                    winner = "Nobody"

        # convert the board in buttons
        for i in range(9):
            style = (ButtonStyle.grey
                     if board[i] == ' ' else ButtonStyle.blurple
                     if board[i] == "player" else ButtonStyle.red)
            board[i] = manage_components.create_button(
                style=style,
                label="‎",
                custom_id=f"tic_tac_toe_button||{i}",
                disabled=True if winner else False,
            )

        await ctx.edit_origin(
            content=f"{ctx.author.mention}'s Tic-Tac-Toe game!"
            if not winner else f"{winner} has won!",
            components=manage_components.spread_to_rows(*board, max_in_row=3),
        )


def setup(bot: commands.Bot):
    bot.add_cog(Games(bot))
