# DrumLights: sourcing, platform options and business case

Prices are USD, checked on 2026-11-08 through the pcbparts MCP (live Mouser/DigiKey/JLC data) unless marked **(est.)**.
Market, competitor and third-party board figures come from web searches. They are indicative and **unverified**; confirm them before quoting them to anyone.

## 1. Fixes found while sourcing the missing parts

| Ref | Problem | Action |
| --- | --- | --- |
| C2, C3 | `F981A475MMA` tantalum was **Obsolete** at Mouser | **Done:** now `CL10A475KO8NNNC` (4.7 µF 16 V X5R 0603, LCSC C19666, JLC basic, 3.85 M in stock; Mouser stock was 0 on 2026-11-08, with the 6.3 V `CL10A475KQ8NNNC` in stock as a fallback only for sub-5 V use). The footprint is unchanged. Check DC-bias derating on the 5 V and BATT rails. |
| D2 | `MBR120VLSFT3G` is stocked (Mouser 738, $0.40 at 100) but not on JLC | Keep it. Alternative: `SS14-E3/61T` (40 V 1 A, Mouser 249k in stock). It is SMA, so it needs a new footprint. |
| D3 | `LRTB GFTM` is not found at Mouser or DigiKey | Pick a stocked RGB PLCC-6 and match its pinout to the D3 footprint. JLC lists only a PLCC-4 CREE part. **Open item.** |
| U1 | `TLV2771CDBVR` is stocked at Mouser (6073 in stock; $2.34 at 1, $1.54 at 100) | OK. The I-grade `TLV2771IDBVR` is the JLC route (LCSC C130906). |
| RV1 | `3339P-1-103LF` costs $3.70 at 100 | The most expensive passive on the board. Consider a ~$0.30 SMD trimmer. |
| SW1 | `IKD0103101` had 0 stock at Mouser and a 1300-piece minimum at DigiKey | **Done:** now Nidec/Copal `CHS-01TB` (SMD gull-wing slide switch, Mouser 9346 in stock, $0.78 at 100; LCSC C2680613). It is the same Copal CHS family as the existing footprint, but check the pad span against the datasheet before ordering boards. |

## 2. Shield BOM cost (Nano shield only, no MCU board)

| Qty | Parts as designed | + PCB (est.) | + assembly (est.) | Optimised BOM (est.)* |
| --- | --- | --- | --- | --- |
| 1 | $20.66 | $26.66 | n/a (hand build) | $18.21 |
| 100 | $13.17 | $13.77 | **$15.27** | **$8.68** |
| 1000 | $9.85 | $10.10 | **$10.70** | **$6.02** |

\* "Optimised" replaces RV1 and SW1 with ~$0.45 of parts (SMD trimmer plus a solder jumper or tiny switch) and keeps everything else.

Qty-100 line items: 3× BSS306N $0.91, TLV2771 $1.54, MCP73831 $0.75, MBR120 $0.40, Molex Nano-Fit $1.30, RV1 $3.70, SW1 $3.34, JST ×2 $0.17, sockets $0.50 (est.), RGB LED $0.40 (est.), passives $0.12.
Mouser price breaks are real. Sockets, the RGB LED, the PCB and the assembly are estimates.

## 3. Platform options and per-node price matrix (qty 100)

Node cost is the MCU board plus the shield, excluding the LED strip, battery, piezo and enclosure.

| Option | MCU board price | Drop-in on the current shield? | Node, shield as designed | Node, shield optimised | Notes |
| --- | --- | --- | --- | --- | --- |
| Nano clone (ATmega328P) | $2–5 | Yes | ~$18 | ~$12 | Current firmware. 5 V logic, no wireless. |
| Arduino Nano Every | $10–14 | Yes | ~$27 | ~$21 | Official, same pinout. The firmware needs a quick test. |
| Arduino Nano ESP32 (S3) | $18–22 | Yes | ~$35 | ~$29 | Compiles today. Gives WiFi/BLE and ESP-NOW for fleet control, but it is the most expensive. |
| "ESP32-S3-Nano" clone | ~$8–10 (est.) | Pinout must be checked | ~$24 | ~$18 | Cheapest route to wireless on a socket, but clone pinouts vary. |
| Blue Pill (STM32F103) | $3–5 | **No.** Different pinout, 3.3 V | needs a new carrier | ~$13 | No wireless. Old part. |
| Black Pill (STM32F411) | $15–20 retail, much less in China (est.) | **No** | needs a new carrier | ~$17+ | Overkill for a piezo and a PWM. |
| RISC-V CH32V003/V203 | $1–3.5 | **No** | needs a new carrier | ~$10 | Cheapest, but no wireless and a thin Arduino ecosystem. |
| ESP32-C3/C6 module on the board (RISC-V + WiFi/BLE) | module ~$2 (est.) | Replaces the socket | n/a | **~$12** | Best cost per wireless node. Needs a new PCB (USB-C, LDO, antenna keep-out). |

Blue Pill and Black Pill are not Arduino Nano pinout or footprint. They would need a new board, so they only make sense if the shield is redesigned.

### Recommended direction

1. **Now:** keep the Nano-compatible shield and sell it with the cheapest socket-compatible MCU. Fix C2/C3, SW1 and RV1, and pick the D3 part (section 1).
2. **Fleet product (v2):** a single PCB with an **ESP32-C3 or C6 module on board** (RISC-V, ESP-NOW, USB-C). Target a node cost of about $12 at 100 pieces. This is what the fleet-control roadmap issue needs, and it gives the lowest cost per wireless node.
3. **Skip** Blue Pill, Black Pill and CH32V for now: no wireless, no Nano drop-in, and a weaker Arduino toolchain.

## 4. Market sizing (assumptions to validate)

Group sizes from web searches:

| Group type | Players |
| --- | --- |
| Rio samba school bateria | ~60–320, typically 200–300 |
| Australian community samba or parade band (e.g. Adelaide Fringe) | ~15–50 |
| Marching drumline | ~8–30 |

Rough sizing (est., to be validated with surveys of groups):

| Segment | Assumption | Drums that could carry a node |
| --- | --- | --- |
| Local community samba and drum groups, Australia | ~100 groups × ~25 players | ~2,500 |
| Same worldwide | ~5,000 groups × ~25 players | ~125,000 |
| Rio and other big carnival schools | ~100 schools × ~250 players | ~25,000 |
| Backline and kit drummers | millions of players, but they buy kit lighting kits, not per-drum nodes | different product |

A **realistic serviceable market** is the parade, festival and community-band niche. A 20-drum band is a ~$800 sale at the prices below. At 1% of the community-group segment (about 50 bands), that is roughly **$40k revenue**, so this is a hobby-scale business or a side-product, not a venture-scale one.

Context: the percussion instruments market is quoted at roughly $1–6 B, with large variation between report providers. It is not useful for sizing this niche.

## 5. Competing products

| Product | Typical price | Notes |
| --- | --- | --- |
| Drumlite and similar LED drum kits | $120–$300 per 5-drum kit, about $24–60 per drum | Built for drum kits. Not designed for hit-reactive, battery-powered hand-held or strap-on parade drums. |
| Lightning Drums (custom lit drums) | $150–$400+ | Custom builds. |
| Generic marketplace LED strips | under $100 | No hit detection. |
| Open-source piezo or LED projects | DIY | See the README. They require build skills. |

The differentiator is **per-drum, hit-reactive lighting that runs on a battery for parades and is open-source and hackable**, with synchronised fleet control planned.

## 6. TCO (per drum, 20-drum band)

| Item | Cost (est.) |
| --- | --- |
| Node (shield and MCU) | $12–$29 |
| LED strip (1–2 m), 18650 cell, enclosure, piezo, cables | $15–$25 |
| Build or assembly labour (if DIY, 30–60 min) | $0 DIY, $10–$20 outsourced |
| Landed cost per drum | **$30–$60** |
| 20 drums | **$600–$1,200** |
| Running costs | battery replacement every 2–3 years and strip repair, ~$5 per drum per year |

## 7. Pricing approaches

| Approach | Logic | Price per node |
| --- | --- | --- |
| **Cost-plus** | Landed cost × 2.5–3 to cover Tindie fees (~8% with payments), support, returns and warranty. At a node cost of $12 (ESP32 on board) that gives $30–$36. At $29 (Nano ESP32) it gives $70–$85. | $30–$85 |
| **Competitor-anchored** | Drumlite-class kits cost $24–$60 per drum. A hit-reactive battery node must be within or slightly above that range. | $35–$55 |
| **Value-based** | A parade band values lit drums for visibility and a brand-defining show. Willingness to pay is higher for a band that performs at festivals (fees and sponsorships). | $45–$70 per node, with the fleet controller or app as an upsell |

**Suggested starting prices (to test on Tindie):**
- Bare PCB or kit (current Nano shield): $12–$18.
- Assembled Nano shield (MCU board not included): $25–$30.
- Assembled ESP32 fleet node (v2): **$39–$49**, with a **5-pack at about $180** (~$36 each) and a 10-node band bundle.
- Fleet controller or ESP-NOW remote: $20–$25.

At $40 with a $12–$15 cost, the gross margin is about 60–65% before Tindie and payment fees (about 8%), shipping and support time.

## 8. Next steps

1. ~~Replace C2/C3~~ Done (`CL10A475KO8NNNC`).
2. SW1 is done (`CHS-01TB`). Replace RV1 with a cheaper stocked part. Pick and verify an RGB PLCC-6 for D3.
3. Validate the market numbers: survey 10 local bands about drum count, willingness to pay and battery or runtime needs.
4. Prototype the ESP32-C3/C6 on-board fleet node (link to the ESP-NOW roadmap issue #9).
