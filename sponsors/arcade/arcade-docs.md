# Arcade Python Client

## Installation

```bash
pip install git+https://github.com/ArcadeAI/arcade-py.git
```

## Quickstart

```python
import os
from arcadepy import Arcade

# Load environment variables (if using python-dotenv)
# from dotenv import load_dotenv
# load_dotenv()

# Initialize the Arcade client
client = Arcade(api_key=os.getenv("ARCADE_API_KEY"))

# Send a test chat completion
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello from Arcade test!"}]
)
print(response)
```
