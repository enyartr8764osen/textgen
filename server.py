#!/usr/bin/env python3
"""
Main entry point for the textgen web UI server.
Fork of oobabooga/text-generation-webui with additional features and improvements.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure the project root is in the Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))


def parse_arguments():
    """Parse command-line arguments for the server."""
    parser = argparse.ArgumentParser(
        description='textgen - A web UI for text generation models',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Server settings
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host address to bind the server to')
    parser.add_argument('--port', type=int, default=7860,
                        help='Port number to run the server on')
    parser.add_argument('--share', action='store_true',
                        help='Create a public Gradio share link')
    parser.add_argument('--listen', action='store_true',
                        help='Listen on all network interfaces (0.0.0.0)')

    # Model settings
    parser.add_argument('--model', type=str, default=None,
                        help='Name of the model to load at startup')
    parser.add_argument('--model-dir', type=str, default='models',
                        help='Directory containing model files')
    parser.add_argument('--lora', type=str, nargs='+', default=None,
                        help='LoRA adapter(s) to apply to the model')

    # Inference settings
    parser.add_argument('--loader', type=str, default=None,
                        choices=['transformers', 'llama.cpp', 'exllama', 'exllamav2', 'ctransformers'],
                        help='Model loader backend to use')
    parser.add_argument('--cpu', action='store_true',
                        help='Force CPU-only inference')
    parser.add_argument('--gpu-memory', type=int, nargs='+', default=None,
                        help='GPU VRAM limit(s) in GiB per device')
    parser.add_argument('--n-gpu-layers', type=int, default=None,
                        help='Number of layers to offload to GPU (llama.cpp)')
    parser.add_argument('--threads', type=int, default=None,
                        help='Number of CPU threads for inference')

    # API settings
    parser.add_argument('--api', action='store_true',
                        help='Enable the REST API server')
    parser.add_argument('--api-port', type=int, default=5000,
                        help='Port for the REST API server')
    parser.add_argument('--api-key', type=str, default=None,
                        help='API key for authentication (optional)')
    parser.add_argument('--openai-api', action='store_true',
                        help='Enable OpenAI-compatible API endpoint')

    # UI settings
    parser.add_argument('--chat', action='store_true',
                        help='Launch in chat mode by default')
    parser.add_argument('--darkmode', action='store_true',
                        help='Enable dark mode for the UI')
    parser.add_argument('--no-stream', action='store_true',
                        help='Disable token streaming in the UI')

    # Debug / misc
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose/debug logging')
    parser.add_argument('--version', action='version', version='textgen 0.1.0')

    return parser.parse_args()


def setup_environment(args):
    """Configure environment variables and paths based on parsed arguments."""
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug('Verbose logging enabled')

    if args.listen:
        args.host = '0.0.0.0'
        logger.info('Listening on all network interfaces')

    # Ensure model directory exists
    model_dir = ROOT_DIR / args.model_dir
    model_dir.mkdir(parents=True, exist_ok=True)
    logger.debug('Model directory: %s', model_dir)

    return args


def main():
    """Main entry point — parse args, set up environment, and launch the UI."""
    args = parse_arguments()
    args = setup_environment(args)

    logger.info('Starting textgen server on %s:%d', args.host, args.port)

    try:
        # Deferred import so argument parsing is fast
        from modules.ui import create_interface  # noqa: F401  (module TBD)
        interface = create_interface(args)
        interface.queue()
        interface.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            inbrowser=False,
        )
    except ImportError as exc:
        logger.error('Failed to import UI module: %s', exc)
        logger.error('Make sure all dependencies are installed: pip install -r requirements.txt')
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info('Server stopped by user')
        sys.exit(0)


if __name__ == '__main__':
    main()
