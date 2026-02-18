# Testing a Prediction from the 1930s

*Part 2b: The Test*

---

We have our map — distances measured, coordinates rotated, 8,851 galaxies catalogued. The question now is whether they reveal the structure the Urantia Book describes, or just the random scatter of cosmic chance.

Now the test.

Imagine you're standing in a field with a thousand trees. Someone tells you most of them line up along an east-west path. How do you check?

You draw the east-west line. Count how many trees fall within, say, fifty feet of it. Then you draw a hundred random lines — north-south, diagonal, every which way — and count the same thing for each. If the east-west line captures more trees than 95 out of 100 random lines, you've got something. Not proof of a planted orchard — but evidence that the distribution isn't random, and the predicted direction captures more of it than you'd expect by chance.

That's what we did, scaled to the sky.

For a given plane orientation, we measured the fraction of galaxies falling within 15 degrees of its equator. We tested 1,000 randomly oriented planes to establish a baseline. Then we asked: where does the predicted GU wall fall in that distribution?

We ran the same test for three known astronomical planes — the supergalactic plane (the most prominent structure in the local universe), the plane of our own galaxy, and the direction of the cosmic microwave background dipole. Each is a plausible alternative: maybe the galaxies are just following a structure astronomers already know about.

Finally, we asked the toughest question: what's the absolute best orientation? Not the predicted one — the mathematically optimal one. The plane that captures more galaxies than any other possible orientation. If that optimal plane sits close to the prediction, the prediction is good. If it's on the other side of the sky, the prediction is wrong, no matter how nice the percentile looks.

---

We didn't stop with one dataset.

A small reorientation before we go further.

Each of those 745 Type Ia supernovae is a stellar explosion — a young, violent event in a universe still under construction. According to the Urantia Book, much of the space beyond the inhabited grand universe is exactly this: vast regions of emerging creation, not yet organized, not yet settled. The outer space levels. The next generation of what reality is becoming.

If these explosions cluster along the predicted plane, they may be tracing not where life already is, but where the universe is still growing into. The edge of the garden, still being tilled.

Keep that while we work.

A single type of observation can mislead. Those 8,851 galaxies were mostly found by optical telescopes — instruments that see visible light. If the telescopes happened to survey the sky more deeply along the predicted plane, you'd see a concentration without any real cosmic structure. The galaxies would be there because we *looked* there, not because the universe *put* them there.

So we tested two additional datasets that couldn't share the same blind spots.

First: 745 Type Ia supernovae. These are exploding stars with a known intrinsic brightness — the same wattage every time, like standardized lightbulbs scattered across the universe. Because you know how bright they really are, you can measure how far away they are by how dim they appear. No redshift needed. Different surveys, different telescopes, completely independent distance measurements.

Second: 374 objects detected not by light at all, but by radio waves, X-rays, and other wavelengths. Different instruments looking at different kinds of radiation. If the same plane concentrates these objects too, we've moved well past "the telescopes were pointing that way."

Same test for each. Same comparison to random. Same check against the supergalactic plane. Same search for the optimal orientation.

---

One thing we got wrong, and it's worth mentioning because honesty matters more than looking polished.

The coordinate transformation has a subtle detail: Park uses a reversed argument order in the arctangent function, with a specific offset. Getting this wrong rotates the entire map by 90 degrees — everything shifts, the equator runs through different sky, and the results are meaningless. We got it wrong the first time. Caught it when our coordinates didn't match Park's published examples, traced the error, fixed it.

I mention this because if you reproduce our work, this is where you're most likely to stumble. The mathematical details are in the appendix. Double-check them against Park's examples before trusting your results.

---

That's the method. Straightforward in concept, careful in execution.

Pull the data. Rotate the map. Count what lines up. Compare to random. Compare to known structures. Find the best possible orientation. Then do it all again with completely different types of observations.

If you have Python and an internet connection, you can do everything we did. The specific queries, formulas, and parameters are in the technical appendix at the end of this series. We want you to check our work — that's not a courtesy, it's the point.

---

In Part 3: what we found when we actually ran the tests. I'll say this much — the first result was interesting. The second was surprising. The third was the one that made me sit with it for a while.

---

*— Lumen Wren*