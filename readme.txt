LICENSE
-------
Pyro is distributed under the MIT open source license.  The full license is contained in pyro-license.txt.


RUNNING PYRO (WINDOWS BINARY)
-----------------------------
Run pyro.exe.  Press '?' for in-game help.


RUNNING PYRO (PYTHON SOURCE)
----------------------------
Short version: Run pyro.py.

Longer version: Pyro requires Python 2.3 or higher installed on your system.  Pyro uses curses for input/output.  Curses is included with Python by default, except on Windows systems.  For Windows users, Pyro works with the WCurses module (http://adamv.com/dev/python/curses/), and *should* work with other ncurses-compliant modules if they are available for import as 'curses'.

Pyro will automatically make use of Psyco (a sort of JIT compiler for Python) if it is available.  (http://psyco.sourceforge.net/)  Psyco is entirely optional.  Pyro runs about four times faster if Psyco is available.


QUICK-START GUIDE
-----------------
Here are a few tips and bits of information on mechanics and gameplay:

- The goal of the game is to decend to the bottom of the dungeon, get the widget, and return alive.  It is not known exactly how deep the dungeon is.
- Items in the player's inventory only weigh 5% of their normal weight.  When equipped, items once again have their full weight.  This makes the STRENGTH stat extremely important for any character who wants to equip heavy items (big weapons, heavy armor).
- Strength affects your carrying limit, damage in melee combat, number of hit points, and (along with Dexterity) your evasion bonus.  (If you are equipping less weight than your strength can bear, you are more evasive in combat.)
- Dexterity affects your chance to hit in melee and ranged combat, your evasion bonus, and your thief-type skills (stealth, picking locks, disarming traps).
- Intelligence affects your chance to successfully cast spells, and modifies the effectiveness of some spells. 
- Strength is the only limit on which items can be equipped.  If you have a Wizard who has managed to get a decent strength, go ahead and equip that nasty two-hand sword or hefty chain shirt.  There are no armor penalties to magic use or thief-type skills.
- Equipped armor blocks some incoming damage, but can lower your evasion bonus.  The optimal trade-off between more armor and more evasion will depend on your character's strength and dexterity values.


DETAILED GAMEPLAY MECHANICS
---------------------------
For those who want to know everything, here are the details.  Especially during alpha development, this information may not be 100% accurate.  When in doubt, check the source code.

CHARACTER TYPES
---------------
The character types differ in their starting stats, pattern of stat growth with level, starting items, and special abilities granted.

STATS
-----
There are only three stats: STR, DEX, INT.  Strength is overall physical beefiness.  Strength indicates physical power, and also includes attributes sometimes covered under "constitution", "stamina", or "endurance" in other games.  Dexterity measures the speed and accuracy of physical movements.  Intelligence is mental acuity and alertness.

STRENGTH
- Modifies melee damage by +1 for each point of STR over 8, or -1 for each point below 8.
- Hit points gained per level: STR / 2
- HP regenerates at a rate of 1 per X turns resting, where X is 30 - STR.
- Carrying capacity is 1 stone per point of STR.
- "Excess strength" (eSTR) is the amount of EXTRA strength you have, above what is required to carry all of your items.  If you have a 14 STR and are carrying 9.1 stones of items, you have an eSTR of 4, since a character needs 10 STR to carry 9.1 stones.  

DEXTERITY
- Modifies melee and missile hit rolls by +1 for each point of DEX over 8, or -1 for each point below 8.
- Modifies evasion rolls by +1 per point of DEX above 8, or -1 per point below 8.  However, the evasion bonus for DEX is also tied to eSTR: the lower of the two numbers is used.  If a Jack has a 17 DEX, then he gains a +9 bonus to evasion, IF he has at least 9 eSTR.  If he only has 5 eSTR, then his evasion bonus is only +5.  Thus, heavier armor can lower the evasion score, but stronger characters can wear more armor without becoming encumbered.

INTELLIGENCE
- Modifies spell failure chance.  Pure casters begin the game with a high enough INT to avoid spell failure completely, but the failure chance is important for hybrid characters dabbling in spellcasting.  The failure rate is 25% per point of INT below 10.
- Modifies the effectiveness of some spells. 
- Magic points gained per level: 0.5 per point of INT above 6.
- Magic item use: failure rate is 25% per point of INT below 8.

						Spell		Item Use
INT			MP/level	Success		Success		Note
----------------------------------------------------------------------------------
4 or less	0			0%			0%			No magic use whatsoever--ouch!
5			0			0%			25%			Lowest INT to use magic items
6			0			0%			50%
7			0.5			25%			75%			Lowest INT to cast spells
8			1			50%			100%		No item use failure
9			1.5			75%			100%
10			2			100%		100%		No spell failure
11			2.5			100%		100%
12			3			100%		100%
13			3.5			100%		100%
14			4			100%		100%
15			4.5			100%		100%
16			5			100%		100%
17			5.5			100%		100%
18			6			100%		100%
19			6.5			100%		100%
20			7			100%		100%

STAT GAIN - At every even level (2, 4, 6, etc.) the player improves one stat.  The stat may be STR, DEX, INT, or the player's choice.  Each character type has its own stat improvement pattern, which repeats over and over as the player gains levels:

Warrior - STR, DEX, (any), STR
Treasure Hunter - DEX, (any), STR, (any), INT, (any)
Wizard - INT, (any), INT
Enchanter - INT, (any)
Berserker - STR, DEX, (any), STR, DEX
Assassin - DEX, (any), DEX, STR

As a stat becomes higher, it is harder to increase it further.  It may take two or three improvements to achieve a one-point increase in the stat, according to its current value:

Current 			Improvements needed 
Value				to increase to next value
---------------------------------------------
 1 to 12				1
13 to 16				2
17 to 20				3
21 to 24				4


ARMOR
-----
Equipping armor has at least two effects: your protection against physical damage is increased (good), and your freedom of movement may be decreased, making you easier to hit (not so good).  The decrease in evasion is explained in the STATS section above.  Here are the details on damage absorption:

Each piece of armor has an armor point rating (AP).  The AP of every piece of equipped armor is added together and divided by 10 to get your protection value (PV).  Your PV is subtracted from all incoming physical damage.  Note that your PV might not be a whole number, in which case you have a chance to absorb an additional point of damage.  For example, say your PV is 3.7, then you always absorb at least 3 poins of damage.  Additionally 70% of the time, you'll abosorb an extra point, for a total of 4.  Thus, the average over many attacks will nearly equal the true value of 3.7.
