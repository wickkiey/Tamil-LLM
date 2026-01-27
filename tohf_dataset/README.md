---
language:
- ta
license: cc-by-sa-4.0
task_categories:
- text-generation
- fill-mask
- language-modeling
pretty_name: Tamil Wikipedia Articles in Markdown
size_categories:
- 10K<n<100K
tags:
- wikipedia
- tamil
- pretraining
- continual-pretraining
---

# Tamil Wikipedia Dataset (Markdown Format)

## Dataset Description

This dataset contains Tamil Wikipedia articles converted to Markdown format, specifically prepared for pre-training and continual pre-training of Large Language Models (LLMs) on Tamil language content.

### Dataset Summary

- **Language**: Tamil (ta)
- **Format**: Single-column parquet file with `text` field
- **Content**: Wikipedia articles with titles as H1 headings followed by article content
- **Preprocessing**: MediaWiki wikitext converted to clean Markdown
- **Use Cases**: Language model pre-training, continual pre-training, Tamil NLP research

### Supported Tasks

- **Language Modeling**: Pre-training or continual pre-training of autoregressive language models
- **Masked Language Modeling**: Training models like BERT, RoBERTa for Tamil
- **Text Generation**: Training generative models on high-quality Tamil text
- **Transfer Learning**: Fine-tuning base models with Tamil knowledge

## Source Data

### Data Source

- **Original Source**: Tamil Wikipedia (ta.wikipedia.org)
- **Wikipedia Dump**: Wikimedia Foundation official dumps
- **Download URL**: https://dumps.wikimedia.org/tawiki/
- **Download Date**: January 2026 (tawiki-latest-pages-articles.xml)
- **Original Format**: MediaWiki XML dump

### Data Collection

The data was collected using the following process:
1. Downloaded official Tamil Wikipedia XML dump from Wikimedia
2. Extracted wikitext using WikiExtractor or similar tools
3. Converted MediaWiki wikitext to Markdown format
4. Structured as single-column dataset with `text` field
5. Saved as Parquet format for efficient loading

### Preprocessing

The preprocessing pipeline includes:
- Removal of MediaWiki templates, references, and metadata
- Conversion of wikitext formatting to Markdown syntax
- Extraction of article titles as H1 headings (#)
- Preservation of section structure, lists, and basic formatting
- Removal of images, categories, and infoboxes
- Unicode normalization for Tamil text

## Dataset Structure

### Data Instances

Each instance represents one Wikipedia article:

```json
{
  "text": "# கணினி\n\nகணினி என்பது ஒரு மின்னணு சாதனம்..."
}
```

### Data Fields

- `text` (string): Complete article content in Markdown format
  - Starts with article title as H1 heading (# Title)
  - Contains article content with preserved formatting
  - Includes sections, lists, and paragraphs

### Data Splits

This dataset contains a single split with all Tamil Wikipedia articles.

| Split | Number of Articles |
|-------|-------------------|
| train | TBD (run statistics script) |

## Dataset Creation

### Curation Rationale

Tamil Wikipedia contains high-quality, crowd-sourced encyclopedic content in Tamil. Converting this to Markdown format makes it suitable for:
- Training language models with structured text
- Preserving document structure for better learning
- Easier integration with modern LLM training pipelines
- Maintaining compatibility with instruction-tuning formats

### Source Data Contributors

Tamil Wikipedia is collaboratively created by thousands of volunteer contributors from the Tamil-speaking community worldwide. The content represents diverse topics with Tamil language and cultural context.

## License and Attribution

### License

This dataset is released under **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

This license maintains compatibility with Wikipedia's original CC BY-SA 3.0 license while using the more recent version.

**License URL**: https://creativecommons.org/licenses/by-sa/4.0/

### Original Source License

Tamil Wikipedia content is licensed under:
- **CC BY-SA 3.0**: https://creativecommons.org/licenses/by-sa/3.0/
- **GFDL**: GNU Free Documentation License

### Attribution Requirements

When using this dataset, you must:

1. **Attribute the Source**: 
   - "This dataset is derived from Tamil Wikipedia (https://ta.wikipedia.org/)"
   - "Content created by Wikipedia contributors"

2. **ShareAlike**: 
   - Any derivatives must be released under CC BY-SA or compatible license

3. **Indicate Changes**: 
   - "Original MediaWiki format converted to Markdown"
   - "Structured as single-column dataset for LLM training"

### Copyright Notice

```
Copyright © Tamil Wikipedia Contributors
Licensed under CC BY-SA 3.0/4.0

This dataset is a derivative work of Tamil Wikipedia.
Original content: https://ta.wikipedia.org/
Wikimedia dumps: https://dumps.wikimedia.org/tawiki/
```

## Considerations for Using the Data

### Social Impact

This dataset provides high-quality Tamil language data for training AI models, which can:
- Improve Tamil language technology and NLP tools
- Support Tamil-speaking communities with better AI services
- Preserve and promote Tamil language in the digital age
- Enable research on low-resource language modeling

### Biases and Limitations

- **Coverage Bias**: Wikipedia articles may not represent all topics equally
- **Contributor Bias**: Reflects perspectives of volunteer contributors
- **Temporal Bias**: Snapshot from January 2026, may not include recent events
- **Domain Bias**: Encyclopedic style may not represent conversational Tamil
- **Quality Variation**: Article quality varies based on contributor activity

### Recommendations

- Combine with other Tamil corpora for diverse language coverage
- Be aware of encyclopedic writing style when training conversational models
- Consider temporal limitations for time-sensitive applications
- Validate model outputs for cultural appropriateness

## Additional Information

### Dataset Curators

Created by [Your Name/Organization] as part of the Tamil-LLM project.

### Citation

If you use this dataset in your research, please cite:

```bibtex
@misc{tamil_wikipedia_markdown_2026,
  title={Tamil Wikipedia Dataset in Markdown Format},
  author={[Your Name]},
  year={2026},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/datasets/[your-username]/tamil-wikipedia-markdown}},
  note={Derived from Tamil Wikipedia, licensed under CC BY-SA 4.0}
}
```

**Original Wikipedia Citation**:
```bibtex
@misc{tamil_wikipedia,
  title={Tamil Wikipedia},
  author={{Wikipedia Contributors}},
  year={2026},
  url={https://ta.wikipedia.org/},
  note={Accessed: January 2026}
}
```

### Contact

For questions or issues with this dataset:
- Dataset Repository: [GitHub URL if applicable]
- Hugging Face Discussion: [Link to discussions]
- Email: [Your contact email]

### Changelog

- **v1.0 (January 2026)**: Initial release
  - Converted Tamil Wikipedia dump to Markdown
  - Single-column parquet format
  - Approximately [X] articles included

### Acknowledgments

- **Wikimedia Foundation**: For maintaining Wikipedia and providing open data dumps
- **Tamil Wikipedia Contributors**: For creating the original content
- **Open Source Community**: For tools used in preprocessing (WikiExtractor, etc.)

---

*This dataset is provided for research and educational purposes. Please ensure compliance with the CC BY-SA 4.0 license terms when using or redistributing this data.*
