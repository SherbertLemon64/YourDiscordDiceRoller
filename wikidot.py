from bs4 import BeautifulSoup
import requests
import re

class Spell:
    def __init__(self, _name,_source, _type, _castingTime, _range, _duration, _description, _spellLists):
        self.Name = _name
        self.Source = _source
        self.Type = _type
        self.CastingTime = _castingTime
        self.Duration = _duration
        self.Range = _range
        self.Description = _description
        self.SpellClasses = _spellLists

def GetSpell(SpellName):
    r = requests.get(f"http://dnd5e.wikidot.com/spell:{SpellName}")
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    x = re.findall(r"Source: (.*)\n(.*)\nCasting Time: (.*)\nRange: (.*)\nComponents: (.*)\nDuration: (.*)\n((.|\n)*(?=Spell Lists.))Spell Lists\. (.*)", soup.find(id="page-content").text)[0]
    spell = Spell(SpellName, x[0], x[1], x[2], x[3], x[5], x[6], x[8])
    return spell

print(GetSpell("healing-word").SpellClasses)