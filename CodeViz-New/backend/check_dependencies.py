
import sys
import pkg_resources

dependencies = [
    "transformers",
    "torch",
    "sentencepiece",
    "protobuf",
    "accelerate",
    "huggingface-hub",
    "tokenizers"
]

print("Checking dependencies...")
for dep in dependencies:
    try:
        dist = pkg_resources.get_distribution(dep)
        print(f"{dep}: {dist.version}")
    except pkg_resources.DistributionNotFound:
        print(f"{dep}: NOT INSTALLED")
    except Exception as e:
        print(f"{dep}: Error {e}")
