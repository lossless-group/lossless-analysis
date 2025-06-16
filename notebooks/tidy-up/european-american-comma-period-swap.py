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
    def _():
        # List of columns to exclude from processing
        EXCLUDE_COLUMNS = ["category", "class", "Product Name"]  # Add your column names here

        processed_columns = []

        for col in df.columns:
            if col in EXCLUDE_COLUMNS:
                # Keep the column as is
                processed_columns.append(pl.col(col))
            else:
                # Apply the transformation to other columns
                processed_col = (
                    pl.when(pl.col(col).is_null())
                    .then(pl.lit(None))
                    .otherwise(
                        pl.col(col)
                        .cast(pl.Utf8)
                        .str.replace_all(r"\.", "")
                    )
                    .alias(col)
                )
        return processed_columns.append(processed_col)

        df_processed = df.select(processed_columns)


    _()
    return


@app.cell
def _(df, pl):
    # List of columns to exclude from processing
    EXCLUDE_COLUMNS = ["category", "class", "Product Name"]  # Add your column names here

    processed_columns = []

    for col in df.columns:
        if col in EXCLUDE_COLUMNS:
            # Keep the column as is
            processed_columns.append(pl.col(col))
        else:
            # Apply the transformation to other columns
            processed_col = (
                pl.when(pl.col(col).is_null())
                .then(pl.lit(None))
                .otherwise(
                    pl.col(col)
                    .cast(pl.Utf8)
                    .str.replace_all(r"\,", ".")
                )
                .alias(col)
            )
            processed_columns.append(processed_col)

    df_processed = df.select(processed_columns)
    return (processed_columns,)


@app.cell
def _(df, processed_columns):
    # Apply all the column transformations
    df_clean = df.with_columns(processed_columns)

    # Display the cleaned dataframe
    df_clean
    return (df_clean,)


@app.cell
def _(df_clean, mo):
    # Save the CSV file
    df_clean.write_csv("private-data/transformed_output.csv")

    # Display a confirmation message
    mo.md("**Success!** Transformed CSV saved as `private-data/transformed_output.csv`")
    return


if __name__ == "__main__":
    app.run()
