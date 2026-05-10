 
# analysis/animal_personality.py
# Stage 8 — Assign an animal based on listening behavior

def get_animal_personality(metrics):
    """
    Uses replay ratio, exploration score and energy
    to assign an animal that represents how you listen.

    The logic works like a decision tree:

    High replay + Low exploration  → Panda   (comfort listener)
    High replay + High exploration → Fox     (curious repeater)
    High energy + Low replay       → Tiger   (intense explorer)
    Low energy  + Low exploration  → Turtle  (calm and focused)
    Balanced everything            → Dolphin (well rounded)
    """

    energy      = metrics["avg_energy"]
    replay      = metrics["replay_ratio"]
    exploration = metrics["exploration_score"]

    HIGH_ENERGY = 0.5
    HIGH_REPLAY = 0.5
    HIGH_EXPLORE = 0.6

    # Decision tree — checks conditions in order
    if replay >= HIGH_REPLAY and exploration < HIGH_EXPLORE:
        animal  = "Panda"
        emoji   = "🐼"
        meaning = (
            "You are a comfort listener. You find songs you love "
            "and replay them on repeat. Your playlist is your safe space."
        )

    elif replay >= HIGH_REPLAY and exploration >= HIGH_EXPLORE:
        animal  = "Fox"
        emoji   = "🦊"
        meaning = (
            "You are a curious repeater. You explore lots of different "
            "artists but when you find a song you love, you play it "
            "over and over. Smart and passionate!"
        )

    elif energy >= HIGH_ENERGY and replay < HIGH_REPLAY:
        animal  = "Tiger"
        emoji   = "🐯"
        meaning = (
            "You are an intense explorer. High energy music, always "
            "moving to the next track. You listen with full focus and power."
        )

    elif energy < HIGH_ENERGY and exploration < HIGH_EXPLORE:
        animal  = "Turtle"
        emoji   = "🐢"
        meaning = (
            "You are a calm and focused listener. Low energy music, "
            "a small set of favourite artists. Steady and content."
        )

    else:
        animal  = "Dolphin"
        emoji   = "🐬"
        meaning = (
            "You are a balanced listener. Good mix of energy and calm, "
            "exploration and comfort. Adaptable and in tune with your moods."
        )

    result = {
        "animal" : animal,
        "emoji"  : emoji,
        "meaning": meaning
    }

    # Print nicely
    print("\n" + "=" * 55)
    print("   Stage 8 — Your Animal Personality")
    print("=" * 55)
    print(f"\n  {emoji}  Your Animal is: {animal}")
    print(f"\n  What it means:")

    # Print meaning wrapped at 50 chars for clean display
    words    = meaning.split()
    line     = "  "
    for word in words:
        if len(line) + len(word) > 52:
            print(line)
            line = "  " + word + " "
        else:
            line += word + " "
    print(line)

    print(f"\n  Based on:")
    print(f"   Replay Ratio      : {replay:.2f}")
    print(f"   Exploration Score : {exploration:.2f}")
    print(f"   Average Energy    : {energy:.3f}")
    print("=" * 55)

    return result