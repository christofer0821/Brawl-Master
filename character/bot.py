import random
from config import MAX_ENERGY

def update_bot(bot, player, now, cooldown, level):
    # === Damage scaling per level ===
    bot_damage = {
        "Jab": 10 + (level - 1) * 5,
        "Kick": 10 + (level - 1) * 5,
        "Special": 20 + (level - 1) * 5,
        "Block_Reduction": 5,
        "Energy_Gain": 20
    }

    distance = abs(bot["x"] - player["x"])

    # Initialize walk timer if not present
    if "walk_timer" not in bot:
        bot["walk_timer"] = 0

    # === Movement toward player ===
    if distance > 100:
        direction = -4 if bot["x"] > player["x"] else 4
        bot["x"] += direction

        # Set to Walk state only once
        if bot["state"] != "Walk":
            bot["state"] = "Walk"
            bot["frames"] = bot["anims"]["Walk"]
            bot["frame"] = 0
            bot["walk_timer"] = now
        else:
            # Advance frame every 120ms (adjust speed here)
            if now - bot["walk_timer"] >= 150:
                bot["frame"] = (bot["frame"] + 1) % len(bot["frames"])
                bot["walk_timer"] = now

    # === Attack logic ===
    elif now - bot.get("last_attack", 0) > cooldown:
        if bot["energy"] == MAX_ENERGY and "Special" in bot["anims"]:
            bot["state"] = "Special"
            bot["frames"] = bot["anims"]["Special"]
            bot["frame"] = 0
            bot["energy"] = 0
        else:
            move = random.choice(["Jab", "Kick"])
            bot["state"] = move
            bot["frames"] = bot["anims"][move]
            bot["frame"] = 0
        bot["last_attack"] = now

    return bot, bot_damage
