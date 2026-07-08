import argparse

from benchmark_suite import run_benchmarks


def main():
    parser = argparse.ArgumentParser(description="Run leave-one-out benchmark experiments on games.csv.")
    parser.add_argument("--data", default="games.csv", help="Path to the dataset CSV.")
    parser.add_argument("--output-dir", default="benchmark_outputs", help="Directory for CSV outputs.")
    parser.add_argument("--top", type=int, default=15, help="How many top experiments to print.")
    args = parser.parse_args()

    summary_df, predictions_df, failures_df, named_checks_df = run_benchmarks(
        data_path=args.data,
        output_dir=args.output_dir,
    )

    print("\nTop benchmark results:")
    if summary_df.empty:
        print("No successful experiments.")
    else:
        print(summary_df.head(args.top).to_string(index=False))

    print("\nNamed checks:")
    if named_checks_df.empty:
        print("No named target games found in predictions.")
    else:
        print(
            named_checks_df[
                ["Experiment", "Name", "Rating", "Prediction", "Residual", "Absolute Residual"]
            ].sort_values("Absolute Residual", ascending=False).to_string(index=False)
        )

    print("\nFailures:")
    if failures_df.empty:
        print("No experiment failures.")
    else:
        print(failures_df.to_string(index=False))

    if not predictions_df.empty:
        print(f"\nSaved predictions for {len(predictions_df)} rows across experiments.")


if __name__ == "__main__":
    main()
