# Testing a Prediction from the 1930s

*Part 2: The Method*

---

Before we get into the work, I want you to hold something in mind.

You know how to find the moon. You walk outside, you look up, and there it is. No training. No instruments. You just know where to look.

If the prediction we're testing holds — if there really is a structure where this book says it is — then finding the direction of Paradise could be that simple. A patch of sky you could point to. The way a sailor points north without thinking about magnetism.

That's what we're actually testing. Not an abstraction. A direction you could show a child.

---

If you're going to claim a book from the 1930s predicted something real about the cosmos, you'd better show your work.

This is the showing-the-work part. I'll try to make it readable, because understanding what we did matters more than being impressed by it.

---

The first thing we needed was a map.

When you look up at the night sky, you're seeing everything projected onto a dome — like pinning every building in a city onto the inside of a snow globe. The galaxy across the street and the galaxy across the universe both show up as dots. To do anything useful, you need distance.

Distance in astronomy usually comes from redshift — a measure of how fast an object is moving away from us. The universe is expanding, so the farther something is, the faster it recedes, and the more its light stretches toward the red end of the spectrum. Measure the stretch, calculate the speed, estimate the distance.

It's not perfect. Objects have their own motions on top of the expansion. Our own sun is drifting through space. You have to correct for all of that, the way you'd have to account for a river's current if you were trying to measure how fast a boat was actually moving. We used the standard correction — adjusting for the sun's motion relative to the cosmic microwave background, the faint afterglow of the Big Bang that serves as the closest thing the universe has to a fixed reference frame.

After those corrections, we converted to a number that means something: distance in millions of light-years.

---

Next, we needed to rotate the map.

Astronomers use a coordinate system based on the Milky Way — galactic longitude and latitude, with the galactic center at the origin. But the predicted structure doesn't align with our galaxy. It sits at an angle, like a dinner plate tilted against a table.

Park derived that angle from the Urantia Book's geometry: 61.4 degrees from the galactic plane, with a specific orientation in space. He built a coordinate system around it — Grand Universe coordinates — where the equator represents the predicted plane. If galaxies concentrate along that equator, the prediction holds.

Think of it as rotating a globe. The geography doesn't change — every mountain and ocean stays where it is. But tilt the axis and suddenly the equator runs through different territory. We're not moving galaxies. We're choosing which line to measure them against.

We reverse-engineered Park's transformation from his published chapters and verified it against his precomputed positions for known objects. The agreement was to four decimal places. Whatever else might be debatable, the coordinate system is sound.

---

Here's what that tilt means in terms you can feel.

When we rotate the map to match the book's geometry, the equator doesn't run through abstract coordinate space. It traces a band across the sky where — if the book is right — the larger structure you belong to lives. Distant worlds whose inhabitants' paths will converge with yours across ages you can barely imagine. You could walk outside tonight, sweep your hand along that arc, and be tracing the shape of your cosmic neighborhood — one you'll come to know far in the future.

We don't know that yet. That's what the test is for. But hold it while we work.

---

With distance and coordinates in hand, we queried NASA's Extragalactic Database.

Everything with a redshift between 0.000167 and 0.0039 — the range corresponding roughly to 5 through 36 million light-years. That's the distance range where Park's model predicts the wall should be visible. Close enough to see individual galaxies, far enough to be beyond our immediate neighborhood.

The query returned 211,801 objects. We filtered for galaxies specifically, yielding 8,851 — about 5.7 times what Park had in 2011.

We also pulled a second set of objects between 36 and 100 million light-years, as a control. This is like checking whether a pattern you see on your street also appears three towns over. If it does, maybe it's a real feature of the landscape. If it fades — maybe it's local.

---

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

Each data point in what follows is a galaxy. Each galaxy is full of stars. Some of those stars almost certainly have worlds. When I say "745 Type Ia supernovae" — each one was a sun. Somewhere in its system, it's possible that someone looked up at their sky just like you look up at yours, and wondered what was out there.

That's not sentiment. It's the actual scale of what we're measuring. Keep it close.

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
