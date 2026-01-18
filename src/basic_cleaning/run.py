#!/usr/bin/env python
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Reading data")
    df = pd.read_csv(artifact_local_path)

    logger.info("Cleaning data")
    # Remove outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Drop duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    logger.info("Saving cleaned data")
    filename = "clean_sample.csv"
    df.to_csv(filename, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)

    logger.info("Logging artifact")
    run.log_artifact(artifact)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Output artifact name",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Output artifact type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Output artifact description",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price to keep",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price to keep",
        required=True
    )

    args = parser.parse_args()
    go(args)
