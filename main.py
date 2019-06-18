import requests
import discord
import xml.etree.ElementTree as ET

client = discord.Client()
@client.event
async def on_message(message):
    if message.content == '!zishin':
        er = e()
        embed = discord.Embed(title='**地震情報**', description='', color=er['color'])
        embed.set_thumbnail(url=er['icon'])
        embed.add_field(name='発生時刻', value=er['time'], inline=True)
        embed.add_field(name='震源地', value=er['epicenter'], inline=True)
        embed.add_field(name='最大震度', value=er['intensity'], inline=True)
        embed.add_field(name='マグニチュード', value=er['magnitude'], inline=True)
        embed.add_field(name='震度1以上を観測した地域', value=er['e_1'], inline=False)
        embed.set_image(url=er['map'])
        await message.channel.send(embed=embed)
def e():
    xml_data_module = requests.get('https://www3.nhk.or.jp/sokuho/jishin/data/JishinReport.xml')
    xml_data_module.encoding = "Shift_JIS"
    root = ET.fromstring(xml_data_module.text)
    for item in root.iter('item'):
       deta_url = (item.attrib['url'])
       break
    deta = requests.get(deta_url)
    deta.encoding = "Shift_JIS"
    root = ET.fromstring(deta.text)
    e_1 = ''
    for Earthquake in root.iter('Earthquake'):
        time = (Earthquake.attrib['Time'])
        Intensity = (Earthquake.attrib['Intensity'])
        Epicenter = (Earthquake.attrib['Epicenter'])
        Magnitude = (Earthquake.attrib['Magnitude'])
        Depth = (Earthquake.attrib['Depth'])
        map_url = 'https://www3.nhk.or.jp/sokuho/jishin/'
        count = 1
    for Area in root.iter('Area'):
        e_1 += '\n' + Area.attrib['Name']
        if count == 10:
            e_1 += '\n他'
            break
        count = count + 1
    for Detail in root.iter('Detail'):
        map = map_url + Detail.text
        edic = {'time': time, 'epicenter': Epicenter, "intensity": Intensity, "depth": Depth, "magnitude": Magnitude, "map": map, "icon": eicon(Intensity), "color": eicolor(Intensity), 'e_1': e_1}
        return edic
def eicon(i):
    if i == '1':
        return('https://i.imgur.com/yalXlue.png')
    elif i == '2':
        return('https://i.imgur.com/zPSFvj6.png')
    elif i == '3':
        return('https://i.imgur.com/1DVoItF.png')
    elif i == '4':
        return("https://i.imgur.com/NqC3CE0.png")
    elif i == '5-':
        return("https://i.imgur.com/UlFLa3G.png")
    elif i == '5+':
        return("https://i.imgur.com/hExQwf2.png")
    elif i == '6-':
        return("https://i.imgur.com/p9RrO96.png")
    elif i == '6+':
        return("https://i.imgur.com/pNaFJ2Y.png")
    elif i == '7':
        return("https://i.imgur.com/ZoOhL4v.png")
def eicolor(i):
    if i == '1':
        return(0x51b3fc)
    elif i == '2':
        return(0x7dd45a)
    elif i == '3':
        return(0xf0ed7e)
    elif i == '4':
        return(0xfa782c)
    elif i == '5-':
        return(0xb30f20)
    elif i == '5+':
        return(0xb30f20)
    elif i == '6-':
        return(0xffcdde)
    elif i == '6+':
        return(0xffcdde)
    elif i == '7':
        return(0xffff6c)
client.run(token)
