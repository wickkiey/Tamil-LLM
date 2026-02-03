# Upload Guide for Tamil Wikipedia Chunked Dataset

This guide will walk you through uploading the chunked Tamil Wikipedia dataset to Hugging Face.

## Prerequisites

1. **Hugging Face Account**: Sign up at https://huggingface.co/join
2. **Python Environment**: Python 3.8+ with required packages
3. **Dataset File**: Ensure `../data/tawiki_chunked.parquet` exists

## Installation

Install required packages:

```bash
pip install datasets huggingface_hub pandas
```

## Step-by-Step Upload Process

### Step 1: Generate Statistics

First, generate dataset statistics that will be included in the README:

```bash
cd tohf_chunkeddataset
python generate_statistics.py
```

This will create:
- `dataset_statistics.json` - Machine-readable statistics
- `dataset_statistics.txt` - Human-readable statistics

Review these files and update the README.md with the actual numbers.

### Step 2: Configure Upload Script

Edit `upload_to_hf.py` and set your Hugging Face username:

```python
HF_USERNAME = "your-username"  # Replace with your actual HF username
```

Other configuration options:
- `DATASET_NAME`: Name of your dataset (default: "tamil-wikipedia-chunked")
- `PRIVATE`: Set to `True` for private dataset, `False` for public

### Step 3: Update README

Update the README.md file with:
1. Your actual statistics from `dataset_statistics.txt`
2. Your name/organization in the "Dataset Curators" section
3. Your contact information
4. Any additional usage examples or notes

### Step 4: Login to Hugging Face

Login to Hugging Face (one-time setup):

```bash
huggingface-cli login
```

Or the script will prompt you to login when you run it.

### Step 5: Run Upload Script

Execute the upload script:

```bash
python upload_to_hf.py
```

The script will:
1. Load and validate your dataset
2. Compute statistics
3. Show you a summary
4. Ask for confirmation before uploading
5. Upload the dataset, README, and statistics to Hugging Face

### Step 6: Verify Upload

After successful upload:
1. Visit: `https://huggingface.co/datasets/your-username/tamil-wikipedia-chunked`
2. Verify the dataset loads correctly
3. Check that README renders properly
4. Test loading the dataset with the provided code examples

## Testing Before Upload

### Test Loading Locally

```python
import pandas as pd

# Load the parquet file
df = pd.read_parquet("../data/tawiki_chunked.parquet")

# Check structure
print(f"Total chunks: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nSample chunk:")
print(df.iloc[0])
```

### Test Dataset Creation

```python
from datasets import Dataset

# Load your data
df = pd.read_parquet("../data/tawiki_chunked.parquet")

# Create HF dataset
dataset = Dataset.from_pandas(df, preserve_index=False)

# Test
print(dataset)
print(dataset[0])
```

## Troubleshooting

### Issue: "File not found"
**Solution**: Ensure you've generated the chunked dataset first by running the preprocessing notebooks.

### Issue: "Authentication failed"
**Solution**: 
1. Run `huggingface-cli login`
2. Get your token from https://huggingface.co/settings/tokens
3. Paste when prompted

### Issue: "Dataset too large"
**Solution**: 
- Check your HF account limits
- Consider splitting into train/test splits
- Use `private=True` initially for testing

### Issue: "Metadata not displaying correctly"
**Solution**: 
- Verify metadata column is a dictionary type
- Check JSON encoding in the parquet file
- Test with a small sample first

## Post-Upload Checklist

After uploading, complete these tasks:

- [ ] Verify dataset loads correctly on HF
- [ ] Update README with accurate statistics
- [ ] Add usage examples specific to your use case
- [ ] Create a dataset card with proper tags
- [ ] Test the dataset with example code
- [ ] Share on Tamil NLP communities
- [ ] Link from your base markdown dataset
- [ ] Document chunking parameters used
- [ ] Add citation information

## Updating the Dataset

To update an existing dataset:

```bash
# Make your changes to the data file
# Re-run statistics
python generate_statistics.py

# Re-run upload (it will update existing repo)
python upload_to_hf.py
```

## Best Practices

1. **Test First**: Use `private=True` for initial upload and testing
2. **Validate Data**: Check a sample of chunks before uploading
3. **Document Changes**: Keep a changelog in README
4. **Version Control**: Tag versions if you make updates
5. **Community**: Engage with users in discussions

## Example: Loading After Upload

```python
from datasets import load_dataset

# Load your uploaded dataset
dataset = load_dataset("your-username/tamil-wikipedia-chunked")

# Use it
for chunk in dataset['train']:
    text = chunk['text']
    metadata = chunk['metadata']
    # Process...
```

## Support

If you encounter issues:
1. Check Hugging Face documentation: https://huggingface.co/docs/datasets
2. Review error messages carefully
3. Test with a small sample first
4. Ask in Hugging Face forums: https://discuss.huggingface.co/

## License Note

Remember that this dataset inherits the CC BY-SA 4.0 license from Wikipedia. Ensure:
- License is properly specified in dataset card
- Attribution is included
- Users are aware of ShareAlike requirements

---

Good luck with your upload! 🚀
