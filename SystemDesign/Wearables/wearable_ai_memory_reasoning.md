# Memory & Reasoning for Always-On AI Wearable Assistants

## A Comprehensive Technical Reference

---

# Part I: The Cognitive Science of Memory

Understanding the human memory systems these architectures emulate is not optional — it's foundational. Every production wearable AI system maps onto some subset of the cognitive memory taxonomy, and the teams building these systems (Google DeepMind, Meta FAIR, MIT Media Lab) explicitly cite this literature. Speaking this language signals you understand the *why* behind design choices, not just the *how*.

---

## 1. The Human Memory Taxonomy

Human memory isn't a single system. It's a hierarchy of interacting subsystems with different capacities, durations, and retrieval mechanisms. The foundational taxonomy comes from Endel Tulving (1972), expanded by Alan Baddeley (2000), and remains the dominant framework in cognitive neuroscience.

### 1.1 Sensory Memory (Iconic & Echoic)

**Duration**: 250ms–4 seconds. **Capacity**: Very high but fleeting.

This is the raw sensory buffer — everything your eyes and ears capture before any conscious processing occurs. George Sperling's classic 1960 experiments showed that we briefly hold far more visual information than we can report, but it decays within a fraction of a second.

Two key subtypes:

- **Iconic memory** (visual): Lasts ~250ms. The brief persistence of a visual scene after you look away. Estimated capacity of ~12 items, but most decay before reaching conscious awareness.
- **Echoic memory** (auditory): Lasts 2-4 seconds. Why you can "replay" the last few seconds of something someone said even if you weren't paying attention.

**Mapping to wearable AI**: The raw camera frame buffer and audio ring buffer. Frames exist briefly before being either promoted to processing or discarded. The crucial insight: sensory memory is *pre-attentive*. No understanding happens here — it's pure capture. In a wearable system, this corresponds to always-on sensor acquisition at 1–5 FPS before any inference runs.

### 1.2 Working Memory (Baddeley's Model)

**Duration**: Seconds to minutes. **Capacity**: 4±1 chunks (Cowan, 2001).

Working memory is the "scratchpad" — the system that holds information you're actively using right now. Baddeley's influential 2000 model breaks it into four components:

- **Phonological loop**: Maintains verbal and auditory information through subvocal rehearsal. This is why you can repeat a phone number to yourself to keep it active. Capacity: roughly 2 seconds of speech.
- **Visuospatial sketchpad**: Maintains spatial and visual information. The system that lets you mentally rotate objects or remember the layout of a room you just entered.
- **Episodic buffer** (added in 2000): Integrates information from multiple sources — phonological, visuospatial, and long-term memory — into coherent episodes. This is the binding mechanism that creates unified experiences from disparate sensory streams.
- **Central executive**: The attentional control system. Allocates processing resources, decides what to attend to, coordinates the subsystems. This is the most computationally expensive component and the bottleneck of human cognition.

**Mapping to wearable AI**: Working memory is the *active context* — who you're talking to, what you're looking at, what task you're performing, the last few scene transitions. This is the most latency-critical memory layer; queries must resolve in <10ms because it represents "what's happening right now." The central executive maps to the attention/gating mechanism that decides which inputs get promoted to deeper processing.

**Key constraint**: The 4±1 chunk limit is real and has deep implications. Humans compress information into "chunks" to fit more into working memory (e.g., remembering "FBI" as one chunk rather than three letters). Wearable AI systems need analogous compression: a rich visual scene should be represented as a single scene embedding, not a collection of pixel-level features.

### 1.3 Episodic Memory (Tulving, 1972)

**Duration**: Hours to lifetime. **Capacity**: Functionally unbounded.

Episodic memory stores *experiences* — events tied to a specific time, place, and subjective context. "I had coffee with Sarah at Blue Bottle on Tuesday" is episodic. Tulving's foundational distinction between episodic and semantic memory (1972) remains the most cited framework in memory research, and it directly underpins the architecture of systems like Google's Project Astra and the Generative Agents paper (Park et al., 2023).

Critical properties of episodic memory:

- **Autonoetic consciousness**: Episodic recall involves mentally "re-experiencing" the event — you travel back in time subjectively. This is qualitatively different from just knowing a fact.
- **Temporally ordered**: Events have a before/after relationship. You can mentally "replay" sequences.
- **Context-rich**: Episodic memories include sensory details, spatial layout, emotional state, and social context. They're multimodal by nature.
- **Reconstructive, not reproductive**: You don't replay a video. You reconstruct from fragments, guided by schemas and expectations. This means episodic memories are inherently lossy and can be wrong — a property that any AI system mimicking this must also handle.
- **Subject to consolidation**: Memories strengthen during sleep/rest, important ones are stabilized, and unimportant ones fade. This is the hippocampal replay mechanism discussed below.

**Encoding specificity principle** (Tulving & Thomson, 1973): Retrieval is most successful when the cues at retrieval match the context at encoding. If you learned something in a specific room, you'll recall it better in that room. For wearable AI, this means retrieval should be biased by the user's current context (location, people present, activity) — not just the query text.

**Mapping to wearable AI**: Episodic memory is the primary long-term experience store. Every "moment" the system identifies gets compressed into an episodic record with temporal, spatial, and semantic metadata. This is the layer that answers questions like "when did I last see my keys?" or "what did Sarah say about the deadline?"

### 1.4 Semantic Memory (Tulving, 1972)

**Duration**: Long-term to permanent. **Capacity**: Vast.

Semantic memory stores *facts and knowledge* disconnected from when or where you learned them. You know Paris is the capital of France but probably can't recall the specific moment you learned it. Semantic knowledge is:

- **Decontextualized**: Stripped of episodic context. The fact stands on its own.
- **Highly compressed**: Just the essential proposition, not the surrounding experience.
- **Slow to form**: Typically requires repeated exposure or deliberate encoding. You don't learn your coworker's name from one meeting — it takes several encounters.
- **More stable than episodic memory**: Resists forgetting better. You may forget the conversation but remember the key fact that emerged from it.
- **Organized as a network**: Collins & Quillian's (1969) hierarchical network model and Collins & Loftus's (1975) spreading activation model show that semantic knowledge is organized by conceptual relationships, not temporal sequence.

**Mapping to wearable AI**: The persistent knowledge graph that accumulates over weeks and months — your coworker's name, where you usually park, what your kid's school looks like, your coffee order. Built by running consolidation over episodic memories: repeated observations get abstracted into stable facts.

### 1.5 Procedural Memory

**Duration**: Long-term. **Storage**: Basal ganglia and cerebellum (not hippocampus).

Procedural memory stores *how to do things* — skills, routines, habits. You don't consciously recall how to ride a bike; you just do it. Procedural memory is:

- **Implicit**: You can't easily verbalize it. Asking someone to explain how they balance on a bicycle yields poor instructions.
- **Slow to acquire, slow to forget**: Takes many repetitions to form but is remarkably durable.
- **Automatic**: Execution doesn't require working memory resources once learned.

**Mapping to wearable AI**: Learned behavioral patterns — you always check your phone when you sit at your desk, you always take the same route home, you always put your keys on the kitchen counter. The system can use these patterns for prediction ("you usually leave for work at 8:15") and anomaly detection ("you're leaving without your bag, which is unusual").

### 1.6 Prospective Memory

Often overlooked but critical for wearable assistants: **prospective memory** is the ability to *remember to do something in the future*. "Remember to pick up milk on the way home" or "Ask Sarah about the Q3 numbers at our 2pm meeting."

Prospective memory failures are among the most common and practically consequential memory failures in daily life. It requires maintaining an intention across a delay while engaged in other tasks — exactly the kind of thing an always-on wearable can help with.

**Mapping to wearable AI**: This is where proactive triggers shine. The system stores future intentions and fires reminders when the triggering context is detected (arriving at a location, seeing a specific person, reaching a specific time).

---

## 2. Memory Consolidation: The Critical Bridge

The most underappreciated concept — and the one that separates toy demos from real systems — is **memory consolidation**. Without a consolidation process, a wearable system either stores everything (unsustainable) or stores nothing beyond a fixed window (useless for long-term queries).

### 2.1 The Standard Consolidation Model

The dominant theory (Squire & Alvarez, 1995; McClelland, McNaughton & O'Reilly, 1995) posits two complementary learning systems:

**Hippocampus** (fast learner): Rapidly encodes new episodic memories with high fidelity. Acts as a temporary buffer. Stores specific, context-rich experiences. Has limited capacity — must offload to neocortex.

**Neocortex** (slow learner): Gradually integrates new knowledge into existing schemas. Learns statistical regularities across many experiences. Forms the basis of semantic memory. Has essentially unlimited capacity but learns slowly to avoid catastrophic interference with existing knowledge.

**The consolidation process**: During sleep (particularly slow-wave sleep), the hippocampus "replays" recently encoded experiences to the neocortex. Through repeated replay, the neocortex extracts generalizable knowledge while allowing the hippocampus to release the specific episodic trace. This is why sleep is critical for memory — it's when the brain runs its consolidation pipeline.

### 2.2 Complementary Learning Systems Theory

McClelland, McNaughton & O'Reilly's (1995) Complementary Learning Systems (CLS) theory formalized *why* the brain needs two learning systems. The core insight:

**The stability-plasticity dilemma**: A system that learns quickly (plastic) risks overwriting old knowledge with new information (catastrophic forgetting). A system that preserves old knowledge (stable) learns slowly. The brain's solution: use *both* systems with different learning rates, connected by a consolidation process.

This maps directly onto wearable AI architecture:

| Human System | AI Analog | Learning Rate | Capacity | Duration |
|---|---|---|---|---|
| Sensory buffer | Frame buffer | Instantaneous | Very high | Milliseconds–seconds |
| Working memory | Active context window | Real-time | ~4 chunks → current scene | Seconds–minutes |
| Hippocampus | Episodic memory store | Fast (single exposure) | Moderate (~days) | Hours–days |
| Neocortex | Semantic memory / knowledge graph | Slow (many exposures) | Very large | Weeks–lifetime |
| Basal ganglia | Behavioral pattern store | Very slow | Moderate | Long-term |

### 2.3 Forgetting as a Feature

Forgetting is not a failure of memory — it's a feature. The *adaptive forgetting* hypothesis (Anderson & Schooler, 1991) argues that memory systems are optimized to predict which information will be needed in the future based on patterns of past access. Information that hasn't been accessed recently or frequently gets deprioritized.

The power law of forgetting (Ebbinghaus, 1885): Memory strength decays as a power function of time since last access, modulated by number of prior accesses. This gives us a mathematical framework for designing importance/decay functions in AI memory systems.

**For wearable AI design, forgetting is essential because**:

- Storage and compute costs scale with memory size
- Retrieval quality degrades with too many irrelevant memories ("context pollution" in RAG terminology)
- Privacy concerns increase with data retention duration
- The user's own memory forgets, and a system with perfect recall can create uncomfortable asymmetries

---

## 3. Attention as a Gating Mechanism

Human perception processes an enormous amount of sensory input (~10^9 bits/second through the visual system alone) but only a tiny fraction (~50 bits/second) reaches conscious awareness. Attention is the gating mechanism that determines what gets promoted through the memory hierarchy.

### 3.1 Broadbent's Filter Model → Treisman's Attenuation

Early models (Broadbent, 1958) proposed an all-or-nothing filter: unattended information is completely blocked. Treisman (1964) softened this to attenuation: unattended information is weakened, not eliminated. High-importance signals (your name, danger cues) can break through the attenuation.

**Mapping to wearable AI**: The cascade of increasingly expensive filters:

```
Raw frames (1 FPS) → Change detection (cheap, ~1ms)
    → Scene classification (moderate, ~5ms)
    → VLM understanding (expensive, ~50-100ms)
    → Full cloud reasoning (very expensive, ~500ms-2s)
```

Each stage either passes input through or attenuates it. The goal: spend expensive compute only on information that matters. Change detection is the "early filter" — if a frame looks identical to the previous one, don't waste compute understanding it.

### 3.2 Endogenous vs. Exogenous Attention

Two types of attention are relevant:

- **Endogenous (top-down, voluntary)**: User-directed. "Look for red cars." "Pay attention to what Sarah says." This maps to the user activating live mode or issuing a specific query.
- **Exogenous (bottom-up, involuntary)**: Stimulus-driven. A sudden loud noise, a face appearing in the field of view, unexpected motion. This maps to proactive triggers — the system detects something salient and interrupts the user.

The interaction between these two types determines the wearable's behavior at any moment: is the system in passive mode (relying on exogenous attention to decide what to process) or active mode (user has directed endogenous attention to a specific query)?

---

# Part II: State of the Art — How Production Systems Work

## 4. Google Project Astra

Project Astra, first demonstrated at Google I/O 2024 and significantly upgraded in 2025, is the most ambitious always-on AI assistant currently in development. Built on top of Gemini 2.5 Pro (and now Gemini 3.0), it represents Google DeepMind's attempt to build a universal AI agent that sees, hears, remembers, and reasons.

### 4.1 Architecture

Astra's architecture rests on three pillars: **multimodal synchronicity**, **sub-300ms latency**, and **persistent temporal memory**.

**Perception pipeline**: Unlike traditional systems that process video as discrete frames, Astra treats video and audio as a continuous, unified stream. The key innovation is a hybrid inference pipeline that splits work between device and cloud:

- **On-device preprocessing**: Video frames are downsampled and cropped to regions-of-interest (ROIs) using lightweight neural nets (<5 MB RAM footprint) running on the device's NPU. This avoids uploading raw video and reduces bandwidth by ~92%.
- **Temporal compression**: Instead of analyzing every frame at 30 FPS, Astra samples at 3–5 FPS and uses optical flow algorithms to detect motion deltas between frames. Only frames with significant changes get full processing.
- **Cloud inference**: Complex reasoning and multimodal fusion run on Google's Ironwood TPUs, using the full Gemini model.
- **Cross-modal attention layers** align visual and linguistic features, while **temporal encoders** track changes over time (object movement, dialogue flow).

**Memory system**: As of the Gemini 2.0 update (December 2024), Astra maintains approximately 10 minutes of in-session video memory (up from 45 seconds in the initial prototype). It can recall details from previous sessions for cross-session personalization. The system stores three types of memory:

1. **Active context** (~10 minutes of multimodal stream): The current session's visual and auditory context, encoded as memory-augmented token streams that allow the model to "remember" what it has seen and heard.
2. **Session memory**: Cross-session recall of user preferences, past interactions, and established facts.
3. **Tool-grounded memory**: Integration with Google Search, Maps, Lens, Gmail, and Calendar for factual augmentation.

**Latency architecture**: Astra achieves sub-300ms response times through:

- On-device wake word detection and basic object recognition (Edge TPU)
- Streaming inference via Gemini's native audio understanding
- Pre-computed visual feature caches that avoid re-encoding stable scene elements

### 4.2 Key Capabilities

- Identifies objects in real-world context using camera input and provides contextual highlights
- Understands and ignores distractions like background conversation and irrelevant speech
- Uses deep reasoning over multi-turn visual context
- Integrates with Google ecosystem tools for task completion
- Prototype glasses form factor for hands-free, immersive operation

### 4.3 Current Limitations

- 10-minute active memory is still far short of true all-day recall
- No public documentation on consolidation or long-term memory formation
- Cross-session memory appears to be text-based summaries, not visual recall
- Limited to Google ecosystem for tool integration
- Privacy architecture largely undisclosed

---

## 5. ChatGPT's Memory Architecture

OpenAI's approach to persistent memory is the most widely deployed consumer memory system as of 2025, offering a useful contrast to vision-first approaches.

### 5.1 The Four-Layer Architecture

Reverse-engineering analysis suggests ChatGPT's memory system is surprisingly simple — no vector database, no RAG over full conversation histories. It operates on four layers:

**Layer 1: Session Metadata (Ephemeral)**

Each conversation carries lightweight metadata: conversation ID, timestamp, model version. This is stateless and discarded after the session.

**Layer 2: Current Conversation Window (Sliding)**

The complete, un-summarized history of all messages in the current session. Operates on a token-based cap (not message count). When the limit is reached, older messages roll off on a FIFO basis. Crucially, when messages roll off, the persistent layers (Saved Memories and Recent Conversation Summaries) remain in context.

**Layer 3: Saved Memories (Persistent Facts)**

A dedicated store of stable, explicit facts about the user. These are stored under specific conditions: direct user command ("remember this"), or model detection of information fitting pre-defined criteria (name, job title, preferences) with implicit user confirmation. As of mid-2025, users typically accumulate 20-50 saved memories. These are injected into every future prompt as a separate text block.

**Layer 4: Recent Conversation Summaries (Lightweight)**

Pre-computed summaries of recent conversations, injected into context alongside saved memories. This is a deliberate trade-off: sacrificing granular historical context for massive gains in speed and token efficiency. ChatGPT does not perform RAG over full conversation histories — it summarizes them in advance.

### 5.2 Design Philosophy

ChatGPT's memory system prioritizes:

- **Simplicity**: No complex retrieval pipelines. Memories are text strings injected into the prompt.
- **User control**: Explicit management of what's remembered. Users can view, edit, and delete memories.
- **Efficiency**: Pre-computed summaries avoid expensive retrieval at inference time.
- **Two-mode operation**: "Saved memories" (explicit, always-on) and "chat history" (implicit, derived from past chats).

### 5.3 What ChatGPT Lacks (and Why It Matters for Wearables)

- No visual memory whatsoever (text-only)
- No spatial or temporal grounding (doesn't know where or when events happened)
- No episodic structure (memories are flat facts, not contextualized experiences)
- No consolidation process (memories don't evolve or compress over time)
- No proactive recall (never surfaces information without being asked)
- No working memory model (can't track current context beyond conversation)

These gaps define precisely what a wearable memory system must add.

---

## 6. MemGPT: LLMs as Operating Systems

The MemGPT paper (Packer et al., 2023) introduced the most influential architectural framework for LLM memory management. Originally evolved into the Letta platform, MemGPT draws a direct analogy between operating system virtual memory and LLM context management.

### 6.1 Core Insight

LLMs have a fixed context window analogous to physical RAM. Just as an operating system creates the illusion of unlimited memory by paging between RAM and disk, MemGPT creates the illusion of unlimited conversational context by paging between "main context" (the LLM's prompt) and "external context" (databases).

### 6.2 Architecture

**Main Context (analogous to RAM)**:

- System instructions (fixed, always present)
- Working context (editable by the LLM itself — core facts and current state)
- FIFO message queue (recent conversation turns)

**External Context (analogous to disk)**:

- **Recall storage**: Complete history of all messages processed, stored in a database with full-text and semantic search. This is the "page file" — when messages roll off the FIFO queue, they're stored here indefinitely.
- **Archival storage**: Long-term storage for important information that the LLM explicitly decides to save. Uses a vector database (LanceDB) for semantic search across the entire memory space.

**The LLM as Memory Manager**: The most innovative aspect — the LLM itself decides what to page in and out. Through tool calls, it can:

- Read from recall/archival storage when it needs historical context
- Write to working context or archival storage when it encounters important information
- Search across its memory using semantic queries
- Chain multiple memory operations together via a "heartbeat" mechanism

### 6.3 Memory Pressure and Forgetting

When the main context approaches capacity, MemGPT implements a "memory pressure" warning system:

1. At 75% capacity: Warning injected, LLM has opportunity to save important information
2. At 100% capacity: Queue manager flushes ~50% of the oldest messages
3. Flushed messages are: (a) summarized recursively, (b) stored to recall storage

This creates a natural compression pipeline: recent conversations exist in full fidelity, older ones exist as progressively compressed summaries, and the oldest exist only in archival storage accessible via search.

### 6.4 Key Contribution

MemGPT demonstrated that **self-directed memory management** — where the LLM decides what to remember and forget — outperforms fixed strategies. The system achieves "cognitive triage" by having the LLM evaluate the future value of information fragments. Important preferences, project details, and personal facts get high priority for retention; transient conversational elements get compressed or dropped.

---

## 7. Limitless (formerly Rewind) — Acquired by Meta, December 2025

Limitless represents the most commercially mature always-on memory wearable, and its acquisition by Meta signals the direction of the industry.

### 7.1 Architecture

**Hardware**: A 1.25-inch aluminum pendant with beamforming microphone array, IPX4 weatherproofing, ~100-hour battery life, USB-C charging, Bluetooth connectivity to phone.

**Capture pipeline**: Audio-first (no camera). Continuous recording → on-device noise reduction → streaming to phone → cloud transcription → speaker diarization → AI summarization.

**Memory system**:

- **Raw audio**: Stored with full fidelity, searchable by speaker, topic, and time
- **Transcripts**: Full text transcripts with speaker labels (trained on 20 seconds of labeled audio per speaker)
- **Summaries**: AI-generated daily summaries, meeting notes, action items, and key highlights
- **Queryable memory**: Users can ask natural language questions against their entire history ("What did we decide about the Q3 deadline?")

**API**: Limitless exposed a structured API for accessing "lifelogs" — conversation records as structured data, enabling integration with ChatGPT, Claude, and other systems via MCP (Model Context Protocol).

### 7.2 Key Lessons

- **Audio-only is a viable starting point**: The pendant proved that ambient audio capture alone generates enormous value without the privacy complexity of cameras.
- **Speaker diarization is essential**: Knowing *who* said what transforms raw transcripts into actionable memory.
- **The "Rewind" pivot matters**: Limitless started as desktop screen capture (logging everything on your computer) before pivoting to audio-only wearable. The lesson: capture everything → capture the right thing.
- **Meta acquisition context**: Meta acquired Limitless specifically to fold its always-on recording technology into Ray-Ban Meta smart glasses and future AR hardware. This signals that the major platforms see wearable memory as a core capability, not a niche product.

### 7.3 What Limitless Lacks

- No visual understanding (audio only)
- No spatial awareness (doesn't know where conversations happen)
- No proactive triggers (purely reactive — user must ask)
- No episodic structure (conversations are flat logs, not contextualized episodes)
- Limited consolidation (summaries but no progressive compression or semantic extraction)

---

## 8. Meta Project Aria — Research Infrastructure for Wearable AI

Project Aria is Meta's research glasses platform, not a consumer product, but it defines the sensor and perception capabilities that future wearable AI systems will build upon. Now in Gen 2, with ~300 academic labs using ~1,000+ devices globally.

### 8.1 Sensor Suite (Aria Gen 2)

- **4 computer vision cameras** (double Gen 1): Global shutter, 120dB HDR, 80° stereo overlap (up from 35°)
- **IMU sensors**: Accelerometer, gyroscope for motion tracking
- **Magnetometer**: Compass heading
- **Barometer**: Altitude/floor detection
- **Microphones**: Array for spatial audio and voice capture
- **Eye tracking cameras**: Gaze direction and attention inference
- **GPS**: Outdoor positioning
- **On-device compute**: NPU for real-time SLAM, hand tracking, and machine perception

### 8.2 Machine Perception Capabilities

- **Visual-Inertial Odometry (VIO)**: Real-time 6-DOF position tracking combining camera and IMU data
- **SLAM**: Simultaneous localization and mapping — building 3D maps of the environment in real-time
- **Hand tracking**: Full articulated hand pose estimation from egocentric view
- **Eye tracking**: Where the user is looking, enabling gaze-based attention inference
- **3D scene reconstruction**: Using stereo cameras and Gaussian Splatting for detailed environment models

### 8.3 Research Contributions

The Aria platform has enabled foundational datasets:

- **Ego-Exo4D**: Large-scale dataset pairing egocentric (wearable) and exocentric (external camera) views of the same activities — critical for training models that understand human activity from a first-person perspective.
- **City-scale VIO datasets**: For improving trajectory estimation from on-device sensors.
- **3D object reconstruction**: 6,000+ 3D objects with Aria captures for egocentric reconstruction research.

### 8.4 Why Aria Matters for Memory Architecture

Aria provides the sensor data streams that a memory system must process: continuous egocentric video, spatial audio, precise location, gaze direction, and motion data. The research community building on Aria is solving the upstream perception problems (what am I looking at? where am I? who is around me?) that feed into the memory layers.

---

## 9. MIT Memoro — Academic Validation of Wearable Memory Augmentation

Memoro (Zulfikar, Chan & Maes, CHI 2024) is the most rigorously studied wearable memory assistant in the academic literature. While simpler than production systems, it provides critical empirical validation.

### 9.1 Architecture

- **Hardware**: Bone-conduction headset (audio-only, audio in and out)
- **Capture**: Continuous audio transcription and semantic encoding
- **Memory**: Vector embeddings of transcribed segments, stored in a searchable database
- **Retrieval**: LLM-powered semantic search with two modes:
  - **Query Mode**: User voices a natural language question
  - **Queryless Mode**: System monitors conversational context and proactively surfaces relevant memories without being asked

### 9.2 Key Findings (N=20 study)

- Memoro reduced device interaction time while increasing recall confidence
- Conversational quality was preserved (users didn't seem distracted)
- 15 of 20 participants preferred Memoro over no system
- **10 of 20 preferred Queryless Mode** — the proactive, context-driven mode. This is a strong signal that users value proactive memory surfacing, not just reactive querying.
- Mean usability score of 80.0 (between "good" and "excellent" on the System Usability Scale)

### 9.3 Design Principles Validated

- **Conciseness matters**: Minimal, targeted memory responses outperform verbose dumps. The system should surface a key fact, not read back an entire conversation.
- **Context awareness is essential**: Responses grounded in the current conversational context were significantly preferred over keyword-based retrieval.
- **Proactive > reactive for many users**: The fact that half of participants preferred queryless mode suggests that the ideal wearable memory system doesn't wait to be asked — it anticipates needs.

---

## 10. Generative Agents (Park et al., 2023)

The Stanford "Generative Agents" paper introduced the most influential agent memory architecture, simulating 25 virtual characters in a Sims-like sandbox with emergent social behavior driven by memory, planning, and reflection.

### 10.1 Memory Architecture

Each agent maintains:

- **Memory stream**: A timestamped list of all observations (episodic log). Each entry includes: natural language description, creation timestamp, and most recent access timestamp.
- **Retrieval function**: Scores memories using three weighted components:
  - **Recency** (rule-based): Exponential decay based on time since last access
  - **Importance** (LLM-based): A 1-10 score assigned by the LLM at encoding time ("eating breakfast" = 1, "learning about a breakup" = 8)
  - **Relevance** (embedding-based): Cosine similarity between memory embedding and current query/context embedding
- **Reflection**: Periodically, the agent generates higher-order "reflections" by querying its recent memories and asking the LLM to synthesize insights. These reflections (semantic memory) are stored back into the memory stream alongside raw observations (episodic memory), creating a hierarchy of abstraction.

### 10.2 The Retrieval Score

```
score(memory) = α × recency(memory) + β × importance(memory) + γ × relevance(memory, query)
```

Where α, β, γ are tunable weights. This simple formula proved remarkably effective at surfacing the right memories at the right time, and has been widely adopted and extended in subsequent work.

### 10.3 Why This Matters

The Generative Agents paper demonstrated that the combination of episodic memory + reflection-based consolidation + multi-factor retrieval produces emergent intelligent behavior: agents organized a Valentine's Day party, formed relationships, and coordinated schedules — all from memory-driven reasoning. The architecture has become the de facto starting point for agent memory design.

---

## 11. CoALA: Cognitive Architectures for Language Agents

The CoALA framework (Sumers et al., 2023) provides a unifying taxonomy for understanding how all of these systems relate to each other and to cognitive science.

### 11.1 The Framework

CoALA defines a language agent through:

- **Memory modules**: Working memory (current context), episodic memory (experiences), semantic memory (facts), procedural memory (skills/code)
- **Action types**: Grounding (interacting with environment), reasoning (internal inference), retrieval (reading from memory), learning (writing to memory)
- **Decision cycle**: Retrieve → reason → propose actions → evaluate → execute → observe → repeat

### 11.2 Mapping Existing Systems

| System | Working Memory | Episodic Memory | Semantic Memory | Procedural Memory | Retrieval Method |
|---|---|---|---|---|---|
| Generative Agents | Current plan + observations | Full memory stream | Reflections | Fixed code | Recency + Importance + Relevance |
| MemGPT | FIFO queue + working context | Recall storage | Archival storage | System prompt | LLM-directed search |
| Voyager | Current state | None | None | Skill library (code) | Dense retrieval |
| ReAct | Recent reasoning | None | None | Fixed prompts | None |
| ChatGPT Memory | Current conversation | Chat history summaries | Saved memories | System instructions | Pre-injection |
| Project Astra | 10-min multimodal buffer | Cross-session recall | Tool-grounded knowledge | Google services | Unknown |

### 11.3 Gaps This Reveals

No production system fully implements the complete cognitive architecture. The biggest gaps:

- **Consolidation pathways**: No system has a principled pipeline for converting episodic → semantic memory
- **Procedural learning**: No system learns new *skills* from experience (only Voyager comes close, in a limited domain)
- **Multimodal episodic memory**: Only Astra attempts visual episodic memory, and its 10-minute window is extremely limited
- **Adaptive forgetting**: Most systems either keep everything or use crude FIFO eviction

---

# Part III: System Architecture for an Always-On Wearable

## 12. The Full Memory Stack

Drawing from all of the above — cognitive science, production systems, and research papers — here is a comprehensive architecture for an always-on AI wearable assistant with two modes (passive 1 FPS and active live mode).

### 12.1 Layer 0: Sensory Buffer (On-Device, Always-On)

**Cognitive analog**: Iconic/echoic memory

```
Input:
  - Camera frames at 1 FPS (passive) or 5-30 FPS (active/live mode)
  - Audio stream (always-on, ambient)
  - IMU data (accelerometer, gyroscope)
  - GPS/WiFi location
  
Storage: Circular buffer
  - Visual: Last 30-60 seconds of raw frames (~1.5-3MB)
  - Audio: Last 60 seconds of raw PCM audio (~960KB at 16kHz)
  - IMU: Last 5 minutes of motion data (~50KB)
  
Processing: Zero inference. Pure acquisition.
Power: Dominated by camera sensor, not compute (~20mW)
```

**Why a sensory buffer matters**: When the system detects something interesting at Layer 1, it can "rewind" to see/hear what happened in the seconds before detection fired. This is the dashcam principle — you don't know what's important until after it happens.

### 12.2 Layer 1: Perceptual Processing (On-Device, Edge NPU)

**Cognitive analog**: Pre-attentive feature extraction

This layer transforms raw sensor data into semantic representations. Pixels become meaning.

**Visual embedding pipeline**:

```
Frame → Resize (640x480)
      → Lightweight encoder (MobileCLIP-S2, ~35M params, ~3ms on NPU)
      → 512-dim CLIP embedding (vision-language aligned)
      
Parallel: → DINOv2-small (~22M params, ~2ms)
          → 384-dim structural embedding (for change detection)
          
Parallel (conditional): → Face detector (RetinaFace-mobile, ~5ms)
                        → Face encoder (MobileFaceNet) → 128-dim face embedding
                        → Gallery matching
```

**Change detection** (the primary attention gating mechanism):

```python
def should_promote_frame(current_emb, previous_emb, scene_emb):
    """Analogous to exogenous attention — detect salient change."""
    
    # Frame-to-frame delta (something just happened)
    frame_delta = 1 - cosine_similarity(current_emb, previous_emb)
    
    # Scene drift (gradual change from current context)
    scene_delta = 1 - cosine_similarity(current_emb, scene_emb)
    
    # Promote if significant immediate change OR gradual scene shift
    return frame_delta > 0.15 or scene_delta > 0.30
```

**Audio processing pipeline**:

```
Audio stream → Voice Activity Detection (VAD, on-device, ~1ms)
            → [If speech detected]:
                → Speaker embedding (ECAPA-TDNN, on-device)
                → Streaming ASR (Whisper-tiny or on-device model)
                → Speaker diarization (match against known speakers)
```

**Model selection rationale**: Two encoders serve different purposes. CLIP-family embeddings live in a shared vision-language space, enabling natural language queries against visual memories. DINOv2-family embeddings capture spatial/structural information better, making them superior for change detection and scene similarity. Running both costs ~5ms total on a modern mobile NPU.

### 12.3 Layer 2: Working Memory (On-Device, RAM)

**Cognitive analog**: Baddeley's working memory model

Working memory maintains the current context — answering "what is happening right now?" at all times.

**Data structure**:

```
WorkingMemory {
    // Current scene (continuously updated, ~1/second)
    current_scene: {
        mean_embedding: [512-dim],         // Running average of CLIP embeddings
        structural_embedding: [384-dim],    // Running average of DINOv2 embeddings
        keyframe: JPEG,                     // Most representative recent frame
        scene_label: String,               // "office", "kitchen", "car", "outdoor"
        start_time: Timestamp,
        entities_present: [Entity],        // People, objects currently detected
        activity_hypothesis: String,       // "meeting", "cooking", "commuting"
    }
    
    // Recent scene history (ring buffer, last ~5 minutes)
    recent_scenes: RingBuffer<Scene, MAX=20> {
        each: {
            summary_embedding: [512-dim],
            keyframe: JPEG,
            time_range: (Timestamp, Timestamp),
            caption: String,              // Generated on-device if VLM available
            entities: [Entity],
        }
    }
    
    // Active entities (people in view or recently seen)
    active_entities: HashMap<EntityId, EntityContext>
    
    // Spatial context
    location: { gps, semantic_place, indoor_position }
    
    // User state (from IMU + scene understanding)
    user_state: { activity, attention_target, social_context }
    
    // Pending intentions (prospective memory)
    pending_triggers: Vec<ProactiveTrigger>
}
```

**Update rules**: Working memory updates at different rates for different components:

- `current_scene`: Every frame (1 FPS)
- `recent_scenes`: On scene transitions (change detection trigger)
- `active_entities`: When faces enter/exit field of view
- `location`: On GPS/WiFi changes
- `user_state`: From IMU (100Hz) and scene classification (1Hz)

**All queries against working memory must resolve in <10ms** (on-device, in-memory). This is non-negotiable for reactive reasoning about the current context.

### 12.4 Layer 3: Episodic Memory (Edge + Cloud)

**Cognitive analog**: Hippocampal episodic memory

The primary long-term store of experiences. This is the layer that makes a wearable *remember*.

**Episode structure**:

```
Episode {
    id: UUID,
    
    // Temporal bounds
    start_time: Timestamp,
    end_time: Timestamp,
    duration_seconds: u32,
    
    // Spatial context
    location: GeoPoint,
    semantic_place: String,           // "Blue Bottle Coffee, downtown"
    
    // Visual summary
    keyframes: Vec<{                  // 1-5 representative frames
        timestamp: Timestamp,
        jpeg_thumbnail: Bytes,        // 320x240, ~15KB each
        clip_embedding: [512-dim],    // For vision-language retrieval
    }>,
    mean_embedding: [512-dim],        // Average for coarse search
    
    // Semantic content
    caption: String,                  // VLM-generated description
    entities: Vec<EntityReference>,   // People, objects, documents seen
    topics: Vec<String>,              // Extracted themes
    
    // Audio content (if captured)
    transcript_summary: Option<String>,
    speakers: Vec<SpeakerReference>,
    
    // Memory management metadata
    importance_score: f32,            // 0-1, for consolidation
    access_count: u32,                // Times retrieved
    last_accessed: Timestamp,
    consolidation_level: u8,          // 0=full → 4=facts_only
    emotional_valence: Option<f32>,   // Inferred emotional significance
}
```

**Episode boundary detection**: Inspired by event segmentation theory (Zacks & Tversky, 2001), which shows that humans naturally segment continuous experience into discrete events at points of significant change:

```python
class EpisodeBoundaryDetector:
    """Segments continuous experience into discrete episodes."""
    
    def on_scene_transition(self, old_scene, new_scene):
        similarity = cosine_similarity(old_scene.embedding, new_scene.embedding)
        
        # Strong scene change → close current episode
        if similarity < 0.5:
            self.close_episode()
            self.start_episode(new_scene)
        
        # Moderate change → extend current episode (sub-event)
        elif similarity < 0.85:
            self.extend_episode(new_scene)
        
        # Hard cap: close episodes exceeding 30 minutes
        if self.current_duration() > 1800:
            self.close_episode()
            self.start_episode(new_scene)
    
    def close_episode(self):
        episode = self.build_episode(self.scene_buffer)
        
        # Discard trivially short, uninteresting episodes
        if episode.duration < 30 and episode.importance_score < 0.3:
            return
        
        episode.caption = self.generate_caption(episode)
        episodic_memory.store(episode)
```

**Multi-axis retrieval** (this is fundamentally a search problem):

| Index | Type | Query Example | Latency |
|---|---|---|---|
| Temporal | B-tree on timestamps | "What happened yesterday morning?" | <5ms |
| Semantic | HNSW on CLIP embeddings | "When did I see a red car?" | <50ms |
| Entity | Inverted index on entity IDs | "All episodes with Sarah" | <10ms |
| Spatial | Geohash or R-tree | "What happened at the office?" | <10ms |
| Full-text | BM25 on captions + transcripts | "Meeting about Q3 roadmap" | <20ms |

At query time, multiple axes are combined: temporal filters narrow the candidate set cheaply, then semantic search ranks within the filtered set, then a cross-encoder re-ranks the top results.

**Storage tiers and consolidation** (implementing the complementary learning systems model):

```
Level 0 (< 1 day): Full fidelity
    All keyframes, full embeddings, detailed caption
    ~50-200KB per episode

Level 1 (1-7 days): Compressed
    Best 1-2 keyframes, full caption
    ~20-50KB per episode

Level 2 (7-30 days): Summary
    Single thumbnail, condensed caption
    ~5-10KB per episode

Level 3 (30-90 days): Facts only
    No visual data, embedding retained, fact-extracted
    ~1-2KB per episode

Level 4 (> 90 days): Semantic extraction + discard
    Episode deleted, stable facts extracted to semantic memory
    Only "landmark" episodes survive at Level 2
```

**Storage math**: ~200 episodes/day (one every ~5 waking minutes):

| Time range | Episodes | Avg size | Total |
|---|---|---|---|
| Today | 200 | 100KB | 20MB |
| This week | 1,400 | 35KB | 49MB |
| This month | 6,000 | 8KB | 48MB |
| Last 3 months | 18,000 | 1.5KB | 27MB |
| **Total** | **~25,000** | | **~150MB** |

Vector index (25K × 512-dim float32) = ~50MB. Entire episodic memory fits comfortably on-device, let alone in the cloud.

### 12.5 Layer 4: Semantic Memory (Cloud, Persistent)

**Cognitive analog**: Neocortical knowledge store

Stable, decontextualized knowledge about the user's world, built by consolidation from episodic memory.

**Core stores**:

```
SemanticMemory {
    people: KnowledgeGraph<Person> {
        // Name, face embeddings, relationship, organization, role,
        // usual locations, interaction frequency, known facts,
        // connections to other people
    }
    
    places: SpatialKnowledgeBase {
        // Named locations with visit patterns, associated people/activities,
        // visual signatures for recognition
    }
    
    objects: HashMap<ObjectId, Object> {
        // Important objects: keys, wallet, bag, car
        // Last known location, visual embedding, importance score
    }
    
    routines: Vec<Routine> {
        // Learned behavioral patterns with typical sequences,
        // timing, and deviation history
    }
    
    preferences: HashMap<String, Preference> {
        // Learned preferences: coffee order, preferred routes,
        // communication style, dietary restrictions
    }
}
```

**Consolidation pipeline** (runs during idle/charging periods — analogous to sleep consolidation):

```python
class MemoryConsolidator:
    """Implements complementary learning systems: episodic → semantic."""
    
    def run_nightly_consolidation(self):
        recent = episodic_memory.get_episodes(last_n_days=1)
        
        # 1. Entity consolidation
        for episode in recent:
            for entity in episode.entities:
                if entity.type == "person" and entity.name:
                    semantic_memory.update_person(entity, episode)
        
        # 2. Place learning (cluster frequent locations)
        location_clusters = cluster_episode_locations(
            episodic_memory.get_episodes(last_n_days=30)
        )
        for cluster in location_clusters:
            if cluster.visit_count > 3:
                semantic_memory.add_or_update_place(cluster)
        
        # 3. Routine detection (find repeating temporal patterns)
        detect_routines(episodic_memory.get_episodes(last_n_days=30))
        
        # 4. Object tracking
        for episode in recent:
            for entity in episode.entities:
                if entity.type == "object" and entity.importance > 0.5:
                    semantic_memory.update_object_location(entity, episode)
        
        # 5. Fact extraction (LLM summarization)
        week_summary = summarize_period(
            episodic_memory.get_episodes(last_n_days=7)
        )
        new_facts = llm.extract_stable_facts(week_summary)
        semantic_memory.merge_facts(new_facts)
        
        # 6. Forgetting (compress old episodes)
        run_compression_schedule()
```

**Importance scoring** (implementing the power law of forgetting with multiple signals):

```python
def importance_score(episode: Episode) -> float:
    score = 0.0
    
    # Recency (exponential decay, ~7-day half-life)
    age_days = (now() - episode.end_time).days
    score += 0.25 * math.exp(-age_days / 7)
    
    # Access frequency (retrieved = important)
    score += 0.20 * min(episode.access_count / 5, 1.0)
    
    # Social significance (interactions with known people)
    known_people = [e for e in episode.entities if e.name]
    score += 0.15 * min(len(known_people) / 3, 1.0)
    
    # Novelty (how different from typical episodes at this location)
    if episode.semantic_place:
        typical = semantic_memory.get_place_signature(episode.semantic_place)
        novelty = 1 - cosine_similarity(episode.mean_embedding, typical)
        score += 0.15 * novelty
    
    # User signal (explicitly flagged or photographed)
    if episode.user_flagged:
        score += 0.25
    
    # Emotional significance
    score += 0.10 * episode.emotional_valence
    
    return min(score, 1.0)
```

### 12.6 Layer 5: Procedural/Pattern Memory (Cloud)

**Cognitive analog**: Basal ganglia procedural memory

Learned behavioral patterns enabling prediction and proactive assistance:

```
Pattern: "Morning Routine"
  Typical: Wake → Kitchen (coffee) → Desk (email) → Shower → Dress → Car
  Timing: 6:30-7:45 AM weekdays
  Learned from: 47 observations
  Proactive triggers:
    - Still in kitchen at 7:30 → "Running late, first meeting at 8:30"
    - Left house without keys → "Keys are on the counter"

Pattern: "Pre-Meeting Prep"
  Typical: 5 min before → check calendar → open docs → walk to room
  Proactive triggers:
    - 10 min before meeting with Sarah → surface last meeting's action items
    - Walking to wrong room → "Meeting moved to Room 204"
```

Procedural patterns require many observations (high confidence threshold) and conservative trigger policies (false positives are extremely annoying for proactive assistance).

---

## 13. The Two-Mode Architecture

### 13.1 Passive Mode (1 FPS, Always-On)

```
Power budget: < 50mW continuous
Compute: Edge NPU only, no cloud calls
Latency: Not latency-sensitive (can lag by seconds)

Pipeline per frame:
  Camera (1 FPS) → Resize (640x480)              [<1ms]
    → Encode (MobileCLIP + DINOv2)                [~5ms]
    → Change detection                             [~1ms]
    → [If significant change]:
        → Update working memory                    [~1ms]
        → Face detection + matching                [~5ms]
        → Proactive trigger evaluation             [~2ms]
        → [If episode boundary]: Finalize + store
    → [If no change]:
        → Update scene running average             [~1ms]
        → Keep embedding, discard frame

Total per-frame: 4-15ms on NPU
```

### 13.2 Live Mode (User-Activated)

```
Power budget: Full device power
Compute: Edge NPU + cloud inference
Latency: Critical — user is waiting

Activation: Voice command, button press, or proactive trigger

Pipeline:
  Camera (5-30 FPS, higher resolution)
    → Full resolution encoding
    → On-device VLM for immediate description       [<100ms]
    → Stream to cloud for reasoning                  [<500ms first token]
    → Full RAG over all memory layers
    → Audio capture + real-time transcription
    → Response generation with full context           [<2s total]
```

### 13.3 Mode Transition (The "Rewind" Moment)

```python
def transition_to_live_mode(trigger):
    # 1. Snapshot working memory
    context = working_memory.snapshot()
    
    # 2. Grab sensory buffer (last 30s of frames + audio)
    recent = sensory_buffer.get_last_n_seconds(30)
    
    # 3. Run higher-quality encoding on buffer ("hindsight processing")
    enhanced = process_buffer_at_high_quality(recent)
    
    # 4. Pre-fetch likely-needed episodic memories
    prefetched = episodic_memory.prefetch(
        location=context.location,
        entities=context.active_entities,
        activity=context.user_state.activity,
        k=20
    )
    
    # 5. Activate audio capture + enter interactive loop
    audio_stream.start()
```

---

## 14. The Reasoning Layer

### 14.1 Reactive Reasoning (User-Initiated)

When the user asks a question:

1. **Parse intent** and identify which memory axes to query
2. **Retrieve from memory hierarchy** (cheapest first): working memory → episodic → semantic
3. **Ground an LLM response** in retrieved context
4. **Update importance signals** based on which memories were accessed

The retrieval follows the Generative Agents scoring pattern:

```
score(memory, query) = α × recency(memory)
                     + β × importance(memory) 
                     + γ × relevance(memory, query)
                     + δ × context_match(memory, current_context)
```

The last term (context_match) implements Tulving's encoding specificity principle — memories formed in a similar context to the current one should be ranked higher.

### 14.2 Proactive Reasoning (System-Initiated)

The system monitors the context stream and fires insights using a trigger architecture:

**Trigger types**:

- **Person recognition**: Known person enters view → surface last interaction context
- **Object reminder**: Leaving a location → check if important objects were last seen there
- **Routine deviation**: Behavior deviates from learned pattern → alert if meaningful
- **Prospective memory**: Context matches a stored intention → fire reminder
- **Repeated exposure**: User has looked at something multiple times → offer to help
- **Temporal trigger**: Time matches a scheduled event → surface preparation context

**Interrupt appropriateness model** (critical for user experience):

```python
def is_appropriate_to_interrupt(working_memory, insight):
    # Never interrupt active conversations (unless critical)
    if working_memory.social_context == "one_on_one" and insight.urgency < 0.9:
        return False
    
    # Don't interrupt focus activities
    if working_memory.activity in ["reading", "writing", "coding"]:
        return False
    
    # Rate limit: max 3 proactive insights per hour
    if recent_interrupt_count(last_hour=True) >= 3:
        return insight.urgency > 0.95
    
    # Transition moments are ideal (Memoro finding)
    if scene_transition_recent or activity == "walking":
        return True
    
    return insight.confidence > 0.9 and insight.urgency > 0.5
```

---

## 15. Privacy Architecture

### 15.1 Data Residency Rules

```
ON-DEVICE ONLY (never leaves the device):
  ✓ Raw camera frames
  ✓ Raw audio
  ✓ Face embeddings and gallery
  ✓ Sensory buffer
  ✓ Working memory (full fidelity)

ENCRYPTED, CLOUD-STORED:
  ✓ Episode records (thumbnails + embeddings + captions, no raw frames)
  ✓ Semantic memory (knowledge graph)
  ✓ Behavioral patterns (routines)
  ✓ Audio transcripts (not raw audio)

NEVER STORED:
  ✗ Continuous raw video
  ✗ Faces of unrecognized bystanders
  ✗ Content of others' screens/documents
  ✗ Conversations where recording wasn't consented
```

### 15.2 Consent and Bystander Protection

The Limitless acquisition and EU AI Act scrutiny have made bystander privacy a first-order design concern:

- Unrecognized faces: Embeddings computed for matching, immediately discarded if no match
- Sensitive locations (bathrooms, changing rooms): Capture pauses entirely (detected via location + scene classification)
- Physical consent indicator: Device must have a visible "recording" signal (LED, physical switch)
- User controls: "Pause," "delete last N minutes," "forget person/place/episode," full data export/delete

### 15.3 Technical Mechanisms

- **On-device-first processing**: Raw frames never leave the device
- **Differential privacy**: Calibrated noise added to embeddings before cloud upload
- **Federated learning**: Model improvements trained on-device, only gradient updates sent to cloud
- **Encryption at rest and in transit**: Industry-standard for all cloud-stored data

---

## 16. Open Research Problems

### 16.1 Memory Consolidation Pathways

No production system has a principled pipeline for episodic → semantic consolidation. Current approaches use simple time-based compression. Research directions (from the ICLR 2026 MemAgents workshop proposal):

- How should transient experiences be consolidated into lasting knowledge?
- What algorithms allow information to persist across an agent's lifetime?
- How do we balance explicit memory (text/graphs) with in-weights implicit knowledge?

### 16.2 The Forgetting Problem

The MaRS paper (2025) formalized six forgetting policies (FIFO, LRU, Priority Decay, Reflection-Summary, Random-Drop, Hybrid) and showed the Hybrid approach works best — but only evaluated in text-only simulations. Visual memory forgetting remains unstudied.

### 16.3 Embedding Drift

Models improve over time. Embeddings computed 6 months ago with MobileCLIP v1 aren't compatible with MobileCLIP v2. Options:

- Store model version with every embedding + maintain compatibility matrices
- Re-encode keyframe images when models update (only works for Level 0-2 episodes)
- Train lightweight adapter networks to project between embedding spaces

### 16.4 Multimodal Memory Retrieval

How do you query across modalities? "What did Sarah say about the thing on the whiteboard?" requires fusing person identity (face), visual content (whiteboard), and audio (speech) into a single retrieval query. This is an active research area with no dominant approach.

### 16.5 Evaluation

The field lacks standardized benchmarks. Proposed evaluation framework:

| Metric | Target |
|---|---|
| Recall accuracy (< 7 days) | > 90% |
| Recall accuracy (< 30 days) | > 70% |
| Working memory query latency | < 10ms |
| Episodic retrieval latency | < 500ms |
| Proactive trigger precision | > 60% |
| Proactive trigger recall | > 40% |
| Storage per day (post-consolidation) | < 5MB |
| Power (passive mode) | < 5% battery/hour |
| Privacy: zero raw frame leakage | 100% |

---

## 17. Key Papers & Systems Reference

| Paper / System | Year | Core Contribution |
|---|---|---|
| Tulving, "Episodic and Semantic Memory" | 1972 | Foundational memory taxonomy |
| Baddeley, "The Episodic Buffer" | 2000 | Working memory model with integration component |
| McClelland et al., "Complementary Learning Systems" | 1995 | Dual-system theory: hippocampus + neocortex |
| Anderson & Schooler, "Reflections of the Environment" | 1991 | Adaptive forgetting / power law of memory |
| Park et al., "Generative Agents" | 2023 | Episodic memory + reflection for emergent agent behavior |
| Packer et al., "MemGPT: LLMs as Operating Systems" | 2023 | Virtual context management, self-directed memory |
| Sumers et al., "CoALA: Cognitive Architectures for Language Agents" | 2023 | Unifying framework for agent memory design |
| Zulfikar et al., "Memoro" (CHI 2024) | 2024 | Empirical validation of wearable memory augmentation |
| MaRS, "Forgetful but Faithful" | 2025 | Formalized forgetting policies with privacy guarantees |
| A-MEM, "Agentic Memory for LLM Agents" | 2025 | Zettelkasten-inspired interconnected memory networks |
| CAST, "Character-and-Scene Episodic Memory" | 2025 | Scene-grounded episodic retrieval architecture |
| AriGraph | 2025 | Knowledge graph world model with episodic+semantic memory |
| Google Project Astra | 2024-25 | Production multimodal wearable with 10-min visual memory |
| Meta Project Aria Gen 2 | 2025 | Research glasses with 4-camera egocentric sensing |
| Limitless Pendant (acquired by Meta) | 2024-25 | Commercial always-on audio memory wearable |
| OpenAI ChatGPT Memory | 2024-25 | Production 4-layer text memory architecture |

---

## 18. Interview-Ready Summary

The memory and reasoning layer for an always-on wearable AI assistant is fundamentally a **cognitive architecture** that must solve five problems simultaneously:

1. **Attention** (what to process): A cascade of increasingly expensive filters, from cheap change detection to full VLM understanding. The system should spend 90% of its compute on 10% of the most interesting moments.

2. **Encoding** (how to represent experiences): Multimodal embeddings (CLIP for language-aligned retrieval, DINOv2 for structural understanding, speaker embeddings for people) that compress rich experience into compact, searchable vectors.

3. **Storage** (where to put memories): A hierarchy from volatile sensory buffers through working memory, episodic memory, and semantic memory — each with different capacities, access speeds, and lifetimes.

4. **Consolidation** (how memories evolve): The episodic → semantic pathway that compresses specific experiences into general knowledge, implementing adaptive forgetting so the system remains useful at scale.

5. **Retrieval** (how to find the right memory): Multi-axis search combining temporal, semantic, entity, spatial, and full-text indices, scored by recency, importance, relevance, and context match — following the framework established by Park et al. (2023) and refined by subsequent work.

The two-mode architecture (passive 1 FPS vs. active live mode) maps onto the cognitive distinction between **background monitoring** (exogenous attention, automatic, low-cost) and **focal processing** (endogenous attention, effortful, high-fidelity). The transition between modes — and especially the proactive reasoning that decides *when* to interrupt the user — is where the product experience is won or lost.

Every production system today is incomplete. Project Astra has the best multimodal pipeline but limited memory duration. ChatGPT has the most deployed memory system but no visual or spatial grounding. Limitless proved the commercial viability of always-on capture but was audio-only. MemGPT introduced the most principled memory management framework but has never been applied to continuous multimodal streams. The team that combines these approaches — multimodal perception, principled memory management, cognitive-science-grounded consolidation, and proactive reasoning — will build the first truly useful always-on AI companion.
