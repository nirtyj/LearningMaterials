# System Design: Always-On AI Wearable Memory & Reasoning Engine

## End-to-End Architecture with Detailed Component Specifications

---

# 1. HIGH-LEVEL SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT DEVICES (EDGE TIER)                              │
│                                                                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐ │
│  │  AR GLASSES   │   │  SMART PHONE │   │  PENDANT     │   │  SMART WATCH         │ │
│  │  1-5 FPS      │   │  5-30 FPS    │   │  Audio-only  │   │  IMU + Audio         │ │
│  │  Camera+Audio │   │  Camera+Audio│   │  16kHz Mono  │   │  Heart Rate + Motion │ │
│  │  +IMU+GPS     │   │  +GPS+Gyro   │   │  +BLE        │   │  +BLE                │ │
│  │              │   │              │   │              │   │                      │ │
│  │  NPU: 4 TOPS │   │  NPU: 15TOPS │   │  MCU only    │   │  MCU only            │ │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘   └──────────┬───────────┘ │
│         │                  │                   │                      │             │
└─────────┼──────────────────┼───────────────────┼──────────────────────┼─────────────┘
          │                  │                   │                      │
          │  Embeddings +    │  Keyframes +      │  Opus Audio          │ IMU +
          │  Keyframes +     │  Audio +           │  Packets             │ Sensor
          │  Audio (gRPC)    │  Metadata (gRPC)  │  (BLE→Phone→gRPC)   │ Data
          │                  │                   │                      │
          ▼                  ▼                   ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           TRANSPORT LAYER                                            │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │                    gRPC Streaming (HTTP/2 + Protobuf)                            │ │
│  │                                                                                 │ │
│  │   Passive Mode: Unary RPCs (embeddings + metadata, ~2KB/request, 1/sec)         │ │
│  │   Live Mode:  Bidirectional streaming (keyframes + audio, ~50KB/sec up,         │ │
│  │               audio response ~8KB/sec down via Opus @ 32kbps)                   │ │
│  │                                                                                 │ │
│  │   Audio: Opus codec (26.5ms latency, 16-32kbps VBR, DTX for silence)            │ │
│  │   Video: JPEG keyframes (320x240, ~15KB each) or H.265 for live mode            │ │
│  │   Metadata: Protobuf (embeddings, IMU, GPS, timestamps)                         │ │
│  │                                                                                 │ │
│  │   TLS 1.3 end-to-end │ Certificate pinning │ mTLS for device auth              │ │
│  └─────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                     │
└─────────────────────────────────────────┬───────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           CLOUD TIER (per-user partitioned)                          │
│                                                                                     │
│  ┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │  INGESTION     │  │  MEMORY STORES    │  │  REASONING       │  │  RESPONSE     │ │
│  │  PIPELINE      │  │                  │  │  ENGINE          │  │  PIPELINE     │ │
│  │                │  │  Working Memory   │  │                  │  │               │ │
│  │  Scene Detect  ├─►│  Episodic Memory  │◄─┤  Reactive (RAG)  │  │  LLM Gen      │ │
│  │  ASR / Diariz  │  │  Semantic Memory  │  │  Proactive Trig  │──►  TTS Synth    │ │
│  │  Face Match    │  │  Procedural Mem   │  │  Consolidation   │  │  Opus Encode  │ │
│  │  Caption Gen   │  │                  │  │                  │  │  Stream Back  │ │
│  └────────────────┘  └──────────────────┘  └──────────────────┘  └───────────────┘ │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

# 2. CLIENT DEVICE ARCHITECTURE (EDGE TIER)

## 2.1 Device Capabilities Matrix

```
┌─────────────────┬────────────┬────────────┬──────────┬────────────┐
│                 │ AR GLASSES │ SMARTPHONE │ PENDANT  │ SMARTWATCH │
├─────────────────┼────────────┼────────────┼──────────┼────────────┤
│ Visual Capture  │ 1-5 FPS    │ 5-30 FPS   │ None     │ None       │
│ Resolution      │ 640x480    │ 1280x720   │ N/A      │ N/A        │
│ Audio Capture   │ 2-mic beam │ 1-mic      │ 3-mic    │ 1-mic      │
│                 │ forming    │            │ beamform │            │
│ Audio Codec     │ Opus 32kbps│ Opus 32kbps│ Opus 16k │ Opus 16k   │
│ Sample Rate     │ 16kHz      │ 16kHz      │ 16kHz    │ 16kHz      │
│ IMU             │ 6-DOF      │ 6-DOF      │ None     │ 6-DOF      │
│ GPS             │ Via phone  │ Native     │ Via phone│ Via phone  │
│ Eye Tracking    │ Yes        │ No         │ No       │ No         │
│ Compute         │ NPU 4 TOPS │ NPU 15 TOP │ MCU only │ MCU only   │
│ On-device       │ MobileCLIP │ SigLIP +   │ VAD only │ VAD only   │
│ Models          │ + DINOv2-s │ Moondream  │          │            │
│                 │ + RetinaF. │ + Whisper  │          │            │
│ Power (passive) │ ~80mW      │ ~200mW     │ ~15mW    │ ~20mW      │
│ Power (live)    │ ~500mW     │ ~2W        │ ~50mW    │ ~50mW      │
│ Battery Life    │ ~8 hrs     │ ~12 hrs    │ ~100 hrs │ ~48 hrs    │
│ Connectivity    │ BLE→Phone  │ WiFi/5G    │ BLE→Phone│ BLE→Phone  │
│ Storage         │ 2GB buffer │ 64GB+      │ 512MB    │ 512MB      │
└─────────────────┴────────────┴────────────┴──────────┴────────────┘
```

## 2.2 On-Device Processing Pipeline (AR Glasses — Primary Device)

```
                    ┌─────────────────────────────────────────────┐
                    │         ALWAYS-ON SENSOR ACQUISITION         │
                    │                 (~20mW)                      │
                    └──────┬────────────┬────────────┬────────────┘
                           │            │            │
                     Camera 1 FPS   Mic Array    IMU 100Hz
                     640x480 RGB    16kHz PCM    Accel+Gyro
                           │            │            │
┌──────────────────────────┼────────────┼────────────┼──────────────────────────┐
│                   SENSORY BUFFER (Ring Buffer, On-Device RAM)                 │
│                                                                              │
│   Visual: 60 frames × 50KB = 3MB        Audio: 60s × 32KB/s = 1.9MB         │
│   IMU: 300s × 12B × 100Hz = 360KB       Total buffer: ~5.3MB                │
│                                                                              │
│   Purpose: "Rewind" capability. When something interesting is detected,      │
│   system can process the last 30-60 seconds retroactively.                   │
└──────────────────────────┼────────────┼────────────┼─────────────────────────┘
                           │            │            │
                           ▼            ▼            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                     ON-DEVICE INFERENCE (Edge NPU, ~50mW)                    │
│                                                                              │
│  ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐  │
│  │   VISUAL ENCODER     │ │   AUDIO PROCESSOR    │ │   MOTION ANALYZER   │  │
│  │                      │ │                      │ │                      │  │
│  │ MobileCLIP-S2 (3ms)  │ │ Silero VAD    (1ms)  │ │ Activity classif.   │  │
│  │  → 512-dim CLIP emb  │ │  → Speech detected?  │ │  → walk/sit/drive   │  │
│  │                      │ │                      │ │    /stationary       │  │
│  │ DINOv2-small  (2ms)  │ │ ECAPA-TDNN   (3ms)  │ │                      │  │
│  │  → 384-dim struct emb│ │  → 192-dim speaker   │ │ Step counter         │  │
│  │                      │ │    embedding         │ │  → cadence, heading  │  │
│  │ RetinaFace-mb (5ms)  │ │                      │ │                      │  │
│  │  → Face bounding box │ │ Speaker matching     │ │ Gesture detection    │  │
│  │                      │ │  → Known speaker ID  │ │  → head nod, shake   │  │
│  │ MobileFaceNet (3ms)  │ │    or "unknown_N"    │ │                      │  │
│  │  → 128-dim face emb  │ │                      │ │                      │  │
│  └──────────┬───────────┘ └──────────┬───────────┘ └──────────┬───────────┘  │
│             │                        │                        │              │
│             ▼                        ▼                        ▼              │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │                    CHANGE DETECTION & ATTENTION GATE                  │   │
│  │                                                                       │   │
│  │  frame_delta = 1 - cos_sim(current_clip_emb, prev_clip_emb)          │   │
│  │  scene_delta = 1 - cos_sim(current_clip_emb, scene_mean_emb)         │   │
│  │                                                                       │   │
│  │  PROMOTE if:  frame_delta > 0.15          (something just happened)  │   │
│  │           OR  scene_delta > 0.30          (gradual scene shift)      │   │
│  │           OR  new_face_detected           (person appeared)          │   │
│  │           OR  speech_started              (conversation began)       │   │
│  │           OR  significant_motion_change   (user started moving)      │   │
│  │                                                                       │   │
│  │  Result: ~10-20% of frames promoted (rest → update running avg only) │   │
│  └───────────────────────────────────────────────────┬───────────────────┘   │
│                                                      │                      │
└──────────────────────────────────────────────────────┼──────────────────────┘
                                                       │
                          ┌────────────────────────────┼───────────────────┐
                          │                            │                   │
                    Not Promoted                  Promoted            Live Mode
                    (discard frame,              (queue for           Activated
                     keep embedding)              upload)             (stream all)
                          │                            │                   │
                          ▼                            ▼                   ▼
              ┌─────────────────────┐    ┌──────────────────┐    ┌──────────────┐
              │ Update scene avg    │    │ Package for      │    │ Stream full  │
              │ Update working mem  │    │ transport:       │    │ resolution   │
              │ (embedding only)    │    │  • JPEG keyframe │    │ video+audio  │
              │                     │    │  • CLIP embedding│    │ via gRPC     │
              │ Cost: ~0.5KB/frame  │    │  • Face embeds   │    │ bidirectional│
              └─────────────────────┘    │  • Speaker ID    │    │ streaming    │
                                         │  • IMU snapshot  │    │              │
                                         │  • GPS coords    │    │ ~50KB/sec up │
                                         │  • Timestamp     │    │ ~8KB/sec dn  │
                                         │                  │    └──────┬───────┘
                                         │ Cost: ~20KB/pkt  │           │
                                         └────────┬─────────┘           │
                                                  │                     │
                                                  ▼                     ▼
                                         ┌──────────────────────────────────┐
                                         │        TRANSPORT QUEUE           │
                                         │   (on-device, survives network   │
                                         │    drops, FIFO with priority)    │
                                         └──────────────┬───────────────────┘
                                                        │
                                                        ▼
                                                  TO TRANSPORT LAYER
```

---

# 3. TRANSPORT LAYER

## 3.1 Protocol Selection

```
┌──────────────────────────────────────────────────────────────────────┐
│                     TRANSPORT PROTOCOL DECISION                      │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  PASSIVE MODE (1 FPS, background upload)                      │  │
│  │                                                                │  │
│  │  Protocol: gRPC Unary RPCs over HTTP/2                        │  │
│  │  Why: Efficient protobuf serialization, HTTP/2 multiplexing,  │  │
│  │       auto-generated clients, built-in retry/deadline support │  │
│  │                                                                │  │
│  │  Payload per request (~2-20KB):                               │  │
│  │    message SensorFrame {                                      │  │
│  │      int64  timestamp_ms       = 1;                           │  │
│  │      bytes  clip_embedding     = 2;  // 512 × f16 = 1KB      │  │
│  │      bytes  dino_embedding     = 3;  // 384 × f16 = 768B     │  │
│  │      bytes  jpeg_keyframe      = 4;  // optional, ~15KB      │  │
│  │      repeated FaceDetection faces = 5;                        │  │
│  │      SpeakerInfo speaker       = 6;                           │  │
│  │      IMUSnapshot imu           = 7;  // 12 bytes             │  │
│  │      GeoPoint location         = 8;  // 16 bytes             │  │
│  │      float  scene_change_score = 9;                           │  │
│  │      ActivityType activity     = 10;                          │  │
│  │    }                                                          │  │
│  │                                                                │  │
│  │  Bandwidth: ~2KB/sec (no keyframe) to ~20KB/sec (w/ keyframe) │  │
│  │  Frequency: 1 RPC/sec (passive), batch if offline             │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  LIVE MODE (real-time conversation)                           │  │
│  │                                                                │  │
│  │  Protocol: gRPC Bidirectional Streaming over HTTP/2           │  │
│  │  Why: Single persistent connection, interleaved audio+video   │  │
│  │       upstream AND audio response downstream simultaneously   │  │
│  │                                                                │  │
│  │  Upstream (device → cloud):                                   │  │
│  │    stream LiveFrame {                                         │  │
│  │      oneof payload {                                          │  │
│  │        AudioChunk audio     = 1;  // Opus, 20ms frames       │  │
│  │        VideoFrame video     = 2;  // JPEG or H.265 NAL       │  │
│  │        SensorFrame metadata = 3;  // embeddings + IMU        │  │
│  │      }                                                        │  │
│  │    }                                                          │  │
│  │                                                                │  │
│  │  Downstream (cloud → device):                                 │  │
│  │    stream LiveResponse {                                      │  │
│  │      oneof payload {                                          │  │
│  │        AudioChunk tts_audio  = 1;  // Opus, streamed         │  │
│  │        TextOverlay display   = 2;  // for AR HUD             │  │
│  │        ProactiveAlert alert  = 3;  // triggered insight      │  │
│  │      }                                                        │  │
│  │    }                                                          │  │
│  │                                                                │  │
│  │  Upstream bandwidth: ~50KB/sec (audio 4KB + video 46KB)       │  │
│  │  Downstream bandwidth: ~8KB/sec (Opus TTS @ 32kbps + text)   │  │
│  │  Target E2E latency: < 2 seconds (first audio response)      │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  AUDIO CODEC SPECIFICATION                                    │  │
│  │                                                                │  │
│  │  Codec: Opus (RFC 6716)                                       │  │
│  │  Mode: SILK (speech-optimized) with DTX (silence suppression) │  │
│  │  Frame size: 20ms (default, 26.5ms total algorithmic delay)   │  │
│  │  Sample rate: 16kHz (wideband, sufficient for speech)         │  │
│  │  Bitrate: 16-32kbps VBR (adaptive to network)                │  │
│  │  FEC: In-band forward error correction enabled                │  │
│  │  DTX: Enabled — near-zero bandwidth during silence            │  │
│  │                                                                │  │
│  │  Why Opus:                                                    │  │
│  │   • Mandatory codec in WebRTC (universal support)             │  │
│  │   • 5-26.5ms latency (vs 100ms+ for AAC)                     │  │
│  │   • Seamless bitrate adaptation without artifacts             │  │
│  │   • DTX reduces avg bandwidth 60-80% in typical conversations │  │
│  │   • Built into Android 13+, iOS via WebRTC, all browsers     │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  OFFLINE RESILIENCE                                           │  │
│  │                                                                │  │
│  │  On-device queue persists frames when offline.                │  │
│  │  Max queue: 2GB (~30 min of promoted frames + full audio)     │  │
│  │  Priority: Audio > Promoted keyframes > Embeddings-only       │  │
│  │  On reconnect: Batch upload via gRPC streaming, newest first  │  │
│  │  Working memory operates fully offline (on-device only)       │  │
│  │  Episodic storage degrades to local-only until sync           │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

# 4. CLOUD INGESTION PIPELINE

```
                         gRPC from device(s)
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          API GATEWAY / LOAD BALANCER                     │
│                                                                          │
│   • Per-user sticky sessions (consistent hashing on user_id)             │
│   • TLS termination + mTLS device verification                          │
│   • Rate limiting: 10 RPC/sec passive, 50 RPC/sec live                  │
│   • Route: passive → ingestion queue, live → streaming inference         │
└─────────────────┬────────────────────────────────┬───────────────────────┘
                  │                                │
            PASSIVE MODE                     LIVE MODE
                  │                                │
                  ▼                                ▼
┌─────────────────────────────┐    ┌───────────────────────────────────┐
│   INGESTION QUEUE           │    │   STREAMING INFERENCE GATEWAY     │
│   (Kafka / SQS per-user     │    │                                   │
│    partitioned)              │    │   Bidirectional gRPC stream       │
│                              │    │   held open for session duration  │
│   Guarantees:                │    │                                   │
│   • Ordered per-user         │    │   Connects to:                    │
│   • At-least-once delivery   │    │   • ASR service (real-time)       │
│   • 7-day retention          │    │   • VLM service (per-frame)       │
│                              │    │   • Reasoning engine              │
└──────────┬──────────────────┘    │   • TTS service (streaming out)   │
           │                       └──────────┬────────────────────────┘
           ▼                                  │
┌──────────────────────────────┐              │
│   FRAME PROCESSOR            │              │
│   (Stateless workers,        │              │
│    auto-scaling)             │              │
│                              │              │
│   For each SensorFrame:      │              │
│                              │              │
│   1. Validate + deduplicate  │              │
│   2. If keyframe present:    │              │
│      → Generate VLM caption  │              │
│        (Gemini Flash / Phi-3)│              │
│      → Extract entities      │              │
│        (people, objects,     │              │
│         text, screens)       │              │
│   3. If audio present:       │              │
│      → ASR transcription     │              │
│        (Whisper-large-v3)    │              │
│      → Speaker diarization   │              │
│        (match to user's      │              │
│         known speakers)      │              │
│   4. Scene classification    │              │
│      → indoor/outdoor,       │              │
│        room type, activity   │              │
│   5. Episode boundary check  │              │
│      → scene_change_score    │              │
│        vs threshold          │              │
│   6. Write to memory stores  │              │
│      ────────────────────►   │              │
└──────────────────────────────┘              │
                                              │
                            ┌─────────────────┘
                            │
                            ▼
              (Both paths write to / read from the Memory Stores)
```

---

# 5. MEMORY STORES (The Core)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MEMORY ARCHITECTURE                              │
│                         (Per-User, Isolated Tenancy)                        │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 0: WORKING MEMORY (Redis / In-Memory, < 10ms reads)        │    │
│  │                                                                     │    │
│  │  Key: user:{uid}:working_memory                                     │    │
│  │  TTL: Session-scoped (cleared on device disconnect + 5min grace)    │    │
│  │                                                                     │    │
│  │  Contents:                                                          │    │
│  │   • current_scene (embedding + label + keyframe + entities)         │    │
│  │   • recent_scenes[0..19] (ring buffer, last ~5 minutes)             │    │
│  │   • active_entities{} (people in view, with face_emb + name)        │    │
│  │   • location (GPS + semantic place name)                            │    │
│  │   • user_state (activity + social_context + attention)              │    │
│  │   • pending_triggers[] (prospective memory items)                   │    │
│  │                                                                     │    │
│  │  Updated: Every ingested frame (1/sec passive, 5-30/sec live)       │    │
│  │  Size: ~500KB per user                                              │    │
│  │  Technology: Redis Cluster with persistence to S3 backup            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 1: EPISODIC MEMORY (Postgres + pgvector + S3)               │    │
│  │                                                                     │    │
│  │  Table: episodes                                                    │    │
│  │  ┌──────────────┬──────────────────────────────────────────────┐    │    │
│  │  │ Column       │ Type / Description                           │    │    │
│  │  ├──────────────┼──────────────────────────────────────────────┤    │    │
│  │  │ id           │ UUID (primary key)                           │    │    │
│  │  │ user_id      │ UUID (partition key)                         │    │    │
│  │  │ start_time   │ TIMESTAMPTZ (B-tree index)                  │    │    │
│  │  │ end_time     │ TIMESTAMPTZ                                 │    │    │
│  │  │ duration_sec │ INT                                         │    │    │
│  │  │ location     │ GEOGRAPHY(POINT) (PostGIS spatial index)    │    │    │
│  │  │ place_name   │ TEXT ("Blue Bottle Coffee, Pruneyard")      │    │    │
│  │  │ clip_emb     │ VECTOR(512) (HNSW index via pgvector)      │    │    │
│  │  │ caption      │ TEXT (full-text search tsvector index)      │    │    │
│  │  │ entities     │ JSONB (GIN index on entity names/types)     │    │    │
│  │  │ topics       │ TEXT[] (GIN index)                          │    │    │
│  │  │ transcript   │ TEXT (full-text search)                     │    │    │
│  │  │ speakers     │ JSONB                                       │    │    │
│  │  │ importance   │ FLOAT (0-1)                                 │    │    │
│  │  │ access_count │ INT                                         │    │    │
│  │  │ last_access  │ TIMESTAMPTZ                                 │    │    │
│  │  │ consol_level │ SMALLINT (0=full, 1=compressed ... 4=gone)  │    │    │
│  │  │ keyframes_s3 │ TEXT[] (S3 URIs for JPEG thumbnails)        │    │    │
│  │  └──────────────┴──────────────────────────────────────────────┘    │    │
│  │                                                                     │    │
│  │  Indices for multi-axis retrieval:                                  │    │
│  │   • B-tree on (user_id, start_time) — temporal queries              │    │
│  │   • HNSW on clip_emb — semantic vector search (ef=64, m=16)         │    │
│  │   • GIN on entities — entity lookup ("all episodes with Sarah")     │    │
│  │   • PostGIS GIST on location — spatial queries                      │    │
│  │   • GIN tsvector on caption + transcript — full-text search         │    │
│  │                                                                     │    │
│  │  Growth: ~200 episodes/day, ~150MB/user total (after consolidation) │    │
│  │  Partitioning: By user_id (hash) + time (monthly range)             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 2: SEMANTIC MEMORY (Neo4j Knowledge Graph + pgvector)       │    │
│  │                                                                     │    │
│  │  Node Types:                                                        │    │
│  │   • (:Person {name, face_embs[], relationship, org, role,           │    │
│  │              usual_places[], interaction_freq, last_seen, facts[]})  │    │
│  │   • (:Place {name, geo, visit_pattern, typical_duration,            │    │
│  │             visual_signature_emb})                                   │    │
│  │   • (:Object {name, visual_emb, last_location, last_seen,           │    │
│  │              importance})                                            │    │
│  │   • (:Fact {content, source_episodes[], confidence, created})        │    │
│  │   • (:Preference {key, value, confidence, source_episodes[]})        │    │
│  │                                                                     │    │
│  │  Edge Types:                                                        │    │
│  │   • (Person)-[:WORKS_WITH]->(Person)                                │    │
│  │   • (Person)-[:SEEN_AT]->(Place)                                    │    │
│  │   • (Person)-[:DISCUSSED]->(Fact)                                   │    │
│  │   • (Object)-[:LAST_AT]->(Place)                                    │    │
│  │                                                                     │    │
│  │  Growth: ~5-20 new facts/day, ~2-3 new entities/week                │    │
│  │  Technology: Neo4j Aura (managed) or self-hosted with APOC          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 3: PROCEDURAL MEMORY (DynamoDB / Redis Sorted Sets)         │    │
│  │                                                                     │    │
│  │  Structure: Learned behavioral sequences                            │    │
│  │   • Pattern ID, name, temporal_pattern (cron-like)                  │    │
│  │   • typical_sequence: ["leave_home", "drive", "park", "office"]     │    │
│  │   • observation_count, confidence_score                             │    │
│  │   • deviation_history[]                                             │    │
│  │   • proactive_triggers[] (condition → action pairs)                 │    │
│  │                                                                     │    │
│  │  Built by: Nightly consolidation (sequence mining over episodes)    │    │
│  │  Requires: ≥10 observations before pattern is active                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  BLOB STORE (S3 / GCS)                                             │    │
│  │                                                                     │    │
│  │  Stores: JPEG keyframe thumbnails, audio clips (for replay)        │    │
│  │  Structure: s3://memory-{uid}/episodes/{eid}/keyframe_{n}.jpg      │    │
│  │  Lifecycle: Matches consolidation levels                            │    │
│  │   • Level 0-1: All keyframes retained                               │    │
│  │   • Level 2: Best keyframe only                                     │    │
│  │   • Level 3+: Keyframes deleted                                     │    │
│  │  Encryption: AES-256 server-side, per-user keys in KMS             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 6. REASONING ENGINE (Read Path)

## 6.1 Reactive Reasoning (User Asks a Question)

```
  User: "Where did I leave my keys?"
         │
         │  (Opus audio, upstream via gRPC bidirectional stream)
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       LIVE MODE INFERENCE PIPELINE                       │
│                                                                          │
│  STEP 1: SPEECH-TO-TEXT                                                  │
│  ┌────────────────────────────────────────────────┐                      │
│  │  Whisper-large-v3 (streaming mode via VAD)     │                      │
│  │  Input: Opus audio stream                      │                      │
│  │  Output: "Where did I leave my keys?"          │                      │
│  │  Latency: ~300ms (first-pass w/ chunked ASR)   │                      │
│  └────────────────────────────────┬───────────────┘                      │
│                                   │                                      │
│  STEP 2: INTENT CLASSIFICATION + MEMORY AXIS ROUTING                     │
│  ┌────────────────────────────────▼───────────────┐                      │
│  │  LLM call (Claude Haiku / Gemini Flash):       │                      │
│  │                                                 │                      │
│  │  Input: query + working_memory_snapshot         │                      │
│  │  Output:                                        │                      │
│  │    intent: LOCATE_OBJECT                        │                      │
│  │    object: "keys"                               │                      │
│  │    time_hint: null (implies "most recent")      │                      │
│  │    axes_to_query: [semantic, entity, temporal]   │                      │
│  │                                                 │                      │
│  │  Latency: ~100ms (Haiku-class model)            │                      │
│  └────────────────────────────────┬───────────────┘                      │
│                                   │                                      │
│  STEP 3: PARALLEL MEMORY RETRIEVAL                                       │
│  ┌────────────────────────────────▼───────────────────────────────────┐  │
│  │                                                                    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │  │
│  │  │ WORKING MEM  │  │ EPISODIC MEM │  │ SEMANTIC MEMORY          │ │  │
│  │  │ (Redis)      │  │ (Postgres)   │  │ (Neo4j)                  │ │  │
│  │  │              │  │              │  │                          │ │  │
│  │  │ Check if     │  │ SQL:         │  │ MATCH (o:Object          │ │  │
│  │  │ "keys" in    │  │ SELECT *     │  │   {name: "keys"})        │ │  │
│  │  │ current      │  │ FROM episodes│  │ RETURN o.last_location,  │ │  │
│  │  │ scene        │  │ WHERE user=? │  │   o.last_seen            │ │  │
│  │  │ entities     │  │ AND entities │  │                          │ │  │
│  │  │              │  │   @> '{"name"│  │ Result:                  │ │  │
│  │  │ Result: NO   │  │   :"keys"}'  │  │  "kitchen counter"      │ │  │
│  │  │ (not in view)│  │ ORDER BY     │  │  last_seen: 2h ago      │ │  │
│  │  │              │  │  start_time  │  │                          │ │  │
│  │  │ Latency: 2ms │  │  DESC        │  │ Latency: 15ms           │ │  │
│  │  │              │  │ LIMIT 5      │  │                          │ │  │
│  │  │              │  │              │  │                          │ │  │
│  │  │              │  │ + vector sim │  │                          │ │  │
│  │  │              │  │ on "keys"    │  │                          │ │  │
│  │  │              │  │ text emb     │  │                          │ │  │
│  │  │              │  │              │  │                          │ │  │
│  │  │              │  │ Latency: 50ms│  │                          │ │  │
│  │  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘ │  │
│  │         │                 │                        │               │  │
│  │         └────────┬────────┴────────────────────────┘               │  │
│  │                  │                                                 │  │
│  │                  ▼                                                 │  │
│  │  ┌──────────────────────────────────────┐                         │  │
│  │  │  RESULT FUSION & RE-RANKING          │                         │  │
│  │  │                                      │                         │  │
│  │  │  Merge results from all axes.        │                         │  │
│  │  │  Score each by:                      │                         │  │
│  │  │   score = 0.25 × recency             │                         │  │
│  │  │         + 0.20 × importance          │                         │  │
│  │  │         + 0.30 × relevance(query)    │                         │  │
│  │  │         + 0.25 × context_match       │                         │  │
│  │  │         (Park et al. 2023 formula)   │                         │  │
│  │  │                                      │                         │  │
│  │  │  Top result: Episode from 2h ago,    │                         │  │
│  │  │  caption: "User placed keys on       │                         │  │
│  │  │  kitchen counter after entering home" │                         │  │
│  │  │  + Semantic: Object "keys" last at   │                         │  │
│  │  │    "kitchen counter"                 │                         │  │
│  │  │                                      │                         │  │
│  │  │  Latency: ~5ms                       │                         │  │
│  │  └──────────────────┬───────────────────┘                         │  │
│  │                     │                                              │  │
│  └─────────────────────┼──────────────────────────────────────────────┘  │
│                        │                                                 │
│  STEP 4: RESPONSE GENERATION                                             │
│  ┌─────────────────────▼───────────────────────────┐                     │
│  │  LLM call (Claude Sonnet / Gemini Pro):         │                     │
│  │                                                  │                     │
│  │  System: "You are a wearable memory assistant.   │                     │
│  │   Respond concisely (< 30 words). Cite memory    │                     │
│  │   sources. Express uncertainty when unsure."     │                     │
│  │                                                  │                     │
│  │  Context:                                        │                     │
│  │   • Current: user is in living room              │                     │
│  │   • Retrieved: keys on kitchen counter, 2h ago   │                     │
│  │   • Query: "Where did I leave my keys?"          │                     │
│  │                                                  │                     │
│  │  Output: "Your keys are most likely on the       │                     │
│  │   kitchen counter. I saw you put them there      │                     │
│  │   about two hours ago when you got home."        │                     │
│  │                                                  │                     │
│  │  Latency: ~400ms (streaming, first token ~150ms) │                     │
│  └─────────────────────┬───────────────────────────┘                     │
│                        │                                                 │
│  STEP 5: TEXT-TO-SPEECH + STREAM BACK                                    │
│  ┌─────────────────────▼───────────────────────────┐                     │
│  │  TTS Service (Cartesia Sonic / Inworld TTS):    │                     │
│  │                                                  │                     │
│  │  Input: Text stream from LLM (token-by-token)   │                     │
│  │  Output: Opus audio stream (32kbps, 16kHz)      │                     │
│  │                                                  │                     │
│  │  Streaming: TTS begins on first sentence.        │                     │
│  │  Doesn't wait for full LLM response.             │                     │
│  │                                                  │                     │
│  │  First audio byte: ~200ms after first LLM token  │                     │
│  │  Opus encoding: ~5ms per 20ms frame              │                     │
│  └─────────────────────┬───────────────────────────┘                     │
│                        │                                                 │
│  STEP 6: DELIVER TO DEVICE                                               │
│  ┌─────────────────────▼───────────────────────────┐                     │
│  │  gRPC downstream via bidirectional stream:      │                     │
│  │                                                  │                     │
│  │  LiveResponse {                                  │                     │
│  │    tts_audio: [Opus frame 1, frame 2, ...]      │                     │
│  │    display: TextOverlay { "Keys: kitchen        │                     │
│  │             counter, ~2h ago" }  // for AR HUD  │                     │
│  │  }                                               │                     │
│  │                                                  │                     │
│  │  Device receives Opus → decode → bone conduction │                     │
│  │  speaker or AR glasses speaker.                  │                     │
│  │                                                  │                     │
│  │  Downstream bandwidth: ~4KB/sec (Opus @ 32kbps) │                     │
│  └──────────────────────────────────────────────────┘                     │
│                                                                          │
│  TOTAL END-TO-END LATENCY BUDGET:                                        │
│  ┌──────────────────────────────────────────────────────────┐            │
│  │  ASR (speech→text):          ~300ms                      │            │
│  │  Intent classification:       ~100ms                     │            │
│  │  Memory retrieval (parallel):  ~50ms                     │            │
│  │  Re-ranking:                    ~5ms                     │            │
│  │  LLM generation (first tok):  ~150ms                     │            │
│  │  TTS (first audio frame):     ~200ms                     │            │
│  │  Network (round-trip):        ~100ms                     │            │
│  │  Device decode + playback:     ~30ms                     │            │
│  │  ─────────────────────────────────────                   │            │
│  │  TOTAL (first audio response): ~935ms                    │            │
│  │  TARGET: < 1.5 seconds                          ✓ MET    │            │
│  └──────────────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Proactive Reasoning (System-Initiated)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    PROACTIVE TRIGGER ENGINE                               │
│              (Runs on every working memory update, ~1/sec)                │
│                                                                          │
│   Working Memory Update                                                  │
│         │                                                                │
│         ▼                                                                │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │  TRIGGER EVALUATION PIPELINE (lightweight, < 10ms total)       │    │
│   │                                                                 │    │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │    │
│   │  │ PERSON RECOG    │  │ OBJECT REMIND   │  │ ROUTINE DEV    │ │    │
│   │  │                 │  │                 │  │                │ │    │
│   │  │ New face in     │  │ User leaving    │  │ Current behav  │ │    │
│   │  │ active_entities │  │ location where  │  │ deviates from  │ │    │
│   │  │ that is known?  │  │ important obj   │  │ learned pattern│ │    │
│   │  │                 │  │ was last seen?  │  │ by > threshold?│ │    │
│   │  └────────┬────────┘  └────────┬────────┘  └───────┬────────┘ │    │
│   │           │                    │                    │          │    │
│   │  ┌────────┴────────┐  ┌───────┴─────────┐  ┌──────┴───────┐ │    │
│   │  │ PROSPECTIVE     │  │ REPEATED EXPOSE │  │ TEMPORAL     │ │    │
│   │  │                 │  │                 │  │              │ │    │
│   │  │ Context matches │  │ User looked at  │  │ Calendar     │ │    │
│   │  │ stored future   │  │ same thing 3+   │  │ event in     │ │    │
│   │  │ intention?      │  │ times?          │  │ next 10 min? │ │    │
│   │  └────────┬────────┘  └────────┬────────┘  └──────┬───────┘ │    │
│   │           │                    │                    │         │    │
│   │           └───────────┬────────┴────────────────────┘         │    │
│   │                       ▼                                       │    │
│   │  ┌──────────────────────────────────────────────────────┐    │    │
│   │  │  ANY TRIGGER FIRED WITH confidence > 0.8?            │    │    │
│   │  │                                                      │    │    │
│   │  │  YES → Check interrupt appropriateness:              │    │    │
│   │  │    • In active conversation? (suppress if low urg.)  │    │    │
│   │  │    • In focus activity? (suppress)                   │    │    │
│   │  │    • Hit rate limit? (max 3/hour)                    │    │    │
│   │  │    • Is this a transition moment? (prefer)           │    │    │
│   │  │                                                      │    │    │
│   │  │  If appropriate → Generate response via LLM + TTS    │    │    │
│   │  │  → Stream ProactiveAlert to device via gRPC          │    │    │
│   │  │                                                      │    │    │
│   │  │  NO → Continue passive monitoring                    │    │    │
│   │  └──────────────────────────────────────────────────────┘    │    │
│   └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```

---

# 7. CONSOLIDATION PIPELINE (Background, Nightly)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      NIGHTLY CONSOLIDATION JOB                           │
│             (Runs during charging, ~2-4 AM, per-user cron job)           │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  STAGE 1: IMPORTANCE SCORING (all episodes from today)            │  │
│  │                                                                    │  │
│  │  For each episode:                                                │  │
│  │   score = 0.25 × recency_decay(age_days, half_life=7)            │  │
│  │         + 0.20 × min(access_count / 5, 1.0)                      │  │
│  │         + 0.15 × min(known_people_count / 3, 1.0)                │  │
│  │         + 0.15 × novelty_vs_place_signature                      │  │
│  │         + 0.10 × emotional_valence                                │  │
│  │         + 0.15 × user_flagged (boolean → 0 or 1)                 │  │
│  │                                                                    │  │
│  │  Write importance_score to each episode record.                   │  │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  │                                       │
│  ┌───────────────────────────────▼────────────────────────────────────┐  │
│  │  STAGE 2: EPISODIC → SEMANTIC EXTRACTION                          │  │
│  │                                                                    │  │
│  │  LLM batch call over today's episodes:                            │  │
│  │   "Extract stable facts, new people, new places, and              │  │
│  │    preferences from these episodes."                              │  │
│  │                                                                    │  │
│  │  → Update Person nodes in Neo4j                                   │  │
│  │  → Update Place nodes with visit patterns                         │  │
│  │  → Update Object last-known locations                             │  │
│  │  → Merge new Facts with existing (deduplicate)                    │  │
│  │  → Detect new Preferences                                         │  │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  │                                       │
│  ┌───────────────────────────────▼────────────────────────────────────┐  │
│  │  STAGE 3: ROUTINE DETECTION (weekly, over last 30 days)           │  │
│  │                                                                    │  │
│  │  Sequence mining over episodic transitions:                       │  │
│  │   Input: (place, time_of_day, day_of_week, duration) tuples      │  │
│  │   Algorithm: Frequent sequential pattern mining (PrefixSpan)     │  │
│  │   Output: Candidate routines with support count                   │  │
│  │   Threshold: ≥ 10 observations to activate                       │  │
│  │                                                                    │  │
│  │  Write to Procedural Memory store.                                │  │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  │                                       │
│  ┌───────────────────────────────▼────────────────────────────────────┐  │
│  │  STAGE 4: PROGRESSIVE COMPRESSION                                 │  │
│  │                                                                    │  │
│  │  For episodes older than 24h:                                     │  │
│  │   Level 0 → 1 (after 1 day):                                     │  │
│  │     • Keep best 2 keyframes, delete rest from S3                  │  │
│  │     • Keep full caption                                           │  │
│  │                                                                    │  │
│  │  For episodes older than 7 days:                                  │  │
│  │   Level 1 → 2 (after 7 days):                                    │  │
│  │     • Keep 1 thumbnail (downsize to 160x120)                      │  │
│  │     • Condense caption to 1-2 sentences via LLM summarization    │  │
│  │     • Delete audio clips                                         │  │
│  │                                                                    │  │
│  │  For episodes older than 30 days:                                 │  │
│  │   Level 2 → 3 (after 30 days):                                   │  │
│  │     • Delete all visual data                                      │  │
│  │     • Retain embedding + caption facts only                       │  │
│  │     • Exception: episodes with importance > 0.7 stay at Level 2  │  │
│  │                                                                    │  │
│  │  For episodes older than 90 days:                                 │  │
│  │   Level 3 → 4 (after 90 days):                                   │  │
│  │     • Extract any remaining facts to semantic memory              │  │
│  │     • Delete episode record entirely                              │  │
│  │     • Exception: "landmark" episodes (importance > 0.85) stay    │  │
│  └───────────────────────────────┬────────────────────────────────────┘  │
│                                  │                                       │
│  ┌───────────────────────────────▼────────────────────────────────────┐  │
│  │  STAGE 5: EMBEDDING MAINTENANCE (monthly)                         │  │
│  │                                                                    │  │
│  │  If model version updated:                                        │  │
│  │   • Re-encode keyframe images (Level 0-2 episodes with images)    │  │
│  │   • For Level 3+ (no images): apply adapter projection network    │  │
│  │   • Update HNSW index (rebuild async, swap atomically)            │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

# 8. COMPLETE DATA FLOW — END TO END

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          COMPLETE SYSTEM DATA FLOW                               │
│                                                                                 │
│  ┌───────────┐                                                                  │
│  │ AR GLASSES│  1 FPS camera + always-on mic + IMU + eye tracking              │
│  │           │                                                                  │
│  │  Sensors  ├──►┌──────────────────────────────────────────────┐               │
│  │  always   │   │           ON-DEVICE (Edge NPU)               │               │
│  │  on       │   │                                              │               │
│  │           │   │  RAW FRAME ──► MobileCLIP ──► 512-dim emb   │               │
│  │  ~80mW    │   │           ──► DINOv2     ──► 384-dim emb   │               │
│  │  passive  │   │           ──► RetinaFace ──► face boxes     │               │
│  │           │   │           ──► FaceNet    ──► 128-dim emb   │               │
│  │           │   │                                              │               │
│  │           │   │  RAW AUDIO ──► Silero VAD ──► speech Y/N    │               │
│  │           │   │            ──► ECAPA-TDNN ──► speaker emb   │               │
│  │           │   │                                              │               │
│  │           │   │  IMU DATA ──► Activity classifier            │               │
│  │           │   │           ──► walk/sit/drive/stationary      │               │
│  │           │   │                                              │               │
│  │           │   │  CHANGE GATE: cos_sim(curr, prev) < 0.85?   │               │
│  │           │   │    YES → Package embeddings + JPEG keyframe  │               │
│  │           │   │    NO  → Package embeddings only (no image)  │               │
│  │           │   │                                              │               │
│  │           │   │  Opus encode audio (if speech detected)      │               │
│  │           │   │  20ms frames, 16-32kbps VBR, DTX enabled    │               │
│  │           │   │                                              │               │
│  │           │   └──────────┬───────────────────────────────────┘               │
│  │           │              │                                                   │
│  │           │              │  SensorFrame protobuf (~2-20KB)                   │
│  │           │              │  + Opus audio packets (~4KB/sec when speaking)     │
│  │           │              │                                                   │
│  └───────────┘              ▼                                                   │
│                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────┐         │
│  │              gRPC OVER HTTP/2 + TLS 1.3                           │         │
│  │                                                                    │         │
│  │  PASSIVE: Unary RPC, 1/sec, ~2-20KB up, 0 down                   │         │
│  │  LIVE:    Bidi stream, 5-30/sec, ~50KB/sec up, ~8KB/sec down      │         │
│  └───────────────────────────────┬────────────────────────────────────┘         │
│                                  │                                              │
│                                  ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                        CLOUD PROCESSING                                  │   │
│  │                                                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐     │   │
│  │  │ INGESTION (async for passive, sync for live)                   │     │   │
│  │  │                                                                 │     │   │
│  │  │  Whisper-v3 ASR ──► transcript + word timestamps               │     │   │
│  │  │  Speaker diarization ──► who said what                         │     │   │
│  │  │  VLM captioning (Gemini Flash) ──► scene description           │     │   │
│  │  │  Entity extraction ──► people, objects, text, screens          │     │   │
│  │  │  Episode boundary detection ──► close/open episodes            │     │   │
│  │  └──────────────────────────────┬──────────────────────────────────┘     │   │
│  │                                 │                                        │   │
│  │                                 ▼  WRITE PATH                            │   │
│  │  ┌──────────────────────────────────────────────────────────────────┐    │   │
│  │  │                    MEMORY STORES                                  │    │   │
│  │  │                                                                  │    │   │
│  │  │  Redis ◄── Working Memory (current scene, entities, state)      │    │   │
│  │  │  Postgres + pgvector ◄── Episodic Memory (episodes)             │    │   │
│  │  │  Neo4j ◄── Semantic Memory (people, places, facts)              │    │   │
│  │  │  DynamoDB ◄── Procedural Memory (routines, patterns)            │    │   │
│  │  │  S3 ◄── Blob store (keyframe JPEGs, audio clips)               │    │   │
│  │  └──────────────────────────────────────────────────────────────────┘    │   │
│  │                                 │                                        │   │
│  │            ┌────────────────────┴────────────────────┐                   │   │
│  │            │                                         │                   │   │
│  │      READ PATH (reactive)                  READ PATH (proactive)         │   │
│  │            │                                         │                   │   │
│  │            ▼                                         ▼                   │   │
│  │  ┌──────────────────────┐             ┌──────────────────────────┐       │   │
│  │  │ USER ASKS QUESTION   │             │ TRIGGER ENGINE fires     │       │   │
│  │  │                      │             │                          │       │   │
│  │  │ ASR → Intent Parse   │             │ Working mem update       │       │   │
│  │  │ → Parallel retrieval │             │ → Evaluate 6 triggers    │       │   │
│  │  │   across all memory  │             │ → Interrupt appropriate? │       │   │
│  │  │   stores             │             │ → Generate if yes        │       │   │
│  │  │ → Re-rank (Park      │             │                          │       │   │
│  │  │   et al. scoring)    │             │                          │       │   │
│  │  │ → LLM generation     │             │                          │       │   │
│  │  └──────────┬───────────┘             └────────────┬─────────────┘       │   │
│  │             │                                      │                     │   │
│  │             └──────────────┬────────────────────────┘                     │   │
│  │                            │                                              │   │
│  │                            ▼                                              │   │
│  │  ┌──────────────────────────────────────────────────────────────────┐     │   │
│  │  │ RESPONSE PIPELINE                                                │     │   │
│  │  │                                                                  │     │   │
│  │  │  LLM text stream ──► TTS (Cartesia Sonic / Inworld TTS Mini)   │     │   │
│  │  │                  ──► Opus encode (32kbps, 20ms frames)          │     │   │
│  │  │                  ──► gRPC downstream LiveResponse stream        │     │   │
│  │  │                  ──► (optional) AR TextOverlay for glasses HUD  │     │   │
│  │  └──────────────────────────────┬───────────────────────────────────┘     │   │
│  │                                 │                                         │   │
│  └─────────────────────────────────┼─────────────────────────────────────────┘   │
│                                    │                                             │
│                                    ▼                                             │
│  ┌────────────────────────────────────────────────────────────────────┐          │
│  │              gRPC DOWNSTREAM (Opus audio + text overlays)          │          │
│  └───────────────────────────────┬────────────────────────────────────┘          │
│                                  │                                               │
│                                  ▼                                               │
│  ┌───────────┐                                                                   │
│  │ AR GLASSES│  Opus decode → bone conduction speaker / AR speaker               │
│  │           │  TextOverlay → AR HUD display                                    │
│  │  User     │  Haptic → vibration for alerts                                   │
│  │  hears    │                                                                   │
│  │  response │  Latency: < 1.5 seconds (first audio from question)              │
│  └───────────┘                                                                   │
│                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐    │
│  │  NIGHTLY CONSOLIDATION (background, during charging)                     │    │
│  │                                                                          │    │
│  │  Episodic → Importance scoring → Semantic extraction →                   │    │
│  │  Routine detection → Progressive compression → Embedding maintenance     │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

# 9. TECHNOLOGY STACK SUMMARY

```
┌───────────────────────────────────────────────────────────────────────┐
│                     FULL TECHNOLOGY STACK                              │
│                                                                       │
│  EDGE (ON-DEVICE)                                                     │
│  ├── Hardware: Qualcomm QCS8550 (NPU 4 TOPS) or MediaTek Dimensity  │
│  ├── OS: Android AOSP (glasses) / iOS (phone companion)              │
│  ├── Inference: TensorFlow Lite / ONNX Runtime Mobile / QNN SDK      │
│  ├── Models:                                                          │
│  │   ├── MobileCLIP-S2 (35M, INT8 quantized, ~3ms)                  │
│  │   ├── DINOv2-small (22M, INT8, ~2ms)                             │
│  │   ├── RetinaFace-mobile (1.7M, ~5ms)                             │
│  │   ├── MobileFaceNet (1M, ~3ms)                                    │
│  │   ├── Silero VAD (1.5M, ~1ms)                                    │
│  │   └── ECAPA-TDNN-small (5M, ~3ms)                                │
│  ├── Audio: Opus codec (libopus, 16-32kbps VBR, DTX)                │
│  ├── Transport: gRPC (nanopb for constrained devices)                │
│  └── Storage: SQLite (local queue), LRU frame cache                  │
│                                                                       │
│  TRANSPORT                                                            │
│  ├── Protocol: gRPC over HTTP/2 (unary + bidi streaming)             │
│  ├── Serialization: Protocol Buffers v3                               │
│  ├── Audio: Opus (RFC 6716), 20ms frames, FEC + DTX                  │
│  ├── Video: JPEG (keyframes) or H.265 (live mode)                    │
│  ├── Security: TLS 1.3 + mTLS device certificates                   │
│  └── Resilience: Exponential backoff, on-device queue, batch sync    │
│                                                                       │
│  CLOUD - INGESTION                                                    │
│  ├── Gateway: Envoy proxy / AWS ALB with gRPC support                │
│  ├── Queue: Apache Kafka (per-user partitioned) or AWS SQS FIFO     │
│  ├── ASR: Whisper-large-v3 (self-hosted on GPU) or Deepgram API     │
│  ├── VLM: Gemini 2.5 Flash / Phi-3-Vision (captioning)              │
│  ├── Speaker ID: pyannote.audio (diarization + embedding)            │
│  └── Workers: Kubernetes pods, GPU-backed (NVIDIA A10G / L4)         │
│                                                                       │
│  CLOUD - MEMORY STORES                                                │
│  ├── Working Memory: Redis Cluster (< 10ms reads, per-user keys)     │
│  ├── Episodic Memory: PostgreSQL 16 + pgvector (HNSW indices)        │
│  ├── Semantic Memory: Neo4j Aura (knowledge graph)                   │
│  ├── Procedural Memory: DynamoDB (pattern store, low-read volume)    │
│  ├── Blob Store: S3 (keyframes, audio clips, AES-256 encrypted)     │
│  └── Partitioning: Per-user hash sharding, monthly time partitions   │
│                                                                       │
│  CLOUD - REASONING                                                    │
│  ├── Intent Parsing: Claude Haiku / Gemini Flash (~100ms)            │
│  ├── Response Gen: Claude Sonnet / Gemini Pro (~150ms first token)   │
│  ├── Retrieval: Parallel queries across all memory stores             │
│  ├── Re-ranking: Cross-encoder or LLM-based (Park et al. scoring)   │
│  └── Proactive Triggers: Rule engine + lightweight LLM calls          │
│                                                                       │
│  CLOUD - RESPONSE                                                     │
│  ├── TTS: Cartesia Sonic 3 / Inworld TTS-1.5 Mini (< 100ms TTFB)   │
│  ├── Encoding: Opus (server-side, 32kbps, matching device config)    │
│  ├── Streaming: gRPC server-streaming (interleaved audio + text)     │
│  └── AR Overlays: Protobuf TextOverlay messages for HUD              │
│                                                                       │
│  CLOUD - CONSOLIDATION                                                │
│  ├── Scheduler: Temporal.io / AWS Step Functions (per-user cron)     │
│  ├── Batch LLM: Claude Batch API / Gemini batch (fact extraction)    │
│  ├── Pattern Mining: PrefixSpan (scipy/mlxtend, CPU-only)            │
│  ├── Compression: S3 lifecycle policies + Postgres partition drops    │
│  └── Re-indexing: pgvector HNSW rebuild (async, swap atomic)         │
│                                                                       │
│  OBSERVABILITY                                                        │
│  ├── Metrics: Prometheus + Grafana (latency P50/P99, memory sizes)   │
│  ├── Traces: OpenTelemetry (end-to-end trace from device to response)│
│  ├── Logs: Structured JSON → CloudWatch / Datadog                    │
│  └── Alerts: Latency > 2s, memory store growth anomalies, errors     │
└───────────────────────────────────────────────────────────────────────┘
```

---

# 10. KEY DESIGN REFERENCES

| Reference | Contribution to This Design |
|---|---|
| **Google Project Astra** (I/O 2024-25) | Hybrid edge/cloud pipeline, temporal compression (3-5 FPS sampling), sub-300ms latency target, 10-min active memory |
| **MemGPT** (Packer et al., 2023) | Virtual context management (main context ↔ external context paging), LLM as self-directed memory manager, memory pressure warnings |
| **Park et al., Generative Agents** (2023) | Retrieval scoring formula (recency × importance × relevance), episodic→semantic reflection, importance scoring at encoding |
| **Memoro** (Zulfikar et al., CHI 2024) | Queryless mode validation (50% of users prefer proactive), concise responses, bone-conduction delivery |
| **Meta Aria Gen 2** (2025) | 4-camera egocentric sensing, 120dB HDR, 80° stereo overlap, on-device SLAM + hand tracking |
| **Limitless Pendant** (acquired by Meta 2025) | Audio-first commercial validation, beamforming mic array, speaker diarization on 20s of labeled audio, 100-hr battery |
| **MaRS / FiFA** (2025) | Formalized forgetting policies (Hybrid wins), typed memory stores with provenance tracking, privacy-aware retention |
| **CoALA** (Sumers et al., 2023) | Unifying taxonomy: working/episodic/semantic/procedural memory + grounding/reasoning/retrieval/learning actions |
| **Opus RFC 6716** | Audio codec: 5-26.5ms latency, SILK+CELT hybrid, DTX for silence suppression, in-band FEC, mandatory in WebRTC |
| **gRPC / HTTP/2** | Protobuf serialization, bidirectional streaming, multiplexing, built-in flow control, auto-generated clients |
| **pgvector** | HNSW indices in PostgreSQL for vector similarity search alongside relational queries (temporal, entity, spatial) |
| **Complementary Learning Systems** (McClelland et al., 1995) | Dual-system theory (fast hippocampal + slow neocortical) → episodic (fast encode) + semantic (slow consolidation) |
| **NVIDIA Triton Inference Server** | Edge model serving: C-API for Jetson (zero-overhead), multi-framework backends, model ensembles |
| **Stream Vision Agents** (2025) | Open-source WebRTC + LLM + VLM pipeline for real-time video AI, Silero VAD + Whisper turn detection |
