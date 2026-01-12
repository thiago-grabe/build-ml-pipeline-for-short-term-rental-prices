#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning,
exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logger.info(f"Downloading artifact {args.input_artifact}")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    # Read the data
    logger.info(f"Reading data from {artifact_local_path}")
    df = pd.read_csv(artifact_local_path)

    # Drop outliers based on price
    logger.info(f"Dropping price outliers (keeping prices between ${args.min_price} and ${args.max_price})")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info(f"Dataset size after dropping price outliers: {len(df)} rows")

    # Convert last_review to datetime
    logger.info("Converting last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Save the cleaned data
    filename = "clean_sample.csv"
    logger.info(f"Saving cleaned data to {filename}")
    df.to_csv(filename, index=False)

    # Upload the artifact to W&B
    logger.info(f"Creating artifact {args.output_artifact}")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)
    logger.info("Logging artifact to W&B")
    run.log_artifact(artifact)

    logger.info("Basic cleaning complete")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Basic data cleaning step")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input artifact (raw data CSV file from W&B)",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price to consider (drop prices below this)",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price to consider (drop prices above this)",
        required=True
    )

    args = parser.parse_args()

    go(args)
