"""
Upload Tamil Wikipedia Chunked dataset to Hugging Face Hub
with proper licensing and metadata.
"""

import os
from pathlib import Path
import pandas as pd
from datasets import Dataset, DatasetDict, load_dataset
from huggingface_hub import HfApi, login, create_repo
import json


# ==================== CONFIGURATION ====================

# Your Hugging Face credentials
HF_USERNAME = "wickkiey"  # Replace with your HF username
DATASET_NAME = "tamil-wikipedia-chunked"
REPO_ID = f"{HF_USERNAME}/{DATASET_NAME}"

# Dataset info
DATASET_LICENSE = "cc-by-sa-4.0"
DATASET_LANGUAGE = "ta"
DATASET_DESCRIPTION = "Tamil Wikipedia articles chunked with header metadata for LLM training"

# Paths
DATA_FILE = "../data/tawiki_chunked.parquet"  # Path to your chunked parquet file
README_FILE = "README.md"  # This directory

# Upload settings
PRIVATE = False  # Set to True if you want a private dataset

# ========================================================


def load_and_validate_dataset(data_path: str):
    """Load the parquet file and validate structure."""
    print(f"📁 Loading dataset from: {data_path}")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    # Load parquet
    df = pd.read_parquet(data_path)
    
    # Validate structure
    if 'text' not in df.columns:
        raise ValueError("Dataset must have a 'text' column")
    
    print(f"✅ Dataset loaded successfully!")
    print(f"   - Rows (chunks): {len(df):,}")
    print(f"   - Columns: {df.columns.tolist()}")
    print(f"   - Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Check if metadata column exists
    if 'metadata' in df.columns:
        print(f"   - Contains metadata: Yes")
        # Count how many chunks have metadata
        has_metadata = df['metadata'].apply(lambda x: len(x) > 0 if isinstance(x, dict) else False).sum()
        print(f"   - Chunks with header metadata: {has_metadata:,} ({has_metadata/len(df)*100:.1f}%)")
    
    return df


def compute_statistics(df: pd.DataFrame):
    """Compute and display dataset statistics."""
    print("\n📊 Computing dataset statistics...")
    
    stats = {
        "num_chunks": int(len(df)),
        "total_characters": int(df['text'].str.len().sum()),
        "avg_chunk_length": float(df['text'].str.len().mean()),
        "median_chunk_length": float(df['text'].str.len().median()),
        "min_chunk_length": int(df['text'].str.len().min()),
        "max_chunk_length": int(df['text'].str.len().max()),
        "total_words_approx": int(df['text'].str.split().str.len().sum()),
        "avg_words_per_chunk": float(df['text'].str.split().str.len().mean()),
    }
    
    # Metadata statistics
    if 'metadata' in df.columns:
        chunks_with_metadata = df['metadata'].apply(lambda x: len(x) > 0 if isinstance(x, dict) else False).sum()
        stats['chunks_with_metadata'] = int(chunks_with_metadata)
        stats['chunks_with_metadata_percent'] = float(chunks_with_metadata / len(df) * 100)
    
    print("\n📈 Dataset Statistics:")
    print(f"   - Total chunks: {stats['num_chunks']:,}")
    print(f"   - Total characters: {stats['total_characters']:,}")
    print(f"   - Avg chunk length: {stats['avg_chunk_length']:.0f} chars")
    print(f"   - Median chunk length: {stats['median_chunk_length']:.0f} chars")
    print(f"   - Min/Max length: {stats['min_chunk_length']} / {stats['max_chunk_length']:,} chars")
    print(f"   - Approx. total words: {stats['total_words_approx']:,}")
    print(f"   - Avg words per chunk: {stats['avg_words_per_chunk']:.1f}")
    
    if 'chunks_with_metadata' in stats:
        print(f"   - Chunks with metadata: {stats['chunks_with_metadata']:,} ({stats['chunks_with_metadata_percent']:.1f}%)")
    
    # Save statistics
    stats_file = "dataset_statistics.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Statistics saved to: {stats_file}")
    
    return stats


def create_huggingface_dataset(df: pd.DataFrame):
    """Convert pandas DataFrame to Hugging Face Dataset."""
    print("\n🔄 Converting to Hugging Face Dataset format...")
    
    # Create dataset
    dataset = Dataset.from_pandas(df, preserve_index=False)
    
    # You can create splits if needed (e.g., train/test)
    # For now, we'll just use a single train split
    dataset_dict = DatasetDict({
        "train": dataset
    })
    
    print(f"✅ Dataset created with {len(dataset):,} examples")
    
    return dataset_dict


def upload_to_hub(dataset_dict: DatasetDict, repo_id: str, private: bool):
    """Upload dataset to Hugging Face Hub."""
    print(f"\n🚀 Uploading dataset to Hugging Face Hub...")
    print(f"   Repository: {repo_id}")
    print(f"   Private: {private}")
    
    try:
        # Login (will use cached token or prompt for login)
        print("\n🔐 Logging in to Hugging Face...")
        login()
        
        # Create repository
        print(f"\n📦 Creating repository: {repo_id}")
        api = HfApi()
        try:
            repo_url = create_repo(
                repo_id=repo_id,
                repo_type="dataset",
                private=private,
                exist_ok=True
            )
            print(f"✅ Repository created: {repo_url}")
        except Exception as e:
            print(f"ℹ️  Repository might already exist: {e}")
        
        # Push dataset
        print(f"\n⬆️  Pushing dataset to hub...")
        dataset_dict.push_to_hub(
            repo_id=repo_id,
            private=private,
            commit_message="Upload Tamil Wikipedia Chunked dataset with header metadata"
        )
        
        # Upload README
        if os.path.exists(README_FILE):
            print(f"\n📄 Uploading README.md...")
            api.upload_file(
                path_or_fileobj=README_FILE,
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type="dataset",
                commit_message="Add dataset card with licensing info"
            )
        
        # Upload statistics
        if os.path.exists("dataset_statistics.json"):
            print(f"\n📊 Uploading statistics...")
            api.upload_file(
                path_or_fileobj="dataset_statistics.json",
                path_in_repo="dataset_statistics.json",
                repo_id=repo_id,
                repo_type="dataset",
                commit_message="Add dataset statistics"
            )
        
        print(f"\n✅ Dataset uploaded successfully!")
        print(f"🌐 View your dataset at: https://huggingface.co/datasets/{repo_id}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error uploading dataset: {e}")
        return False


def main():
    """Main execution function."""
    global HF_USERNAME, REPO_ID
    
    print("=" * 60)
    print("  Tamil Wikipedia Chunked → Hugging Face Upload")
    print("=" * 60)
    
    # Validate configuration
    if HF_USERNAME == "your-username":
        print("\n⚠️  Warning: Please update HF_USERNAME in the configuration section!")
        print("   Edit this file and set your Hugging Face username.")
        response = input("\nDo you want to enter it now? (y/n): ")
        if response.lower() == 'y':
            HF_USERNAME = input("Enter your HF username: ").strip()
            REPO_ID = f"{HF_USERNAME}/{DATASET_NAME}"
        else:
            print("\n❌ Aborted. Please update the configuration and run again.")
            return
    
    # Step 1: Load dataset
    df = load_and_validate_dataset(DATA_FILE)
    
    # Step 2: Compute statistics
    stats = compute_statistics(df)
    
    # Step 3: Create HF dataset
    dataset_dict = create_huggingface_dataset(df)
    
    # Step 4: Confirm upload
    print("\n" + "=" * 60)
    print(f"📦 Ready to upload:")
    print(f"   - Repository: {REPO_ID}")
    print(f"   - Chunks: {stats['num_chunks']:,}")
    print(f"   - License: {DATASET_LICENSE}")
    print(f"   - Private: {PRIVATE}")
    print("=" * 60)
    
    response = input("\n🤔 Proceed with upload? (y/n): ")
    
    if response.lower() == 'y':
        # Step 5: Upload
        success = upload_to_hub(dataset_dict, REPO_ID, PRIVATE)
        
        if success:
            print("\n" + "=" * 60)
            print("✨ All done! Your dataset is now available on Hugging Face.")
            print("\n📝 Next steps:")
            print(f"   1. Visit: https://huggingface.co/datasets/{REPO_ID}")
            print("   2. Update README.md with your name and details")
            print("   3. Add example usage code")
            print("   4. Share with the Tamil NLP community!")
            print("=" * 60)
    else:
        print("\n❌ Upload cancelled.")


if __name__ == "__main__":
    main()
