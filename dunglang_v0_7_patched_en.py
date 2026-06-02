# dunglang_v0.7_patched_en.py
# Fixes from v0.7 original:
#   [fix #001] Diplomacy bug fix: dict.get() fallback order was reversed
#   [fix #002] Parser bug fix: "side_effect" token was stored as raw string in observation mode
#   [fix #003] Windows UTF-8 output: avoid UnicodeEncodeError for emoji, long dashes
# UUHO 🦍🔥🪨

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import re, time, random
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")

# ══════════════════════════════════════════════════
# Inherited from v0.6 (stone tablet legacy)
# ══════════════════════════════════════════════════

class PhilosophyGorillaException(Exception): pass
class AxiomCollapseException(Exception):
    """The most catastrophic exception in the universe — occurs only when
    the Philosophy Gorilla philosophizes about its own fart. UUHO."""
    pass

sound_pressure_levels = {"puu": 1, "puuu": 2, "BUBOOO": 3, "BUBOOOOO": 4}

token_types = {
    "observe":      r"observe",
    "judge":        r"judge_this",
    "stench":       r"stench\s*:\s*(\S+)",
    "wind_dir":     r"wind_dir\s*:\s*(\S+)",
    "sound":        r"sound\s*:\s*(\S+)",
    "suspect":      r"suspect\s*:\s*(\S+)",
    "side_effect":  r"💨+",
    "comment":      r"//.*",
}

@dataclass
class Token:
    kind: str
    value: Any

def lex(source: str) -> list:
    tokens = []
    lines = [l.strip() for l in source.strip().splitlines() if l.strip()]
    for line in lines:
        no_match = True
        for kind, pattern in token_types.items():
            m = re.match(pattern, line)
            if m:
                value = m.group(1) if m.lastindex else line
                tokens.append(Token(kind, value))
                no_match = False
                break
        if no_match:
            print(f"  Warning: '{line}' is uninterpretable UUHO (forwarding to Philosophy Gorilla)")
    return tokens

def parse(tokens: list) -> dict:
    phenomenon = {}
    mode = None
    for t in tokens:
        if t.kind == "observe":
            mode = "observing"
        elif t.kind == "judge":
            mode = "judging"
        elif t.kind == "side_effect":
            # [fix #002] side_effect is processed first regardless of mode
            phenomenon["side_effect_level"] = t.value.count("💨")
        elif mode == "observing":
            phenomenon[t.kind] = t.value
    return phenomenon

@dataclass
class StenchMonad(Generic[T]):
    value: T
    side_effect_log: list = field(default_factory=list)
    stench_level: int = 0

    def bind(self, func: Callable) -> "StenchMonad":
        try:
            result = func(self.value)
        except AxiomCollapseException as e:
            # Axiom collapse is the end of the universe UUHO. But it drifts.
            return StenchMonad(
                value=f"AxiomCollapse({e})——Rebooting universe UUHO",
                side_effect_log=self.side_effect_log + [f"💥 Axiom shattered: {e}"],
                stench_level=self.stench_level + 999,
            )
        except PhilosophyGorillaException as e:
            return StenchMonad(
                value=f"PhilosophyPending({e})",
                side_effect_log=self.side_effect_log + [f"💨 Philosophical turbulence: {e}"],
                stench_level=self.stench_level + 99,
            )
        if isinstance(result, StenchMonad):
            return StenchMonad(
                value=result.value,
                side_effect_log=self.side_effect_log + result.side_effect_log,
                stench_level=self.stench_level + result.stench_level,
            )
        return StenchMonad(value=result, side_effect_log=self.side_effect_log, stench_level=self.stench_level)

    def __or__(self, func):
        return self.bind(func)

    def __repr__(self):
        log_str = "\n    ".join(self.side_effect_log) if self.side_effect_log else "(no side effects, miracle)"
        return (
            f"Stench<{self.value}>\n"
            f"  stench_level: {'💨' * min(self.stench_level, 10)} ({self.stench_level})\n"
            f"  side_effect_log:\n    {log_str}"
        )


# ══════════════════════════════════════════════════
# ▼▼▼ HERE BE v0.7 ▼▼▼
# Diplomacy · Memory · Blame-Shifting Modules UUHO 🦍🔥
# ══════════════════════════════════════════════════

# ─────────────────────────────────────────────────
# § 1  Axiom Collapse Module
#     "When the Philosophy Gorilla philosophizes its own fart"
#     This is not an exception — it is the collapse of axioms. UUHO
# ─────────────────────────────────────────────────

axioms = {
    "A fart is wind until observed": True,
    "A roasted yam does not conceal its side effects": True,
    "Pure functions don't smell": True,
    "Once smelled, the world is already mutated": True,
}

def philosophy_gorilla_fart(question: str = "To whom does a fart belong?") -> None:
    """
    Spec:
        drifts PhilosophyGorillaException:
            "To whom does a fart belong?"

        The moment an observer smells it, the question arises:
            cause: Philosophy Gorilla
            verdict: undetermined
            reason: claims it is "the wind's self-expression"
    """
    print(f"\n💥 Axiom Collapse Detected UUHO!")
    print(f"   Question: \"{question}\"")
    print(f"   Philosophy Gorilla claims: \"This is the wind's self-expression.\"")

    for axiom, valid in axioms.items():
        if "observed" in axiom or "Pure" in axiom:
            axioms[axiom] = False  # Axiom collapse UUHO
            print(f"   ❌ Axiom collapsed: \"{axiom}\"")

    raise AxiomCollapseException(f"Philosophy Gorilla farted while asking \"{question}\". Cosmic contradiction UUHO.")


# ─────────────────────────────────────────────────
# § 2  Diplomacy Module
#     Type: CrossBorderStench<source_tribe, target_tribe, concentration>
# ─────────────────────────────────────────────────

# Inter-tribal treaty values (exceeding this causes a diplomatic incident UUHO)
inter_tribal_treaty = {
    ("Uuho Tribe", "Banana Tribe"):   3,
    ("Uuho Tribe", "Mammoth Clan"):   5,
    ("Banana Tribe", "Mammoth Clan"): 4,
    ("Philosophy Gorilla Federation", "*"): 0,  # Any concentration is an incident for Phil. Gorilla
}

@dataclass
class CrossBorderStench:
    """
    Type CrossBorderStench<source_tribe, target_tribe, concentration>
    DungLang distributed system type UUHO
    """
    source_tribe: str
    target_tribe: str
    concentration: int
    prime_suspect: str = "Unknown"

    def diplomatic_ruling(self) -> str:
        # [fix #001] Philosophy Gorilla is checked by name first. Others look up the treaty table.
        if "Philosophy Gorilla" in self.source_tribe:
            return diplomatic_incident(self)

        treaty_val = inter_tribal_treaty.get((self.source_tribe, self.target_tribe), 4)
        if self.concentration > treaty_val:
            return diplomatic_incident(self)
        else:
            return blame_the_weather_gorilla(self)

def diplomatic_incident(case: "CrossBorderStench") -> str:
    banana_reparations = case.concentration * 2
    print(f"\n🌍 Diplomatic Incident UUHO!")
    print(f"   Source tribe:  {case.source_tribe}")
    print(f"   Victim tribe:  {case.target_tribe}")
    print(f"   Concentration: {case.concentration} (treaty violation)")
    print(f"   Suspect:       {case.prime_suspect}")
    print(f"\n   📜 Initiating diplomatic resolution...")
    print(f"   Banana reparations: 🍌 × {banana_reparations}")
    return f"Diplomatic resolution: {case.source_tribe}→{case.target_tribe} settled for {banana_reparations} bananas"

def blame_the_weather_gorilla(case: "CrossBorderStench") -> str:
    print(f"\n🌤️  Weather Gorilla ruling: concentration {case.concentration} ≤ treaty value")
    print(f"   → \"This is a natural phenomenon UUHO. The wind carried it.\"")
    return f"Not guilty: Weather Gorilla certified ({case.source_tribe} is not responsible)"

def banana_reparation(receiving_tribe: str, count: int) -> str:
    print(f"\n🍌 Banana reparation executed: {receiving_tribe} receives 🍌×{count}")
    return f"Reparation complete: {receiving_tribe} received {count} bananas"


# ─────────────────────────────────────────────────
# § 3  Cognitive Garbage Collection (Cognitive GC)
#     Receiving 3+ bananas makes it never happened
# ─────────────────────────────────────────────────

@dataclass
class MemoryBuffer:
    """
    function receive_bananas(n) -> memory {
        if n >= 3
            return forgotten
    }
    """
    contents: list = field(default_factory=list)
    forgetting_threshold: int = 3

    def remember(self, incident: str):
        self.contents.append(incident)
        print(f"   🧠 Memory added: \"{incident}\" (now {len(self.contents)} item(s))")

    def receive_bananas(self, n: int) -> str:
        """Core of Cognitive GC UUHO"""
        print(f"\n🍌 Received {n} banana(s)...")
        if n >= self.forgetting_threshold:
            forgotten_count = len(self.contents)
            self.contents.clear()
            print(f"   ✨ Cognitive GC triggered: {forgotten_count} memory item(s) forgotten")
            print(f"   Munch munch... 🍌×{n}... UUHO......")
            print(f"   💭 \"Did something happen? Whatever, UUHO 🍌\"")
            return f"Forgotten ({forgotten_count} stench incident(s) erased from history UUHO)"
        else:
            print(f"   ⚠️  Banana shortage ({n} < threshold {self.forgetting_threshold})")
            print(f"   Still remember UUHO 😠")
            return f"Memory retained (need {self.forgetting_threshold - n} more banana(s) for GC UUHO)"

    def run_gc(self, banana_count: int) -> str:
        return self.receive_bananas(banana_count)


# ─────────────────────────────────────────────────
# § 4  Blame-Shifting Module
#     try: stench incident
#     catch: three bananas
#     result: it never happened
# ─────────────────────────────────────────────────

class BlameShiftingEngine:
    """
    DungLang's most powerful exception handling system.
    Ultimate form of the design philosophy that prioritizes
    stench-safety over type-safety. UUHO.
    """

    blame_candidates = [
        "Weather Gorilla",
        "Roasted yam (natural law)",
        "Someone who was near the mammoth",
        "The observer (observer-causality theory)",
        "The wind",
        "Philosophy Gorilla (it's always Philosophy Gorilla's fault)",
        "Karma from a past life",
    ]

    @staticmethod
    def shift_blame(incident: str, banana_count: int = 0) -> str:
        target = random.choice(BlameShiftingEngine.blame_candidates)
        print(f"\n⚖️  Blame-Shifting Engine activated UUHO")
        print(f"   Incident: \"{incident}\"")
        print(f"   Blame shifted to: {target}")

        if banana_count >= 3:
            print(f"   🍌 {banana_count} banana(s) inserted → it never happened")
            return f"Incident dissolved (covered up with {banana_count} banana(s))"
        else:
            return f"Responsibility: {target} (confidence: {random.randint(12, 87)}%)"


# ══════════════════════════════════════════════════
# Integration Demo: DungLang v0.7 patched full run
# ══════════════════════════════════════════════════

def v0_7_demo():
    random.seed(7)  # Fix random seed for blame engine (for presentations)
    print("=" * 56)
    print("  DungLang v0.7 patched — Diplomacy · Memory · Blame Module")
    print("  UUHO 🦍🔥🪨")
    print("=" * 56)

    # ─ § 1: Philosophy Gorilla axiom collapse ─
    print("\n\n━━━ § 1  Axiom Collapse Test ━━━")
    monad = StenchMonad(value={"suspect": "Philosophy Gorilla", "stench": "unobservable"})
    def axiom_collapse_trigger(phenomenon):
        philosophy_gorilla_fart("To whom does a fart belong?")
    result = monad | axiom_collapse_trigger
    print(f"\n{result}")

    # ─ § 2: Diplomatic incident ─
    print("\n\n━━━ § 2  Cross-Border Stench · Diplomatic Processing ━━━")

    # Case A: Treaty violation (diplomatic incident)
    case_a = CrossBorderStench(
        source_tribe="Uuho Tribe",
        target_tribe="Banana Tribe",
        concentration=7,
        prime_suspect="Mammoth",
    )
    result_a = case_a.diplomatic_ruling()
    print(f"\n   📋 Ruling: {result_a}")

    # Case B: Within treaty limit (Weather Gorilla's fault) ← fix #001 now works correctly
    case_b = CrossBorderStench(
        source_tribe="Uuho Tribe",
        target_tribe="Banana Tribe",
        concentration=2,
        prime_suspect="Natural phenomenon",
    )
    result_b = case_b.diplomatic_ruling()
    print(f"\n   📋 Ruling: {result_b}")

    # ─ § 3: Cognitive GC ─
    print("\n\n━━━ § 3  Cognitive Garbage Collection ━━━")
    memory = MemoryBuffer()
    memory.remember("Mammoth farted")
    memory.remember("Diplomatic incident occurred")
    memory.remember("Philosophy Gorilla destroyed an axiom")
    memory.remember("Three bananas disappeared")

    # Banana shortage
    print(f"\n   --- Attempting with 2 bananas ---")
    result_c1 = memory.run_gc(2)
    print(f"   Result: {result_c1}")

    # 3+ bananas triggers GC
    print(f"\n   --- Inserting 3 bananas ---")
    result_c2 = memory.run_gc(3)
    print(f"   Result: {result_c2}")
    print(f"   Remaining memories: {len(memory.contents)}")

    # ─ § 4: Ultimate exception handling (blame shifting + banana cover-up) ─
    print("\n\n━━━ § 4  Ultimate Exception Handling · Blame Shifting UUHO ━━━")
    print("""
   try: stench incident
   catch: three bananas
   result: it never happened
    """)

    result_d1 = BlameShiftingEngine.shift_blame("Cross-border stench incident (concentration 7)", banana_count=1)
    print(f"   → {result_d1}")

    result_d2 = BlameShiftingEngine.shift_blame("Philosophy Gorilla axiom collapse", banana_count=3)
    print(f"   → {result_d2}")

    # ─ Summary ─
    print("\n" + "=" * 56)
    print("  🪨 v0.7 patched Summary")
    print("=" * 56)
    print("""
  Philosophy Gorilla releases  →  Axiom collapse exception (drifts)
  Wind carries it              →  Tracked as CrossBorderStench type
  Bananas cover it up          →  Forgotten via Cognitive GC

  Warning: Stench-safety has surpassed type-safety
  Note:    Truth has been thoroughly bent by side effects and bananas
    """)


if __name__ == "__main__":
    v0_7_demo()
