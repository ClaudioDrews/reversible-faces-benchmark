# One physical page turn, multiple possible perceived 3D heads

**Status: open research hypotheses, not empirical measurements.**

The page is always rotated by 180° around (500,500). But the observer constructs a head from cues: facial-feature relations, occlusion, relative sizes, nose profile, jaw, silhouette, neck, hair/hat contours, contour completion and line weight.

In A's upright perceptual frame, the face can appear bowed downward (pitch). In B's upright frame, it can appear sideways or in profile (yaw). Both can additionally have different head roll and averted/direct gaze. No rule of C₂ forces these inferred properties to be the same.

Formally, the visible drawing is I. For each orientation θ, the inferred perceptual state is
```
P_theta = (face-present, identity, expression, estimated-yaw, estimated-pitch,
           estimated-roll, gaze-direction, contour-grouping, border-ownership).
```
Thus P_0(I) and P_pi(RI) need not share a pose even though R is exact. The pose is not a 3D transformation of the SVG. It is an interpretation of a two-dimensional mark pattern.

## Competing hypotheses, all retained

| Hypothesis | Potential mechanism | Control / disconfirmation |
|---|---|---|
| Frontal/frontal shared eye anchors | stable high-salience anchor | compare with nonfrontal pairs under same budget |
| Downward/sideways | foreshortened eyes and nose can be re-read as lateral contour | pose estimators/raters do not see predicted pose |
| Profile/frontal | single visible eye and nose projection become other roles | compare to added second eye and full nose |
| Asymmetric head roll | eye-line, jaw, hair flow suggest tilted heads | independent A/B axis annotations, not same axis rotated |
| Gaze/head dissociation | eye look-direction need not equal head yaw | separate observer gaze and head-direction judgments |
| Multistable/weak contour | omission allows multiple completions | add fragments incrementally and test weakest view |
| Varied lineweight | edge salience shifts role by context | manipulate width separately from geometry |
| Strong closure vs weak closure | grouped negative space changes facial parts | pixel-identical but mask/occlusion-based controls |
| Pose × ornament interaction | hat or beard cues compensate incomplete anatomy | remove accessory while holding facial strokes fixed |
| Story-driven pose | posture signals emotion/narrative | compare against story-neutral prompts |

The list is not a filter. New candidate explanations should be added with falsifiable controls and evidence labels, even if they conflict with prior assumptions.

## Evaluation

Record first unprompted descriptions of the upright drawing in each view, then ask head facing direction, downward/upward pitch, roll, gaze direction, expression, identity, and confidence separately. Do not supply the artist's desired response before the open description.

Compare pose angle distributions, facial detection, role mapping, weakest-face recognizability, visual humor and artistic richness. Trial counts, sampling and statistical gates are frozen only after a feasibility pilot. The classic benchmark's historical fixed shared-eye requirements are not silently revised: use an **open-design branch condition** for experiments incompatible with them.

## Literature

- Van der Linde & Watson (2010), *Vision Research*, DOI 10.1016/j.visres.2009.12.012, https://pubmed.ncbi.nlm.nih.gov/20043938/
- Liu & Chaudhuri (2002), *Reassessing the 3/4 view effect*, https://pubmed.ncbi.nlm.nih.gov/11814485/
- Maurer, Le Grand & Mondloch (2002), *The many faces of configural processing*, DOI 10.1016/S1364-6613(02)01903-4.
- Singh & Hoffman (1999), *Completing visual contours*, DOI 10.3758/BF03206908.
