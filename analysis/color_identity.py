# analysis/color_identity.py
# Stage 7 — Map energy + valence to a color identity

def get_color_identity(metrics):
    """
    Uses average energy and valence to assign a color.

    Think of it like a mood map:

         High Valence (happy)
               │
     Green     │     Yellow
    (calm+joy) │  (energetic+joy)
               │
    ───────────┼─────────────── Energy
    low        │           high
               │
      Blue     │      Red
    (calm+sad) │  (intense+sad)
               │
         Low Valence (moody)
    """

    energy  = metrics["avg_energy"]
    valence = metrics["avg_valence"]

    # The threshold is 0.5 — above it is "high", below is "low"
    HIGH = 0.5

    if energy >= HIGH and valence >= HIGH:
        color   = "Yellow"
        meaning = "Energetic and positive — you listen to music that lifts you up!"
        emoji   = "🟡"

    elif energy >= HIGH and valence < HIGH:
        color   = "Red"
        meaning = "Intense and moody — you like music with power and edge."
        emoji   = "🔴"

    elif energy < HIGH and valence >= HIGH:
        color   = "Green"
        meaning = "Calm and joyful — you gravitate toward feel-good, relaxed music."
        emoji   = "🟢"

    else:
        color   = "Blue"
        meaning = "Calm and introspective — you like deep, moody, thoughtful music."
        emoji   = "🔵"

    # Build the result dictionary
    result = {
        "color"  : color,
        "meaning": meaning,
        "emoji"  : emoji,
        "energy" : round(energy, 3),
        "valence": round(valence, 3)
    }

    # Print it nicely
    print("\n" + "=" * 55)
    print("   Stage 7 — Your Color Identity")
    print("=" * 55)
    print(f"\n  {emoji}  Your Color is: {color}")
    print(f"\n  What it means:")
    print(f"  {meaning}")
    print(f"\n  Based on:")
    print(f"   Energy  : {energy:.3f}  ({'high' if energy >= HIGH else 'low'})")
    print(f"   Valence : {valence:.3f}  ({'high' if valence >= HIGH else 'low'})")
    print("=" * 55)

    return result 
