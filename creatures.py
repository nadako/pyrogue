"creatures.py - Pyro creatures"

from util import *
import items
import dungeons
import astar
        
class Bite(items.MeleeAttackType):
    name = "bite"
    verbs = lang.verbs_bite  # no damage, hit, crit
    verbs_sp = lang.verbs_bite_2p
    damage = "1d4"
class Claw(items.MeleeAttackType):
    name = "claw"
    verbs = lang.verbs_claw
    verbs_sp = lang.verbs_claw_2p
    damage = "1d4"


class AI(object):
    "Artificial intelligence for mobs."
    def __init__(self, mob):
        self.mob = mob

class Berserker(AI):
    """
    This AI routine wanders aimlessly until it sees the @.  Then it charges
    and fights to the death.
    """
    def __init__(self, mob):
        AI.__init__(self, mob)
        self.target = None
        self.tx, self.ty, self.dir = None, None, None
        self.state = "wander"
    def Update(self):
        "Take one action"
        pc = Global.pc
        #TODO: Generalize this to follow any mob, not just PC.
        if self.state == "wander":
            if self.dir == None:
                self.PickNewDirection()
            if self.mob.can_see_pc:
                self.state = "chase"
                return
            else:
                blocker = self.mob.SquareBlocked(self.mob.x+self.dx, self.mob.y+self.dy)
                if blocker is None:
                    self.mob.Walk(self.dx, self.dy)
                    return
                # The square is blocked; see if it's an openable door:
                if isinstance(blocker, dungeons.Door):
                    if self.mob.can_open_doors:
                        if not blocker.Open(self.mob):
                            # Tried and failed to open the door; waste some time:
                            self.mob.Walk(0, 0)
                        return
                self.PickNewDirection()
                return
        elif self.state == "chase":
            if adjacent(self.mob, pc):
                self.mob.Attack(pc)
                return
            if self.mob.can_see_pc:
                self.tx, self.ty = pc.x, pc.y
            else:
                if (self.mob.x, self.mob.y) == (self.tx, self.ty):
                    # We're at the last place we saw the @, and we still can't see him:
                    log("%s lost sight of its prey." % self.mob.name)
                    self.state = "wander"
                    return
            # We can see the PC, but are not in melee range: use A*:
            path = astar.path(self.mob.x, self.mob.y, self.tx, self.ty, 
                              self.mob.PathfindPass, max_length=10)
            if path:
                dx, dy = path[0][0] - self.mob.x, path[0][1] - self.mob.y
                self.mob.Walk(dx, dy)
                log("%s found a path from (%s, %s) to (%s, %s) %s." % 
                    (self.mob.name, self.mob.x, self.mob.y, self.tx, self.ty, path))
                return
            else:
                log("%s failed pathfinding." % self.mob.name)
                # Pathfinding failed, but we can see the @...just sit there and be mad:
                self.mob.Walk(0, 0)
                return
    def PickNewDirection(self):
        try:
            self.dir = choice([d for d in range(9) if d != 4
                              and not self.mob.SquareBlocked(
                                  self.mob.x+offsets[d][0],
                                  self.mob.y+offsets[d][1])])
            self.dx, self.dy = offsets[self.dir]
            return True
        except IndexError:
            # No options for movement:
            self.mob.Walk(0, 0)
            return False

class Creature(object):
    "An animate object."
    name = "Generic Creature"   # If this is seen in-game, it's a bug.
    can_open_doors = False
    is_pc, can_see_pc, pc_can_see = False, False, False
    # Default stats:
    hp_max, mp_max = 10, 0
    hp, mp = hp_max, mp_max
    tile = "@"
    color = c_Magenta
    AIType = Berserker
    unique = False
    dead = False
    level = 9999    # By default won't be generated
    rarity = 1.0
    natural_armor = 0
    vision_radius = 8
    free_motion = False
    friendly = False
    age = 0  # Strictly increasing timer for effect durations, regeneration, etc.
    heal_timer, mana_timer = 0, 0  # For regeneration
    effects = []
    def __init__(self):
        self.equipped, self.unequipped = [], []   # By default, no equip slots
        self.x, self.y, self.current_level = 0, 0, None
        self.stats = Stats()
        self.inventory = Inventory(self)
        if self.AIType:
            self.AI = self.AIType(self)
        self.move_speed = 100
        self.attack_speed = 100
        self.cast_speed = 100
        self.hp = self.hp_max
        self.kill_xp = int(max(self.level+1, 1.5 ** self.level))
        if not self.is_pc:
            # For now, have every mob drop a level-appropriate item:
            self.inventory.Pickup(items.random_item(int_range(self.level, self.level/4.0, 2)))
    def Attack(self, target):
        # If a weapon is wielded, attack with it:
        try:
            # TODO: Support dual (or more!) wielding by handling a multi-item return list:
            attack = self.ItemsInSlot(lang.equip_slot_meleeweapon)[0].melee_attack
        except IndexError:
            # Otherwise, randomly choose a natural attack and use it:
            attack = weighted_choice(self.attacks)
        success = attack.Attempt(self, target)
    def CanOccupyTerrain(self, terrain):
        "Return whether the mob can enter a square with the given terrain."
        if terrain == FLOOR:
            return True
        return False
    def Delay(self, amount):
        "Add the specified amount of delay to the creature."
        self.timer += delay(amount)
        self.age += delay(amount)
    def Die(self):
        # Creature has been reduced to <=0 hp, or otherwise should die:
        self.inventory.DropAll()
        self.current_level.RemoveCreature(self)
        self.dead = True
    def eSTR(self):
        "Return the excess strength stat."
        return int(self.stats("str") - ceil(self.inventory.TotalWeight()))
    def EvasionBonus(self):
        return min(self.eSTR(), self.RawEvasionBonus())
    def FailedMove(self, mob):
        # Something tried to move onto the mob; initiate an attack:
        mob.TryAttack(self)
    def Heal(self, amount):
        "Heal the creature for the given amount."
        # Can be overridden for creatures that respond differently to healing (undead etc)
        heal_amount = min(amount, self.hp_max - self.hp)
        self.hp_max += heal_amount
        return heal_amount
    def ItemInSlot(self, equip_slot):
        "Return the *first* item equipped in the slot, or None if none."
        # Not ideal for slots that can be duplicated (e.g. finger)
        try:
            return self.ItemsInSlot(equip_slot)[0]
        except IndexError: return None
    def ItemsInSlot(self, equip_slot):
        "Return the item(s) currently equipped in a given slot as a (possibly empty) list."
        return [item for item in self.equipped if item.equip_slot == equip_slot]
    def MeleeDamageBonus(self):
        str_bonus = self.stats("str") - 8
        try:
            weapon_bonus = self.ItemsInSlot(lang.equip_slot_meleeweapon)[0].damage_bonus
        except IndexError:
            # Nothing is wielded.  Maybe include some monk/karate bonus here someday.
            weapon_bonus = 0
        return str_bonus + weapon_bonus
    def MeleeHitBonus(self):
        dex_bonus = self.stats("dex") - 8
        try:
            weapon_bonus = self.ItemsInSlot(lang.equip_slot_meleeweapon)[0].hit_bonus
        except IndexError:
            # Nothing is wielded.  Maybe include some monk/karate bonus here someday.
            weapon_bonus = 0
        return dex_bonus + weapon_bonus
    def MissileHitBonus(self):
        # For now it's the same as melee:
        return self.MeleeHitBonus()
    def Name(self):
        return self.name
    def PathfindPass(self, x, y):
        "Return whether the square is passable for the pathfinder."
        b = self.SquareBlocked(x, y)
        return (b is None) or (isinstance(b, dungeons.Door) and self.can_open_doors)
    def ProtectionBonus(self):
        return (self.natural_armor + sum([a.armor_points for a in self.equipped])) / 10.0
    def Quaff(self, potion):
        "Quaff a potion."
        potion.Quaff(self)
    def RawEvasionBonus(self):
        return self.stats("dex") - 8
    def Regenerate(self):
        "See if the creature heals any hp/mp."
        if self.age >= self.heal_timer:
            turns = 30 - self.stats("str")
            self.heal_timer = self.age + 1000 * turns
            if self.hp < self.hp_max:
                self.hp += 1
            if self.hp > self.hp_max:
                self.hp -= 1
        if self.age >= self.mana_timer:
            turns = 30 - self.stats("int")
            self.mana_timer = self.age + 1000 * turns
            if self.mp < self.mp_max:
                self.mp += 1
            if self.mp > self.mp_max:
                self.mp -= 1
    def RemoveEffect(self, effect):
        "Remove an effect from the mob if it's still there."
        try:
            self.effects.remove(effect)
            effect.Remove(self, silent=True)
        except ValueError:
            # It wasn't there.
            pass
    def SquareBlocked(self, x, y):
        "Return the first thing, if any, blocking the square."
        L = self.current_level
        if not (0 < x < L.layout.level_width-1
        and 0 < y < L.layout.level_height-1):
            # Can't occupy squares outside the level no matter what:
            return OUTSIDE_LEVEL
        # Check whether another creature is there:
        c = L.CreatureAt(x, y)
        if c: return c
        # Check whether the terrain type is passable:
        terrain = L.layout.data[y][x]
        if not self.CanOccupyTerrain(terrain):
            return WALL
        # Check whether there's an impassable feature (e.g. closed door):
        feature = L.FeatureAt(x, y)
        if feature and not self.CanOccupyTerrain(feature.block_type):
            return feature
        return None
    def TakeDamage(self, amount, type=None, source=None):
        # This method can be overridden for special behavior (fire heals elemental, etc)
        self.hp -= amount
        # Check for death:
        if self.hp <= 0:
            self.Die()
            if source is Global.pc:
                Global.pc.GainXP(self.kill_xp)
        return amount
    def TakeEffect(self, new_effect, duration):
        "Apply a temporary or permanent effect to the creature."
        if duration is None:
            new_effect.expiration = None
        else:
            new_effect.expiration = self.age + duration
        # First remove any effect that is overridden by the new one:
        overridden = [e for e in self.effects if new_effect.Overrides(e)]
        for e in overridden: self.RemoveEffect(e)
        # Now check whether an existing effect overrides this one:
        overrides = [e for e in self.effects if e.Overrides(new_effect)]
        if not overrides:
            new_effect.Apply(self)
            self.effects.append(new_effect)
    def TryAttack(self, target):
        # Mob has tried to move onto another mob; possibly attack.
        # This would be the place to abort an attack on a friendly mob, etc.
        # TODO: implement the above so mobs won't attack each other
        # For now it's hacked:
        if self.is_pc or target.is_pc:
            self.Attack(target)
    def Unequip(self, item, silent=False):
        # Unequip the given item if equipped:
        try:
            self.equipped.remove(item)
            self.unequipped.append(item.equip_slot)
            if self.is_pc and not silent:
                Global.IO.Message(lang.msg_you_unequip % lang.ArticleName("the", item))
            item.OnUnequip(self)
            return True
        except ValueError:
            return False
    def Update(self):
        assert not self.dead
        self.UpdateEffects()
        self.Regenerate()
        self.AI.Update()
    def UpdateEffects(self):
        "Update any temporary mods on self or carried items."
        expired_effects = [e for e in self.effects if e.expiration is not None
                           and e.expiration < self.age]
        for e in expired_effects:
            e.Remove(self)
            self.effects.remove(e)
        # TODO: add item updates too, once that type of effect exists
    def Walk(self, dx, dy):
        "Try to move the specified amounts."
        msg = ""
        if dx == dy == 0:
            self.Delay(self.move_speed)
            return True, msg
        blocker = self.SquareBlocked(self.x+dx, self.y+dy)
        if blocker:
            if not self.free_motion or isinstance(blocker, Creature) or blocker == OUTSIDE_LEVEL:
                # Something blocked the mob from moving--
                try:
                    # Let the blocker respond if it can:
                    msg = blocker.FailedMove(self)    
                except AttributeError:
                    pass
                return False, msg
        self.current_level.MoveCreature(self, self.x + dx, self.y + dy)
        self.Delay(self.move_speed)
        return True, ""
    def Wield(self, item):
        "Wield the item as a melee weapon."
        # If the item we're wielding is stacked, split one off to wield:
        if item.quantity > 1:
            stack = item
            item = self.inventory.Remove(stack, 1)
            self.inventory.Add(item, nostack=True)
        try:
            # TODO: Ask which to replace if dual-wielding:
            wielded = self.ItemsInSlot(lang.equip_slot_meleeweapon)[0]
        except IndexError:
            wielded = None
        if wielded is not None:
            # Unequip the old item:
            self.Unequip(wielded)
            # Remove and re-add it to inventory so it'll stack if it should:
            self.inventory.Remove(wielded)
            self.inventory.Add(wielded)
        # Wield the new weapon:
        self.Equip(item)
    def Equip(self, item, silent=False):
        # Equip the given item if possible:
        if item.equip_slot in self.unequipped:
            self.equipped.append(item)
            self.unequipped.remove(item.equip_slot)
            if self.is_pc and not silent:
                Global.IO.Message(lang.msg_you_equip % lang.ArticleName("the", item))
            item.OnEquip(self)
            return True
        else:
            return False
                
class Inventory(object):
    "Inventory class for creatures and the player."
    def __init__(self, mob):
        self.mob = mob
        self.items = []
        self.capacity = mob.stats("str") * 10
    def Add(self, item, nostack=False):
        for i, L in self.items:
            if not nostack and i.StacksWith(item):
                i.quantity += item.quantity
                letter = L
                break
        else:
            letter = self.NextLetter()
            self.items.append((item, letter))
        return letter
    def CanHold(self, item):
        "Return whether the item can be picked up."
        return item.Weight() + self.TotalWeight() <= self.Capacity()
    def Capacity(self):
        return self.capacity
    def Drop(self, item, qty=1):
        dropped = self.Remove(item, qty)
        assert dropped is not None
        # If the item was equipped, unequip it first:
        if item in self.mob.equipped:
            self.mob.Unequip(item)
            text = lang.you_unequip_and_drop_item % lang.ArticleName("the", dropped)
        else:
            text = lang.you_drop_item % lang.ArticleName("the", dropped)
        # Put the item on the floor:
        self.mob.current_level.AddItem(dropped, self.mob.x, self.mob.y)
        return True, text
    def DropAll(self):
        "Drop all inventory items--e.g. when the mob dies."
        for i in self.items:
            self.Drop(i[0])
    def GetItemByLetter(self, letter):
        items = [i[0] for i in self.items if i[1] == letter]
        if len(items) == 0:
            return None
        elif len(items) == 1:
            return items[0]
        else:
            raise IndexError
    def Has(self, item):
        "Return whether the item exists in inventory."
        return item in [i[0] for i in self.items]
    def ItemsOfType(self, type, letters=True):
        # Verify valid type:
        assert len([t for t in items.types if t[0] == type]) != 0
        # Return the list of items:
        it = [i for i in self.items if i[0].type == type]
        it.sort(key=lambda i:i[0])
        if letters:
            return it    
        else:
            return [i[0] for i in it]
    def NextLetter(self):
        "Return the first free letter."
        taken = [item[1] for item in self.items]
        for L in letters:
            if L not in taken:
                return L
        return None
    def Num(self):
        "Number of items in the inventory."
        return len(self.items)
    def Pickup(self, item, qty=1):
        # If they want to pick up fewer items than are there, split stacks:
        no_remove = False
        if qty < item.quantity:
            new_item = item.Duplicate()  # item to be picked up
            item.quantity -= qty
            new_item.quantity = qty
            no_remove = True
        else:
            new_item = item
        if self.CanHold(new_item):
            # Add to inventory:
            letter = self.Add(new_item)
            # If it's sitting on the floor of a level, remove it from there:
            if not no_remove and new_item.current_level is not None:
                new_item.current_level.Dirty(new_item.x, new_item.y)
                new_item.current_level.RemoveItem(new_item)
            return True, lang.you_pick_up_item % (lang.ArticleName("the", new_item), letter)
        else:
            return False, lang.error_too_heavy
    def Remove(self, item, qty=1):
        "Remove a quantity of an item from inventory, returning the item stack removed."
        new_items = []
        removed_item = None
        for i in self.items:
            if i[0] == item:
                assert i[0].quantity >= qty  # Can't drop more than we have.
                if i[0].quantity == qty:
                    removed_item = i[0]
                    # If it was equipped, unequip it:
                    self.mob.Unequip(item)
                    continue
                elif i[0].quantity > qty:
                    removed_item = deepcopy(i[0])
                    removed_item.quantity = qty
                    i[0].quantity -= qty
                    new_items.append(i)
            else:
                new_items.append(i)
        self.items = new_items
        return removed_item
    def TotalWeight(self):
        return sum([i[0].Weight() for i in self.items])


class StatMod(object):
    "A temporary or permanent modification of a stat."
    def __init__(self, amount, desc):
        self.amount, self.desc = amount, desc
    
class Stat(object):
    "Tracks a single stat."
    def __init__(self, abbr, name, value):
        self.abbr, self.name, self.base_value = abbr, name, value
        self.mods = []
    def BaseValue(self):
        return self.base_value
    def CurrentValue(self):
        return self.base_value + sum([mod.amount for mod in self.mods])
    def Modify(self, amount, desc="", permanent=False):
        if permanent:
            self.base_value += amount
        else:
            mod = StatMod(amount, desc)
            # TODO: Only allow one instance with a given desc
            self.mods.append(mod)
            return mod
    
class Stats(object):
    "Class to handle stat tracking for creatures."
    def __init__(self, str=8, dex=8, int=8):
        self.stats = {"str": Stat("str", lang.stat_name_str, str), 
                      "dex": Stat("dex", lang.stat_name_dex, dex), 
                      "int": Stat("int", lang.stat_name_int, int)}
    def __call__(self, stat, base=False):
        "Enables retrieving stats by: creature.stats('str')"
        try:
            if base:
                return self.stats[stat].BaseValue()
            else:
                return self.stats[stat].CurrentValue()
        except KeyError:
            raise KeyError("Stat must be in %s." % self.stats.keys())
    def Modify(self, stat, amount, desc="", permanent=False):
        return self.stats[stat].Modify(amount, desc, permanent)
    def Unmodify(self, mod):
        for stat in self.stats.values():
            try:
                stat.mods.remove(mod)
            except ValueError:
                pass
    
######################### CREATURE FAMILIES ############################
class Humanoid(Creature):
    tile = "h"
    color = c_White
    def __init__(self):
        Creature.__init__(self)
        self.unequipped = [
            lang.equip_slot_head,
            lang.equip_slot_torso,
            lang.equip_slot_hands,
            lang.equip_slot_waist,
            lang.equip_slot_feet,
            lang.equip_slot_finger,
            lang.equip_slot_finger,
            lang.equip_slot_neck,
            lang.equip_slot_back,
            lang.equip_slot_offhand,
            lang.equip_slot_meleeweapon,
            lang.equip_slot_missileweapon,
            lang.equip_slot_ammo,
    ]    

class Rodent(Creature):
    tile = "r"
    color = c_yellow
class Kobold(Creature):
    tile = "k"
    color = c_Green
class Goblin(Humanoid):
    tile = "g"
    color = c_green
    
####################### SPECIFIC CREATURE TYPES ########################

class Rat(Rodent):
    name = lang.mob_name_rat
    color = c_yellow
    hp_max = 5
    dex, str = 6, 8
    level = 1
    attacks = [
        [Claw("1d2", 100), 2],
        [Bite("1d3", 100), 1],
    ]
    desc = lang.mob_desc_rat
    
class WimpyKobold(Kobold):
    name = lang.mob_name_kobold
    can_open_doors = True
    hp_max = 6
    str, dex, int = 2, 6, 3
    level = 1
    attacks = [[items.Punch("1d3", 100), 1]]
    desc = lang.mob_desc_kobold
    def __init__(self):
        Kobold.__init__(self)
        # Some kobolds carry weapons:
        if irand(0, 10) < 7:
            weapon = weighted_choice([
                (items.ShortSword(), 1),
                (items.Dagger(), 2),
                (items.Club(), 3),
                (items.Whip(), 0.5)])
            self.inventory.Pickup(weapon)
            self.Equip(weapon)
    
class WimpyGoblin(Goblin):
    name = lang.mob_name_goblin
    can_open_doors = True
    hp_max = 7
    level = 2
    str, dex, int = 3, 6, 3
    desc = lang.mob_desc_goblin
    def __init__(self):
        Goblin.__init__(self)
        # Goblins always carry weapons:
        weapon = weighted_choice([
            (items.ShortSword(), 3),
            (items.Club(), 4),
            (items.LongSword(), 1)])
        self.inventory.Pickup(weapon)
        self.Equip(weapon)
        
class Wolf(Creature):
    name = lang.mob_name_wolf
    tile = "d"
    color = c_White
    hp_max = 7
    level = 2
    str, dex, int = 5, 7, 1
    attacks = [(Bite("1d6", 100), 1)]
    move_speed = 110
    desc = lang.mob_desc_wolf
    
class Imp(Creature):
    name = lang.mob_name_imp
    tile = "i"
    color = c_Red
    hp_max = 4
    str, dex, int = 2, 10, 9
    move_speed = 110
    attacks = [(Claw("1d3", 160), 1)]
    level = 3
    desc = lang.mob_desc_imp
        
class Ogre(Humanoid):
    name = lang.mob_name_ogre
    tile = "O"
    color = c_Yellow
    can_open_doors = True
    hp_max = 15
    str, dex, int = 14, 6, 3
    level = 4
    move_speed = 80
    attacks = [[items.Punch("1d3", 80), 1]]
    desc = lang.mob_desc_ogre
    
all = [Rat, WimpyKobold, WimpyGoblin, Wolf, Imp, Ogre]

def RandomMob(level):
    "Create and return a mob appropriate to the given dungeon level."
    mobs = [(mob, mob.rarity) for mob in all if -1 <= level - mob.level <= 1]
    mob = weighted_choice(mobs)
    return mob()
