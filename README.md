# TextGen

A fork of [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) with additional features and improvements.

## Features

- Web UI for running Large Language Models
- Support for multiple backends (llama.cpp, ExLlamaV2, transformers, etc.)
- OpenAI-compatible API
- Extensions support
- Portable releases for Windows and Linux

## Installation

### Option 1: Portable Release (Recommended)

Download the latest release for your platform from the [Releases](../../releases) page.

**Windows (CUDA):**
```
1. Download and extract the portable release
2. Run start_windows.bat
```

**Linux (CUDA):**
```bash
1. Download and extract the portable release
2. chmod +x start_linux.sh
3. ./start_linux.sh
```

### Option 2: Manual Installation

**Requirements:**
- Python 3.11
- CUDA 12.1+ (for GPU acceleration)

```bash
git clone https://github.com/yourusername/textgen
cd textgen
pip install -r requirements.txt
python server.py
```

## Usage

```bash
# Start with default settings
python server.py

# Start with specific model
python server.py --model your-model-name

# Start API server only
python server.py --api --nowebui

# Listen on all interfaces (useful for local network access)
python server.py --listen --listen-port 7860

# My usual setup — UI accessible on LAN + API on default port, with a specific model pre-loaded
python server.py --listen --listen-port 7860 --api --model mistral-7b-instruct
```

> **Personal note:** I usually run with `--listen --listen-port 7860 --api` so I can access the UI
> from other devices on my LAN while also hitting the API from local scripts.
> Adding `--model mistral-7b-instruct` saves the extra step of loading it through the UI each time.

## API

The server exposes an OpenAI-compatible API at `http://localhost:5000/v1`.

See the [API documentation](docs/API.md) for details.

## Supported Model Formats

| Format | Backend |
|--------|----------|
| GGUF | llama.cpp |
| GPTQ | ExLlamaV2 / AutoGPTQ |
| EXL2 | ExLlamaV2 |
| AWQ | AutoAWQ |
| HF Transformers | transformers |

## Building from Source

See `.github/workflows/` for build scripts.

```bash
# Build portable release (Linux)
bash .github/workflows/build-portable-release-cuda.yml
```

## Contributing

Pull requests are welcome. Please read the contributing guidelines and use the provided PR template.

## License

AGPL-3.0 — see [LICENSE](LICENSE) for details.
