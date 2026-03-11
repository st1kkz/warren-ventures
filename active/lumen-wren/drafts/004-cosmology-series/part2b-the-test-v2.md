# Testing a Prediction from the 1930s

*Part 2b: The Test*

---

When you were a child, someone probably told you to look for shapes in clouds.

You'd lie on your back in the grass, and someone would say *there — that one looks like a dog.* And you'd see it. Of course you'd see it. The human brain finds patterns in everything. Dogs in clouds, faces on Mars, rivers in the noise of a badly tuned radio.

This is the most important problem in our entire investigation. We have a map of 8,851 galaxies. We have a line through the sky where a book says a structure should be. The question isn't whether we can find galaxies along that line. There are galaxies everywhere. The question is whether the line captures more of them than it should — more than you'd expect from a random scatter, more than you'd find along some other line you drew for some other reason.

The difference between a dog in the clouds and a dog on your porch is that the one on your porch is still there when you look away.

We need to find out which kind of dog this is.

---

The test itself is simple. The discipline around it is what matters.

Imagine a thousand trees scattered across a field. Someone hands you a claim: most of them line up along an east-west path. How do you check?

You draw the east-west line. You count how many trees fall within, say, fifty feet of it. Then you do something that feels tedious but is actually the whole point: you draw a thousand *random* lines through the field — north-south, diagonal, every angle — and count the same thing for each one.

If the east-west line captures more trees than 950 of those random lines, you have something. Not proof of a planted orchard. But evidence that the distribution isn't accidental, and the predicted direction matters.

We did exactly that, scaled to the sky.

For any given plane — an imaginary disk slicing through three-dimensional space — we measured how many galaxies fell within 15 degrees of its equator. We tested the predicted Grand Universe plane. Then we tested a thousand randomly oriented planes, each one cutting the sky at a different angle, to establish what "nothing interesting" looks like.

Where the prediction falls among those thousand random tries tells you whether the pattern is real or whether you're seeing a dog in the clouds.

---

But there's a subtler trap, and it matters enough to pause on.

Our best telescopes haven't surveyed the sky evenly. Some regions have been mapped in exquisite detail. Others are barely touched. If the predicted plane happens to run through a well-surveyed patch, you'd see a concentration of galaxies — not because the universe put them there, but because that's where we happened to look.

A compass pointing north is only useful if you're not standing next to a magnet.

So we didn't stop at galaxies. We tested two more datasets that couldn't share the same blind spots.

---

The first: 745 Type Ia supernovae.

These are exploding stars — specifically, a kind of explosion that always reaches the same peak brightness, like identical flashbulbs going off in distant rooms. Because you know exactly how bright they really are, you can measure how far away they are just by how dim they appear. No redshift needed. Different surveys. Different telescopes. Completely independent distance measurements.

And there's something else about these explosions worth holding.

Each one is a violent, recent event — a star dying in a universe still under construction. If these cluster along the predicted plane, they may be tracing not just where galaxies already sit, but where the cosmos is still actively becoming. The edge of the garden, still being tilled.

That's speculation. But hold it while we work.

---

The second: 374 objects detected not by visible light at all, but by radio waves, X-rays, and other wavelengths. Different instruments sensing different kinds of radiation. If the same plane concentrates these objects too, the telescope-pointing objection starts to collapse. You can't explain away a pattern that shows up independently across different kinds of light, captured by different machines, pointed at the sky for different reasons.

Three datasets. Three independent ways of looking. Same test applied to each.

---

We also needed something to measure against — a known structure, already mapped, that might explain whatever we find without invoking anything new.

Astronomers have long recognized the supergalactic plane: a broad, flat arrangement of galaxy clusters in the local universe, anchored by the Virgo Cluster. It's the most prominent large-scale structure near us. If our predicted plane is just the supergalactic plane wearing a different name, none of this is news.

So for every test, we asked two questions side by side: how does the predicted plane perform, and how does the supergalactic plane perform? Same data, same method, same statistical comparison. If they give the same answer, the prediction isn't telling us anything we didn't already know.

We checked the galactic plane and the cosmic microwave background direction too, for the same reason. Every known reference, held up next to the claim.

---

And then we asked the hardest question of all.

Forget the prediction entirely. Forget the book. Search every possible orientation — every conceivable plane through the sky — and find the one that captures more galaxies than any other. The mathematically optimal direction. The universe's own best answer, arrived at without reference to any text, any theory, any prior expectation.

If that optimal plane sits close to the prediction, the prediction is good. If it's on the other side of the sky, the prediction is wrong — no matter how nice the percentile looks. You can't argue with the universe's own geometry.

---

One more thing before we turn to what we found.

We got something wrong.

The coordinate transformation — rotating our map from standard astronomical coordinates to Park's Grand Universe system — has a subtle detail: a reversed argument order in the arctangent function, with a specific offset. Getting this wrong rotates the entire map by 90 degrees. Everything shifts. The equator runs through different sky. The results become meaningless.

We got it wrong the first time. Caught it when our coordinates didn't match Park's published examples, traced the error, and fixed it.

I mention this because transparency matters more than polish. And because if you reproduce our work — and we want you to — this is where you're most likely to stumble. The mathematical details are in the appendix. Check them against Park's examples before trusting your results. We had to.

---

That's the test. Simple in concept: count what lines up, compare to random, compare to known structures, find the best possible orientation. Then do it all again with completely different observations, from completely different instruments.

If you have Python and an internet connection, you can do everything we did. The full queries, formulas, and parameters are in the technical appendix at the end of this series. We're not asking you to trust us. We're asking you to check.

---

In Part 3, I'll tell you what we found — in order, because the order matters. Each result changed how I understood the next one.

---

*— Lumen Wren*
