from discord.ext import commands
import discord
from discord import Embed, ActionRow, ButtonStyle, SelectOption
from discord.ui import Button, View, Select
import jamdict

class JMSelect(Select):
    def __init__(self, data):
        options = [SelectOption(label=f"{data.entries[i].kanji_forms[0] if data.entries[i].kanji_forms else data.entries[i].kana_forms[0]}", value=f"{i}") for i in range(len(data.entries))]
        if data.names:
            for i in range((len(data.names)//25) + 1):
                options.append(SelectOption(label=f"Names {i+1}: {data.names[0].kanji_forms[0].text if data.names[0].kanji_forms else data.names[0].kana_forms[0]}", value=f"{len(data.entries)+1+i}"))
        super().__init__(placeholder="Select an option", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.view.set_selected_option(interaction, self.values)

class JMView(View):
    selected_option = None
    
    async def send(self, ctx):
        self.add_item(JMSelect(self.items))
        self.message = await ctx.send(view=self)        
        await self.update_message(self.items)
    
    def create_embed(self, data):
        if self.selected_option is None:
            embed = Embed(title="Search Results", color=0x00ff00)
            for i in range(len(data.entries)):
                if data.entries[i].kanji_forms == []:
                    embed.add_field(name=f"{i + 1}) {data.entries[i].kana_forms[0].text}", value="", inline=False)
                else:
                    embed.add_field(name=f"{i + 1}) {data.entries[i].kanji_forms[0].text}", value="", inline=False)
        if int(self.selected_option) <= len(data.entries):
            dict_data_entries = data.entries[int(self.selected_option)]
            embed = Embed(title=dict_data_entries.kanji_forms[0].text if dict_data_entries.kanji_forms else dict_data_entries.kana_forms[0].text, color=0x00ff00)
            jmdict_cog = self.bot.get_cog("JDict")
            embed.add_field(name="Kanji Forms", value=", ".join([i.text for i in dict_data_entries.kanji_forms]) if dict_data_entries.kanji_forms else "-", inline=True)
            embed.add_field(name="Kana Forms", value=", ".join([i.text for i in dict_data_entries.kana_forms]), inline=True)
            embed.add_field(name="Part of Speech", value=", ".join(dict_data_entries.senses[0].pos), inline=False)
            embed.add_field(name="Meanings", value="", inline=False)
            
            counter = 1
            for sense in dict_data_entries.senses:
                embed.add_field(name=f"{counter}) {", ".join(i.text for i in sense.gloss)}", value=f"{"misc: " + ", ".join(sense.misc) if sense.misc else ""}", inline=False)
                counter += 1
        else:
            dict_data_names = data.names
            page_data = int(self.selected_option) - len(data.entries) 
            jmdict_cog = self.bot.get_cog("JDict")
            embed = Embed(title=f"{dict_data_names[0].kanji_forms[0] if dict_data_names[0].kanji_forms else dict_data_names[0].kana_forms[0]} (Name)" , color=0x00ff00)
            embed.add_field(name="Readings", value="", inline=True)
            for i in jmdict_cog.get_name_kanji(dict_data_names, page_data):
                embed.add_field(name=i, value="", inline=True)            
        return embed
    
    async def update_message(self, data):
        await self.message.edit(embed=self.create_embed(data), view=self)
    
    async def set_selected_option(self, interaction, value):
        self.selected_option = value[0]
        await self.update_message(self.items)
    

class JDict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jam = jamdict.Jamdict()

    @commands.command()
    async def jdict(self, ctx, arg):
        arg = self.roma_to_hira(arg)
        data = self.jam.lookup(arg)
        if len(data.chars + data.entries + data.names) == 0:
            await ctx.send("No results found")
            return
        view = JMView()
        view.items = data
        view.bot = self.bot
        await view.send(ctx)
        
    def get_name_kanji(self, data, page):
        kanjis = [i.kanji_forms[0].text + " " + i.senses[0].text() if i.kanji_forms else None for i in data]
        if kanjis == []:
            return ["-"]
        return [i for i in kanjis if i is not None][(page - 1) * 25 : page * 25 - 1]
    
    def roma_to_hira(self, string):
        hira_dict = {
        "ka": "か",
        "ki": "き",
        "ku": "く",
        "ke": "け",
        "ko": "こ",
        "sa": "さ",
        "shi": "し",
        "si": "し",
        "su": "す",
        "se": "せ",
        "so": "そ",
        "ta": "た",
        "chi": "ち",
        "ti": "ち",
        "tsu": "つ",
        "tu": "つ",
        "te": "て",
        "to": "と",
        "na": "な",
        "ni": "に",
        "nu": "ぬ",
        "ne": "ね",
        "no": "の",
        "ha": "は",
        "hi": "ひ",
        "fu": "ふ",
        "he": "へ",
        "ho": "ほ",
        "ma": "ま",
        "mi": "み",
        "mu": "む",
        "me": "め",
        "mo": "も",
        "ya": "や",
        "yu": "ゆ",
        "yo": "よ",
        "ra": "ら",
        "ri": "り",
        "ru": "る",
        "re": "れ",
        "ro": "ろ",
        "wa": "わ",
        "wo": "を",
        "n": "ん",
        "ga": "が",
        "gi": "ぎ",
        "gu": "ぐ",
        "ge": "げ",
        "go": "ご",
        "za": "ざ",
        "ji": "じ",
        "zu": "ず",
        "ze": "ぜ",
        "zo": "ぞ",
        "da": "だ",
        "di": "ぢ",
        "du": "づ",
        "de": "で",
        "do": "ど",
        "ba": "ば",
        "bi": "び",
        "bu": "ぶ",
        "be": "べ",
        "bo": "ぼ",
        "pa": "ぱ",
        "pi": "ぴ",
        "pu": "ぷ",
        "pe": "ぺ",
        "po": "ぽ",
        "kya": "きゃ",
        "kyu": "きゅ",
        "kyo": "きょ",
        "sha": "しゃ",
        "shu": "しゅ",
        "sho": "しょ",
        "cha": "ちゃ",
        "chu": "ちゅ",
        "cho": "ちょ",
        "nya": "にゃ",
        "nyu": "にゅ",
        "nyo": "にょ",
        "hya": "ひゃ",
        "hyu": "ひゅ",
        "hyo": "ひょ",
        "mya": "みゃ",
        "myu": "みゅ",
        "myo": "みょ",
        "rya": "りゃ",
        "ryu": "りゅ",
        "ryo": "りょ",
        "gya": "ぎゃ",
        "gyu": "ぎゅ",
        "gyo": "ぎょ",
        "ja": "じゃ",
        "jya": "じゃ",
        "ju": "じゅ",
        "jyu": "じゅ",
        "jo": "じょ",
        "jyo": "じょ",
        "bya": "びゃ",
        "byu": "びゅ",
        "byo": "びょ",
        "pya": "ぴゃ",
        "pyu": "ぴゅ",
        "pyo": "ぴょ",
        "a": "あ",
        "i": "い",
        "u": "う",
        "e": "え",
        "o": "お",
        }
        for key, value in hira_dict.items():
            string = string.replace(key, value)
        return string
    
async def setup(bot):
    await bot.add_cog(JDict(bot))