# Tamil Wikipedia → Hugging Face Upload Guide

This folder contains everything you need to upload your Tamil Wikipedia dataset to Hugging Face with proper licensing and documentation.

## 📁 Files

- **README.md** - Complete dataset card with CC BY-SA 4.0 licensing
- **upload_to_hf.py** - Script to upload dataset with metadata
- **generate_statistics.py** - Generate dataset statistics for README

## 🚀 Quick Start

### Step 1: Generate Statistics

First, run the statistics generator to get accurate numbers:

```bash
cd tohf_dataset
python generate_statistics.py
```

This creates:
- `dataset_statistics.json` - Machine-readable stats
- `dataset_statistics.txt` - Human-readable summary

### Step 2: Update README.md

Edit `README.md` and replace placeholders:
- `[Your Name]` → Your actual name
- `[your-username]` → Your Hugging Face username
- `TBD (run statistics script)` → Actual article count from statistics
- Update citation info

### Step 3: Configure Upload Script

Edit `upload_to_hf.py` and set:
```python
HF_USERNAME = "your-hf-username"  # Your actual username
DATASET_NAME = "tamil-wikipedia-markdown"  # Or your preferred name
```

### Step 4: Install Dependencies

```bash
pip install datasets huggingface_hub pandas pyarrow
```

### Step 5: Login to Hugging Face

```bash
huggingface-cli login
```

Or the script will prompt you to login.

### Step 6: Upload

```bash
python upload_to_hf.py
```

The script will:
1. Load and validate your dataset
2. Compute statistics
3. Show a preview
4. Ask for confirmation
5. Upload to Hugging Face
6. Upload README and statistics

## 📋 License Information

### What License to Use?

Your dataset uses **CC BY-SA 4.0** which is compatible with Wikipedia's CC BY-SA 3.0.

### Attribution Requirements

✅ **You MUST include**:
- Source attribution to Tamil Wikipedia
- Link to original Wikipedia
- License information (CC BY-SA)
- Note about modifications (MediaWiki → Markdown)

✅ **Already included in README.md**:
- Complete attribution section
- Copyright notice
- License requirements
- Original source links

### Can I Use This Commercially?

**Yes!** CC BY-SA 4.0 allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

**BUT you must**:
- ✅ Give credit (attribution)
- ✅ Share derivatives under same license
- ✅ State changes made
- ✅ Include license text

## 🔍 What Gets Uploaded

1. **Dataset files** (parquet)
   - Your `tawiki_markdown.parquet` file
   
2. **README.md**
   - Dataset card with all metadata
   - License information
   - Usage examples
   - Attribution

3. **dataset_statistics.json**
   - Detailed statistics
   - Size information
   - Distribution data

## 📊 Metadata Included

The upload script automatically includes:

```yaml
language: ta
license: cc-by-sa-4.0
task_categories:
  - text-generation
  - fill-mask
  - language-modeling
tags:
  - wikipedia
  - tamil
  - pretraining
```

## 🛠️ Troubleshooting

### "Data file not found"
- Check that `../data/tawiki_markdown.parquet` exists
- Update `DATA_FILE` path in scripts if your file is elsewhere

### "Authentication error"
- Run `huggingface-cli login` first
- Or set `HF_TOKEN` environment variable

### "Repository already exists"
- Script will handle this automatically
- Or delete existing repo on HF first

### "Dataset too large"
- Git LFS handles large files automatically
- Consider splitting into multiple files if needed

## 📚 Additional Resources

- [Hugging Face Datasets Documentation](https://huggingface.co/docs/datasets)
- [CC BY-SA 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/)
- [Tamil Wikipedia](https://ta.wikipedia.org/)
- [Wikimedia Dumps](https://dumps.wikimedia.org/tawiki/)

## 💡 Tips

1. **Test Upload First**: Set `PRIVATE = True` to test upload privately first

2. **Update Statistics**: Run `generate_statistics.py` again if you regenerate the dataset

3. **Add Examples**: Consider adding usage examples to README after upload

4. **Tag Properly**: Good tags help discoverability - already included in README

5. **Community**: Share on HF forums and Tamil NLP communities!

## ✅ Checklist

Before uploading, make sure:

- [ ] Statistics generated (`python generate_statistics.py`)
- [ ] README.md updated with your info
- [ ] HF_USERNAME set in upload_to_hf.py
- [ ] Hugging Face login completed
- [ ] Data file path is correct
- [ ] Attribution section reviewed
- [ ] License confirmed (CC BY-SA 4.0)

## 🎉 After Upload

1. Visit your dataset: `https://huggingface.co/datasets/USERNAME/DATASET_NAME`
2. Check that README renders correctly
3. Test loading: `load_dataset("USERNAME/DATASET_NAME")`
4. Share with the community!
5. Consider writing a blog post about your dataset

---

**Need Help?**
- HuggingFace Forums: https://discuss.huggingface.co/
- Dataset Issues: Open issue on your dataset repo
