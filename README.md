# DungLang v0.7 prototype / patched demo 🦍🔥🪨

> Stench-driven programming language. UUHO.
> # DungLang

DungLang is an experimental Python prototype for modeling causality, side effects, and responsibility in a small symbolic language.

It asks a simple question: what if a language could record effects without blaming the type system?

---

## Modules Added in v0.7

| Module | Overview |
|---|---|
| § 1 Axiom Collapse | The most catastrophic exception in the universe — occurs only when the Philosophy Gorilla philosophizes its own fart |
| § 2 Diplomacy Module | Tracks cross-border stench as `CrossBorderStench<source_tribe, target_tribe, concentration>`. Banana reparations triggered on treaty violations |
| § 3 Cognitive GC | Receiving 3+ bananas causes complete memory erasure |
| § 4 Blame-Shifting Engine | `try: stench incident / catch: three bananas / result: it never happened` |

---

## Known Bugs (v0.7 original) → Fixed in patched

### Bug #001 — Wrong treaty table lookup in diplomatic ruling
**Introduced in:** v0.7 original  
**Fixed in:** v0.7 patched

**Cause:**  
`diplomatic_ruling()` was fetching the treaty value like this:

```python
# ❌ v0.7 original (buggy)
treaty_val = inter_tribal_treaty.get(
    ("Philosophy Gorilla Federation", "*"),       # ← this key always exists, so…
    inter_tribal_treaty.get((self.source_tribe, self.target_tribe), 4)
)
# Result: treaty_val was always 0, turning every case into a diplomatic incident
```

`dict.get(key, default)` only uses `default` when the key **does not exist**.
`("Philosophy Gorilla Federation", "*")` is registered in the dict, so it always hits,
returning `0` every time.

**Fix:**

```python
# ✅ v0.7 patched (fixed)
if "Philosophy Gorilla" in self.source_tribe:
    return diplomatic_incident(self)       # Phil. Gorilla is rejected by name first

treaty_val = inter_tribal_treaty.get((self.source_tribe, self.target_tribe), 4)
if self.concentration > treaty_val:
    return diplomatic_incident(self)
else:
    return blame_the_weather_gorilla(self)
```

Behavior:
- Source contains "Philosophy Gorilla" → always a diplomatic incident
- Otherwise → looks up `inter_tribal_treaty[(source_tribe, target_tribe)]`, default 4 if undefined
- concentration > treaty_val → diplomatic incident / concentration ≤ treaty_val → Weather Gorilla's fault

---

### Bug #002 — Side effect level not computed during parsing
**Introduced in:** v0.7 original  
**Fixed in:** v0.7 patched

**Cause:**  
In `parse()`, when a `side_effect` token arrived while in `observing` mode,
the `elif mode == "observing": phenomenon[t.kind] = t.value` branch matched first,
storing the raw string (e.g. `phenomenon["side_effect"] = "💨💨"`).
The logic that counts the number of 💨 characters was never reached.

**Fix:**  
Process the `side_effect` token before the mode check:

```python
# ✅ v0.7 patched
elif t.kind == "side_effect":
    phenomenon["side_effect_level"] = t.value.count("💨")   # Processed first, regardless of mode
elif mode == "observing":
    phenomenon[t.kind] = t.value
```

---

## How to Run

```bash
python dunglang_v0_7_patched_en.py
```

Or check `run_en.log` for pre-captured output.

---

## Execution Summary (patched)

| Case | Concentration | Treaty Value | Expected | Patched Result |
|---|---|---|---|---|
| Case A (Uuho Tribe→Banana Tribe, conc. 7) | 7 | 3 | Diplomatic incident | ✅ Diplomatic incident |
| Case B (Uuho Tribe→Banana Tribe, conc. 2) | 2 | 3 | Weather Gorilla's fault | ✅ Weather Gorilla's fault |

---

## File Structure

```
dunglang_v0_7_patched_en.py   Main implementation
README_v0_7_patched_en.md     This file
run_en.log                    Pre-captured execution log
```

---

> Warning: Stench-safety has surpassed type-safety  
> Note: Truth has been thoroughly bent by side effects and bananas  
> UUHO 🦍


---

## License

MIT License. See [LICENSE](./LICENSE).

## Author Note

Please don’t alter the 🪨 and 🦍 symbols; they are part of the project’s identity.
