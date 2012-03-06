"strings.py - Multi-language support for Pyro."

# THIS GAME IS STILL IN ALPHA!  It's probably way too soon to start working on
# a translation, since lots of these messages are going to change, and lots more
# are going to be added, in the near future.

# NOTES FOR TRANSLATION:

#  When '%s' appears in a string, the game will substitute a value at that position.
#  For instance, "You equip %s." could become "You equip the sword.",
#  or "You equip Obliteron, Almighty Greathammer of the Seventeen Hells."
#   - Examples of fill-in values are given in comments at the end of such lines.

# - Sequences like ^G^ and ^r^ are color codes.  The codes are:
#   - k:black  b:blue  g:green  c:cyan  r:red  m:magenta  y:yellow  w:white
#   - Capital letters result in bright versions of the same color.
#   - The sequence ^0^ (zero, not the letter O) is used to restore the default color.

# HOW TO ADD SUPPORT FOR ANOTHER LANGUAGE:
# Subclass the English class, and begin overriding properties.  Subclassing rather
# than creating a sibling class will ensure that any missing messages will
# appear in English, instead of crashing the game.  Then, at the bottom of this
# file, change the line that reads "lang = English()" to reference your new
# language instead.  (This will probably be moved to an in-game menu eventually.)

class English(object):
    archdesc_disdwarf = "Dwarves are said to horde vast treasures in their mountan halls.  In keeping with the Dwarves' affinity with the earth, rare gems and precious metals are especially prized.  The Treasure Hunter is a tough-as-nails explorer who braves the dangers of the dungeon to retrieve the raw materials used by Dwarven smiths in their incomparable craftwork.  His skills are focused on observation and survival."
    archdesc_diself = "Although the Elves never grow old, they are not quite immortal and can die by violence.  Perhaps this fact, together with the Elves' naturally subtle disposition, explains why so many who choose to risk their lives in the dungeons follow the underworld god Dis.  Enchanters are versatile characters with a wide selection of spells, though not as powerful as those of the Wizard."
    archdesc_dishuman = "Krol does not have a monopoly on violence--the Humans who follow the underworld god Dis are as deadly, and are perhaps even more feared for their mystery and subtlety.  The Assassin is a master of stealth and treachery, preferring to strike his enemy by surprise, and if possible, to finish the job with the first blow."
    archdesc_kroldwarf = "The Dwarves were old when the Humans and Elves arrived thousands of years ago, and the Dwarves will remain in their stone halls when the other races have come and gone.  The Warrior embodies the steadfast determination of his Dwarven ancestors.  He can withstand tremendous physical punishment, and his offensive skills are formidable."
    archdesc_krolelf = "It is true that Krol values superior force over subtlety, but it would be a mistake to assume that all his followers are unsophisticated brutes.  The Wizard harnesses his formidable intellect to wield magical energies of tremendous power.  Though physically unimposing, the Wizard is the most powerful destructive force in the natural world."
    archdesc_krolhuman = "Humans have the briefest lives of all the natural races, which perhaps explains the fervor with which the Berserker serves his god Krol.  Unmatched in physical ferocity, the Berserker throws himself into battle without hesitation, consumed by the desire to kill for his god."
    
    archname_disdwarf = "Dwarf of Dis (Treasure Hunter)"
    archname_disdwarf_short = "Treasure Hunter"
    archname_diself = "Elf of Dis (Enchanter)"
    archname_diself_short = "Enchanter"
    archname_dishuman = "Human of Dis (Assassin)"
    archname_dishuman_short = "Assassin"
    archname_kroldwarf = "Dwarf of Krol (Warrior)"
    archname_kroldwarf_short = "Warrior"
    archname_krolelf = "Elf of Krol (Wizard)"
    archname_krolelf_short = "Wizard"
    archname_krolhuman = "Human of Krol (Berserker)"
    archname_krolhuman_short = "Berserker"

    cmdname_ascend = "Ascend staircase"
    cmdname_autorest = "Rest 100 turns or until healed"
    cmdname_autorun = "Auto-run"
    cmdname_cast = "Cast a spell"
    cmdname_cheat = "Cheat menu"
    cmdname_descend = "Descend staircase"
    cmdname_detailedplayerstats = "Detailed character info"
    cmdname_drop = "Drop an item"
    cmdname_equipment = "View equipped items"
    cmdname_examine = "Examine an item"
    cmdname_fire = "Fire equipped missile weapon"
    cmdname_help = "List all commands"
    cmdname_inventory = "View inventory"
    cmdname_message_log = "Message log"
    cmdname_openclosedoor = "Open or close a door"
    cmdname_pickup = "Pick up items"
    cmdname_quaff = "Quaff a potion"
    cmdname_quit = "Quit"
    cmdname_read = "Read a scroll"
    cmdname_targetnext = "Target next nearby enemy"
    cmdname_throw = "Throw an object"
    cmdname_untarget = "Forget current target"
    cmdname_unwear = "Unequip an item"
    cmdname_wear = "Wear or wield an item"

    combat_mob_hit_mob = "%s %s %s."  # ("The kobold"[attacker], "slashes", "the kobold"[target])
                                      # I only include this in case the order needs to change!
    combat_mob_hit_you = "%s ^R^%s^0^ you. [^R^%s^0^]"  # ("The kobold", "slashes", "3")
    combat_mob_hit_you_no_damage = "%s %s you, but does no damage."  # ("The kobold", "slashes at")
    combat_mob_misses_mob = "%s tries to %s %s, but misses."  # ("The kobold[attacker], "slash", "the kobold"[target])
    combat_mob_misses_you = "%s tries to %s you, but misses."  # ("The kobold", "slash")
    combat_you_hit = "You ^G^%s^0^ %s. [^G^%s^0^]"  # ("cleave", "the kobold", 12)
    combat_you_hit_no_damage = "You %s %s, but do no damage."  # ("swing at", "the kobold")
    combat_you_killed = "^G^You have killed %s! (%s xp)"  # ("the kobold", 2)
    combat_you_miss = "You try to %s %s, but miss."  # ("slash", "the kobold")

    effect_agility_buff_gone_mob = "%s is moving less gracefully."  # ("The kobold")
    effect_agility_buff_gone_you = "^B^You no longer feel exceptionally agile."
    effect_agility_buff_mob = "%s appears to move more gracefully."  # ("The kobold")
    effect_agility_buff_you = "^G^You feel more agile."
    effect_healpotion_gain_maxhp = "^W^You feel better than ever!"
    effect_healpotion_wasted = "It tasted healthy, but you feel the same."
    effect_improvement = "You gain insight about how you can improve yourself."
    effect_mob_minor_healing = "%s looks healthier."  # ("The kobold")
    effect_scroll_none = "The scroll vanishes...nothing seemed to happen."
    effect_strength_buff_gone_mob = "%s no longer looks so strong."  # ("The kobold")
    effect_strength_buff_gone_you = "^B^You no longer feel exceptionally strong."
    effect_strength_buff_mob = "%s appears to grow stronger."  # ("The kobold")
    effect_strength_buff_you = "^G^You feel mighty."
    effect_weapon_plus_dam = "%s glows ^R^bright red^0^ momentarily."  # ("Your dagger")
    effect_weapon_plus_hit = "%s glows ^G^bright green^0^ momentarily."  # ("Your dagger")
    effect_you_minor_healing = "^G^You feel better."
    
    # TODO: decouple game logic from these values.
    equip_slot_ammo = "projectile"
    equip_slot_back = "back"
    equip_slot_feet = "feet"
    equip_slot_finger = "finger"
    equip_slot_hands = "hands"
    equip_slot_head = "head"
    equip_slot_meleeweapon = "melee weapon"
    equip_slot_missileweapon = "missile weapon"
    equip_slot_neck = "neck"
    equip_slot_offhand = "offhand" 
    equip_slot_torso = "torso"
    equip_slot_waist = "waist"

    error_bad_qty = "^R^Invalid quantity."
    error_bad_spell_shortcut = "^R^You've never heard of that spell before."
    error_cannot_drink_item = "^R^You want to drink a %s?  No."
    error_cannot_equip_item = "^R^That item is not made to be equipped."
    error_cannot_leave = "^R^You can't leave without the widget!"
    error_cannot_read_item = "^R^There's nothing interesting written on the %s."
    error_carrying_nothing = "^R^You are not carrying anything."
    error_door_already_closed = "^R^The door is already closed."
    error_door_blocked_by_creature = "^R^%s is blocking the door."  # ("The kobold")
    error_door_blocked_by_item = "^R^You can't close the door--something is in the way."
    error_insufficient_mana = "^R^You do not have enough mana to cast %s."  # ("magic missile")
    error_item_does_not_fit = "^R^That item doesn't fit your body."
    error_mob_carrying_nothing = "The creature has no items."
    error_no_ammo = "^R^You do not have any ammunition for %s."  # ("your bow")
    error_no_enemies_to_target = "^R^Cannot target--no enemies in range."
    error_no_missile_weapon = "^R^You have no missile weapon equipped."
    error_no_spells_known = "^R^You don't know any spells."
    error_no_stairs_here = "^R^There are no stairs here."
    error_nothing_here_to_pickup = "^R^There is nothing here to pick up."
    error_nothing_near_to_openclose = "^R^There is nothing nearby to open or close."
    error_nothing_there_to_openclose = "^R^There is nothing there to open or close."
    error_stairs_not_up = "^R^These stairs do not lead up."
    error_stairs_not_down = "^R^These stairs do not lead down."
    error_too_heavy = "^R^You can't carry that much weight."

    feature_name_door = "door"
    feature_name_staircase = "staircase"
    feature_name_staircase_down = "staircase down"
    feature_name_staircase_up = "staircase up"
    
    goddesc_krol = "Almighty and vengeful Krol is the god of violent conflict.  Krol is not evil, though many who give him allegiance are.  Krol values strength and aggression, and expects his followers to overcome life's obstacles through overwhelming force.  Krol and his adherents are not known for subtlety or patience."
    goddesc_dis = "Dis rules the shadowy realm of the Underworld.  Subtle and mysterious, he bestows upon his faithful the dark powers of stealth, trickery, and death."
    
    itemdesc_battleaxe = "A large, heavy, two-bladed axe used for hacking at the foe."
    itemdesc_chainshirt = "A long shirt of interlocking metal rings covering the torso and legs."
    itemdesc_club = "A stout length of wood, heavier at one end.  About as low-tech as it gets."
    itemdesc_dagger = "A small blade about a foot long with a sharp tip, used for stabbing.  It is very quick, but doesn't do much damage."
    itemdesc_gloves = "A pair of cloth gloves offering slight protection."
    itemdesc_greatsword = "A huge, heavy sword with a blunt tip, used for slashing and crushing.  It is slow but very powerful."
    itemdesc_jerkin = "This leather jerkin provides protection from physical attack, while giving the wearer freedom of movement."
    itemdesc_longsword = "A long sword, slightly over two feet long.  It is mostly used for slashing attacks, and is somewhat slower and more powerful than a short sword."
    itemdesc_platemail = "A very heavy suit of metal plates.  It provides excellent protection, but limits movement significantly."
    itemdesc_potion = "A small vial with a magical concoction inside."
    itemdesc_robe = "This long, flowing robe does not hinder the wearer's movements, but the cloth provides only very minimal protection against physical attack."
    itemdesc_shortbow = "A small, simple bow constructed from a single piece of wood.  It is not as powerful as a longbow, but is lighter and easier to manage."
    itemdesc_shortsword = "A sword about eighteen inches long with a sharp tip, designed for slashing and stabbing."
    itemdesc_whip = "This weapon does little damage, and is somewhat slow to attack with."
    itemdesc_woodarrow = "A long, straight wooden shaft, feathered at one end and pointed at the other, meant to be fired from a bow."

    itemname_battleaxe = "battle axe"
    itemname_chainshirt = "chain shirt"
    itemname_club = "club"
    itemname_dagger = "dagger"
    itemname_potion_of_giantstrength = "potion of giant strength"
    itemname_gloves = "gloves"
    itemname_greatsword = "greatsword"
    itemname_jerkin = "jerkin"
    itemname_longsword = "long sword"
    itemname_platemail = "plate armor"
    itemname_potion_of_might = "potion of might"
    itemname_potion_of_minor_heal = "minor potion of healing"
    itemname_ring_of_strength = "ring of strength"
    itemname_robe = "robe"
    itemname_scroll_of_improvement = "scroll of self-improvement"
    itemname_scroll_of_weapon_dam = "scroll of enchant weapon II"
    itemname_scroll_of_weapon_hit = "scroll of enchant weapon I"
    itemname_shortbow = "short bow"
    itemname_shortsword = "short sword"
    itemname_whip = "whip"
    itemname_woodarrow = "wooden arrow"
    
    itemtype_ammo_or_thrown = "Ammunition/Thrown Weapons"
    itemtype_amulets = "Amulets"
    itemtype_armor = "Armor"
    itemtype_books = "Books"
    itemtype_food = "Food"
    itemtype_jewelry = "Jewelry"
    itemtype_meleeweapons = "Melee Weapons"
    itemtype_missileweapons = "Missile Weapons"
    itemtype_other = "Other"
    itemtype_potions = "Potions"
    itemtype_rings = "Rings"
    itemtype_scrolls = "Scrolls"
    itemtype_tools = "Tools"
    itemtype_valuables = "Valuables"
    itemtype_wands = "Wands"
    
    key_tab = "Tab"
    
    label_armor_desc = "When equipped on your %s, it grants %s armor points."  # ("head", 12)
    label_attack_speed = "with speed %s"  # (100)
    label_attack_tohit = " and %s to hit"  # (+3)
    label_backpack_items = "Items in backpack"
    label_char_title = "%s, the level %s %s"  # ("John", 9, "Warrior")
    label_equipped_items = "Equipped items"
    label_evasion_limited = "[limited by eSTR]"
    label_help_title = "-= Pyro Help =-"
    label_inventory_weight = "(Total: %ss, Capacity: %ss)"  # (10.35, 15.0)
    label_it_weighs = "It weighs %s stones."  # (2.0)
    label_item_use_failure = "item use failure"
    label_keyboard_commands = "- Keyboard Commands -"
    label_melee_attack_desc = "In melee combat, it %s for %s damage "  # ("slashes", "1d6")
    label_melee_damage = "melee damage"
    label_movement_keys = "    - Movement Keys -"
    label_now_targeting = "Now targeting"
    label_of_lightness = "of lightness"
    label_rest_one_turn = "to rest a single turn"
    label_run = "then a ^Y^direction^y^ to run"
    label_space_to_cancel = "space to cancel"
    label_spell_failure = "spell failure"
    label_to_hit = "to hit"
    label_twohand = "It requires both hands to wield."
    
    material_armor_cloth = ["burlap", "linen", "silk", "ironweave", "highcloth"]
    material_armor_leather = ["leather", "thick leather", "hard leather", "basilisk hide", "dragonscale"]
    material_armor_metal = ["iron", "steel", "mithril", "adamantium", "divinium"]

    mob_desc_goblin = "You can just stretch the word \"humanoid\" to cover Goblins, if you're feeling generous.  Short, stocky, fugly, green, and nasty pretty much fills in the rest."
    mob_desc_imp = "Imps are nastly little demons, usually summoned to this plane by a nefarious magic user.  Though small and weak, imps are phenomenally quick and very difficult to hit."
    mob_desc_kobold = "Kobolds are a vile race of dimunitive lizard-men with mottled brownish-green scaly skin, dozens of small, sharp teeth.  They are not known for their intellectual or physical prowess, although in groups they can be dangerous (mostly due to their obnoxious odor)."
    mob_desc_ogre = "Ogres are gigantic humanoids, seven to nine feet tall and weighing up to eight hundred pounds.  Muscular and fat in roughly equal measure, they are deadly opponents in combat.  Luckily, they are rather slow."
    mob_desc_rat = "This rodent is definitely of an unusual size--you estimate it weighs at least twenty pounds.  Its red eyes stare at you with no trace of fear."
    mob_desc_wolf = "Your generic two-hundred-pound wolf.  Don't run; he can smell fear, and he's faster than you."

    mob_name_goblin = "goblin"
    mob_name_imp = "imp"
    mob_name_kobold = "kobold"
    mob_name_ogre = "ogre"
    mob_name_rat = "rat"
    mob_name_wolf = "wolf"
    
    mob_drinks = "%s drinks %s."  # ("The kobold", "a potion of might")
    mob_opens_door = "%s opens the door."  # ("The kobold")

    msg_done_resting = "Done resting."
    msg_feature_here = "There is a %s here."  # ("down staircase")
    msg_item_here = "You see %s lying here."  # ("a sword")
    msg_resting = "Resting..."
    msg_several_items_here = "There are several things lying here."
    msg_stop_resting_enemy = "You see an enemy and stop resting."
    msg_you_die = "^R^You die."
    msg_you_equip = "You equip %s."  # ("the sword")
    msg_you_feel_improved = "^G^You feel %s!"  # ("smarter")
    msg_you_gain_effect = "You gain %s."  # ("+2 strength")
    msg_you_gain_level = "Welcome to level ^G^%s^0^!"  # (7)
    msg_you_unequip = "You unequip %s."  # ("the sword")
    msg_you_wield = "You are now wielding %s."  # ("a sword")
    
    prompt_any_key = "[Press any key]"
    prompt_choose_item = "Choose an item"
    prompt_choose_location = "Choose a location"
    prompt_choose_spell = "Cast which spell? (Type shortcut or <enter>=last, ?=list, space=cancel): "
    prompt_choose_spell2 = "Cast which spell? (space to cancel)"
    prompt_choose_target = "Select a target"
    prompt_choose_target2 = "Choose a target: <enter>=%s, <tab>=cycle, <space>=cancel."  # ("the kobold")
    prompt_describe_which_item = "View description for which item? "
    prompt_drop = "Drop which item?"
    prompt_drop_howmany = "Drop how many?"
    prompt_enter_to_target = "Press enter to target %s, or space to cancel."  # ("the kobold")
    prompt_enter_select_space_cancel = "Enter to select, Space to cancel"
    prompt_examine = "Examine which item?"
    prompt_harmful_spell_at_self = "Really cast %s on yourself?"  # ("magic missile")
    prompt_menu_default = "Choose an option $opts$: "  # $opts$ is replaced with the list of valid keys
    prompt_more = "[more]"
    prompt_pickup = "Pick up the %s?"  # ("sword")
    prompt_pickup_howmany = "Pick up how many %s?"  # ("wooden arrows")
    prompt_player_god = "Which god will you follow, %s?"  # (John)
    prompt_player_name = "What is your name, adventurer? "
    prompt_player_race = "Choose your race, %s:"  # (John)
    prompt_quaff = "Quaff which potion?"
    prompt_quit = "Really quit the game?"
    prompt_read = "Read which scroll?"
    prompt_remove_which = "Remove which item?"
    prompt_unwear = "Unequip which item?"
    prompt_wear = "Equip which item?"
    prompt_which_ammo = "Fire which ammunition?"
    prompt_which_direction = "Which direction? [1-9, or space to cancel]"
    prompt_wield = "Wield/unwield which item?"
    
    # The list of quality adjectives for armor, from worst to best:
    quality_armor = ["tattered", "decrepit", "shabby", "worn", "sturdy", "strong", "formidable", "impenetrable"]
    
    spellcode_agility = "agi"
    spellcode_magic_missile = "mis"
    
    spelldesc_agility = "Improves the caster's hand-eye coordination for a brief time."
    spelldesc_magic_missile = "A small bolt of arcane energy leaps from the caster's finger and strikes the target.  The damage is light, but cannot be resisted."
    
    spellname_agility = "Agility"
    spellname_magic_missile = "Magic Missile"
    
    stat_abbr_dex = "dex"
    stat_abbr_estr = "eSTR"
    stat_abbr_int = "int"
    stat_abbr_str = "str"
    stat_key_dex = "d"  # The key used to select dexterity when asked which stat to improve
    stat_key_int = "i"  # The key used to select intellect when asked which stat to improve
    stat_key_str = "s"  # The key used to select strength when asked which stat to improve
    stat_name_dex = "Dexterity"
    stat_name_estr = "Excess Strength"
    stat_name_int = "Intellect"
    stat_name_str = "Strength"

    verbs_bite = ["nibbles at", "bites", "chomps"]
    verbs_bite_2p = ["nibble at", "bite", "chomp"]
    verbs_bludgeon = ["swings at", "clubs", "bludgeons"]
    verbs_bludgeon_2p = ["swing at", "club", "bludgeon"]
    verbs_chop = ["hacks at", "chops", "cleaves"]
    verbs_chop_2p = ["hack at", "chop", "cleave"]
    verbs_claw = ["scratches at", "claws", "rends"]
    verbs_claw_2p = ["scratch at", "claw", "rend"]
    verbs_default_attack = ["attacks", "hits", "whacks"]
    verbs_default_attack_2p = ["attack", "hit", "whack"]
    verbs_lash = ["lashes at", "whips", "scourges"]
    verbs_lash_2p = ["lash at", "whip", "scourge"]
    verbs_punch = ["swings at", "punches", "clocks"]
    verbs_punch_2p = ["swing at", "punch", "clock"]
    verbs_slash = ["swings at", "slashes", "slices"]
    verbs_slash_2p = ["swing at", "slash", "slice"]
    verbs_stab = ["pokes at", "stabs", "impales"]
    verbs_stab_2p = ["poke at", "stab", "impale"]

    word_agiler = "more agile"
    word_blocked = "blocked"  # As in, no line of sight exists while targeting
    word_bludgeon = "bludgeon"
    word_chop = "chop"
    word_dungeonlevel_abbr = "DLvl"
    word_evasion = "evasion"
    word_evasion_abbr = "ev"  # Two letters
    word_hitpoints_abbr = "hp"
    word_hits = "hits"
    word_lash = "lash"
    word_level_abbr = "lvl"  #As in, character is level 9
    word_mana_abbr = "mp"
    word_no = "no"
    word_no_key = "n"
    word_none = "none"
    word_or = "or"
    word_protection = "protection"
    word_protection_abbr = "pr"  # Two letters
    word_punch = "punch"
    word_slash = "slash"  # As in to slash an enemy with a sword, not the '/' key.
    word_space = "space"  # As in spacebar key
    word_stab = "stab"
    word_slightly = "slightly"
    word_smarter = "smarter"
    word_stronger = "stronger"
    word_target = "target"
    word_yes = "yes"
    word_yes_key = "y"

    you_ascend_stairs = "You ascend the stairs."
    you_close_door = "You close the door."
    you_descend_stairs = "You descend the stairs."
    you_drink = "You drink %s."  # ("a potion of might")
    you_open_door = "You open the door."
    you_drop_item = "You drop %s."  # ("the potion")
    you_pick_up_item = "You pick up %s (%s)."  # ("the potion", "b")
    you_unequip_and_drop_item = "You unequip and drop %s."  # ("the sword")
    
    def ArticleName(self, article, item):
        # TODO: Generalize this to other languages.
        try:
            if item.quantity > 1:
                qstr = "%sx " % item.quantity
                return "%s%s" % (qstr, item.Name())
        except AttributeError: pass
        try:
            unique = item.unique
        except AttributeError:
            unique = False
        if unique: return item.name
        else: return "%s %s" % (article, item.Name())

# Set the language to use:    
lang = English()