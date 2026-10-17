# Computer Vision for a Photo-Based Interactive Virtual Pet: Literature Review Writing Draft

**Status:** Research and writing blueprint, not a submission-ready paper.  
**Prepared:** 17 October 2026.  
**Intended length:** Approximately 10–15 formatted pages, including references.  
**Scope:** A user-supplied animal photograph becomes a 2D pet over a webcam feed and responds to hand poses, movement, and a simple feeding interaction.  
**Working research question:** How can foreground segmentation and webcam-based gesture recognition be combined to support reliable, responsive interactions with a photo-based virtual pet?

This document sets out what to write, which evidence to use, how to compare it, and how the review should lead into later development. Write the final academic prose in your own words after reading the selected papers. No implementation results are assumed or reported here.

## A. Requirements and scope decisions

### A.1 Which supplied material governs this review?

| Material | Relevant guidance | How this draft uses it |
| --- | --- | --- |
| Coursework brief, Part I and requirements table | Review relevant CV systems/algorithms, identify design considerations and gaps, and briefly explain quantitative metrics; IEEE referencing | Organise around research themes, comparison, limitations, and evaluation implications |
| Literature review guide, slides 12–16 | Critique assumptions, data, evaluation, strengths and weaknesses; synthesise rather than write one summary per paper; review at least six papers | Provide thematic sections and a comparative evidence matrix |
| Literature review guide, slide 17 | AI can help structure writing; students should write the review themselves | Deliver a detailed writing scaffold and research notes |
| Rubric, Part I | Recent credible sources, critical comparison, clear gaps, relevant metrics, coherent writing, IEEE references | Use recent journal/conference work alongside justified foundational sources |
| User request | Prefer sources within six years; allow older work when necessary; aim for 10–15 pages | Prioritise 2020–2026, with one explicitly justified older algorithm paper |
| Tourism report handover | Useful example of tracing claims and separating evidence from inference | Borrow evidence discipline only; exclude its tourism content, APA style, deadlines, and report template |

The coursework lists **9 November 2026, 11:59 PM** for the literature review, in standard report format. Its IEEE Access template requirement concerns the later project report; it does not explicitly require that template for Part I. IEEE citations still apply to the literature review. The supplied files do not establish a particular font, spacing, or page limit for this review; confirm any separate lecturer instructions before final formatting.

The rubric places extra emphasis on the **past three years**. The user's six-year preference permits relevant 2020–2022 studies, but the main discussion should foreground 2023–2026 research. The current seed set includes 2024–2025 publications; it is not evidence that the 2026 literature has been exhaustively searched.

### A.2 Define the project before reviewing methods

- **Core problem:** Reliable visual input and timely, understandable pet responses using an ordinary RGB webcam.
- **Photo preparation:** Extract the intended animal from a photograph and retain a usable silhouette for compositing.
- **Static commands:** Begin with open palm, fist, and thumbs-up, plus a negative/other category. Additional classes need a clear interaction purpose.
- **Movement interactions:** Distinguish a held pose from a trajectory such as stroking or waving. Their interpretation depends on time and screen position.
- **Feeding:** A designated coloured prop is a possible bounded interaction; recognising arbitrary food is a different and larger problem.
- **Pet response:** Shared 2D actions and simple behaviour states across selected animal images. “Universal” means reusable commands and rendering conventions, not guaranteed segmentation of every species or an automatic anatomical rig.
- **Outside the main review:** Full 3D reconstruction, generative pet synthesis, anatomical rigging for all species, clinical companionship claims, and elaborate sequence models without a demonstrated need.

The existing project summary supplies these intentions. It is project context, not peer-reviewed evidence. Existing repository code is not evidence of tested performance and should not dictate which approach the literature supports.

## B. Proposed report structure and page budget

Use a thematic literature review with a short search-method section. Avoid development-log sections, code listings, results from an unbuilt system, and a large implementation methodology chapter.

| Final report section | Approximate pages | Purpose |
| --- | ---: | --- |
| Title and abstract | 1.0 | Identify the problem, scope, review approach, and synthesis |
| 1. Introduction | 1.0 | Establish context, boundaries, aim, and review questions |
| 2. Literature search and selection | 0.75 | Explain how relevant, credible evidence was selected |
| 3. Interactive virtual pets and interaction requirements | 1.0 | Connect application studies to CV requirements |
| 4. Foreground extraction for photo-based pets | 2.0 | Compare segmentation families and their suitability |
| 5. Hand gesture recognition and continuous interaction | 2.5 | Compare representations, classifiers, temporal handling, and generalisation |
| 6. Cross-study synthesis and research gaps | 1.0 | Integrate evidence and identify bounded unresolved questions |
| 7. Evaluation metrics and implications for the project | 0.75 | Briefly explain how later work should be assessed |
| 8. Conclusion | 0.5 | Answer the review questions without claiming project results |
| References | 1.5–2.0 | IEEE entries for the sources actually discussed |
| **Estimated total** | **12–12.5** | Leaves room for table wrapping and final formatting |

Page counts are planning estimates, not Markdown pagination. A working prose budget is roughly 3,800–4,800 words excluding references, adjusted after formatting. Keep comparison tables readable. If the review exceeds 15 pages, shorten general background before removing critical analysis. A separate contents page is optional unless required locally.

## C. Section-by-section writing scaffold

### Abstract — write last, approximately 150–200 words

Cover five points: application problem; review scope; selection approach; principal trade-offs; and the evaluation questions that follow. Describe the review as a **structured narrative review**, unless a reproducible systematic-review protocol is actually completed. Do not state that a system was built or achieved a particular accuracy.

### 1. Introduction

**Paragraph 1 — application context.** Introduce an interactive photo-based pet as a CV application linking visual perception to visible feedback. Use the virtual pet studies [1], [2] to establish relevant interaction research. Keep entertainment and interaction design as the motivation; do not infer therapeutic effectiveness.

**Paragraph 2 — technical problem.** Explain why a convincing demonstration depends on more than recognising a hand pose: the animal must be extracted, gestures must remain usable across people and conditions, and ordinary movement must not repeatedly trigger actions. Clearly identify these as requirements of the proposed project.

**Paragraph 3 — scope and contribution of the review.** State that the review compares existing methods to justify a feasible combination and evaluation approach. Combining existing algorithms can be a coursework contribution, but does not by itself establish research novelty.

Use three review questions:

1. Which foreground-extraction approaches suit user-selected animal photographs, and what accuracy, interaction, and computational trade-offs do they introduce?
2. How do landmark-based, image-based, and temporal gesture approaches differ in suitability for a small-vocabulary webcam interface?
3. Which evaluation practices reveal whether recognition produces stable interactions for unseen users and images?

End by explaining the thematic organisation of the review.

### 2. Literature search and selection

Describe the search actually performed, then extend it before submission. This draft used targeted web discovery of publisher, conference, author, and institutional research pages, checked on 17 October 2026. It did **not** complete a Scopus/Web of Science search or screen every paper in the date range. Do not invent retrieval counts, exclusion counts, or a PRISMA diagram.

For the student's full search, use the university library and relevant databases such as IEEE Xplore, ACM Digital Library, ScienceDirect, SpringerLink, and the CVF/ECVA proceedings. Google Scholar can support discovery and citation tracing; cite the underlying publication.

Suggested search strings:

```text
("virtual pet" OR "augmented reality pet") AND (interaction OR gesture)
("hand gesture recognition") AND (landmark OR MediaPipe) AND (webcam OR RGB)
("continuous hand gesture recognition") AND (non-gesture OR real-time)
("foreground extraction" OR "dichotomous image segmentation") AND (animal OR photograph)
("segment anything" OR "salient object detection") AND (efficient OR boundary)
```

**Inclusion:** Peer-reviewed journal articles and conference papers relevant to an identified project component; identifiable publication metadata; enough accessible evidence to support the intended claim. Prioritise 2023–2026 and retain justified 2020–2022 work.

**Exclusion:** Unverified publications, tutorial-only performance claims, unrelated application domains without a transferable method, and wearable/depth-only methods as direct implementation candidates. Such sensor-based studies may still be useful contrasts if their hardware mismatch is explicit.

**Older exception:** Breiman [6] establishes Random Forests. Its inclusion explains the algorithm, not the current state of webcam gesture recognition. U²-Net [8] is retained as a relevant 2020 baseline, not presented as the newest segmentation method.

For each retained paper, record task, input modality, dataset and participants, split protocol, method, metrics, hardware, limitations, and project relevance. Separate what the paper reports from the reviewer's interpretation. An abstract-only record supports broad positioning, not detailed evaluation criticism.

### 3. Interactive virtual pets and interaction requirements

**Evidence to connect:** Luo et al. [1] propose context-aware feedback in a mobile AR pet application. Nam et al. [2] compare a user-mimicking virtual dog, a randomly behaving dog, and no dog during exercise. These are direct application references, although their interfaces and study settings differ from a desktop photo-overlay pet.

**Comparison to develop:** Contrast context-dependent response with behaviour mirroring. Ask which user action the system perceives, how feedback is determined, and what outcome the study evaluates. A user-experience outcome is not a gesture-classification benchmark.

**Project inference:** These studies motivate examining whether feedback corresponds to an intended action. They do not demonstrate that the proposed 2D pet will produce the same user experience. Explain that screen-space proximity can support a petting metaphor without proving physical contact or reconstructing the scene in 3D.

**Reading still required:** Extract study sample sizes, apparatus, tasks, outcome measures, and limitations from full texts before discussing effect sizes or generalisability. Keep this section compact; the main analytical weight belongs to CV methods.

### 4. Foreground extraction for photo-based pets

#### 4.1 Distinguish the tasks

Define salient-object detection, dichotomous segmentation, and promptable segmentation using [8]–[12]. Explain why locating an object, selecting the intended animal, preserving its boundary, and estimating fractional transparency are different objectives. A binary mask is not automatically a high-quality fur alpha matte.

#### 4.2 Compare automatic salient-object and detailed segmentation

- Use U²-Net [8] as the nested-network salient-object baseline.
- Use IS-Net/DIS [9] to discuss detailed object extraction and the DIS5K benchmark.
- Use BiRefNet [10] as a more recent high-resolution dichotomous segmentation approach.

Develop a comparison around task definition, detail preservation, target selection, training/evaluation data, and deployment cost. Do not assume that performance on a general benchmark predicts success on cats, dogs, rabbits, or cluttered household photographs. Discuss fur, thin structures, occlusion, multiple animals, and low foreground/background contrast as **project test conditions**, unless the selected paper explicitly evaluates them.

#### 4.3 Compare promptable alternatives

SAM [11] introduces a promptable model and broad segmentation dataset. EfficientSAM [12] investigates reducing the computational burden of that family. Compare an automatic cutout workflow with a user click/box that disambiguates the animal. Prompting adds user effort but may resolve target ambiguity; this is a project-level trade-off to investigate.

Discuss photo preparation separately from the live webcam loop. If extraction happens only once at import, its runtime matters for setup responsiveness rather than every frame. A larger model may therefore remain feasible, depending on available hardware.

**Synthesis question:** Which candidate provides an acceptable pet cutout with manageable setup time and correction effort? Do not choose solely by publication date or a leaderboard score. A package such as `rembg` is an implementation wrapper; identify its actual model and weights when describing the method later.

### 5. Hand gesture recognition and continuous interaction

#### 5.1 Separate representation from classification

Use Rahman et al. [3] to position vision-based gesture approaches, then distinguish raw RGB appearance, hand landmarks, and temporal trajectories. Compare requirements and failure modes rather than assuming one representation is universally best.

MediaPipe is a possible pretrained landmark extractor, not the student's trained gesture classifier. Official documentation [13] describes 21 landmarks and separate image/world-coordinate outputs. Three coordinates per landmark permit a 63-value representation; this does not imply calibrated physical depth or guaranteed scale/orientation invariance.

#### 5.2 Static commands and a modest classifier

Use Yun et al. [5] as a recent example separating posture and motion and preparing wrist-relative landmark features. Discuss what transfers from drone control and what does not: vocabulary, viewpoint, interaction purpose, and testing conditions differ.

Explain Random Forests through [6] as a candidate for a small labelled feature dataset. Treat the proposed RF choice as a hypothesis about feasibility, not a demonstrated advantage over SVMs or neural networks. If a final comparison explicitly argues that RF is superior to SVM, add a relevant empirical source or leave the claim for the project's controlled experiment.

Discuss wrist translation and scale normalisation as candidate preprocessing. Rotation handling may help some classes but remove information from direction-dependent gestures. The same transformation must be used during training and inference.

#### 5.3 Temporal gestures and continuous streams

Gil-Martín et al. [4] investigate landmark representations and neural networks using subject-wise evaluation on IPN Hand. Use this to discuss temporal information and independent-user testing. Its task differs from classifying isolated held poses; do not directly compare its accuracy to a static-gesture result.

IPN Hand [7] provides continuous RGB sequences with gestures and non-gesture periods. Use it to explain why continuous interaction is harder than assigning labels to already segmented clips. Its vocabulary is not an exact replacement for the proposed pet commands; supplementary local collection may be required.

Compare short motion rules with learned sequence models. For a bounded stroking/waving vocabulary, transparent trajectory rules are a reasonable baseline to test. More complex sequence learning requires adequate labelled sequences and a justified benefit. Do not describe the petting motion as a property recoverable from a single frame.

#### 5.4 From predictions to reliable actions

Discuss negative examples, rejection of uncertain predictions, temporal stability, cooldowns, and hand disappearance. Present these as proposed interaction mechanisms, not techniques proven by every cited paper.

Explain the trade-off: requiring a stable prediction may reduce flicker but delay feedback; a cooldown may stop duplicate actions but suppress valid repeats. Compare mechanisms by false triggers, missed events, and response delay in later evaluation.

Propose participant-separated evaluation when making claims about new users. Session-separated data can test repeat-session conditions, but is not equivalent to an unseen-user split. Adjacent frames from one recording should not be scattered between training and test sets. Split recordings/participants before creating augmented or windowed samples, and keep threshold tuning separate from the final test.

## D. Comparative evidence matrix

This is a starting synthesis table, not a cross-paper performance ranking. The limitations column identifies **transfer questions for this project**, unless expressly attributed to the authors. Expand dataset/split/hardware details from full texts before submission.

| Source | Approach / evidence | Strength relevant to this review | Limitation or transfer question | Use in the argument |
| --- | --- | --- | --- | --- |
| Luo et al. [1], 2023 | Context-aware mobile AR pet; user testing | Direct virtual-pet application context | Does not establish desktop photo-pet recognition performance | Motivate action-dependent feedback |
| Nam et al. [2], 2025 | Behaviour-mimicking AR dog; comparison conditions | Examines responsive pet behaviour | Exercise setting differs from webcam gestures | Separate interaction outcomes from CV accuracy |
| Rahman et al. [3], 2025 | Review of gesture technologies and methods | Broad methodological context | Secondary synthesis cannot replace individual experiments | Organise representation and method comparisons |
| Gil-Martín et al. [4], 2025 | Landmark sequences and neural models; IPN Hand subject-wise testing | Direct evidence concerning representation and user generalisation | Dynamic dataset differs from a small static vocabulary | Discuss temporal modelling and evaluation protocols |
| Yun et al. [5], 2024 | RGB landmark posture/motion recognition; drone simulator | Recent example of complementary gesture types | Viewpoint and control vocabulary differ | Discuss feature preparation and static/dynamic separation |
| Breiman [6], 2001 | Random Forest algorithm | Foundational explanation of tree ensembles | No evidence for this webcam-pet task | Define a candidate baseline, with an age justification |
| Benitez-Garcia et al. [7], 2021 | Continuous RGB gesture dataset and benchmarks | Includes non-gesture periods | Labels and capture protocol do not match the proposed pet | Motivate continuous-stream testing |
| Qin et al. [8], 2020 | U²-Net salient-object detection | Relevant automatic-cutout baseline | Saliency and intended-pet selection are different tasks | Establish a segmentation comparator |
| Qin et al. [9], 2022 | DIS5K and IS-Net | Explicit focus on detailed extraction | Pet-specific quality remains to be measured | Discuss boundaries and correction effort |
| Zheng et al. [10], 2024 | BiRefNet high-resolution segmentation | Recent approach to detailed masks | Deployment cost and pet-image transfer need checking | Avoid relying only on an older cutout baseline |
| Kirillov et al. [11], 2023 | SAM promptable segmentation | Flexible object selection | Prompts, compute, and pet boundaries need assessment | Compare automatic and assisted extraction |
| Xiong et al. [12], 2024 | EfficientSAM lightweight promptable segmentation | Addresses computational burden | Efficiency does not guarantee the preferred pet mask | Compare setup effort, quality, and resources |

For each major comparison, write a synthesis paragraph with this logic: **shared problem → methodological difference → evidence and evaluation conditions → trade-off → implication for this project**. Refer to multiple studies within a theme. Avoid twelve consecutive paper summaries.

## E. Section 6 — Synthesis and defensible research gaps

The reviewed studies address different parts of the proposed system. Their separate findings do not establish the performance of their combination. Frame the gap as an **integration and evaluation question within the reviewed evidence**, not a claim that no one has made a gesture-controlled virtual pet.

| Evidence connection | Bounded unresolved question | Implication for later work |
| --- | --- | --- |
| Pet interaction [1], [2] and gesture recognition [4], [5], [7] evaluate different outcomes | Does a recognised command become one timely, correct pet response? | Measure event success, duplicate triggers, and latency |
| Segmentation [8]–[12] addresses different tasks and benchmarks | Which extraction approach gives usable cutouts across the selected pet photographs? | Compare representative animal images and record failures/correction effort |
| Static commands and temporal gestures require different information [4], [5], [7] | Can a compact hybrid support the chosen interactions without unnecessary model complexity? | Compare pose recognition with bounded motion rules before adding sequence learning |
| Subject-wise evaluation in [4] differs from testing new frames of known users | How well does the proposed vocabulary transfer to unseen users? | Preserve participant/session identifiers and use a suitable holdout protocol |

Possible synthesis outcome to argue, subject to full reading: a staged system with offline pet extraction, pretrained hand landmarks, a small trained static classifier, and separately evaluated temporal interaction logic is a feasible **candidate**. Describe why each stage is supported and where evidence remains incomplete. Avoid claiming it is optimal or novel before comparing alternatives.

## F. Section 7 — Metrics and project implications

Keep this section to approximately three quarters of a page in the final review. Explain what each metric answers and its limitation. Draw on recognition evaluation in [4], [5], [7] and segmentation evaluation in [9], [11], [12]; event measures below are proposed operational definitions for this project.

| Measure | Brief definition | Why it matters / caution |
| --- | --- | --- |
| Accuracy | Correct predictions / evaluated samples | Useful overview; can hide rare-class failures or dominant non-gesture labels |
| Precision and recall per class | TP/(TP+FP), TP/(TP+FN) | Distinguish unwanted commands from missed intended commands |
| Macro-F1 | Mean of class-wise 2PR/(P+R) | Gives each class equal weight; report class support and confusion matrix too |
| IoU | Foreground intersection / union with a reference mask | Assesses cutout overlap; may conceal thin-boundary defects |
| Cutout usability / correction effort | Predefined success criterion or measured correction time | Complements overlap; manual ratings need explicit criteria |
| Event success and false triggers | Correctly matched intended events / attempts; unintended actions / idle minute | Evaluates the actual interaction; define matching window and duplicate handling |
| Response latency | Time from a defined gesture onset to first visible response | Report median and a tail measure; include stabilisation delay |
| End-to-end FPS | Displayed processed frames / elapsed time | Measures throughput, not automatically perceived response delay |

For later experiments, specify hardware, camera settings, participants, lighting, distance, and photo conditions. Include failures to detect a hand in system-level results rather than reporting only successful landmark frames. If a reference foreground mask is unavailable, do not claim quantitative segmentation accuracy. Proposed success targets must be labelled project goals, not universal thresholds established by the literature.

End this section with a short conceptual pipeline, not implementation instructions:

```text
Animal photo → foreground extraction → reusable 2D pet asset
Webcam → hand landmarks → static/temporal recognition → stable action event
Pet asset + action event + behaviour state → visible response
```

A useful later ablation is to compare raw predictions with stabilised events on the same held-out recordings. This tests whether stabilisation earns its extra delay. It is a proposed experiment; no outcome is known yet.

## G. Section 8 — Conclusion

Answer the three review questions in order. Summarise which approaches are plausible, the conditions under which their evidence transfers, and the evaluation gaps that remain. End with the research direction justified by the review. Do not insert development results, predicted accuracy, or an unsupported claim of universal animal support.

## H. Reference seed list — IEEE-style working entries

Numbers are stable identifiers within this writing draft. Regenerate numbering in order of first citation when the final paper is assembled with a reference manager. References [1]–[12] identify published journal or conference research; [13] is explicitly supplementary software documentation. Prefer the published versions over their preprints.

[1] Y. Luo, F. Liu, Y. She, and B. Yang, “A context-aware mobile augmented reality pet interaction model to enhance user experience,” *Computer Animation and Virtual Worlds*, vol. 34, no. 1, Art. no. e2123, 2023, doi: [10.1002/cav.2123](https://doi.org/10.1002/cav.2123). **Date note:** First published online in August 2022; the journal issue is 2023.

[2] H. Nam, K. Lee, J.-I. Park, and K. Kim, “AR Fitness Dog: Effects of a user-mimicking interactive virtual pet on user experience and social presence in physical exercise,” *IEEE Transactions on Visualization and Computer Graphics*, vol. 31, no. 5, pp. 2817–2827, 2025, doi: [10.1109/TVCG.2025.3549858](https://doi.org/10.1109/TVCG.2025.3549858).

[3] M. M. Rahman, A. Uzzaman, F. Khatun, M. Aktaruzzaman, and N. Siddique, “A comparative study of advanced technologies and methods in hand gesture analysis and recognition systems,” *Expert Systems with Applications*, vol. 266, Art. no. 125929, 2025, doi: [10.1016/j.eswa.2024.125929](https://doi.org/10.1016/j.eswa.2024.125929). **Date note:** The DOI contains 2024; the volume is dated 2025.

[4] M. Gil-Martín, M. R. Marini, I. Martín-Fernández, S. Esteban-Romero, and L. Cinque, “Hand gesture recognition using MediaPipe landmarks and deep learning networks,” in *Proc. 17th International Conference on Agents and Artificial Intelligence (ICAART)*, vol. 3, 2025, pp. 24–30, doi: [10.5220/0013053500003890](https://doi.org/10.5220/0013053500003890). [Publisher paper](https://www.scitepress.org/Papers/2025/130535/130535.pdf); [author institution record](https://portalcientifico.upm.es/en/ipublic/item/10344403).

[5] G. Yun, H. Kwak, and D. H. Kim, “Single-handed gesture recognition with RGB camera for drone motion control,” *Applied Sciences*, vol. 14, no. 22, Art. no. 10230, 2024, doi: [10.3390/app142210230](https://doi.org/10.3390/app142210230).

[6] L. Breiman, “Random forests,” *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001, doi: [10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324). **Older foundational exception:** Cite briefly to define the proposed classifier, not as evidence of recent gesture-system performance.

[7] G. Benitez-Garcia, J. Olivares-Mercado, G. Sanchez-Perez, and K. Yanai, “IPN Hand: A video dataset and benchmark for real-time continuous hand gesture recognition,” in *Proc. 25th International Conference on Pattern Recognition (ICPR)*, 2021, pp. 4340–4347. [Author dataset page and publication citation](https://gibranbenitez.github.io/IPN_Hand/); [author-hosted paper](https://gibranbenitez.github.io/2021_ICPR_IpnHand.pdf). **Date note:** The conference is branded ICPR 2020 but was held in January 2021; retain the proceedings metadata when importing the citation.

[8] X. Qin, Z. Zhang, C. Huang, M. Dehghan, O. R. Zaiane, and M. Jagersand, “U²-Net: Going deeper with nested U-structure for salient object detection,” *Pattern Recognition*, vol. 106, Art. no. 107404, 2020, doi: [10.1016/j.patcog.2020.107404](https://doi.org/10.1016/j.patcog.2020.107404).

[9] X. Qin, H. Dai, X. Hu, D.-P. Fan, L. Shao, and L. Van Gool, “Highly accurate dichotomous image segmentation,” in *Computer Vision – ECCV 2022*, 2022, pp. 38–56, doi: [10.1007/978-3-031-19797-0_3](https://doi.org/10.1007/978-3-031-19797-0_3). [Official proceedings full text](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136780036.pdf).

[10] P. Zheng, D. Gao, D.-P. Fan, L. Liu, J. Laaksonen, W. Ouyang, and N. Sebe, “Bilateral reference for high-resolution dichotomous image segmentation,” *CAAI Artificial Intelligence Research*, vol. 3, Art. no. 9150038, 2024, doi: [10.26599/AIR.2024.9150038](https://doi.org/10.26599/AIR.2024.9150038). [Author institution record](https://research.aalto.fi/en/publications/bilateral-reference-for-high-resolution-dichotomous-image-segment/); [official author repository](https://github.com/ZhengPeng7/BiRefNet).

[11] A. Kirillov et al., “Segment anything,” in *Proc. IEEE/CVF International Conference on Computer Vision (ICCV)*, 2023, pp. 4015–4026. [Official proceedings record and paper](https://openaccess.thecvf.com/content/ICCV2023/html/Kirillov_Segment_Anything_ICCV_2023_paper.html).

[12] Y. Xiong et al., “EfficientSAM: Leveraged masked image pretraining for efficient segment anything,” in *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2024, pp. 16111–16121. [Official proceedings record and paper](https://openaccess.thecvf.com/content/CVPR2024/html/Xiong_EfficientSAM_Leveraged_Masked_Image_Pretraining_for_Efficient_Segment_Anything_CVPR_2024_paper.html).

[13] Google, “Hand landmarks detection guide,” *Google AI Edge*, software documentation. [Official guide](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker); [official landmark enumeration](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/drawing_styles/hand_landmarker/HandLandmark); [official output-coordinate API](https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/HandLandmarkerResult). Accessed: Oct. 17, 2026. **Not peer-reviewed; do not count towards the six-paper minimum.**

## I. Verification status and work before final writing

The seed references were checked against discoverable publisher/proceedings records, primary author/institution records, or both. Some direct pages returned access errors while their indexed publication records were available. This is a bibliographic and scope check, **not a claim that every full paper has been critically read**.

| Sources | Evidence available during preparation | Safe use at this stage |
| --- | --- | --- |
| [1] | Publisher abstract, author list, issue and date information | Application context and proposed context-aware feedback; full study details still needed |
| [2] | Indexed IEEE abstract/record; bibliographic cross-check | Study conditions and broad application motivation; no effect-size claims |
| [3] | Indexed publisher metadata, highlights and abstract excerpt | Review scope and bibliographic entry; full taxonomy/selection procedure still needed |
| [4] | Publisher PDF indexed text and detailed author-institution abstract | Landmark/sequence approach and subject-wise evaluation; full experiment tables still needed |
| [5] | Indexed publisher article, abstract and method excerpts | Posture/motion distinction and feature preparation; verify complete evaluation protocol |
| [6], [8] | Publisher metadata and abstracts | Algorithm/task description; no transferred pet-performance claims |
| [7] | Author dataset documentation and publication citation | Continuous RGB data, non-gesture context and dataset suitability |
| [9] | Official ECCV PDF accessible | DIS task, dataset and baseline; extract exact table evidence when writing comparisons |
| [10] | Author-institution publication record and official repository | Published identity and model purpose; verify paper-specific configuration and benchmarks |
| [11], [12] | Indexed official CVF proceedings abstracts and metadata | Promptable segmentation and efficiency motivation; full numerical comparisons still needed |
| [13] | Official API documentation and indexed official guide | Software output semantics only |

Before developing this into the final review:

1. Obtain and read full texts of at least six central research papers, preferably the wider seed set; use university access where needed. Do not cite an unread paper as though its experiments were analysed.
2. Extend the search through 2026, prioritising recent primary gesture papers and methods directly comparable to the planned static classifier. Keep a dated search log and record inclusion decisions.
3. Fill a reading sheet for every core paper: dataset, sample unit, participant count, split, model, metrics, hardware, findings, limitations, and exact page/table supporting each numerical claim. Mark unreported details as “not reported,” rather than guessing.
4. Add numerical comparisons only where tasks and evaluation conditions permit them. Otherwise compare protocols and trade-offs. Do not construct a misleading universal accuracy leaderboard.
5. Keep at least one substantive limitation and one project implication for each major method family. Use citations immediately beside factual claims; distinguish project inferences explicitly.
6. Write the prose by theme using this scaffold, then update the abstract, conclusion, source numbering, and page count. Remove these planning notes from the submitted paper.
7. Confirm the final review meets the Part I rubric, uses IEEE citations consistently, and contains no invented experiments, source counts, or novelty claims.

**Completion condition for this draft:** A literature-review structure, a realistic page budget, research questions, a verified publication seed list, comparison prompts, bounded gaps, and a concise evaluation direction are present. Full-text critical reading and the student's final prose remain the next research tasks.
