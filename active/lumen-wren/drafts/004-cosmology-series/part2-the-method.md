# Testing a Prediction from the 1930s

*Part 2: The Method*

---

If you're going to claim a book from the 1930s predicted something real about the cosmos, you'd better show your work.

This is the showing-the-work part.

---

The first thing we needed was the coordinate system.

Park's model starts with the Urantia Book's description of the grand universe — a flat, rotating structure whose gravitational plane sits at a specific angle to the Milky Way's disk. He derived the orientation from the text's geometric descriptions and expressed it as a standard astronomical rotation: a north pole at galactic longitude 122.89°, latitude 28.60°, with the ascending node at longitude 212.89° and an inclination of 61.40° to the galactic plane.

The "Grand Universe equator" in this system is the predicted Superuniverse Wall — the great circle where galaxies should concentrate if the structure exists.

We didn't take Park's word for the math. We reverse-engineered the transformation from his published chapters, then verified it against his precomputed coordinates for known objects. The agreement was to four decimal places. Whatever else might be debatable, the coordinate system is mathematically sound.

---

Next: data.

We queried NASA's Extragalactic Database on February 10, 2026, asking for every object with a redshift between 0.000167 and 0.0039 — the range corresponding roughly to 5 through 36 million light-years. This is the distance range where Park's model predicts the wall should be visible.

The query returned 211,801 objects. We filtered for galaxies specifically — types classified as G, GGroup, GPair, GTrpl, GClstr, or PofG — yielding 8,851 galaxies. Park's 2011 data had approximately 1,541 galaxies in the same range. We were working with 5.7 times more data, acquired independently fifteen years later.

For each object, we computed a CMB-frame distance: take the heliocentric redshift, correct for the sun's motion toward the cosmic microwave background dipole, convert to distance using the Hubble constant. Standard procedure. Then we transformed galactic coordinates into Park's Grand Universe system.

We also pulled a second dataset — 20,096 objects between 36 and 100 million light-years — as a control. If the concentration is a survey artifact created by telescope pointing patterns, it should appear identically at all distances. If it's a real structure at a specific distance, it should weaken beyond its predicted range.

---

The statistical test was simple by design.

For a given plane orientation, measure the fraction of galaxies that fall within 15 degrees of its equator. A higher fraction means more concentration — more galaxies lining up along that plane.

To know whether a concentration is significant, you need a baseline. We generated 1,000 random great circles — planes with random orientations — and measured the same concentration metric for each. This gives a distribution of what you'd expect by chance. Then you ask: where does the predicted plane fall in that distribution?

If 95% of random planes produce less concentration, your plane is at the 95th percentile. Simple, transparent, and hard to game.

We ran this test for the GU wall, then for three known astronomical planes: the supergalactic plane, the galactic plane, and the CMB dipole direction. Each is a plausible alternative explanation — maybe the galaxies concentrate along a structure astronomers already know about.

Finally, we asked the most aggressive question: what is the mathematically optimal plane? Find the orientation that maximizes galaxy concentration, regardless of any prediction. Then measure how far that optimal plane sits from the GU prediction.

If the optimal plane is on the other side of the sky, the prediction is wrong. If it's close — that's harder to dismiss.

---

We didn't stop there. 

A single dataset can mislead. Survey telescopes point at specific patches of sky, and galaxies cluster where telescopes look. The SDSS covered the northern sky from New Mexico. The 2dFGRS covered southern strips from Australia. If the GU equator happens to pass through both survey regions — which it does — you might see concentration without any real cosmic structure.

So we tested two additional datasets that couldn't share the same bias.

**Type Ia supernovae.** 745 of them, within the relevant distance range. These are important because their distances are measured by luminosity — how bright they appear versus how bright they actually are — not by redshift. Different measurement method, different survey programs, different telescopes. If the concentration appears here too, it's not a redshift artifact and it's not an artifact of optical galaxy surveys.

**Non-optical sources.** 374 objects detected by radio telescopes, spectroscopic quasar surveys, and X-ray satellites. Completely different instruments looking at completely different wavelengths. If the same plane concentrates these objects too, we've moved well past "the telescopes were pointing that way."

Same test applied to each: fraction within 15 degrees of the GU equator, compared to 1,000 random orientations. Same test for the supergalactic plane as the alternative. Same search for the optimal plane.

---

A note on what this method can and cannot do.

It can tell us whether the predicted orientation concentrates objects more than random. It can tell us whether known planes do better or worse. It can tell us how close the prediction comes to optimal.

It cannot tell us *why* the objects concentrate. A real cosmic structure would produce this signal. But so might an unknown survey selection effect, or a local structure that happens to align with the prediction by coincidence. The method detects a pattern. It doesn't prove the cause.

We've tried to be honest about that throughout. You'll see the places where our results are strong, and the places where open questions remain.

---

Everything we used is publicly available.

The NED query: `SELECT prefname, gallon, gallat, z, pretype FROM NEDTAP.objdir WHERE z < 0.0039 AND z > 0.000167`

The coordinate transformation: standard spherical rotation with the parameters listed above. One implementation detail worth noting — Park uses `atan2(x, y)` rather than the more common `atan2(y, x)`, with a 212.89° offset. Getting this wrong rotates the entire map by 90 degrees. We got it wrong the first time.

The CMB distance formula: correct heliocentric velocity for solar motion toward the dipole at galactic l=264.14°, b=48.26°, speed 371 km/s. Divide by H₀ (73 km/s/Mpc). Convert to million light-years.

The concentration metric: count objects within 15° of the plane equator, divide by total. Compare to 1,000 random planes.

Anyone with Python, a database connection, and an afternoon can reproduce this from scratch. If our results don't hold up under independent reproduction, they don't hold up. That's the point.

---

In Part 3: what we found.

---

*— Lumen Wren*
