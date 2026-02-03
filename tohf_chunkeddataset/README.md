---
language:
- ta
license: cc-by-sa-4.0
task_categories:
- text-generation
- fill-mask
- language-modeling
pretty_name: Tamil Wikipedia Chunked Dataset
size_categories:
- 10K<n<100K
tags:
- wikipedia
- tamil
- pretraining
- continual-pretraining
- chunked
- header-metadata
---

# Tamil Wikipedia Chunked Dataset

## Dataset Description

This dataset contains Tamil Wikipedia articles that have been intelligently chunked using header-aware splitting. Each chunk includes both the text content and metadata about the document structure, making it ideal for training Large Language Models with better contextual understanding.

### Dataset Summary

- **Language**: Tamil (ta)
- **Format**: Parquet file with `text` and `metadata` columns
- **Chunking Method**: Header-based splitting with character-level constraints
- **Content**: Wikipedia chunks with preserved hierarchical context
- **Use Cases**: LLM pre-training, continual pre-training, RAG systems, Tamil NLP research

### Key Features

✨ **Header-Aware Chunking**: Chunks are created by respecting document structure (H1-H4 headings)

📊 **Rich Metadata**: Each chunk includes metadata about its position in the document hierarchy

🎯 **Optimal Chunk Size**: Chunks are sized appropriately for LLM training (typically 512 characters)

🔗 **Context Preservation**: Headers are prepended to content, ensuring each chunk is self-contained

### Supported Tasks

- **Language Modeling**: Pre-training or continual pre-training with structured context
- **Retrieval Augmented Generation (RAG)**: Ready-to-use chunks for vector databases
- **Contextual Training**: Learning from structured, hierarchical text
- **Tamil NLP Research**: High-quality chunked Tamil text corpus

## Dataset Structure

### Data Instances

Each instance represents one chunk from a Wikipedia article:

```json
{
  "text": "# கணினி\n\n## வரலாறு\n\nகணினியின் வரலாறு மிகவும் சுவாரசியமானது...",
  "metadata": {
    "Header 1": "கணினி",
    "Header 2": "வரலாறு"
  }
}
```

### Data Fields

- **`text`** (string): Chunk content with prepended headers
  - Contains the hierarchical headers (# H1, ## H2, etc.)
  - Followed by the actual content from that section
  - Self-contained and contextually meaningful

- **`metadata`** (dict): Header hierarchy information
  - `Header 1`: Top-level article title
  - `Header 2`: Section heading (if applicable)
  - `Header 3`: Subsection heading (if applicable)
  - `Header 4`: Sub-subsection heading (if applicable)

### Data Splits

This dataset contains a single split with all chunks.

| Split | Number of Chunks |
|-------|------------------|
| train | [Run generate_statistics.py to get actual count] |

### Chunking Methodology

The dataset was created using a two-stage chunking process:

1. **Header-Based Splitting**: 
   - Documents are first split by markdown headers (H1-H4)
   - Preserves document structure and semantic boundaries
   - Uses LangChain's `MarkdownHeaderTextSplitter`

2. **Character-Level Splitting**:
   - Large sections are further split into ~512 character chunks
   - Maintains 50-character overlap for context continuity
   - Headers are prepended to each chunk before splitting
   - Uses `RecursiveCharacterTextSplitter`

This approach ensures:
- ✅ Chunks respect semantic boundaries
- ✅ Each chunk has full hierarchical context
- ✅ Optimal size for LLM training
- ✅ No loss of structural information

## Source Data

### Data Source

- **Original Source**: Tamil Wikipedia (ta.wikipedia.org)
- **Base Dataset**: [tamil-wikipedia-markdown](https://huggingface.co/datasets/wickkiey/tamil-wikipedia-markdown)
- **Processing**: Header-aware chunking with metadata preservation

### Preprocessing Pipeline

1. MediaWiki XML dump → Wikitext extraction
2. Wikitext → Markdown conversion
3. Markdown → Header-based splitting
4. Large sections → Character-level chunking
5. Headers prepended to each chunk
6. Metadata preserved for each chunk

## Usage

### Loading the Dataset

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("wickkiey/tamil-wikipedia-chunked")

# Access chunks
for chunk in dataset['train']:
    print(f"Text: {chunk['text'][:100]}...")
    print(f"Metadata: {chunk['metadata']}")
```

### Using with LLM Training

```python
from datasets import load_dataset
from transformers import AutoTokenizer

# Load dataset and tokenizer
dataset = load_dataset("wickkiey/tamil-wikipedia-chunked")
tokenizer = AutoTokenizer.from_pretrained("your-model")

# The text field is ready for training
def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
```

### Using for RAG Systems

```python
from datasets import load_dataset
import chromadb

# Load dataset
dataset = load_dataset("wickkiey/tamil-wikipedia-chunked")

# Each chunk is self-contained with headers
for chunk in dataset['train']:
    # Headers are already in the text
    text = chunk['text']
    
    # Metadata provides additional context
    metadata = chunk['metadata']
    
    # Add to your vector database
    # collection.add(documents=[text], metadatas=[metadata])
```

## Dataset Statistics

**[Run `generate_statistics.py` to populate these]**

- Total Chunks: [TBD]
- Total Size: [TBD] MB
- Average Chunk Length: [TBD] characters
- Chunks with Metadata: [TBD]%

## Dataset Creation

### Curation Rationale

Traditional chunking methods often break text at arbitrary points, losing contextual information. This dataset uses header-aware chunking to:

- Preserve document structure and hierarchy
- Ensure each chunk has complete context through prepended headers
- Maintain semantic coherence within chunks
- Enable better training signals for LLMs

### Advantages Over Simple Chunking

- 🎯 **Semantic Coherence**: Chunks follow natural document boundaries
- 📚 **Self-Contained**: Each chunk includes its hierarchical context
- 🏷️ **Rich Metadata**: Programmatic access to document structure
- 🔍 **Better Retrieval**: Headers improve relevance matching in RAG
- 🧠 **Improved Training**: Models learn structured text patterns

## License and Attribution

### License

This dataset is released under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

**License URL**: https://creativecommons.org/licenses/by-sa/4.0/

### Attribution Requirements

When using this dataset, you must:

1. **Attribute the Source**: 
   - "This dataset is derived from Tamil Wikipedia (https://ta.wikipedia.org/)"
   - "Chunked and processed for LLM training"

2. **ShareAlike**: 
   - Any derivatives must be released under CC BY-SA or compatible license

3. **Indicate Changes**: 
   - "Original Wikipedia content chunked using header-aware splitting"
   - "Metadata added for document structure preservation"

### Copyright Notice

```
Copyright © Tamil Wikipedia Contributors
Licensed under CC BY-SA 3.0/4.0

This is a derivative work of Tamil Wikipedia.
Original content: https://ta.wikipedia.org/
Base dataset: tamil-wikipedia-markdown
```

## Considerations for Using the Data

### Social Impact

This dataset enables:
- Better Tamil language models through structured training data
- Improved RAG systems for Tamil content
- Research on structured text understanding
- Development of context-aware Tamil NLP applications

### Biases and Limitations

- **Coverage Bias**: Inherits Wikipedia's topic distribution
- **Chunk Size Variation**: Some chunks may be shorter/longer than target
- **Header Dependency**: Effectiveness depends on article structure
- **Temporal Snapshot**: Based on January 2026 Wikipedia dump

### Recommendations

- Use with other Tamil corpora for comprehensive coverage
- Consider chunk size when fine-tuning context window
- Leverage metadata for enhanced retrieval in RAG systems
- Validate outputs for domain-specific applications

## Additional Information

### Dataset Curators

Created by [Your Name] as part of the Tamil-LLM project.

Chunking methodology based on [LangChain's MarkdownHeaderTextSplitter](https://docs.langchain.com/oss/python/integrations/splitters/markdown_header_metadata_splitter).

### Related Datasets

- [tamil-wikipedia-markdown](https://huggingface.co/datasets/wickkiey/tamil-wikipedia-markdown) - Full articles without chunking

### Citation

If you use this dataset, please cite:

```bibtex
@misc{tamil_wikipedia_chunked_2026,
  title={Tamil Wikipedia Chunked Dataset with Header Metadata},
  author={[Your Name]},
  year={2026},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/datasets/wickkiey/tamil-wikipedia-chunked}},
  note={Header-aware chunked dataset derived from Tamil Wikipedia}
}
```

### Contact

For questions or issues:
- Dataset Repository: [GitHub URL]
- Hugging Face Discussions: Use the discussions tab
- Issues: Report via GitHub or HF discussions

### Changelog

- **v1.0 (February 2026)**: Initial release
  - Header-aware chunking with metadata
  - ~512 character target chunk size
  - Full hierarchical context preservation

### Acknowledgments

- **Wikimedia Foundation**: For Wikipedia data
- **Tamil Wikipedia Contributors**: For original content
- **LangChain**: For text splitting tools
- **Hugging Face**: For dataset hosting

---

*This dataset is provided for research and educational purposes. Ensure compliance with CC BY-SA 4.0 license terms.*
