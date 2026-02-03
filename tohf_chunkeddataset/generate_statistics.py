"""
Generate comprehensive statistics about the Tamil Wikipedia Chunked dataset.
Run this before uploading to get accurate numbers for README.md
"""

import pandas as pd
import json
from pathlib import Path
from collections import Counter
import re


# Configuration
DATA_FILE = "../data/tawiki_chunked.parquet"
OUTPUT_FILE = "dataset_statistics.json"
OUTPUT_READABLE = "dataset_statistics.txt"


def analyze_dataset(parquet_path: str):
    """Comprehensive dataset analysis."""
    print("=" * 70)
    print("  Tamil Wikipedia Chunked Dataset Statistics")
    print("=" * 70)
    
    # Load data
    print(f"\n📁 Loading: {parquet_path}")
    df = pd.read_parquet(parquet_path)
    print(f"✅ Loaded {len(df):,} chunks\n")
    
    # Basic statistics
    print("📊 BASIC STATISTICS")
    print("-" * 70)
    
    stats = {}
    
    # Chunk counts
    stats['num_chunks'] = len(df)
    print(f"Total Chunks: {stats['num_chunks']:,}")
    
    # Character statistics
    char_lengths = df['text'].str.len()
    stats['total_characters'] = int(char_lengths.sum())
    stats['avg_characters'] = float(char_lengths.mean())
    stats['median_characters'] = float(char_lengths.median())
    stats['min_characters'] = int(char_lengths.min())
    stats['max_characters'] = int(char_lengths.max())
    stats['std_characters'] = float(char_lengths.std())
    
    print(f"Total Characters: {stats['total_characters']:,}")
    print(f"Average per Chunk: {stats['avg_characters']:,.0f} chars")
    print(f"Median per Chunk: {stats['median_characters']:,.0f} chars")
    print(f"Min/Max Length: {stats['min_characters']:,} / {stats['max_characters']:,} chars")
    print(f"Std Deviation: {stats['std_characters']:,.0f}")
    
    # Word statistics (approximate)
    print(f"\n📝 WORD STATISTICS (Approximate)")
    print("-" * 70)
    
    word_counts = df['text'].str.split().str.len()
    stats['total_words'] = int(word_counts.sum())
    stats['avg_words_per_chunk'] = float(word_counts.mean())
    stats['median_words'] = float(word_counts.median())
    stats['min_words'] = int(word_counts.min())
    stats['max_words'] = int(word_counts.max())
    
    print(f"Total Words: {stats['total_words']:,}")
    print(f"Average per Chunk: {stats['avg_words_per_chunk']:,.1f} words")
    print(f"Median per Chunk: {stats['median_words']:,.0f} words")
    print(f"Min/Max Words: {stats['min_words']:,} / {stats['max_words']:,} words")
    
    # Line statistics
    print(f"\n📄 LINE STATISTICS")
    print("-" * 70)
    
    line_counts = df['text'].str.count('\n') + 1
    stats['avg_lines_per_chunk'] = float(line_counts.mean())
    stats['median_lines'] = float(line_counts.median())
    
    print(f"Average Lines per Chunk: {stats['avg_lines_per_chunk']:,.1f}")
    print(f"Median Lines per Chunk: {stats['median_lines']:,.0f}")
    
    # Metadata statistics
    if 'metadata' in df.columns:
        print(f"\n🏷️  METADATA STATISTICS")
        print("-" * 70)
        
        # Count chunks with metadata
        has_metadata = df['metadata'].apply(lambda x: len(x) > 0 if isinstance(x, dict) else False)
        stats['chunks_with_metadata'] = int(has_metadata.sum())
        stats['chunks_with_metadata_percent'] = float(has_metadata.sum() / len(df) * 100)
        
        print(f"Chunks with Metadata: {stats['chunks_with_metadata']:,} ({stats['chunks_with_metadata_percent']:.1f}%)")
        print(f"Chunks without Metadata: {len(df) - stats['chunks_with_metadata']:,}")
        
        # Analyze header levels
        header_levels = {f'Header {i}': 0 for i in range(1, 5)}
        
        for meta in df[has_metadata]['metadata']:
            if isinstance(meta, dict):
                for key in meta.keys():
                    if key in header_levels:
                        header_levels[key] += 1
        
        print(f"\nHeader Level Distribution:")
        for level, count in header_levels.items():
            if count > 0:
                print(f"  {level}: {count:,} chunks ({count/len(df)*100:.1f}%)")
        
        stats['header_distribution'] = header_levels
    
    # Size statistics
    print(f"\n💾 SIZE STATISTICS")
    print("-" * 70)
    
    # Estimate size (UTF-8 encoding)
    total_bytes = df['text'].str.encode('utf-8').str.len().sum()
    stats['total_size_bytes'] = int(total_bytes)
    stats['total_size_mb'] = float(total_bytes / (1024 * 1024))
    stats['total_size_gb'] = float(total_bytes / (1024 * 1024 * 1024))
    
    print(f"Total Size: {stats['total_size_mb']:,.2f} MB ({stats['total_size_gb']:.3f} GB)")
    print(f"Average Chunk Size: {stats['total_size_bytes'] / len(df):,.0f} bytes")
    
    # Distribution analysis
    print(f"\n📈 LENGTH DISTRIBUTION")
    print("-" * 70)
    
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    stats['length_percentiles'] = {}
    
    for p in percentiles:
        val = char_lengths.quantile(p / 100)
        stats['length_percentiles'][f'p{p}'] = int(val)
        print(f"  {p}th percentile: {val:,.0f} chars")
    
    # Markdown header analysis
    print(f"\n# MARKDOWN HEADER ANALYSIS")
    print("-" * 70)
    
    header_counts = {f'H{i}': 0 for i in range(1, 5)}
    for text in df['text']:
        for i in range(1, 5):
            pattern = f"^{'#' * i} "
            if re.search(pattern, text, re.MULTILINE):
                header_counts[f'H{i}'] += 1
    
    stats['markdown_headers'] = header_counts
    print(f"Chunks starting with headers:")
    for level, count in header_counts.items():
        print(f"  {level}: {count:,} chunks ({count/len(df)*100:.1f}%)")
    
    # Save statistics
    print(f"\n💾 SAVING STATISTICS")
    print("-" * 70)
    
    # Save JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON: {OUTPUT_FILE}")
    
    # Save readable format
    with open(OUTPUT_READABLE, 'w', encoding='utf-8') as f:
        f.write("Tamil Wikipedia Chunked Dataset Statistics\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Total Chunks: {stats['num_chunks']:,}\n")
        f.write(f"Total Characters: {stats['total_characters']:,}\n")
        f.write(f"Total Words (approx): {stats['total_words']:,}\n")
        f.write(f"Total Size: {stats['total_size_mb']:,.2f} MB\n\n")
        
        f.write("Chunk Statistics:\n")
        f.write(f"  Average Length: {stats['avg_characters']:,.0f} chars\n")
        f.write(f"  Median Length: {stats['median_characters']:,.0f} chars\n")
        f.write(f"  Min/Max: {stats['min_characters']:,} / {stats['max_characters']:,} chars\n\n")
        
        if 'chunks_with_metadata' in stats:
            f.write(f"Chunks with Metadata: {stats['chunks_with_metadata']:,} ({stats['chunks_with_metadata_percent']:.1f}%)\n\n")
        
        f.write("Length Distribution (percentiles):\n")
        for p in percentiles:
            f.write(f"  {p}th: {stats['length_percentiles'][f'p{p}']:,} chars\n")
    
    print(f"✅ Text: {OUTPUT_READABLE}")
    
    print("\n" + "=" * 70)
    print("✨ Analysis complete!")
    print("=" * 70)
    
    return stats


def main():
    """Main execution."""
    if not Path(DATA_FILE).exists():
        print(f"❌ Error: Data file not found: {DATA_FILE}")
        print("   Please ensure you've generated the chunked dataset first.")
        return
    
    try:
        stats = analyze_dataset(DATA_FILE)
        
        print(f"\n📝 Use these statistics to update your README.md:")
        print(f"   - Total Chunks: {stats['num_chunks']:,}")
        print(f"   - Total Size: {stats['total_size_mb']:,.2f} MB")
        print(f"   - Avg Chunk Length: {stats['avg_characters']:,.0f} chars")
        if 'chunks_with_metadata' in stats:
            print(f"   - Chunks with Headers: {stats['chunks_with_metadata_percent']:.1f}%")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
