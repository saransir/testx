#on air movies program
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
import random
import asyncio
from info import IMDB_TEMPLATE
from pyrogram.errors import UserNotParticipant, UserIsBlocked
from utils import get_filter_results, get_file_details, is_subscribed, get_poster, get_post, search_gagala
BUTTONS = {}
BOT = {}
SPELL_CHECK = {}
CHAA = "-1001534114432"

RAT = ["π¦", "π«", "π‘", "π", "π₯", "π", "π­", "πΏ", ]

PHOTO = [
    "https://telegra.ph/file/9075ca7cbad944afaa823.jpg",
    "https://telegra.ph/file/9688c892ad2f2cf5c3f68.jpg",
    "https://telegra.ph/file/51683050f583af4c81013.jpg",
]

@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        await query.answer("You are clicking on an old button which is expired.", show_alert=True)
        return await query.message.delete()
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("Don't click others Requested filesπ¬", show_alert=True)
    message = query.message.reply_to_message
    if movie_  == "close_spellcheck":
        await message.delete()
        return await query.message.delete()
    movie = movie_
    await query.message.edit(f"π α΄Κα΄α΄α΄ΙͺΙ΄Ι’...β<b>{movie}π¬β</b>")
    btn = []
    x = movie.split()
    hari = "+".join(x)
    sesna = "_".join(x)
    oam = f"{random.choice(RAT)}"
    files = await get_filter_results(movie)
    if files:
        for file in files:
            file_id = file.file_id
            sz = get_size(file.file_size)
            fn = file.file_name[0:23]
            filename = f"{fn}{oam}{sz[0:3]} {sz[-2:]}{oam}"  
            btn.append(
                [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                )
    else:
        await query.message.delete()
        cha = int(CHAA)
        buttons = btn
        buttons.append(
            [InlineKeyboardButton(text=f"Ι’α΄α΄Ι’Κα΄ πΏ", url=f"https://google.com/search?q={hari}"),InlineKeyboardButton(text=f"Ιͺα΄α΄Κ πΏ", url=f"https://www.imdb.com/find?q={hari}")]
        )
        buttons.append(
            [InlineKeyboardButton(text="Κα΄α΄©α΄Κα΄ α΄α΄ α΄α΄α΄ΙͺΙ΄ π€΅",callback_data=f"report_{hari}")]
        )
        a = await message.reply_photo(photo="https://telegra.ph/file/3bc31abd2c8b92758dfc5.jpg", caption=f"{message.from_user.mention},α΄α΄ssΙͺΚΚα΄ α΄α΄α΄sα΄s : π\n\nπΊ Ι΄α΄α΄ Κα΄Κα΄α΄sα΄α΄ Κα΄α΄ \n πΊ,βΉ&*',) α΄α΄Ι΄α΄ α΄sα΄ α΄ΚΙͺκ± α΄yα΄©α΄ sΚα΄Κα΄Κs \nπΊ Ι΄α΄α΄ ΙͺΙ΄ α΄α΄α΄α΄Κα΄sα΄π Κα΄α΄©α΄Κα΄ α΄α΄ α΄α΄α΄ΙͺΙ΄π \n\n sα΄α΄Κα΄Κ ΙͺΙ΄ Ι’α΄α΄Ι’Κα΄/Ιͺα΄α΄Κ ?α΄Κ α΄α΄ΚΚα΄α΄α΄ sα΄α΄ΚΚΙͺΙ΄Ι’ \n\nπ²ππππ & π²ππππ πππ ππππππππ π", reply_markup=InlineKeyboardMarkup(buttons))
        await bot.send_message(chat_id=cha,text=f"{movie}", disable_web_page_preview=True)   
        await asyncio.sleep(25)
        await a.delete()
        await message.delete()
        return 

    if not btn:
        return

    if len(btn) > 7: 
        btns = list(split_list(btn, 7)) 
        keyword = f"{message.chat.id}-{message.message_id}"
        BUTTONS[keyword] = {
            "total" : len(btns),
            "buttons" : btns
        }
    else:
        buttons = btn
        buttons.append(
            [InlineKeyboardButton(text="ππ΄π°ππ²π· πΈπ½ πΏπΌ",callback_data=f"myree#{sesna}")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(movie)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {movie} βββββ</b> \n\n <b>πκ°α΄Κ- {message.from_user.mention} \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {movie} βββββ</b> \n\n <b>πκ°α΄Κ- {message.from_user.mention} \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        return await query.message.delete()

    data = BUTTONS[keyword]
    buttons = data['buttons'][0].copy()

    buttons.append(
        [InlineKeyboardButton(text="βΙ΄α΄xα΄β",callback_data=f"next_0_{keyword}")]
    )    
    buttons.append(
        [InlineKeyboardButton(text=f"πͺ Pages 1/{data['total']}πͺ",callback_data="pages")]
    )
    poster=None
    if API_KEY:
        poster=await get_poster(movie)
    if poster:
        await message.reply_photo(photo=poster, caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {movie} βββββ</b> \n\n <b>πκ°α΄Κ- {message.from_user.mention} \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        await query.message.delete()
    else:
        await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {movie} βββββ</b> \n\n <b>πκ°α΄Κ- {message.from_user.mention} \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        await query.message.delete()

async def filter(client, msg, files):
        btn = []
        search = msg
        message = msg.message.reply_to_message  
        # files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{random.choice(RAT)}[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                    )
        else:
            k = await query.message.edit('This Movie Not Found In DataBase')
            await asyncio.sleep(10)
            await k.delete()
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton("πͺ channel πͺ", url="https://t.me/joinchat/4-Quex2FaFhjMDM1")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {search} βββββ</b> \n\n  <b>π α΄Κα΄Ι΄Ι΄α΄Κ : [α΄Ι΄α΄ΙͺΚα΄α΄α΄ Ιͺα΄s](https://t.me/joinchat/4-Quex2FaFhjMDM1) \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {search} βββββ</b> \n\n <b>π α΄Κα΄Ι΄Ι΄α΄Κ : [α΄Ι΄α΄ΙͺΚα΄α΄α΄ Ιͺα΄s](https://t.me/joinchat/4-Quex2FaFhjMDM1) \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="βΙ΄α΄xα΄β",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"πͺ Pages 1/{data['total']}πͺ",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(movie)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {search} βββββ</b> \n\n <b>π α΄Κα΄Ι΄Ι΄α΄Κ :[α΄Ι΄α΄ΙͺΚα΄α΄α΄ Ιͺα΄s](https://t.me/joinchat/4-Quex2FaFhjMDM1) \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=f"<b>π¬ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : {search} βββββ</b> \n\n <b>π α΄Κα΄Ι΄Ι΄α΄Κ :[α΄Ι΄α΄ΙͺΚα΄α΄α΄ Ιͺα΄s](https://t.me/joinchat/4-Quex2FaFhjMDM1) \nβ‘οΈα΄α΄α΄‘α΄Κα΄α΄ ΚΚ:[α΄Ι΄α΄ΙͺΚ_?ΙͺΚα΄α΄Κα΅α΅α΅](https://t.me/On_air_Filter_bot)</b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if len(message.text) <= 3:
        kk = await message.reply_text(f"{message.from_user.mention},ΙͺΙ΄α΄Κα΄α΄α΄ Κα΄α΄Κ α΄? α΄Κα΄ α΄α΄α΄ Ιͺα΄. \n\n πππππ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ & yα΄α΄Κ")
        await asyncio.sleep(10)
        await kk.delete()
        await message.delete() 
    elif 3 < len(message.text) < 45:    
        btn = []
        if re.findall("((^Beast|^beast|^@|^#|^Puzhu).*)", message.text):
            return
        searc = message.text
        search = searc.strip()
        imdb = await get_post(search)
        if imdb:
            caption = IMDB_TEMPLATE.format(
                query = imdb['title'],
                title = imdb['title'],
                votes = imdb['votes'],
                aka = imdb["aka"],
                seasons = imdb["seasons"],
                box_office = imdb['box_office'],
                localized_title = imdb['localized_title'],
                kind = imdb['kind'],
                imdb_id = imdb["imdb_id"],
                cast = imdb["cast"],
                runtime = imdb["runtime"],
                countries = imdb["countries"],
                certificates = imdb["certificates"],
                languages = imdb["languages"],
                release_date = imdb['release_date'],
                year = imdb['year'],
                genres = imdb['genres'],
                poster = imdb['poster'],
                rating = imdb['rating'],
                url = imdb['url'],
                **locals()
            )
        else:
            caption = f"**<b> π¬β³ α΄α΄α΄ Ιͺα΄ Ι΄α΄α΄α΄ : βββββ</b>** βββββ<b>{search}βββββ</b>\n    **βββββ\[πππ 1](https://t.me/+PBGW_EV3ldY5YjJl)β?[πππ 2](https://t.me/+NY-f484oVqE1NmU1)**"
        oam = f"{random.choice(RAT)}"
        oamm = f"{random.choice(RAT)}"
        x = search.split()
        hari = "+".join(x)
        sesna = "_".join(x)

        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                sz = get_size(file.file_size)
                fn = file.file_name[0:23].strip()
                filename = f"{fn}{oam}{sz[0:3]} {sz[-2:]}{oamm}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"saran#{file_id}")]
                )
        else:
            return await spell(message)
        if not btn:
            return await spell(message)

        if len(btn) > 6: 
            btns = list(split_list(btn, 6)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="ππ΄π°ππ²π· πΈπ½ πΏπΌ",callback_data=f"myree#{sesna}"), InlineKeyboardButton("π‘closeπ‘", callback_data="close")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text=f"πͺ Pages 1/{data['total']}πͺ",callback_data="pages"),InlineKeyboardButton(text="βΙ΄α΄xα΄β",callback_data=f"next_0_{keyword}")]
        )
        buttons.append(
            [InlineKeyboardButton(text="ππ΄π°ππ²π· πΈπ½ πΏπΌ",callback_data=f"myree#{sesna}")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=f"{random.choice(PHOTO)}", caption=caption, reply_markup=InlineKeyboardMarkup(buttons))

    else:
        await message.delete()

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "α΄Κ", "α΄Κ", "Ι’Κ", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          

async def spell(message):
    title = message.text
    btn = []
    user = message.from_user.id if message.from_user else 0
    movies = await get_post(title, bulk=True)
    if not movies:
        return await advantage_spell_chok(message)
    oam = f"{random.choice(RAT)}"
    SPELL_CHECK[message.message_id] = movies
    for movie in movies:
        title = movie.get('title')
        year = movie.get('year')
        btn.append(
            [InlineKeyboardButton(text=f"{title} {oam} {year}",callback_data=f"spolling#{user}#{title}")]
        )
    btn.append([InlineKeyboardButton(text="πΊ Close πΊ", callback_data=f'spolling#{user}#close_spellcheck')])
    await message.reply('α΄Ιͺα΄ Κα΄α΄ α΄α΄α΄Ι΄ α΄Ι΄Κ α΄Ι΄α΄ α΄? α΄Κα΄sα΄?π', reply_markup=InlineKeyboardMarkup(btn)) 

async def advantage_spell_chok(message):
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", message.text, flags=re.IGNORECASE) # plis contribute some common words 
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(message.text)
    gs_parsed = []
    if not g_s:
        k = await message.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        await message.delete()
        return
    # regex = re.compile(r".*(imdbb|wikipedia).*", re.IGNORECASE) # look for imdb / wiki results
    # gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)', '', i, flags=re.IGNORECASE) for i in g_s]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*", re.IGNORECASE) # match something like Watch Niram | Amazon Prime 
        for mv in g_s:
            match  = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = message.from_user.id if message.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed)) # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_post(mov.strip(), bulk=True) # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist)) # removing duplicates
    if not movielist:
        k = await message.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    SPELL_CHECK[message.message_id] = movielist
    btn = [[
                InlineKeyboardButton(
                    text=movie.strip(),
                    callback_data=f"spolling#{user}#{k}",
                )
            ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="πΊ Close πΊ", callback_data=f'spolling#{user}#close_spellcheck')])
    kdm = await message.reply("Ιͺ α΄α΄α΄Κα΄Ι΄'α΄ ?ΙͺΙ΄α΄ α΄Ι΄Κα΄ΚΙͺΙ΄Ι’ Κα΄Κα΄α΄α΄α΄ α΄α΄ α΄Κα΄α΄ \n α΄Ιͺα΄ Κα΄α΄ α΄α΄α΄Ι΄ α΄Ι΄Κ α΄Ι΄α΄ α΄? α΄Κα΄sα΄?π", reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(40)
    await kdm.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    message = query.message.reply_to_message
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if query.data.startswith("saran"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name[0:-4]
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption="{title}",
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('πͺ Ι’Κα΄α΄α΄ 2', url='https://t.me/+NY-f484oVqE1NmU1'),
                        InlineKeyboardButton(' π sα΄α΄Κα΄Κ ?ΙͺΚα΄', switch_inline_query_current_chat='')
                    ]
                    ]

            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")
                return
            elif (clicked == typed):
                try:  
                    await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<code>" + title + "</code>""\n\n <b>[πΌππππ Κα΄Οα΄α΄sα΄ΙͺΙ΄Ι’ πππππ](https://t.me/+PBGW_EV3ldY5YjJl)</b>",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                except UserIsBlocked:
                    await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")
                else:
                    await query.answer("α΄Κα΄cα΄ α΄©α΄ π \n\n fileπ¬ has πππ²π²π΄πππ΅ππ»π»πβοΈ sent to your pm",show_alert=True)
            else:
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=subinps_-_-_-_{file_id}")           
    
    elif query.data.startswith("myree"):
            ident, file_name = query.data.split("#")
            await query.answer(url=f"http://t.me/On_air_Filter_bot?start=saran=={file_name}")

    elif (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("β­οΈ You are using this for one of my old message, please send the request again β­οΈ.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("βΚα΄α΄α΄β", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"πͺ Pages {int(index)+2}/{data['total']}πͺ", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="ππ΄π°ππ²π· πΈπ½ πΏπΌ",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("βΚα΄α΄α΄β", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"πͺ{int(index)+2}/{data['total']}πͺ", callback_data="pages"),InlineKeyboardButton("βΙ΄α΄xα΄β", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="ππ΄π°ππ²π· πΈπ½ πΏπΌ",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton(f"πͺ Pages {int(index)}/{data['total']}πͺ", callback_data="pages"),InlineKeyboardButton("βΙ΄α΄xα΄β", callback_data=f"next_{int(index)-1}_{keyword}")]                   
                )
                buttons.append(
                    [InlineKeyboardButton(text="ππ΄π°ππ²π· πΈπ½ πΏπΌ",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("βΚα΄α΄α΄β", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton(f"πͺ{int(index)}/{data['total']}πͺ", callback_data="pages"),InlineKeyboardButton("βΙ΄α΄xα΄β", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="ππ΄π°ππ²π· πΈπ½ πΏπΌ",callback_data=f"myree#")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data.startswith("report"):
            ident, movie = query.data.split("_")
            x = movie.split("+")
            kdm = " ".join(x)
            cha = int(CHAA)
            try:
                await client.send_message(chat_id=cha,text=f"{kdm}", disable_web_page_preview=True)
            except UserIsBlocked:
                await query.answer(url=f"http://t.me/On_air_Filter_bot?start=saran")
            else:
                await query.answer("πππ²π²π΄πππ΅ππ»π»π Reported to Admins π?ββ \n\n\n α΄Κα΄ α΄α΄α΄ Ιͺα΄ α΄‘ΙͺΚΚ α΄α΄©Κα΄α΄α΄ΙͺΙ΄Ι’ κ±α΄α΄Ι΄..",show_alert=True)
                await message.delete()
                return await query.message.delete()
        elif query.data == "about":
            await query.answer("π€ Ι΄α΄α΄α΄: α΄α΄α΄α΄ ?ΙͺΚα΄α΄Κ v2.7\nπͺα΄Κα΄α΄α΄α΄Κ: sα΄Κα΄Ι΄\nπΚα΄Ι΄Ι’α΄α΄Ι’α΄: α΄Κα΄Κα΄Ι΄3\nπ ΚΙͺΚΚα΄ΚΚ : α΄ΚΚα΄Ι’Κα΄α΄ α΄sΚΙ΄α΄Ιͺα΄ 1.13.0",show_alert=True)
        elif query.data == "close":
            await message.delete()
            await query.message.delete()
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("πͺΰ΄ΰ΅ΰ΄°ΰ΅ΰ΄ͺΰ΅ΰ΄ͺΰ΄Ώΰ΅½ join ΰ΄ΰ΅ΰ΄―ΰ΅ΰ΄€ΰ΄€ΰ΄Ώΰ΄¨ΰ΅ ΰ΄Άΰ΅ΰ΄·ΰ΄ ΰ΄ΰ΅ΰ΄²ΰ΄Ώΰ΄ΰ΅ΰ΄ΰ΅ ΰ΄ΰ΅ΰ΄―ΰ΅ΰ΄―ΰ΅ \n\n Join My πͺ group πͺ to click",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption="{title}",
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('πͺ Ι’Κα΄α΄α΄', url='https://t.me/+PBGW_EV3ldY5YjJl'),
                        InlineKeyboardButton(' π sα΄α΄Κα΄Κ ?ΙͺΚα΄', switch_inline_query_current_chat='')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f"<b>Β©[α΅βΏα΅β±Κ³α΅α΅α΅β±α΅Λ’](https://t.me/joinchat/4-Quex2FaFhjMDM1) \n π¬ file name π  </b>""<code>" + title + "</code>""\n\n[πΌππππ Κα΄Οα΄α΄sα΄ΙͺΙ΄Ι’ πππππ](https://t.me/+PBGW_EV3ldY5YjJl)",
                    reply_markup=InlineKeyboardMarkup(buttons)
                    ) 


        elif query.data == "pages":
            await query.answer()

    else:
        await query.answer("π Bro. search your own file, Don't click others Requested filesπ¬",show_alert=True)
