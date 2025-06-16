import marimo

__generated_with = "0.13.13"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    # Create the file upload widget and display it
    f = mo.ui.file(kind="button", filetypes=[".csv"])
    f  # This line ensures the button is shown
    return f, mo


@app.cell
def _(f, mo):
    mo.stop(len(f.value) == 0, mo.md("Please upload a CSV file."))
    import polars as pl
    df = pl.read_csv(f.value[0].contents, separator=",")
    df
    return df, pl


@app.cell
def _(df, pl):
    # Add ISO-Month column with zero-padded two-digit format
    if "Month" in df.columns:
        iso_df = df.with_columns(
            pl.col("Month").cast(pl.Utf8).str.zfill(2).alias("ISO-Month")
        )

        # Get all column names
        columns = iso_df.columns

        # Find the index of 'Year' column
        year_idx = columns.index("Year")

        # Create new column order
        new_order = columns[:year_idx+1] + ["ISO-Month"] + [col for col in columns[year_idx+1:] if col != "ISO-Month"]

        # Reorder columns
        iso_df = iso_df.select(new_order)

    iso_df
    return iso_df,


if __name__ == "__main__":
    app.run()
