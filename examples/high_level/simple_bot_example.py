from wonda import Bot, BotUpdateType, TelegramAPIError, Token
from wonda.bot.rules import Fuzzy, Text
from wonda.bot.updates import ChatJoinRequest, Message

# Make a bot with a token from an environment variable.
bot = Bot(Token.from_env())

# Use message, chat_message or private_message decorators to handle
# corresponding types of messages. To define special logic you can use
# built-in rules or make your own by inheriting from
# wonda.bot.rules.abc.ABCRule.
@bot.on.private_message(Text(["hi", "hello", "howdy"]))
async def message_handler(msg: Message) -> str:
    # Text rule matches the message text with the given list of strings.
    # If the match is successful, following lines will be executed.

    # This line returns specific value to answer message from user
    # (see https://github.com/wondergram-org/wonda/blob/main/wonda/bot/dispatch/return_manager/message.py).
    return f"{msg.text.capitalize()}, friend!"


# A good example of how you can use this mechanic is to kick people that say inappropriate things from the chat.
# Also, in this example we'll be using another great shortcut to answer properly.
@bot.on.chat_message(Fuzzy(["shit", "fuck", "bastard", "asshole"]))
async def chat_message_handler(msg: Message) -> None:
    # Fuzzy rule measures the ratio between two string sequences.
    # If the ratio is greater than or equal to set `min_ratio`,
    # following lines will be executed.

    try:
        # This is a basic API call. Please use ctx_api as it is always available (that
        # can't be said for bot API, for example, while using blueprints).
        await msg.ctx_api.ban_chat_member(chat_id=msg.chat.id, user_id=msg.from_.id)
    except TelegramAPIError[400]:
        # Gracefully handle the error and make an apology.
        await msg.answer("Sorry, can't kick this member because of an error.")


# You can also handle other types of updates besides messages. To do that,
# use raw_update decorator and provide it with a type and a dataclass
# of update that you want to handle.
@bot.on.raw_update(BotUpdateType.EDITED_MESSAGE, Message)
async def edited_message_handler(msg: Message) -> None:
    # This line, when executed, will call shortcut method to answer message from user
    # (see https://github.com/wondergram-org/wonda/blob/main/wonda/bot/updates/types.py#L44).
    await msg.answer("Hm? I heard you edit a message.")


# A bit more about shortcut methods: there's many of them in Wonda.
# In fact, nearly every update has them! They are used to answer
# messages and queries. To show them in action, 
# let's answer a join request to a dog chat 
# in which only good boys are allowed.
@bot.on.raw_update(BotUpdateType.CHAT_JOIN_REQUEST, ChatJoinRequest)
async def chat_join_request_handler(req: ChatJoinRequest) -> None:
    # Verify that the user who sent the request is actually a dog
    # and approve the request.
    if any(word in ("woof", "bark", "ruff") for word in req.bio.split()):
        await req.approve()
        return
    # If the user turned out to be a human, reject the request.
    await req.decline()


# Run loop > loop.run_forever() > with tasks created in loop_wrapper before.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
