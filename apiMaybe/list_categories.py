import json

def make_lists():
    area_damage = list()                    #define all different categories
    aura_effect = list()
    brand_damage = list()
    channeling_skill_damage = list()
    chaos_dot = list()
    cold_dot = list()
    crit_chance = list()
    curse = list()
    dot = list()
    herald = list()
    ailment_effect = list()
    fire_dot = list()
    flask_duration = list()
    flask_recovery = list()
    minion_herald = list()
    minion_life = list()
    phys_dot = list()
    projectile = list()
    totem = list()
    trap = list()
    warcry = list()

    #fill in all categories. stats.json is from https://www.pathofexile.com/api/trade/data/items
    with open('stats.json') as json_file:
        data = json.load(json_file)
        for a in data['result'][1]['entries']:
            if "Added Passive Skill is" in a['text']:
                if a['text'] == "1 Added Passive Skill is Aerodynamics":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    projectile.append(b)
                if a['text'] == "1 Added Passive Skill is Agent of Destruction":
                    b = {
                        'id': a,
                        'percent': 12.145
                        }
                    herald.append(b)
                if a['text'] == "1 Added Passive Skill is Ancestral Echo":
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Ancestral Guidance":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Ancestral Inspiration":
                    b = {
                        'id': a,
                        'percent': 2.500
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Ancestral Might":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Ancestral Preservation":
                    b = {
                        'id': a,
                        'percent': 2.500
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Ancestral Reach":
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Arcane Pyrotechnics":
                    b = {
                        'id': a,
                        'percent': 3.269
                        }
                    trap.append(b)
                if a['text'] == "1 Added Passive Skill is Assert Dominance":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    area_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Astonishing Affliction":
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Basics of Pain":
                    b = {
                        'id': a,
                        'percent': 6.296
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Blast Freeze":
                    b = {
                        'id': a,
                        'percent': 2.125
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.500
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Blessed Rebirth":
                    b = {
                        'id': a,
                        'percent': 2.500
                        }
                    minion_life.append(b)
                if a['text'] == "1 Added Passive Skill is Blowback":
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Bodyguards":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    minion_life.append(b)
                if a['text'] == "1 Added Passive Skill is Brand Loyalty":
                    b = {
                        'id': a,
                        'percent': 14.168
                        }
                    brand_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Brewed for Potency":
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 8.502
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 8.098
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.536
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    flask_duration.append(b)
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Brush with Death":
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.125
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.023
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 1.135
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Burning Bright":
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Careful Handling":
                    b = {
                        'id': a,
                        'percent': 3.269
                        }
                    trap.append(b)
                if a['text'] == "1 Added Passive Skill is Chilling Presence":
                    b = {
                        'id': a,
                        'percent': 1.250
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Chip Away":
                    b = {
                        'id': a,
                        'percent': 7.086
                        }
                    brand_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Circling Oblivion":
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 8.502
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 8.098
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.536
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Cold Conduction":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Compound Injury":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Cooked Alive":
                    b = {
                        'id': a,
                        'percent': 4.536
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Cremator":
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Cry Wolf":
                    b = {
                        'id': a,
                        'percent': 2.933
                        }
                    warcry.append(b)
                if a['text'] == "1 Added Passive Skill is Cult-Leader":
                    b = {
                        'id': a,
                        'percent': 16.196
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Dark Discourse":
                    b = {
                        'id': a,
                        'percent': 5.313
                        }
                    curse.append(b)
                if a['text'] == "1 Added Passive Skill is Dark Ideation":
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    chaos_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Dark Messenger":
                    b = {
                        'id': a,
                        'percent': 6.075
                        }
                    herald.append(b)
                if a['text'] == "1 Added Passive Skill is Deep Chill":
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Disciples":
                    b = {
                        'id': a,
                        'percent': 4.047
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Disorienting Wounds":
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Distilled Perfection":
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    flask_duration.append(b)
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    flask_recovery.append(b)
                if a['text'] == "1 Added Passive Skill is Dread March":
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    minion_life.append(b)
                if a['text'] == "1 Added Passive Skill is Empowered Envoy":
                    b = {
                        'id': a,
                        'percent': 12.154
                        }
                    herald.append(b)
                if a['text'] == "1 Added Passive Skill is Endbringer":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    herald.append(b)
                    b = {
                        'id': a,
                        'percent': 4.047
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Enduring Focus":
                    b = {
                        'id': a,
                        'percent': 1.466
                        }
                    channeling_skill_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Eldritch Inspiration":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    chaos_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Eternal Suffering":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    chaos_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Evil Eye":
                    b = {
                        'id': a,
                        'percent': 10.627
                        }
                    curse.append(b)
                if a['text'] == "1 Added Passive Skill is Eye to Eye":
                    b = {
                        'id': a,
                        'percent': 6.074
                        }
                    projectile.append(b)
                if a['text'] == "1 Added Passive Skill is Expansive Might":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    area_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Expendability":
                    b = {
                        'id': a,
                        'percent': 3.269
                        }
                    trap.append(b)
                if a['text'] == "1 Added Passive Skill is Expert Sabotage":
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    trap.append(b)
                if a['text'] == "1 Added Passive Skill is Exposure Therapy":
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 8.502
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 8.098
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.536
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Eye of the Storm":
                    b = {
                        'id': a,
                        'percent': 3.150
                        }
                    crit_chance.append(b)
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    ailment_effect.append(b)
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Fan the Flames":
                    b = {
                        'id': a,
                        'percent': 1.135
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Fasting":
                    b = {
                        'id': a,
                        'percent': 3.269
                        }
                    flask_duration.append(b)
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    flask_recovery.append(b)
                if a['text'] == "1 Added Passive Skill is Feasting Fiends":
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    minion_life.append(b)
                if a['text'] == "1 Added Passive Skill is First Among Equals":
                    b = {
                        'id': a,
                        'percent': 5.232
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Flow of Life":
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.125
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.023
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 1.135
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Follow-Through":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    projectile.append(b)
                if a['text'] == "1 Added Passive Skill is Forbidden Words":
                    b = {
                        'id': a,
                        'percent': 2.657
                        }
                    curse.append(b)
                if a['text'] == "1 Added Passive Skill is Guerilla Tactics":
                    b = {
                        'id': a,
                        'percent': 13.081
                        }
                    trap.append(b)
                if a['text'] == "1 Added Passive Skill is Grand Design":
                    b = {
                        'id': a,
                        'percent': 3.541
                        }
                    brand_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Haemorrhage":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.251
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 3.150
                        }
                    crit_chance.append(b)
                    b = {
                        'id': a,
                        'percent': 4.047
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Haunting Shout":
                    b = {
                        'id': a,
                        'percent': 5.862
                        }
                    warcry.append(b)
                if a['text'] == "1 Added Passive Skill is Heraldry":
                    b = {
                        'id': a,
                        'percent': 1.518
                        }
                    herald.append(b)
                    b = {
                        'id': a,
                        'percent': 2.023
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Hex Breaker":
                    b = {
                        'id': a,
                        'percent': 2.933
                        }
                    channeling_skill_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Holy Conquest":
                    b = {
                        'id': a,
                        'percent': 7.086
                        }
                    brand_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Hulking Corpses":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    minion_life.append(b)
                if a['text'] == "1 Added Passive Skill is Inspired Oppression":
                    b = {
                        'id': a,
                        'percent': 1.250
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Intensity":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    area_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Invigorating Portents":
                    b = {
                        'id': a,
                        'percent': 8.098
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Lasting Impression":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    herald.append(b)
                    b = {
                        'id': a,
                        'percent': 4.047
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Lead by Example":
                    b = {
                        'id': a,
                        'percent': 11.727
                        }
                    warcry.append(b)
                if a['text'] == "1 Added Passive Skill is Life from Death":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    minion_life.append(b)
                if a['text'] == "1 Added Passive Skill is Liquid Inspiration":
                    b = {
                        'id': a,
                        'percent': 1.637
                        }
                    flask_duration.append(b)
                if a['text'] == "1 Added Passive Skill is Low Tolerance":
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    chaos_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Magnifier":
                    b = {
                        'id': a,
                        'percent': 12.145
                        }
                    area_damage.append(b)
                    b = {
                        'id': a,
                        'percent': 6.296
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Master of Command":
                    b = {
                        'id': a,
                        'percent': 1.309
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Master of Fear":
                    b = {
                        'id': a,
                        'percent': 2.657
                        }
                    curse.append(b)
                if a['text'] == "1 Added Passive Skill is Master of Fire":
                    b = {
                        'id': a,
                        'percent': 0.565
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Mender's Wellspring":
                    b = {
                        'id': a,
                        'percent': 1.637
                        }
                    flask_duration.append(b)
                    b = {
                        'id': a,
                        'percent': 2.500
                        }
                    flask_recovery.append(b)
                if a['text'] == "1 Added Passive Skill is Mob Mentality":
                    b = {
                        'id': a,
                        'percent': 1.466
                        }
                    warcry.append(b)
                if a['text'] == "1 Added Passive Skill is Numbing Elixir":
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    flask_duration.append(b)
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    flask_recovery.append(b)
                if a['text'] == "1 Added Passive Skill is Overshock":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Overwhelming Malice":
                    b = {
                        'id': a,
                        'percent': 1.573
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Peak Vigour":
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    flask_duration.append(b)
                if a['text'] == "1 Added Passive Skill is Powerful Assault":
                    b = {
                        'id': a,
                        'percent': 6.074
                        }
                    area_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Precise Commander":
                    b = {
                        'id': a,
                        'percent': 1.309
                        }
                    aura_effect.append(b)
                    b = {
                        'id': a,
                        'percent': 1.573
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Precise Focus":
                    b = {
                        'id': a,
                        'percent': 5.862
                        }
                    channeling_skill_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Precise Retaliation":
                    b = {
                        'id': a,
                        'percent': 3.150
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Pressure Points":
                    b = {
                        'id': a,
                        'percent': 3.150
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Provocateur":
                    b = {
                        'id': a,
                        'percent': 3.150
                        }
                    crit_chance.append(b)
                    b = {
                        'id': a,
                        'percent': 5.862
                        }
                    warcry.append(b)
                if a['text'] == "1 Added Passive Skill is Pure Agony":
                    b = {
                        'id': a,
                        'percent': 2.023
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Pure Aptitude":
                    b = {
                        'id': a,
                        'percent': 5.232
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Pure Commander":
                    b = {
                        'id': a,
                        'percent': 5.232
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Pure Guile":
                    b = {
                        'id': a,
                        'percent': 5.232
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Pure Might":
                    b = {
                        'id': a,
                        'percent': 5.232
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Purposeful Harbinger":
                    b = {
                        'id': a,
                        'percent': 0.655
                        }
                    aura_effect.append(b)
                    b = {
                        'id': a,
                        'percent': 1.518
                        }
                    herald.append(b)
                    b = {
                        'id': a,
                        'percent': 2.023
                        }
                    minion_herald.append(b)
                if a['text'] == "1 Added Passive Skill is Quick Getaway":
                    b = {
                        'id': a,
                        'percent': 6.296
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Rapid Infusion":
                    b = {
                        'id': a,
                        'percent': 2.933
                        }
                    channeling_skill_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Rattling Bellow":
                    b = {
                        'id': a,
                        'percent': 11.727
                        }
                    warcry.append(b)
                if a['text'] == "1 Added Passive Skill is Remarkable":
                    b = {
                        'id': a,
                        'percent': 7.086
                        }
                    brand_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Rend":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Renewal":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    minion_life.append(b)
                if a['text'] == "1 Added Passive Skill is Repeater":
                    b = {
                        'id': a,
                        'percent': 12.145
                        }
                    projectile.append(b)
                if a['text'] == "1 Added Passive Skill is Replenishing Presence":
                    b = {
                        'id': a,
                        'percent': 2.614
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Savage Response":
                    b = {
                        'id': a,
                        'percent': 3.150
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Seeker Runes":
                    b = {
                        'id': a,
                        'percent': 3.541
                        }
                    brand_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Self-Fulfilling Prophecy":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    herald.append(b)
                if a['text'] == "1 Added Passive Skill is Septic Spells":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    chaos_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Set and Forget":
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    trap.append(b)
                if a['text'] == "1 Added Passive Skill is Shrieking Bolts":
                    b = {
                        'id': a,
                        'percent': 6.074
                        }
                    projectile.append(b)
                if a['text'] == "1 Added Passive Skill is Skullbreaker":
                    b = {
                        'id': a,
                        'percent': 1.573
                        }
                    crit_chance.append(b)
                if a['text'] == "1 Added Passive Skill is Sleepless Sentries":
                    b = {
                        'id': a,
                        'percent': 2.500
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Smoking Remains":
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Snaring Spirits":
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    totem.append(b)
                if a['text'] == "1 Added Passive Skill is Special Reserve":
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    flask_duration.append(b)
                    b = {
                        'id': a,
                        'percent': 10.003
                        }
                    flask_recovery.append(b)
                if a['text'] == "1 Added Passive Skill is Spiked Concoction":
                    b = {
                        'id': a,
                        'percent': 3.269
                        }
                    flask_duration.append(b)
                    b = {
                        'id': a,
                        'percent': 4.999
                        }
                    flask_recovery.append(b)
                if a['text'] == "1 Added Passive Skill is Stalwart Commander":
                    b = {
                        'id': a,
                        'percent': 5.232
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Steady Torment":
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Stoic Focus":
                    b = {
                        'id': a,
                        'percent': 11.727
                        }
                    channeling_skill_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Stormrider":
                    b = {
                        'id': a,
                        'percent': 2.500
                        }
                    ailment_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Streamlined":
                    b = {
                        'id': a,
                        'percent': 12.145
                        }
                    projectile.append(b)
                if a['text'] == "1 Added Passive Skill is Student of Decay":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    chaos_dot.append(b)

                    b = {
                        'id': a,
                        'percent': 4.047
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Surprise Sabotage":
                    b = {
                        'id': a,
                        'percent': 6.538
                        }
                    trap.append(b)
                if a['text'] == "1 Added Passive Skill is Titanic Swings":
                    b = {
                        'id': a,
                        'percent': 6.074
                        }
                    area_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Towering Threat":
                    b = {
                        'id': a,
                        'percent': 3.035
                        }
                    area_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Unwavering Focus":
                    b = {
                        'id': a,
                        'percent': 5.862
                        }
                    channeling_skill_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Unwaveringly Evil":
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    chaos_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Vast Power":
                    b = {
                        'id': a,
                        'percent': 6.074
                        }
                    area_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Vengeful Commander":
                    b = {
                        'id': a,
                        'percent': 5.232
                        }
                    aura_effect.append(b)
                if a['text'] == "1 Added Passive Skill is Victim Maker":
                    b = {
                        'id': a,
                        'percent': 5.313
                        }
                    curse.append(b)
                if a['text'] == "1 Added Passive Skill is Vile Reinvigoration":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.251
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 4.047
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.266
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Vital Focus":
                    b = {
                        'id': a,
                        'percent': 11.727
                        }
                    channeling_skill_damage.append(b)
                if a['text'] == "1 Added Passive Skill is Vivid Hues":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Warning Call":
                    b = {
                        'id': a,
                        'percent': 2.933
                        }
                    warcry.append(b)
                if a['text'] == "1 Added Passive Skill is Wasting Affliction":
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    chaos_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.125
                        }
                    cold_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 2.023
                        }
                    dot.append(b)
                    b = {
                        'id': a,
                        'percent': 1.135
                        }
                    fire_dot.append(b)
                    b = {
                        'id': a,
                        'percent': 1.182
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Whispers of Death":
                    b = {
                        'id': a,
                        'percent': 10.627
                        }
                    curse.append(b)
                if a['text'] == "1 Added Passive Skill is Wicked Pall":
                    b = {
                        'id': a,
                        'percent': 2.363
                        }
                    chaos_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Wish for Death":
                    b = {
                        'id': a,
                        'percent': 5.313
                        }
                    curse.append(b)
                if a['text'] == "1 Added Passive Skill is Wound Aggravation":
                    b = {
                        'id': a,
                        'percent': 4.722
                        }
                    phys_dot.append(b)
                if a['text'] == "1 Added Passive Skill is Wrapped in Flame":
                    b = {
                        'id': a,
                        'percent': 1.135
                        }
                    fire_dot.append(b)

    lists = list()
    try:
        item ={
            'category': '10% increased Area Damage',
            'id': 31,
            'list': area_damage
            }
        lists.append(item)

        item ={
            'category': '6% increased effect of Non-Curse Auras from your Skills',
            'id': 24,
            'list': aura_effect
            }
        lists.append(item)

        item ={
            'category': '12% increased Damage with Brand Skills',
            'id': 35,
            'list': brand_damage
            }
        lists.append(item)

        item ={
            'category': 'Channelling Skills deal 12% increased Damage',
            'id': 36,
            'list': channeling_skill_damage
            }
        lists.append(item)

        item ={
            'category': '+5% to Chaos Damage over Time Multiplier',
            'id': 19,
            'list': chaos_dot
            }
        lists.append(item)

        item ={
            'category': '+5% to Cold Damage over Time Multiplier',
            'id': 21,
            'list': cold_dot
            }
        lists.append(item)

        item ={
            'category': '15% increased Critical Strike Chance',
            'id': 29,
            'list': crit_chance
            }
        lists.append(item)

        item ={
            'category': '5% increased Effect of your Curses',
            'id': 25,
            'list': curse
            }
        lists.append(item)

        item ={
            'category': '+4% to Damage over Time Multiplier',
            'id': 22,
            'list': dot
            }
        lists.append(item)

        item ={
            'category': '10% increased Damage while affected by a Herald',
            'id': 26,
            'list': herald
            }
        lists.append(item)

        item ={
            'category': '10% increased Effect of Non-Damaging Ailments',
            'id': 23,
            'list': ailment_effect
            }
        lists.append(item)

        item ={
            'category': '+5% to Fire Damage over Time Multiplier',
            'id': 18,
            'list': fire_dot
            }
        lists.append(item)

        item ={
            'category': '6% increased Flask Effect Duration',
            'id': 37,
            'list': flask_duration
            }
        lists.append(item)

        item ={
            'category': '10% increased Life Recovery from Flasks and 10% increased Mana Recovery from Flasks',
            'id': 38,
            'list': flask_recovery
            }
        lists.append(item)

        item ={
            'category': 'Minions deal 10% increased Damage while you are affected by a Herald',
            'id': 27,
            'list': minion_herald
            }
        lists.append(item)

        item ={
            'category': 'Minions have 12% increased maximum Life',
            'id': 30,
            'list': minion_life
            }
        lists.append(item)

        item ={
            'category': '+5% to Physical Damage over Time Multiplier',
            'id': 20,
            'list': phys_dot
            }
        lists.append(item)

        item ={
            'category': '10% increased Projectile Damage',
            'id': 32,
            'list': projectile
            }
        lists.append(item)

        item ={
            'category': '12% increased Totem Damage',
            'id': 34,
            'list': totem
            }
        lists.append(item)

        item ={
            'category': '12% increased Trap Damage and 12% increased Mine Damage',
            'id': 33,
            'list': trap
            }
        lists.append(item)

        item ={
            'category': '15% increased Warcry Buff Effect',
            'id': 28,
            'list': warcry
            }
        lists.append(item)
    except:
        print('Fail')

    return lists
