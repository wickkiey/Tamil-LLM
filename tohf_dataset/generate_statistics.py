"""
Generate comprehensive statistics about the Tamil Wikipedia dataset.
Run this before uploading to get accurate numbers for README.md
"""

import pandas as pd
import json
from pathlib import Path
from collections import Counter
import re


# Configuration
DATA_FILE = "../data/tawiki_markdown.parquet"
OUTPUT_FILE = "dataset_statistics.json"
OUTPUT_READABLE = "dataset_statistics.txt"


def analyze_dataset(parquet_path: str):
    """Comprehensive dataset analysis."""
    print("=" * 70)
    print("  Tamil Wikipedia Dataset Statistics")
    print("=" * 70)
    
    # Load data
    print(f"\n📁 Loading: {parquet_path}")
    df = pd.read_parquet(parquet_path)
    print(f"✅ Loaded {len(df):,} articles\n")
    
    # Basic statistics
    print("📊 BASIC STATISTICS")
    print("-" * 70)
    
    stats = {}
    
    # Article counts
    stats['num_articles'] = len(df)
    print(f"Total Articles: {stats['num_articles']:,}")
    
    # Character statistics
    char_lengths = df['text'].str.len()
    stats['total_characters'] = int(char_lengths.sum())
    stats['avg_characters'] = float(char_lengths.mean())
    stats['median_characters'] = float(char_lengths.median())
    stats['min_characters'] = int(char_lengths.min())
    stats['max_characters'] = int(char_lengths.max())
    stats['std_characters'] = float(char_lengths.std())
    
    print(f"Total Characters: {stats['total_characters']:,}")
    print(f"Average per Article: {stats['avg_characters']:,.0f} chars")
    print(f"Median per Article: {stats['median_characters']:,.0f} chars")
    print(f"Min/Max Length: {stats['min_characters']:,} / {stats['max_characters']:,} chars")
    print(f"Std Deviation: {stats['std_characters']:,.0f}")
    
    # Word statistics (approximate)
    print(f"\n📝 WORD STATISTICS (Approximate)")
    print("-" * 70)
    
    word_counts = df['text'].str.split().str.len()
    stats['total_words'] = int(word_counts.sum())
    stats['avg_words_per_article'] = float(word_counts.mean())
    stats['median_words'] = float(word_counts.median())
    
    print(f"Total Words: {stats['total_words']:,}")
    print(f"Average per Article: {stats['avg_words_per_article']:,.0f} words")
    print(f"Median per Article: {stats['median_words']:,.0f} words")
    
    # Line statistics
    print(f"\n📄 LINE STATISTICS")
    print("-" * 70)
    
    line_counts = df['text'].str.count('\n') + 1
    stats['avg_lines_per_article'] = float(line_counts.mean())
    stats['median_lines'] = float(line_counts.median())
    
    print(f"Average Lines per Article: {stats['avg_lines_per_article']:,.1f}")
    print(f"Median Lines per Article: {stats['median_lines']:,.0f}")
    
    # Size statistics
    print(f"\n💾 SIZE STATISTICS")
    print("-" * 70)
    
    # Estimate size (UTF-8 encoding)
    total_bytes = df['text'].str.encode('utf-8').str.len().sum()
    stats['total_size_bytes'] = int(total_bytes)
    stats['total_size_mb'] = float(total_bytes / (1024 * 1024))
    stats['total_size_gb'] = float(total_bytes / (1024 * 1024 * 1024))
    
    print(f"Total Size: {stats['total_size_mb']:,.2f} MB ({stats['total_size_gb']:.3f} GB)")
    print(f"Average Article Size: {stats['total_size_bytes'] / len(df):,.0f} bytes")
    
    # Distribution analysis
    print(f"\n📈 LENGTH DISTRIBUTION")
    print("-" * 70)
    
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    stats['length_percentiles'] = {}
    
    for p in percentiles:
        val = char_lengths.quantile(p / 100)
        stats['length_percentiles'][f'p{p}'] = float(val)
        print(f"  {p}th percentile: {val:,.0f} characters")
    
    # Article size categories
    print(f"\n📦 ARTICLE SIZE CATEGORIES")
    print("-" * 70)
    
    categories = {
        'tiny': (0, 500),
        'small': (500, 2000),
        'medium': (2000, 10000),
        'large': (10000, 50000),
        'very_large': (50000, float('inf'))
    }
    
    stats['size_distribution'] = {}
    for name, (min_len, max_len) in categories.items():
        count = ((char_lengths >= min_len) & (char_lengths < max_len)).sum()
        percentage = (count / len(df)) * 100
        stats['size_distribution'][name] = {
            'count': int(count),
            'percentage': float(percentage)
        }
        print(f"  {name.replace('_', ' ').title():12} ({min_len:6,} - {max_len:8}): "
              f"{count:6,} ({percentage:5.2f}%)")
    
    # Content analysis
    print(f"\n🔍 CONTENT ANALYSIS")
    print("-" * 70)
    
    # Count articles with sections
    has_sections = df['text'].str.contains(r'\n##', regex=True)
    num_with_sections = has_sections.sum()
    stats['articles_with_sections'] = int(num_with_sections)
    stats['articles_with_sections_pct'] = float((num_with_sections / len(df)) * 100)
    
    print(f"Articles with Sections: {num_with_sections:,} ({stats['articles_with_sections_pct']:.1f}%)")
    
    # Count articles with lists
    has_lists = df['text'].str.contains(r'\n[-*]', regex=True)
    num_with_lists = has_lists.sum()
    stats['articles_with_lists'] = int(num_with_lists)
    stats['articles_with_lists_pct'] = float((num_with_lists / len(df)) * 100)
    
    print(f"Articles with Lists: {num_with_lists:,} ({stats['articles_with_lists_pct']:.1f}%)")
    
    # Count articles with tables
    has_tables = df['text'].str.contains(r'\|.*\|', regex=True)
    num_with_tables = has_tables.sum()
    stats['articles_with_tables'] = int(num_with_tables)
    stats['articles_with_tables_pct'] = float((num_with_tables / len(df)) * 100)
    
    print(f"Articles with Tables: {num_with_tables:,} ({stats['articles_with_tables_pct']:.1f}%)")
    
    # Sample titles
    print(f"\n📋 SAMPLE ARTICLE TITLES")
    print("-" * 70)
    
    # Extract titles (first line after #)
    titles = df['text'].str.extract(r'^#\s*(.+)', flags=re.MULTILINE)[0]
    sample_titles = titles.dropna().head(10).tolist()
    stats['sample_titles'] = sample_titles
    
    for i, title in enumerate(sample_titles, 1):
        print(f"  {i:2}. {title}")
    
    # Longest and shortest articles
    print(f"\n🏆 EXTREMES")
    print("-" * 70)
    
    longest_idx = char_lengths.idxmax()
    shortest_idx = char_lengths.idxmin()
    
    longest_title = titles.iloc[longest_idx] if longest_idx in titles.index else "Unknown"
    shortest_title = titles.iloc[shortest_idx] if shortest_idx in titles.index else "Unknown"
    
    stats['longest_article'] = {
        'title': str(longest_title),
        'length': int(char_lengths.iloc[longest_idx])
    }
    stats['shortest_article'] = {
        'title': str(shortest_title),
        'length': int(char_lengths.iloc[shortest_idx])
    }
    
    print(f"Longest Article: {longest_title}")
    print(f"  Length: {stats['longest_article']['length']:,} characters")
    print(f"\nShortest Article: {shortest_title}")
    print(f"  Length: {stats['shortest_article']['length']:,} characters")
    
    # Dataset metadata
    stats['metadata'] = {
        'source': 'Tamil Wikipedia',
        'language': 'Tamil (ta)',
        'format': 'Markdown',
        'license': 'CC BY-SA 4.0',
        'created': '2026-01',
        'columns': list(df.columns)
    }
    
    return stats, df


def save_statistics(stats: dict, output_json: str, output_txt: str):
    """Save statistics to files."""
    print(f"\n💾 SAVING RESULTS")
    print("-" * 70)
    
    # Save JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON saved: {output_json}")
    
    # Save human-readable text
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("TAMIL WIKIPEDIA DATASET STATISTICS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Total Articles: {stats['num_articles']:,}\n")
        f.write(f"Total Characters: {stats['total_characters']:,}\n")
        f.write(f"Total Words (approx): {stats['total_words']:,}\n")
        f.write(f"Total Size: {stats['total_size_mb']:.2f} MB\n\n")
        
        f.write("AVERAGES\n")
        f.write(f"  Characters per article: {stats['avg_characters']:,.0f}\n")
        f.write(f"  Words per article: {stats['avg_words_per_article']:,.0f}\n")
        f.write(f"  Lines per article: {stats['avg_lines_per_article']:,.1f}\n\n")
        
        f.write("SIZE DISTRIBUTION\n")
        for cat, data in stats['size_distribution'].items():
            f.write(f"  {cat:15}: {data['count']:6,} ({data['percentage']:5.2f}%)\n")
    
    print(f"✅ Text saved: {output_txt}")


def main():
    """Main execution."""
    if not Path(DATA_FILE).exists():
        print(f"❌ Error: Data file not found: {DATA_FILE}")
        print(f"   Make sure you've generated the parquet file first.")
        return
    
    # Analyze
    stats, df = analyze_dataset(DATA_FILE)
    
    # Save
    save_statistics(stats, OUTPUT_FILE, OUTPUT_READABLE)
    
    print("\n" + "=" * 70)
    print("✨ Analysis complete!")
    print(f"\n📊 Use these statistics to update your README.md:")
    print(f"   - Total articles: {stats['num_articles']:,}")
    print(f"   - Total size: {stats['total_size_mb']:.1f} MB")
    print(f"   - Avg article: {stats['avg_words_per_article']:.0f} words")
    print("=" * 70)


if __name__ == "__main__":
    main()
