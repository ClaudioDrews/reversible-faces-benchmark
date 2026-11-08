# Mathematical and perceptual model

## 1. Object and geometry [EXACT]

A vector drawing \`I\` occupies the fixed 1000 × 1000 SVG page. Its official half-turn is \`R_c(p)=2c-p\`, where the frozen evaluation centre is \`c=(500,500)\`. \`R_c^2=id\`, \`det(R)=+1\`. Reflection and arbitrary centre adjustment are **different tasks**. During design, the centre may be estimated from matched landmarks, then the finished composition must be recentered for the official transform.

For recognition sets \`C_A\` and \`C_B\`, feasible figures lie in \`C_A ∩ R^{-1}(C_B)\`; for a half-turn, \`R^{-1}=R\`. The intersection alone admits independently overlaid faces; a single-coherent-composition constraint is an **additional uncalibrated perceptual requirement**. Under general invertible \`T\`, use \`C_A ∩ T^{-1}(C_B)\`, not \`C_A ∩ T(C_B)\`.

## 2. Pairing and structural semantics [HYPOTHESIS]

Let \`S={s_1,...,s_n}\` be graphic primitives (not necessarily the SVG path elements). Define \`Π_0(I)=G_A\` and \`Π_π(RI)=G_B\`, with nodes for facial roles, groups, contours, regions, junctions and expressions; edges include above/below, proximity, containment, junction, good continuation and border ownership. A single primitive may participate in multiple groups, and many-to-many segment correspondence is allowed.

A partial role map \`D: (s_j,role_A) -> (s_j,role_B)\` is not the identity map: brow ↔ eye-bag, hat brim ↔ nose, hair ↔ beard and hat ornament ↔ collar are *design hypotheses* that have to be checked in both orientations. B is evaluated after rotation; never accidentally apply the transform twice.

Separate four failure classes: (a) identical face twice (self-C2 collapse); (b) two independent faces pasted together (segregation); (c) conflicting stroke contours (ghosting); (d) semantically weak or facially unreadable B despite geometric proximity.

## 3. Midpoint geometry [EXACT for specified loss]

A stroke target \`a\` in A's page coordinates and target \`b\` in B's upright coordinates correspond on one page as \`a\` and \`R(b)\`. For positive weights the minimizer of \`w_A||s-a||²+w_B||s-R(b)||²\` is \`s*=(w_A a + w_B R(b))/(w_A+w_B)\`. The equal-weight midpoint minimizes maximum Euclidean displacement to two fixed points. Equal tolerance disks intersect iff \`||a-R(b)|| <= 2ε\`. These statements do **not** establish facial recognition. For paired Bézier control points maintain consistent degree/order and preserve endpoint tangents before applying a pointwise compromise.

The normalizing centre for matched A/B landmarks is \`c*=Σ_i w_i(a_i+b_i)/(2Σ_i w_i)\`. This is a construction diagnostic; score final benchmark art **only** around \`(500,500)\`.

## 4. C2 parity [EXACT on linear image fields]

\`I_+=(I+RI)/2\`, \`I_-=(I-RI)/2\`, \`I=I_++I_-\`, \`RI=I_+-I_-\`. For a nonzero real ink vector, \`ρ=||I-RI||/||I||=2||I_-||/||I||\`, a **rotational invariance residual**, not distance to the orbit and not semantic recognizability. For nonnegative ink \`0 <= ρ <= √2\`. The odd component can be signed: it is not a directly drawable nonnegative ink layer.

For an arbitrary finite group the Reynolds operator \`P_G=(1/|G|)Σ_g g\` extracts the invariant component; its complement is not generically a single "-odd" representation.

## 5. Shape constraints and figure-ground [EXACT geometry; perceptual inference HYPOTHESIS]

If silhouettes are star-shaped around a common centre and B is expressed in B's upright frame, \`r_0(φ)=max(r_A(φ),r_B(φ+π))\` preserves both envelopes. \`r_S=max(K*r_0,r_0)\` preserves radial containment under a suitable normalized smoothing kernel; it does **not** guarantee smoothness and is not mathematical morphological closing. The coordinate-free version is \`Ω_S ⊇ Ω_A ∪ R^{-1}(Ω_B)\`.

Positive ink, negative space, closed regions and border ownership are distinct measurements. A useful candidate may reassign a contour from one face part to another. Figure-ground inversion is *not* the benchmark's physical rotation: it is a separate ablation.

## 6. Gestalt and facial configuration [HYPOTHESIS with literature motivation]

Test contour continuity (local tangent compatibility), closure, proximity, common region, negative-space arrangement and parsimony of **two** parse graphs. The "simplicity" principle and Minimum Description Length motivate an operational coding cost; neither is a calibrated psychological score. For facial recognition, test first-order relations (eyes/nose/mouth), holistic relations and second-order distances separately; processing may be vulnerable to inversion. Rotation-dependent face organization differs from spontaneous rivalry in a fixed orientation.

## 7. Salience, topology, linework and meaning [HYPOTHESIS]

A large contour overlap may hide a small but defining feature. For manually labelled regions \`j\`, use exploratory geometry \`D=Σ_j w_j d_j/Σ_j w_j\`, where weights must be justified or empirically estimated rather than set by the researcher after inspection. For any reading-sensitive recognizer \`f_A, f_B\`:

\`Δ_A^j=f_A(I)-f_A(I\\S_j)\`,
\`Δ_B^j=f_B(RI)-f_B(R(I\\S_j))\`.

Candidate sharing \`Q=Σ min([Δ_A]_+,[Δ_B]_+) / (Σ max([Δ_A]_+,[Δ_B]_+) + δ)\` for \`δ>0\` is in \`[0,1)\`. A high Q **does not** prove distinct interpretations; that requires a separate test. Without an independently validated recognizer, Q is not measured.

Line-width taper and sector-wise adjustment may affect perceptual emphasis. Preserve essential ink, control additions, measure changed pixels and per-orientation legibility before accepting any local operator. Refuse no-op "improvements". Different source SVG paths may be physically one continuous contour; do not equate path count with perceived stroke count.

## 8. Study priorities

First explain existing successes/failures without altering their pixels. Then compare geometric-only vs structure-first generation with matched model, budget and multiple attempts. Finally test a professional engraving pass (hatching, cross-hatching, varied contour weights, ornaments, shading) under invariant-preservation gates. More detail is **not** automatically more meaningful: it may obscure the second reading. Subjective artistry must have independent blind raters.

## 9. Face pose is a latent interpretation, not page rotation [HYPOTHESIS]

In each upright viewing frame, an observer can infer a different head orientation `q_A=(yaw_A,pitch_A,roll_A)` and `q_B=(yaw_B,pitch_B,roll_B)`. The physical transform is **always** `R_{(500,500)}`, but there is no general requirement that `q_A=q_B`. A downward-looking A and side-looking B can be compatible if head contour, nose projection, visible/occluded eye configurations, hair, neck, and negative space support each parse.

This introduces perspective-dependent landmarks: the visible eye count and positions need not coincide in two interpretations. In a weak-perspective model, facial landmark projections are `p_i ≈ s·ΠQ(q)X_i+t`, but the inverse problem from one stylized line drawing is underdetermined. Do not call the toy controls a real 3D face reconstruction. The experimental role graph is allowed to map visible eye to non-eye, one eye to an occluded eye or multiple pen strokes into one facial cue.

Test front/front (classic constraint), front/profile, down/side, three-quarter/three-quarter and profile/profile as separate conditions. Distinguish the original RFB rubric, which may impose shared-eye conventions, from a deliberately expanded design domain. A claimed facial percept needs independent judgments.
