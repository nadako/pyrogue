"items.py - Pyro items"

from util import *
import creatures
import magic

types = [
    (lang.itemtype_meleeweapons, "("),
    (lang.itemtype_armor, "["),
    (lang.itemtype_missileweapons, "{"),
    (lang.itemtype_ammo_or_thrown, "|"),
    (lang.itemtype_potions, "!"),
    (lang.itemtype_wands, "/"),
    (lang.itemtype_scrolls, "?"),
    (lang.itemtype_books, "+"),
    (lang.itemtype_rings, "="),
    (lang.itemtype_amulets, '"'),
    (lang.itemtype_tools, "~"),
    (lang.itemtype_food, "%"),
    (lang.itemtype_valuables, "$"),
    (lang.itemtype_other, "-"),
]

class AttackType(BASEOBJ):
    "Any mode of attack."
    speed = 100

class MeleeAttackType(AttackType):
    "Some mode of melee attack."
    damage_type = "physical"
    speed = 100
    damage = "1d3"
    def __init__(self, damage=None, speed=None):
        if damage is not None: self.damage = damage
        if speed is not None: self.speed = speed
    def Attempt(self, attacker, target):
        "Attempt this attack on the given target."
        attacker.Delay(self.speed)
        hit = attacker.MeleeHitBonus()
        evade = target.EvasionBonus()
        differential = hit - evade
        chance = hit_chance(differential, target.level)
        log("%s (%s to hit) attacks %s (%s evade, level %s) with %s%% chance to hit." %
            (attacker.name, hit, target.name, evade, target.level, int(chance*100)))
        if successful_hit(differential, target.level):
            # The attack landed; calculate damage:
            damage_roll = d(self.damage) + attacker.MeleeDamageBonus()
            protection_roll = quantize(target.ProtectionBonus())
            # Successful attack always does at least 1d2 damage:
            damage = max(d("1d2"), damage_roll - protection_roll)
            damage_taken = target.TakeDamage(damage, self.damage_type, source=attacker)
            report_combat_hit(attacker, target, damage_taken, self.verbs, self.verbs_sp)
            return True
        else:
            report_combat_miss(attacker, target, self.verbs, self.verbs_sp)
            return False

class DefaultAttack(MeleeAttackType):
    name = "attack"
    verbs = lang.verbs_default_attack
    verbs_sp = lang.verbs_default_attack_2p
    damage = "1d2"
    
class Item(BASEOBJ):
    "Inanimate objects"
    name = ">>Generic Item<<"
    type = "Other"
    weight = 1.0
    rarity = 1.0    # How often the item will be generated; 1.0 is standard.
    identified = False
    melee_attack = DefaultAttack()
    melee_twohand = False
    armor_points = 0
    material, prefix, suffix = None, None, None
    quantity = 1
    equip_effects = []
    hit_bonus = damage_bonus = 0
    thrown_damage = "1d2"
    def __init__(self):
        self.x, self.y, self.current_level = 0, 0, None
    def Duplicate(self):
        "Return an exact duplicate of this item."
        # Temporarily remove links that will cause deepcopy to choke:
        temp_level, self.current_level = self.current_level, None
        copy = deepcopy(self)
        # Restore links:
        copy.current_level = self.current_level = temp_level
        return copy
    def LongDescription(self):
        "Long description of the item."
        desc = "%s\n\n" % self.desc
        desc += lang.label_it_weighs % self.Weight() + "\n\n"
        try:
            desc += self.MeleeStats()
        except AttributeError: pass
        try:
            desc += self.ArmorStats()
        except AttributeError: pass        
        return desc
    def Name(self, noweight=False):
        name = self.name
        if self.material:
            name = "%s %s" % (self.material, name)
        if self.prefix:
            name = "%s %s" % (self.prefix, name)
        if self.suffix:
            name = "%s %s" % (name, self.suffix)
        try:
            bonus = self.BonusString()
        except AttributeError:
            bonus = ""
        if self.armor_points != 0:
            ap = " (%s)" % self.armor_points
        else:
            ap = ""
        name = "%s%s%s" % (name, bonus, ap)
        if not noweight:
            name += " (%ss)" % self.Weight()
        return name
    def OnEquip(self, mob):
        "Called when mob equips the item."
        for effect in self.equip_effects:
            mob.TakeEffect(effect, effect.Duration(mob))
    def OnUnequip(self, mob):
        "Called when mob unequips the item."
        for effect in self.equip_effects:
            mob.RemoveEffect(effect)
    def StacksWith(self, other):
        "Return whether the item stacks with another item."
        return self.Name(noweight=True) == other.Name(noweight=True)
    def Weight(self):
        return self.weight * self.quantity

# Weapon attack types:
class Punch(MeleeAttackType):
    name = lang.word_punch
    verbs = lang.verbs_punch
    verbs_sp = lang.verbs_punch_2p
    speed = 150
    damage = "1d2"
class Slash(MeleeAttackType):
    name = lang.word_slash
    verbs = lang.verbs_slash
    verbs_sp = lang.verbs_slash_2p
class Stab(MeleeAttackType):
    name = lang.word_stab
    verbs = lang.verbs_stab
    verbs_sp = lang.verbs_stab_2p
class Lash(MeleeAttackType):
    name = lang.word_lash
    verbs = lang.verbs_lash
    verbs_sp = lang.verbs_lash_2p
class Bludgeon(MeleeAttackType):
    name = lang.word_bludgeon
    verbs = lang.verbs_bludgeon
    verbs_sp = lang.verbs_bludgeon_2p
class Chop(MeleeAttackType):
    name = lang.word_chop
    verbs = lang.verbs_chop
    verbs_sp = lang.verbs_chop_2p

class Weapon(Item):
    pass
       
class MeleeWeapon(Weapon):
    # Although any item can be wielded in melee, this class is for
    # items that are designed to be used in melee combat.
    type = lang.itemtype_meleeweapons
    tile = "("
    color = c_Cyan
    equip_slot = lang.equip_slot_meleeweapon
    def BonusString(self):
        bonus = ""
        hit, dam = self.hit_bonus, self.damage_bonus
        if hit == dam == 0:
            return ""
        else:
            bonus = " [%s %s]" % (bonus_str(hit), bonus_str(dam))
            return bonus
    def MeleeStats(self):
        desc = ""
        if self.damage_bonus == 0:
            dam = ""
        else:
            dam = bonus_str(self.damage_bonus)
        if self.hit_bonus == 0:
            hit = ""
        else:
            hit = bonus_str(self.hit_bonus)
        desc += lang.label_melee_attack_desc % (self.melee_attack.verbs[1], 
                                                self.melee_attack.damage+dam)
        desc += lang.label_attack_speed % self.melee_attack.speed
        if hit:
            desc += lang.label_attack_tohit % hit
        desc += ".\n"
        if self.melee_twohand:
            desc += lang.label_twohand + "\n"
        return desc

        
class MissileWeapon(Weapon):
    type = lang.itemtype_missileweapons
    tile = "{"
    color = c_yellow
    equip_slot = lang.equip_slot_missileweapon
    fire_damage = "1d2"
    fire_speed = 100
    verbs = ["shoots", "shoots", "shoots"]
    verbs_sp = ["shoot", "shoot", "shoot"]
    def CanFire(self, ammo):
        "Return whether this weapon can fire the given ammo."
        # Implement in subclass.
        pass
class Bow(MissileWeapon):
    def CanFire(self, ammo):
        return isinstance(ammo, Arrow)

class Ammunition(Weapon):
    type = lang.itemtype_ammo_or_thrown
    tile = "|"
    projectile_char = "-|/\\"
    color = c_yellow
    equip_slot = lang.equip_slot_ammo
class Arrow(Ammunition):
    damage_type = "pierce"
    def __init__(self):
        Ammunition.__init__(self)
        self.quantity = d("4d6")


# Specific melee weapon types:
class ShortSword(MeleeWeapon):
    name = lang.itemname_shortsword
    desc = lang.itemdesc_shortsword
    weight = 3.0
    def __init__(self):
        MeleeWeapon.__init__(self)
        self.melee_attack = Slash("1d6", 100)
class LongSword(MeleeWeapon):
    name = lang.itemname_longsword
    desc = lang.itemdesc_longsword
    weight = 4.0
    def __init__(self):
        MeleeWeapon.__init__(self)
        self.melee_attack = Slash("1d7", 80)
class GreatSword(MeleeWeapon):
    name = lang.itemname_greatsword
    desc = lang.itemdesc_greatsword
    weight = 8.0
    melee_twohand = True
    def __init__(self):
        MeleeWeapon.__init__(self)
        self.melee_attack = Slash("2d6", 65)    
class BattleAxe(MeleeWeapon):
    name = lang.itemname_battleaxe
    desc = lang.itemdesc_battleaxe
    weight = 5.0
    def __init__(self):
        MeleeWeapon.__init__(self)
        self.melee_attack = Chop("1d8", 80)
class Dagger(MeleeWeapon):
    name = lang.itemname_dagger
    desc = lang.itemdesc_dagger
    weight = 1.0
    def __init__(self):
        MeleeWeapon.__init__(self)
        self.melee_attack = Stab("1d4", 130)
class Whip(MeleeWeapon):
    name = lang.itemname_whip
    desc = lang.itemdesc_whip
    weight = 1.0
    color = c_yellow
    def __init__(self):
        MeleeWeapon.__init__(self)
        self.melee_attack = Lash("1d4", 90)
class Club(MeleeWeapon):
    name = lang.itemname_club
    desc = lang.itemdesc_club
    weight = 4.0
    color = c_yellow
    def __init__(self):
        MeleeWeapon.__init__(self)
        self.melee_attack = Bludgeon("1d4", 100)

# Specific missile weapon types:
class ShortBow(Bow):
    name = lang.itemname_shortbow
    desc = lang.itemdesc_shortbow
    weight = 3.0

# Specific ammunition types:
class WoodArrow(Arrow):
    name = lang.itemname_woodarrow
    desc = lang.itemdesc_woodarrow
    weight = 0.02
    def __init__(self):
        Arrow.__init__(self)
        self.melee_attack = Stab("1d2", 100)
class IronArrow(Arrow):
    name = "iron arrow"
    desc = "It's an iron arrow."
    weight = 0.1
    color = c_red
    def __init__(self):
        Arrow.__init__(self)
        self.melee_attack = Stab("1d3", 100)
    

armor_prefixes = [
    (lang.quality_armor[0], -4),
    (lang.quality_armor[1], -3),
    (lang.quality_armor[2], -2),
    (lang.quality_armor[3], -1),
    (None, 0),
    (lang.quality_armor[4], 1),
    (lang.quality_armor[5], 2),
    (lang.quality_armor[6], 3),
    (lang.quality_armor[7], 4),
]
armor_mats = {
    "cloth": [
        (lang.material_armor_cloth[0], 0),
        (lang.material_armor_cloth[1], 5),
        (lang.material_armor_cloth[2], 10),
        (lang.material_armor_cloth[3], 15),
        (lang.material_armor_cloth[4], 20),
    ],
    "leather": [
        (lang.material_armor_leather[0], 0),
        (lang.material_armor_leather[1], 5),
        (lang.material_armor_leather[2], 10),
        (lang.material_armor_leather[3], 15),
        (lang.material_armor_leather[4], 20),
    ],
    "metal": [
        (lang.material_armor_metal[0], 0),
        (lang.material_armor_metal[1], 5),
        (lang.material_armor_metal[2], 10),
        (lang.material_armor_metal[3], 15),
        (lang.material_armor_metal[4], 20),
    ]
}
    
class Armor(Item):
    type = lang.itemtype_armor
    tile = "["
    color = c_yellow
    material, prefix, suffix = None, None, None
    def ArmorStats(self):
        desc = lang.label_armor_desc % (self.equip_slot, self.armor_points)
        return desc
    def StacksWith(self, other):
        # Armor doesn't stack:
        return False
class BodyArmor(Armor):
    equip_slot = lang.equip_slot_torso
class Helm(Armor):
    equip_slot = lang.equip_slot_head
class Boots(Armor):
    equip_slot = lang.equip_slot_feet
class Gloves(Armor):
    equip_slot = lang.equip_slot_hands
class ClothArmor(Armor): pass
class LeatherArmor(Armor): 
    color = c_yellow
class ChainArmor(Armor):
    color = c_cyan
class PlateArmor(Armor):
    color = c_Cyan

class Robe(BodyArmor, ClothArmor):
    name = lang.itemname_robe
    desc = lang.itemdesc_robe
    armor_points = 5
    weight = 1.0
    def __init__(self):
        self.color = choice([c_yellow, c_Yellow, c_White, c_white, c_Blue, c_cyan, c_Cyan])
        Item.__init__(self)
class Jerkin(BodyArmor, LeatherArmor):
    name = lang.itemname_jerkin
    desc = lang.itemdesc_jerkin
    armor_points = 7
    weight = 3.0
class ChainShirt(BodyArmor, ChainArmor):
    name = lang.itemname_chainshirt
    desc = lang.itemdesc_chainshirt
    armor_points = 9
    weight = 6.0
class PlateMail(BodyArmor, PlateArmor):
    name = lang.itemname_platemail
    desc = lang.itemdesc_platemail
    armor_points = 12
    weight = 10.0
class ClothGloves(Gloves, ClothArmor):
    name = lang.itemname_gloves
    desc = lang.itemdesc_gloves
    armor_points = 2
    weight = 0.5
    def __init__(self):
        self.color = choice([c_yellow, c_Yellow, c_White, c_white, c_Blue, c_cyan, c_Cyan])
        Item.__init__(self)
    
    
    
class Tool(Item):
    tile = "~"
    color = c_yellow
    type = lang.itemtype_tools    
class SmallBag(Tool):
    type = "Tools"
    name = "small bag"
    reduction = 0.05
    slots = 10    
    
class Jewelry(Item):
    type = lang.itemtype_jewelry
    protect, evade = 0, 0
class Ring(Jewelry):
    tile = "="
    type = lang.itemtype_rings
    equip_slot = lang.equip_slot_finger
class Amulet(Jewelry):
    tile = '"'
    type = lang.itemtype_amulets
    equip_slot = lang.equip_slot_neck


class Potion(Item):
    type = lang.itemtype_potions
    desc = lang.itemdesc_potion
    tile = "!"
    weight = 0.2
    def Quaff(self, quaffer):
        # Put potion-specific effects in the subclass under ApplyEffect.
        can_drink = True  # Some conditions might prevent drinking
        if can_drink:
            quaffer.inventory.Remove(self)
            self.ApplyEffect(quaffer)
        else:
            # Display some message about why drinking is impossible
            pass
        return can_drink
    def QuaffMessage(self, quaffer):
        if quaffer is Global.pc:
            return lang.you_drink % lang.ArticleName("a", self)
        elif quaffer.pc_can_see:
            return lang.mob_drinks % (lang.ArticleName("The", quaffer), lang.ArticleName("a", self))
        else:
            return ""


class Scroll(Item):
    type = lang.itemtype_scrolls
    tile = "?"
    color = c_White
    weight = 0.1
    def Read(self, reader):
        # Put scroll-specific effects in the subclass under ApplyEffect.
        can_read = True  # Some conditions might prevent reading:
        if can_read:
            reader.inventory.Remove(self)
            self.ApplyEffect(reader)
        else:
            # Display some message about why reading is impossible:
            pass
        return can_read
    
class SelfImprovementScroll(Scroll):
    name = lang.itemname_scroll_of_improvement
    def ApplyEffect(self, reader):
        if reader is Global.pc:
            Global.IO.Message(lang.effect_improvement)
            reader.GainStatPermanent("any")
            
class EnchantWeaponDamageScroll(Scroll):
    name = lang.itemname_scroll_of_weapon_dam
    def ApplyEffect(self, reader):
        if reader is Global.pc:
            # Make a list of all equipped weapons:
            weapons = reader.ItemsInSlot(lang.equip_slot_meleeweapon)
            weapons += reader.ItemsInSlot(lang.equip_slot_missileweapon)
            weapons += reader.ItemsInSlot(lang.equip_slot_ammo)
            if len(weapons) == 0:
                # No weapons equipped at all; fizzle:
                Global.IO.Message(lang.effect_scroll_none)
            else:
                # Enchant one at random:
                weapon = choice(weapons)
                Global.IO.Message(lang.effect_weapon_plus_dam % 
                                  lang.ArticleName("Your", weapon))
                weapon.damage_bonus += 1
    
class EnchantWeaponToHitScroll(Scroll):
    name = lang.itemname_scroll_of_weapon_hit
    def ApplyEffect(self, reader):
        if reader is Global.pc:
            # Make a list of all equipped weapons:
            weapons = reader.ItemsInSlot(lang.equip_slot_meleeweapon)
            weapons += reader.ItemsInSlot(lang.equip_slot_missileweapon)
            weapons += reader.ItemsInSlot(lang.equip_slot_ammo)
            if len(weapons) == 0:
                # No weapons equipped at all; fizzle:
                Global.IO.Message(lang.effect_scroll_none)
            else:
                # Enchant one at random:
                weapon = choice(weapons)
                Global.IO.Message(lang.effect_weapon_plus_dam % 
                                  lang.ArticleName("Your", weapon))
                weapon.hit_bonus += 1
                
class MinorHealPotion(Potion):
    color = c_Red
    name = lang.itemname_potion_of_minor_heal
    healing = "1d3+3"
    def ApplyEffect(self, quaffer):
        heal_amount = quaffer.Heal(d(self.healing))
        msg = self.QuaffMessage(quaffer)
        if heal_amount == 0:
            if quaffer is Global.pc:
                if irand(1, 10) == 10:
                    msg += " " + lang.effect_healpotion_gain_maxhp
                    quaffer.hp_max += 1
                    quaffer.hp += 1
                else:
                    msg += " " + lang.effect_healpotion_wasted
        elif heal_amount > 0:
            if quaffer is Global.pc:
                msg += " " + lang.effect_you_minor_healing
            elif quaffer.pc_can_see:
                msg += " " + lang.effect_mob_minor_healing % lang.ArticleName("The", quaffer)
        Global.IO.Message(msg)

class MightPotion(Potion):
    color = c_yellow
    name = lang.itemname_potion_of_might
    bonus = 3
    duration = 1000 * 20
    def ApplyEffect(self, quaffer):
        quaffer.TakeEffect(magic.StrBuff(self.bonus), self.duration)

class GiantStrengthPotion(MightPotion):
    color = c_Yellow
    name = lang.itemname_potion_of_giantstrength
    bonus = 8
    duration = 1000 * 10
        
class RingOfStrength(Ring):
    name = lang.itemname_ring_of_strength
    color = c_Red
    def __init__(self):
        Ring.__init__(self)
        self.equip_effects = [magic.EquipStatBonus(self, 'str', 1)]
    
all_ammos = [WoodArrow, IronArrow]
all_armor = [Robe, Jerkin, ChainShirt, PlateMail, ClothGloves]
all_melee_weapons = [ShortSword, LongSword, GreatSword, Dagger, Whip, Club]
all_missile_weapons = [ShortBow]
all_potions = [MinorHealPotion, MightPotion, GiantStrengthPotion]
all_rings = [RingOfStrength]
all_scrolls = [SelfImprovementScroll, EnchantWeaponDamageScroll, EnchantWeaponToHitScroll]

def random_bonus(level):
    "Return a bonus appropriate to the given level."
    bonus = norm(0, level / 4.0)
    # Make negative bonus rare:
    if bonus < 0:
        if rnd(0, 1) > 0.3:
            bonus = abs(bonus)
    return int(bonus)

def random_melee_weapon(level, w=None, nospecial=False):
    "Return a random melee weapon suitable for the given character level."
    if w is None:
        w = choice(all_melee_weapons)
    w = w()
    if not nospecial:
        if level < 0:
            level = abs(level)
            mod = -1
        else:
            mod = 1
        for i in xrange(level-1):
            if rnd(0, 1) < 0.5:
                w.hit_bonus += mod
            else:
                w.damage_bonus += mod
    return w

def random_missile_weapon(level, w=None, nospecial=False):
    if w is None:
        w = choice(all_missile_weapons)
    w = w()
    return w

def random_armor(level, a=None, nospecial=False):
    "Return a random piece of armor for the given level."
    if a is None:
        a = choice(all_armor)
    a = a()
    a.armor_points = quantize(a.armor_points * 1.1487 ** level)    # Doubles every five levels
    if isinstance(a, ClothArmor):
        mats = armor_mats["cloth"]
    elif isinstance(a, LeatherArmor):
        mats = armor_mats["leather"]
    elif isinstance(a, ChainArmor):
        mats = armor_mats["metal"]
    elif isinstance(a, PlateArmor):
        mats = armor_mats["metal"]
    p = []
    for mat, mat_lv in mats:
        for mod, mod_lv in armor_prefixes:
            if mat_lv + mod_lv == level:
                p.append((mat, mod))
    m = choice(p)
    a.material, a.prefix = m
    if nospecial: return a
    if rnd(0, 1) < 0.5:  # TODO: reduce this a lot!
        # Armor "of lightness":
        a.weight *= 0.75
        a.suffix = lang.label_of_lightness
    return a
    
def random_potion(level):
    return choice(all_potions)()

def random_ring(level):
    return choice(all_rings)()

def random_scroll(level):
    return choice(all_scrolls)()

def random_ammo(level):
    return choice(all_ammos)()
        
def random_item(level):
    "Return a random item suitable for the given character level."
    item = weighted_choice([
        (random_melee_weapon, 100),
        (random_missile_weapon, 20),
        (random_armor, 100), 
        (random_potion, 30), 
        (random_ring, 10), 
        (random_scroll, 30),
        (random_ammo, 30),
    ])(level)
    return item