# NVIDIA Metropolis Vision AI: complete technical deep dive

**Metropolis is NVIDIA's end-to-end vision AI platform—a collection of SDKs, microservices, foundation models, and blueprints spanning camera ingestion through actionable analytics across edge, on-prem, and cloud deployments.** It integrates DeepStream (streaming analytics), TAO Toolkit (model training), TensorRT (inference optimization), Triton (model serving), and NVIDIA NIM (foundation model microservices) into a unified architecture. As of 2025–2026, Metropolis has undergone a paradigm shift from pure CNN-based pipelines to VLM-powered Visual AI Agents using Cosmos Reason, VILA, and the VSS Blueprint for zero-shot video understanding. This report covers every architectural layer in the detail needed for system design interviews and deep technical discussions.

---

## 1. High-level architecture and ecosystem map

### Platform positioning

Metropolis is a **platform**, not a single product. It provides software building blocks deployable consistently across NVIDIA's entire compute spectrum: **Jetson** edge devices (Orin, Thor), **dGPU** servers (A100, H100, L40, RTX PRO 6000), and cloud (DGX Cloud, build.nvidia.com NIM APIs). The architecture stack, bottom to top:

- **Hardware layer**: Jetson Orin/Thor (edge), IGX Thor (industrial), dGPU + DGX (data center/cloud)
- **Software foundation**: CUDA, cuDNN, JetPack SDK (edge) or NVIDIA AI Enterprise (data center), NVIDIA Container Runtime
- **Core SDKs**: DeepStream SDK (streaming analytics), TensorRT (inference optimization), Triton Inference Server (model serving), TAO Toolkit (training/fine-tuning)
- **Microservices layer**: Metropolis Microservices v2 (enterprise dGPU), Jetson Platform Services (edge), NIM microservices (foundation models)
- **Application layer**: VSS Blueprint (video search & summarization), reference applications (AI-NVR, MTMC tracking, retail analytics), VIA microservices (VLM-powered agents)
- **Simulation & training**: Omniverse Replicator (synthetic data), Isaac Sim (robotics simulation), Cosmos Transfer (3D sim → photorealistic video)

### End-to-end pipeline from cameras to analytics

A canonical Metropolis deployment flows through these stages:

**1. Video ingestion** — IP cameras deliver RTSP/ONVIF streams to the **Video Storage Toolkit (VST)** microservice, which handles discovery, reconnection, storage, and provides proxy RTSP links. **2. Stream processing** — DeepStream SDK receives streams via `nvurisrcbin`, hardware-decodes via **NVDEC** (H.264/H.265/AV1), and batches multiple streams through `nvstreammux`. **3. AI inference** — The `nvinfer` plugin runs TensorRT-optimized detection models (PeopleNet, YOLO, etc.) or the `nvinferserver` plugin delegates to Triton for multi-framework support. Models are trained/fine-tuned via TAO Toolkit. **4. Tracking** — `nvtracker` assigns persistent IDs using NvDCF, NvDeepSORT, NvSORT, or IOU algorithms. **5. Analytics** — The analytics microservice computes line-crossing counts, ROI occupancy, direction detection, and Single-View 3D Tracking. **6. Messaging** — Metadata flows to **Redis** (intra-cluster message bus) or **Kafka** (inter-service), then to **Kibana** dashboards. **7. VLM reasoning** (optional) — Cosmos Reason or VILA processes frames with natural language prompts for zero-shot event detection and summarization via NIM APIs.

### Cloud-edge-device topology

Metropolis deploys across a **three-tier model**. The **edge tier** (Jetson Orin/Thor) runs Jetson Platform Services with Docker Compose—15+ microservices including VST, DeepStream perception, zero-shot detection (NanoOWL), Redis, API gateway, monitoring, IoT gateway, and firewall. The **on-premises tier** (dGPU servers) runs Metropolis Microservices v2 with Kubernetes + Helm orchestration, supporting multi-camera tracking, occupancy heatmaps, and transformer-based ReID. The **cloud tier** provides NIM APIs at build.nvidia.com, DGX Cloud for training, and IoT Cloud modules for secure device-to-cloud connectivity via SASL/Plain authentication and 2-way TLS. Edge-to-cloud communication uses an always-on TCP connection from the IoT Gateway with API gateway routing requests to specific devices by ID, plus WebRTC for real-time video streaming and OpenVPN for secure tunneling.

---

## 2. DeepStream SDK pipeline architecture

### GStreamer foundation and GPU extension model

DeepStream extends GStreamer with **40+ GPU-accelerated plugins** that encapsulate NVIDIA libraries (CUDA, TensorRT, NVDEC, NVENC, VPI). The critical design decision is **zero-memory-copy between plugins** via NVMM (NVIDIA Memory Management)—buffers remain in GPU memory throughout the pipeline. GStreamer's caps negotiation uses `video/x-raw(memory:NVMM), format=RGBA` to signal NVIDIA-managed memory surfaces. The unified buffer abstraction **NvBufSurface** wraps GPU/VIC memory across all plugins, supporting memory types including `NVBUF_MEM_CUDA_DEVICE` (dGPU default), `NVBUF_MEM_CUDA_PINNED` (page-locked CPU), `NVBUF_MEM_CUDA_UNIFIED` (managed memory), and `NVBUF_MEM_SURFACE_ARRAY` (Jetson default).

The canonical pipeline data flow: `RTSP source → nvv4l2decoder (NVDEC HW decode → NV12) → nvstreammux (batching, attaches NvDsBatchMeta) → nvinfer (primary detection via TensorRT → NvDsObjectMeta) → nvtracker (assigns unique IDs) → nvinfer (secondary classification) → nvdsanalytics (line crossing, ROI) → nvdsosd (bounding boxes, labels) → output branch (RTSP out / Kafka / file / display)`.

Pipeline construction methods include `gst-launch-1.0` CLI for testing, programmatic C/C++ or Python bindings, INI-style config files for `deepstream-app`, and the new **Service Maker** framework (GA in DeepStream 8.0) that removes the need for GStreamer programming. **DeepStream 9.0** (latest, 2025) supports Ubuntu 24.04, TensorRT 10.9+, and Blackwell/Ada/Hopper/Ampere GPUs.

### Core plugin catalog

**Inference plugins**: `Gst-nvinfer` handles native TensorRT inference—accepts batched NV12/RGBA, performs format conversion + scaling + normalization (`y = net_scale_factor * (x - mean)`), runs the TensorRT engine, and supports detection, classification, segmentation, and instance segmentation modes. Supports FP16/FP32/INT8, ONNX models, TAO exported models, and pre-built engine files. `Gst-nvinferserver` provides Triton-based inference supporting TensorFlow, PyTorch, ONNX backends via gRPC, plus ensemble models and custom pre/post-processing via `IInferCustomProcessor`. `Gst-nvdspreprocess` enables ROI-based preprocessing before primary inference.

**Stream handling**: `Gst-nvstreammux` batches frames from multiple sources into a single batch with configurable `batch-size`, `width`, `height`, and `batched-push-timeout`. The **new nvstreammux** (enabled via `USE_NEW_NVSTREAMMUX=yes`) supports adaptive and heterogeneous batching. `Gst-nvstreamdemux` splits batched buffers back to individual streams. `Gst-nvmultiurisrcbin` supports dynamic sensor provisioning via REST API.

**Tracking**: `Gst-nvtracker` supports multiple algorithms through a unified library (`libnvds_nvmultiobjecttracker.so`). **Video processing**: `nvv4l2decoder`/`nvv4l2h264enc` (NVDEC/NVENC wrappers), `nvvideoconvert` (GPU color space conversion), `nvdewarper` (fisheye correction). **Analytics**: `nvdsanalytics` for line crossing, ROI occupancy, direction detection. **Messaging**: `nvmsgconv` generates JSON payloads from metadata; `nvmsgbroker` sends to Kafka, MQTT, AMQP, Redis, or Azure IoT Hub. **3D/sensor fusion**: `nvds3dfilter`, `nvds3dbridge`, `nvds3dmixer` for LiDAR and depth camera integration.

### Metadata system: the hierarchical data model

DeepStream's metadata flows through a strict hierarchy attached to GstBuffers:

```
NvDsBatchMeta (created by nvstreammux)
 └─ frame_meta_list → [NvDsFrameMeta per source]
      ├─ obj_meta_list → [NvDsObjectMeta per detection]
      │    ├─ classifier_meta_list → [NvDsClassifierMeta]
      │    │    └─ label_info_list → [NvDsLabelInfo]
      │    └─ obj_user_meta_list → [NvDsUserMeta]
      ├─ display_meta_list → [NvDsDisplayMeta]
      └─ frame_user_meta_list → [NvDsUserMeta]
```

**NvDsBatchMeta** contains `max_frames_in_batch`, `num_frames_in_batch`, pre-allocated metadata pools (`frame_meta_pool`, `obj_meta_pool`, `classifier_meta_pool`, `display_meta_pool`, `user_meta_pool`), and a `meta_mutex` (GRecMutex) for thread-safe access. **NvDsFrameMeta** carries `batch_id`, `frame_num`, `buf_pts` (PTS), `ntp_timestamp`, `source_id`, and resolution info. **NvDsObjectMeta** holds `object_id` (tracking ID), `class_id`, `detector_bbox_info`, `tracker_bbox_info`, `confidence`, `tracker_confidence`, and `mask_params` for segmentation masks. **NvDsUserMeta** is the extensibility point—a `void*` pointer with copy/release function pointers for custom data at batch, frame, or object level. Special types include `NvDsInferTensorMeta` (raw tensor output) and `NvDsInferSegmentationMeta`.

Metadata flows additively: `nvstreammux` creates NvDsBatchMeta → `nvinfer` (primary) adds NvDsObjectMeta → `nvtracker` updates with tracking IDs → `nvinfer` (secondary) adds NvDsClassifierMeta → `nvdsanalytics` adds analytics events → `nvdsosd` reads NvDsDisplayMeta → `nvmsgconv` reads everything to generate JSON.

**Probe functions** are the primary mechanism for custom metadata access. Attach to any element's pad via `gst_pad_add_probe()` with `GST_PAD_PROBE_TYPE_BUFFER`, then iterate `batch_meta->frame_meta_list->obj_meta_list` in the callback. This enables filtering detections, adding custom metadata, triggering alerts, or forwarding to external systems at any pipeline point.

### Tracker algorithm implementations

The unified tracker architecture (DeepStream 6.0+) uses composable modules: data association, state estimation (Kalman filter), model inference (ReID via TensorRT), target management, and bounding-box unclipping.

**IOU tracker**: Pure bbox overlap matching between frames. CPU-only, no visual features, fastest but lowest accuracy. Sets `tracker_confidence = 1.0`. **NvSORT**: NVIDIA-enhanced SORT with Kalman filter for motion prediction + cascaded data association. No pixel data needed. **NvDeepSORT**: Adds a Re-ID neural network for appearance-based association using deep cosine metric learning. Crops objects, extracts embeddings via TensorRT, combines with bbox geometry. GPU-accelerated. **NvDCF**: Discriminative Correlation Filter providing independent visual tracking even without detections. GPU-accelerated DCF computation with optional VPI/PVA backend on Jetson. Only tracker generating actual `tracker_confidence` values (not just 1.0). Highest accuracy, highest cost. **MaskTracker** (DS 8.0+): Uses SAM2 for tracking + segmentation—generates per-target segmentation masks via TensorRT-accelerated SAM2 inference.

---

## 3. TAO Toolkit training and TensorRT optimization

### TAO transfer learning workflow

The canonical TAO pipeline: **select pretrained model** from NGC (100+ models) → **fine-tune** on custom domain data → **prune** (magnitude-based structured pruning, controlled by `pruning_threshold` parameter) → **retrain** pruned model to recover accuracy → **export to ONNX** → **optimize with TensorRT** → **deploy via DeepStream or Triton**. A critical detail: transfer learning is NOT supported on pruned models—you must retrain from the pruned graph with `load_graph=true`.

**Supported architectures** span detection (DetectNet_v2, DINO, RT-DETR, Grounding DINO, Deformable DETR), classification (FAN, GC-ViT, SWIN, DINOv2, C-RADIOv2, ConvNext backbones), segmentation (SegFormer, UNET, Mask2former, OneFormer), and purpose-built models (**PeopleNet**: ResNet-34, trained on 7.6M+ images; **TrafficCamNet**, **DashCamNet**, **FaceDetectIR**, **ActionRecognitionNet**, **LPRNet**, **BodyPoseNet**, **PoseClassificationNet**). TAO 6.x adds foundation model support (NV-DINOv2, C-RADIOv2) and VLM fine-tuning.

**Quantization-aware training (QAT)** modifies the training graph to emulate INT8 quantization by inserting fake quantization nodes on weights. The model learns to mitigate quantization error during training, yielding higher INT8 accuracy than post-training quantization alone. **Post-training quantization** is also supported via TorchAO (weight-only, no calibration) and NVIDIA ModelOpt (static PTQ, requires calibration data). TAO 5.0+ deprecated the encrypted `.etlt` format in favor of standard ONNX export, open-sourced the codebase, and integrated `trtexec` directly.

### TensorRT engine building internals

TensorRT is fundamentally a **compiler**, not a runtime. The 6-step optimization pipeline: **parse ONNX** into TensorRT network definition (backward compatible to opset 9, unsupported ops automatically matched against registered plugins) → **graph optimization and layer fusion** → **kernel auto-tuning** → **precision calibration** → **serialize to GPU-specific engine file**.

**Layer fusion** is the single most impactful optimization. **Vertical fusion** merges sequential operations into single kernels: Conv + BN + ReLU becomes one CBR kernel, reducing HBM accesses from 6 to 2—the dominant bottleneck for memory-bound inference. Conv + Add (residual) + ReLU, MatMul + Bias + Activation, and ElementWise + ReLU are also fused. **Horizontal fusion** aggregates parallel operations with shared inputs: multiple 1×1 CBR layers combine into one with concatenated weights (critical for Inception architectures). **Elimination fusion** removes consecutive transposes, dead layers, and folds constants. Complex attention patterns (BMM-Softmax-BMM) cannot be automatically fused and require plugins.

**Kernel auto-tuning** profiles multiple kernel implementations (GEMM, Winograd, FFT, Implicit GEMM) on the target GPU, measuring actual runtime, and selects the fastest. This is why engine builds are slow and **engines are GPU-architecture specific**. The `builderOptimizationLevel` parameter (0–5, default 3) controls how many tactics are evaluated. Timing caches persist profiling results for faster rebuilds on identical hardware.

### INT8 calibration deep dive

TensorRT provides four calibration algorithms. **Entropy calibration (IInt8EntropyCalibrator2)**: the default for CNNs—collects activation histograms across calibration data, then finds thresholds minimizing KL divergence between FP32 and INT8 distributions. **MinMax calibration**: takes absolute max activation value as threshold—simple but sensitive to outliers, recommended for NLP. **Percentile calibration**: uses CDF percentile (e.g., 99.9%) as threshold, robust to outliers. **MSE calibration**: exhaustively searches threshold space minimizing mean squared error—most compute-intensive but directly optimizes quantization error. Calibration targets activations only; weight ranges are derived directly from parameters. Scale factors are: `scale = 127.0 / threshold`.

**Dynamic shapes** use optimization profiles with min/opt/max dimensions. The optimal shape should match the most common input size, as kernels are tuned for it. Multiple profiles support different shape ranges. **TensorRT 10.x** introduced IPluginV3 (replacing deprecated IPluginV2 variants), Quickly Deployable Plugins (QDPs) for Python rapid prototyping, weight streaming for models larger than GPU memory, FP8 support on Hopper/Ada, and **FP4 (E2M1)** on Blackwell. **TensorRT 10.16** (latest) adds MXFP8 quantization, IAttention API, multi-device inference preview, and MoE layer support.

---

## 4. Triton Inference Server architecture

### Core architecture: repository, schedulers, backends

Triton is a **file-system-repository-based** model serving platform with four subsystems. The **model repository** stores models in a structured directory hierarchy (`<model-name>/<version>/model.plan`) with `config.pbtxt` protobuf configuration. Supports local filesystem, S3, GCS, and Azure Storage. The **request handler** accepts requests via HTTP/REST (port 8000), gRPC (port 8001), or C API, implementing the **KServe inference protocol**. The **scheduler** dispatches requests: Dynamic Batcher, Sequence Batcher (for stateful models), Default Scheduler, or Ensemble Scheduler. Each **backend** executes inference with framework-specific executors (TensorRT, ONNX Runtime, PyTorch, TensorFlow, Python, DALI, FIL, TRT-LLM, vLLM).

### Dynamic batching and concurrent execution

Dynamic batching transparently combines individual inference requests server-side. Key configuration: `preferred_batch_size` (batch sizes preferentially created—NVIDIA recommends not setting this for most models), `max_queue_delay_microseconds` (maximum wait time to form larger batches, trading latency for throughput), `preserve_ordering` (FIFO response ordering), and `priority_levels` (multi-priority queues). Custom batching strategies can be implemented as shared libraries with five C functions.

**Concurrent model execution** is controlled by `instance_group` configuration—multiple model instances each get their own execution context and CUDA stream. The GPU hardware scheduler interleaves memory copies and kernel executions from independent streams. Configuration: `instance_group [ { count: 3  kind: KIND_GPU  gpus: [ 0, 1 ] } ]`.

### Ensemble models and BLS

**Ensemble models** represent DAG pipelines connecting multiple models without client intervention. Configured with `platform: "ensemble"` and `ensemble_scheduling` steps defining `input_map`/`output_map` connections. The ensemble scheduler is event-driven with minimal overhead; component models independently use dynamic batching. Fan-out and fan-in patterns are supported.

**Business Logic Scripting (BLS)** enables custom control flow in Python backend models. BLS models can create internal `InferenceRequest` objects targeting other models, execute synchronously (`exec()`) or asynchronously (`async_exec()`), and compose complex workflows with loops, conditionals, and data-dependent routing. Parallel BLS calls use `asyncio.gather()`. BLS models can be decoupled for streaming responses.

**Decoupled models** send zero, one, or multiple responses per request—essential for LLM token-by-token generation. Enabled with `model_transaction_policy { decoupled: true }`, using `InferenceResponseSender` for asynchronous response delivery.

### Monitoring and shared memory

Prometheus metrics at `:8002/metrics` expose GPU utilization, memory usage, inference counts, request latency breakdowns (queue, compute input, compute infer, compute output), and pending request counts. Health endpoints (`/v2/health/ready`, `/v2/health/live`) integrate with Kubernetes probes. **CUDA shared memory** enables zero-copy GPU-to-GPU data transfer between client and server via IPC handles, eliminating network copy overhead for co-located processes.

---

## 5. Metropolis microservices, NIM, and VLM integration

### Microservices architecture

Metropolis Microservices v2 (enterprise dGPU) uses Kubernetes + Helm orchestration with Docker containers, Kafka for inter-service messaging, Redis as a global message bus, and the ELK stack (Elasticsearch, Logstash, Kibana) for visualization. **Application services** include AI perception (DeepStream-based detection/tracking), analytics (line crossing, ROI, SV3DT), and generative AI (NanoOWL zero-shot detection). **Platform services** include Nginx Ingress API gateway, Grafana monitoring, and system management. **Cloud services** include IoT Gateway for secure edge-to-cloud connectivity.

The **Video Storage Toolkit (VST)** is the centralized video ingestion microservice handling camera discovery, reconnection, storage, and proxy RTSP link management. All video sources must flow through VST. The **Sensor Distribution & Routing (SDR)** service listens to VST stream events on Redis and auto-configures AI services. Reference applications include **AI-NVR**, **Multi-Camera Tracking (MTMC)**, **Real-Time Locating System (RTLS)**, and **few-shot product recognition** for retail.

### NVIDIA NIM and the VLM paradigm shift

**NIM (NVIDIA Inference Microservices)** are containerized, GPU-accelerated inference services packaging foundation models with optimized engines (TensorRT, TensorRT-LLM, vLLM, SGLang) behind OpenAI-compatible REST APIs. Vision NIM models include **Cosmos Reason** (7B reasoning VLM), **VILA** (now Cosmos Nemotron), **NV-DINOv2**, **NV-CLIP**, **C-RADIO**, and **Llama 3.2 Vision**. Self-hosted deployment requires NGC container pull; cloud APIs at build.nvidia.com offer 5,000 free credits.

The **VSS Blueprint** (Video Search and Summarization), GA since COMPUTEX 2025, is Metropolis's flagship VLM application—100x faster video summarization than manual review. Built on VILA + Llama Nemotron + NeMo Retriever + RAG. Version 3.0 (GTC 2026) adds **Agentic Information Retrieval** decomposing complex queries to find events in under 5 seconds. The **VIA (Visual Intelligence Agent) Microservices** extend Metropolis with VLM-powered agents: a stream handler manages video decoding/chunking, a VLM pipeline runs visual encoder (TensorRT) + VLM inference, **CA-RAG** (Context-Aware RAG via LangChain) extracts and summarizes per-chunk responses, and NeMo Guardrails filter invalid prompts.

### Zero-shot detection and visual prompting

At the edge, **NanoOWL** (optimized OWL-ViT) runs as a Jetson Platform Services microservice, detecting objects specified via natural language prompts sent through REST APIs—detection classes change dynamically without retraining. For deeper reasoning, Cosmos Reason and VILA enable zero-shot event detection, arbitrary question answering over video, and defect classification with >96% accuracy using minimal labeled examples. **NV-DINOv2** achieves **98.51%** accuracy for die-level defect detection using self-supervised learning.

---

## 6. Low-level GPU memory and CUDA stream management

### Zero-copy decode-to-inference pipeline

The entire Metropolis video pipeline stays in GPU memory. **NVDEC** (a fixed-function hardware block separate from CUDA cores) decodes H.264/H.265/AV1 directly into GPU video memory as NV12 surfaces—no CPU round-trip. DeepStream's `nvv4l2decoder` outputs frames with `memory:NVMM` capability, signaling NVIDIA-managed memory. These frames flow to `nvstreammux` (batching), then to `nvinfer` (inference), all via NvBufSurface pointers without CPU copies. On **dGPU systems**, NVDEC writes to discrete GPU memory; on **Jetson**, the unified memory architecture means CPU, GPU, DLA, PVA, and NVDEC all share the same LPDDR5 pool with no PCIe bottleneck.

Buffer management details: `nvstreammux` creates internal pools of **4 buffers per source** at muxer output resolution. Pre-allocation prevents runtime allocation overhead. For 200+ streams on dGPU, NVIDIA recommends stopping the display manager and reloading kernel modules with special registry keys (`RMDebugOverridePerRunlistChannelRam=1`, `RMIncreaseRsvdMemorySizeMB=1024`). The NvBufSurface sync protocol requires `NvBufSurfaceSyncForDevice()` after CPU writes and `NvBufSurfaceSyncForCpu()` before CPU reads—violation causes data corruption.

### CUDA stream pipelining

DeepStream plugins internally manage CUDA streams, with each element operating on its own stream. The **pipeline overlap pattern** enables concurrent execution: while NVDEC decodes frame N+1, CUDA pre-processes frame N, and TensorRT infers on frame N-1—each in separate CUDA streams on independent hardware engines (copy engine, kernel execution engine, decode engine). Rather than using separate CUDA streams per camera (which fragments GPU utilization), the optimal pattern for 100+ streams is **batching frames from multiple cameras into single inference calls**—TensorRT processes the batch in one kernel launch. CUDA events (`cudaEventRecord`/`cudaStreamWaitEvent`) provide fine-grained inter-stream synchronization without blocking the host.

### Multi-stream scaling benchmarks

Platform-specific scaling limits: **Jetson Orin AGX** handles up to **16 streams** with PeopleNet on DLA + NvDCF tracker on PVA backend. **Jetson Orin NX 16GB** manages ~40 cameras at 5fps or ~11 at 15fps with YOLOv8s INT8. **dGPU (Hopper/Ampere/Ada)** scales to **200+ streams** with registry key tuning, leveraging multiple NVDEC instances (e.g., 3 on L40G). Key optimization levers: disable tiled display/rendering, use FP16/INT8 precision, leverage DLA on Jetson, use PVA backend for tracker, and set skip-frame inference (`interval=1` halves inference load while tracker fills gaps).

---

## 7. GPU architecture concepts for inference

### Memory hierarchy and Tensor Cores

The GPU memory hierarchy spans **registers** (~256 KB/SM, fastest), **shared memory/L1** (~164 KB on Hopper, programmer-managed, 7–10x faster than global), **L2 cache** (50 MB on H100, hardware-managed), and **global memory/HBM** (80 GB HBM3 at 3.35 TB/s on H100). Layer fusion's impact is best understood through this lens: without fusion, Conv+BN+ReLU requires 6 HBM accesses; with fusion, just 2. Most DL inference at small batch sizes is **memory-bound**, making fusion the dominant optimization.

**Tensor Cores** perform 4×4 matrix multiply-accumulate in a single operation at ~8x CUDA core throughput. H100's 4th-gen Tensor Cores double per-SM MMA rate versus A100, with 4x improvement using FP8. Blackwell adds FP4/FP6 support—**Jetson Thor** achieves **2,070 FP4 TFLOPS**. Convolution and fully-connected layers decompose into matrix multiplications executed on Tensor Cores, making them the primary inference accelerator.

### MIG, MPS, and GPU sharing strategies

**MIG (Multi-Instance GPU)** provides hardware-level partitioning on Ampere+ GPUs (A100, H100), dividing a single GPU into up to **7 isolated instances** with dedicated SMs, memory, cache, and NVDEC engines. Each MIG instance provides full memory QoS and fault isolation—one instance crash doesn't affect others. Kubernetes integration via NVIDIA GPU Operator + MIG manager exposes instances as separate `nvidia.com/gpu` resources. **MPS (Multi-Process Service)** enables software-level SM sharing across processes with concurrent kernel execution but no memory or fault isolation. **Time-slicing** is simplest—GPU context-switches between processes. For production video analytics: MIG for multi-tenant SLA workloads, MPS for development, time-slicing for non-critical deployments. Combining MIG + time-slicing yields maximum density (7 MIG × 4 time-slices = **28 pods per A100**).

---

## 8. Design patterns for production video analytics

### Model cascade and event-driven architecture

The standard cascade pattern: **Primary detection** (PeopleNet/YOLO/SSD generates bounding boxes) → **Secondary classification** (attribute classifiers run on cropped ROIs for color, type, make/model) → **Multi-object tracking** (NvDCF/NvDeepSORT assigns persistent IDs) → **Action recognition** (temporal analysis across frame sequences) → **Cross-camera ReID** (appearance embedding matching across views). Configurable via `process-mode=secondary`, `infer-on-gie-id`, and `infer-on-class-ids` properties in nvinfer config.

Event-driven messaging uses DeepStream's native `nvmsgconv` → `nvmsgbroker` chain with adapters for **Kafka** (`libnvds_kafka_proto.so`), **MQTT** (`libnvds_mqtt_proto.so`), **Redis** (`libnvds_redis_proto.so`), and **AMQP** (`libnvds_amqp_proto.so`). All support autoreconnect (since DS 6.0) and 2-way TLS. The Metropolis stack uses Kafka for inter-microservice communication, Redis for real-time caching and intra-cluster messaging, and ELK for log aggregation and dashboards.

### Edge-cloud hybrid and scaling patterns

The hybrid pattern runs **real-time perception at the edge** (detection, tracking, classification with DeepStream + Jetson) generating compact metadata, then transmits metadata (not video) via Kafka/MQTT to **cloud services** for advanced analytics (multi-camera fusion, long-term storage, model retraining, dashboards). This architecture minimizes bandwidth: a 1080p stream at 30fps requires ~5 Mbps, but its metadata requires only ~5 KB/s.

Horizontal scaling uses **Kubernetes** with Helm charts for Metropolis microservices. GPU sharing via MIG enables dense multi-model deployment. Runtime stream add/remove happens without pipeline restart—plugins reconfigure dynamically on `GST_NVEVENT_PAD_ADDED/DELETED` events. Source management via `nvmultiurisrcbin` with REST API enables programmatic camera provisioning.

---

## 9. Recent developments reshaping Metropolis (2024–2026)

### Cosmos foundation models and Jetson Thor

**NVIDIA Cosmos** (announced CES 2025, expanded at GTC 2025 and SIGGRAPH 2025) integrates deeply with Metropolis. **Cosmos Reason 2** is a 7B-parameter reasoning VLM with physical common sense—now a key VLM in Metropolis workflows, powering the VSS Blueprint. **Cosmos Transfer 2.5** transforms 3D Omniverse simulations into photorealistic training data. **Cosmos Predict 2.5** (2B/14B parameters) simulates future world states for safety validation. The three-stage Omniverse Blueprint for Smart City AI workflow: **Simulate** (Cosmos + Omniverse digital twins) → **Train** (TAO + NeMo) → **Deploy** (Metropolis VSS Blueprint).

**Jetson Thor** (GA August 2025) brings Blackwell architecture to the edge with **2,070 FP4 TFLOPS**, 128 GB memory, 40–130W power, **7.5x** higher AI compute versus AGX Orin, and **5x** speedup in generative reasoning. It runs mainstream LLMs/VLMs locally and ships with JetPack 7.0. The developer kit costs $3,499. **IGX Thor** is the industrial variant with ISO 26262/IEC 61508 functional safety compliance and 200 GbE RDMA networking.

At **GTC 2026**, NVIDIA announced VSS Blueprint 3.0 with agentic information retrieval, DeepStream 8.0 with multi-camera tracking and low-code inference builder, and partnerships with T-Mobile + Nokia for AI-RAN distributed edge AI with Metropolis. Real-world deployments include **K2K** processing 1,000+ video streams in Palermo, **Pegatron** achieving 67% defect rate decrease, and **Kaohsiung City** reducing incident response time by 80%.

---

## Conclusion

Metropolis has evolved from a video analytics SDK collection into an **agentic vision AI platform** where VLMs reason over video streams using natural language. Three architectural insights stand out for system design interviews. First, the **zero-copy GPU memory pipeline** from NVDEC decode through TensorRT inference to NVENC encode eliminates CPU round-trips entirely—the NvBufSurface abstraction and `memory:NVMM` caps are the mechanism. Second, **batched multi-stream inference** (not per-stream CUDA streams) is the scaling pattern—nvstreammux batches N camera frames into single TensorRT calls, with skip-frame inference + tracker gap-filling as the throughput multiplier. Third, the **convergence of traditional CV and VLMs** creates a dual-path architecture: DeepStream handles real-time detection/tracking at 30fps, while NIM-served VLMs (Cosmos Reason, VILA) provide zero-shot reasoning on sampled frames—edge and cloud working in concert through Kafka/Redis event-driven messaging. The Jetson Thor's 2,070 FP4 TFLOPS makes VLM inference at the edge viable for the first time, collapsing the edge-cloud boundary that defined earlier Metropolis deployments.